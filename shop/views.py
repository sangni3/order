import json
import jwt
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
import re
from .models import Category, Goods, User, Cart, Order,Banner,OrderGoods,comments
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import time
import random
from django.conf import settings
from alipay import  AliPay
import os

from shop.serializers import MainSer, BannerSer, CateSer, CartSer, OrderGoodsSer, CommentSer


# Create your views here.



# 主页
class MainView(APIView):
    def get(self, request):
        # 主要显示
        goods=Goods.objects.all().values()
        banner=Banner.objects.all().values()
        category=Category.objects.all().values()
        goodlist = MainSer( goods, many=True )
        catelist = CateSer(category,many=True )
        banners = BannerSer( banner, many=True)
        is_login = request.session.get( 'is_login' )
        cart_list=[]
        if is_login:
            phone = request.session.get( 'userPhone' )
            user = User.objects.get( userPhone=phone )
            cart = Cart.objects.filter( user=user ).all()
            cart_list = {}
            for i in cart:
                cart_list[i.productid.productid]=i.productnum

        return Response( {'goodlist':goodlist.data,'banners':banners.data,'category':catelist.data,'carts':cart_list})

# 评论
class CommentsView(APIView):
    def get(self,request):
        goodsid=request.GET.get('goodsid')
        goods=Goods.objects.get(productid=goodsid)
        comment=comments.objects.filter(goods=goods).all().values()
        commentList=CommentSer(comment,many=True)
        return Response({'comments':commentList.data})
    def post(self,request):
        token = request.session.get( "token" )
        if  (token):
            token = jwt.decode( token, "secret", algorithms=["HS256"] )
            user = User.objects.get( userPhone=token['phone'] )
            comment = request.POST.get( 'comment' )
            goodsid = request.POST.get( 'goodsid' )
            print(goodsid)
            goods=Goods.objects.get(productid=goodsid)
            a=comments.objects.create(comments=comment,goods=goods,user=user)
            a.save()
            return Response({'data':1,'status':'发送成功'})
        return Response({'data':0,'status':'未登录'})

# 购物车
class CartView(APIView):
    def get(self, request):
        phone = request.session.get( 'userPhone' )
        if phone:
            user = User.objects.get( userPhone=phone )
            cart = Cart.objects.filter( user=user ).all()
            address = user.userAdderss
            cart_list = []
            for i in cart:
                goods = {'productid': i.productid.productid,
                         'productname': i.productid.productname,
                         'img': i.productid.productimg.url,
                         'num': i.productnum,
                         'price': i.productid.marketprice,
                         }
                cart_list.append( goods )
            return JsonResponse( {'carts': cart_list, 'address': address} )
        return JsonResponse( {"data": 0, "status": "error"} )
    def post(self, request):
        phone = request.session.get( 'userPhone' )
        user = User.objects.get( userPhone=phone )
        cart = json.loads( request.body )
        orderid = time.time() + random.randrange( 1, 100000 )
        orderid = "%d" % orderid
        total_amount = 0
        total_count = 0
        car = cart['cart']
        for i in car:
            goods = Goods.objects.get( productid=i )
            total_count += int( car[i] )
            total_amount += int( goods.marketprice ) * int( car[i] )
            Cart.objects.get( productid=goods ).delete()
        order = Order.createorder( orderid, user, cart['address'],
                                   cart['note'], total_amount, total_count, 8 )
        order.save()
        for i in car:
            goods = Goods.objects.get( productid=i )
            ordergoods = OrderGoods.createOrderGoods( order, goods, car[i], goods.marketprice )
            ordergoods.save()
        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
            alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
            sign_type=settings.ALIPAY_SIGN_TYPE,
            debug=True,
        )
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no=orderid,
            total_amount=total_amount,
            subject=settings.ALIPAY_SUBJECT,
            return_url='http://localhost:8000/paysuc?out_trade_no='+orderid,
        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        return Response(pay_url)


#支付成功
def paysuc(request):
    order_id=request.GET.get('out_trade_no')
    order=Order.objects.get(order_id=order_id)
    order.status=2
    order.save()
    return HttpResponseRedirect('http://localhost:8080/#/order')

#加入购物车
def update_cart(request):
    # 判断是否登录
    is_login = request.session.get( 'is_login' )
    if is_login:
        userPhone = request.session.get( "userPhone" )
        user = User.objects.get( userPhone=userPhone )
        productid=request.POST.get('productid')
        count=request.POST.get('count')
        goods=Goods.objects.get( productid=productid)
        if count=='0':
            Cart.objects.get(user=user ,productid=goods).delete()
            return JsonResponse({})
        else:
            try:
                cart = Cart.objects.get(user=user ,productid=goods)
            except Cart.DoesNotExist as e :
                cart=Cart.createcart(user,goods,count)
                cart.save()
            cart.productnum=count
            cart.save()
            return JsonResponse({})
    return JsonResponse({'data':0,'status':"error"})

#删除购物车商品
def subcart(request):
    token = request.session.get( "token" )
    token = jwt.decode( token, "secret", algorithms=["HS256"] )
    user = User.objects.get( userPhone=token['phone'] )
    productid=request.POST.get('productCode')
    goods = Goods.objects.get( productid=productid )
    Cart.objects.get( user=user, productid=goods ).delete()
    return JsonResponse({'data':1,'status':'success'})

#确认支付与收货
class ConfirmView(APIView):
    def post(self, request):
        token = request.session.get( "token" )
        if token:
            token = jwt.decode( token, "secret", algorithms=["HS256"] )
            user = User.objects.get( userPhone=token['phone'] )
            btn=request.POST.get('btn')
            order = request.POST.get( 'order_id' )
            orders = Order.objects.get( user=user, order_id=order )
            if btn=='2':
                orders.status=4
                orders.save()
                return JsonResponse( {'data':1,'stutas':'success'} )
            elif btn=='1':
                a=orders.total_amount
                alipay = AliPay(
                    appid=settings.ALIPAY_APP_ID,
                    app_notify_url=None,
                    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
                    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
                    sign_type=settings.ALIPAY_SIGN_TYPE,
                    debug=True,
                )
                order_string = alipay.api_alipay_trade_wap_pay(
                    out_trade_no=order,
                    total_amount=int(a),
                    subject=settings.ALIPAY_SUBJECT,
                    return_url='http://localhost:8000/paysuc?out_trade_no=' + order,
                )
                pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
                print('yyyy')
                return Response(pay_url)
        return JsonResponse({})
#订单
def saveorder(request):
    token = request.session.get("account")
    user = User.objects.get(userAccount=token)
    carts = Cart.objects.filter(user=user,isDelete=False)

    if carts.count() == 0:
        return JsonResponse({"data": 1, "status": "error"})

    cartorder = carts.filter(isChose=True)
    if cartorder.count() == 0:
        return JsonResponse({"data": 2, "status": "error"})

    orderid = time.time() + random.randrange(1, 100000)
    orderid = "%d" % orderid
    total=0

    for item in cartorder:
        total+=int(item.productprice)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    order = Order.createorder(orderid, user,total ,now)
    order.save()
    for item in cartorder:
        item.orderid = orderid
        item.isDelete = True
        item.save()

    return JsonResponse({"data": 0, "status": "success"})

#查看订单
def orderlist(request):
    token = request.session.get( "token" )
    if token:
        token = jwt.decode( token, "secret", algorithms=["HS256"] )
        user = User.objects.get( userPhone=token['phone']  )
        orders=Order.objects.filter(user=user).all().values()
        orders2=OrderGoodsSer(orders,many=True)
        goodslist=[]
        for i in orders:
            goodlist=OrderGoods.objects.filter(order=i['order_id'])
            goodslist.append([item.goods.productimg.url for item in goodlist])
        return JsonResponse({'orderlist': orders2.data,'goodsimg':goodslist})
    return JsonResponse({"data": 1, "status": "error"})
# 我的主页
def profile(request):
    token = request.session.get( "token" )
    if token:
        token = jwt.decode( token, "secret", algorithms=["HS256"] )
        user=User.objects.get(userPhone=token['phone'])
        order=Order.objects.filter(user=user)
        res= {'name': user.userName,'avatar':str(user.userImg),'num':len(order)}
        return JsonResponse(res)
    return JsonResponse({"data": 1, "status": "error"})

# 注册
def register(request):
    return render(request, 'home/register.html', {"title": "注册"})


# 保存用户
def saveuser(request):
    pattern = re.compile( r'(\d{4})$' )
    useraccount = len(User.objects.all())+1
    userPhone = request.POST.get("userPhone")
    userPass = request.POST.get("password")
    userName = re.findall(pattern, userPhone)[0]
    userAdderss = request.POST.get("address")
    userImg = request.FILES.get('img')
    if userImg==None:
        userImg='media/author.jpg'
    user = User.createuser(useraccount, userPass, userName, userPhone, userAdderss, userImg, 0)
    user.save()
    # 重定向到mine
    return JsonResponse({"data": 0, "status": "success"})


# 验证用户手机是否可用
def checkuserphone(request):
    phone = request.POST.get("phone")
    try:
        user = User.objects.get(userPhone=phone)
    except User.DoesNotExist as e:
        # 没找到用户说明可以注册
        return JsonResponse({"data": 0, "status": "success"})
    # 找到用户说明不可以注册
    return JsonResponse({"data": 1, "status": "error"})





# 登录
def login(request):
    if request.method == 'POST':
        phone =request.POST.get( 'userPhone' )
        password =request.POST.get( 'password' )
        response = {}
        user=User.objects.filter( userPhone=phone, userPasswd=password)
        if user.exists():
            # token - session 模块
            if not request.session.session_key:
                request.session.save()
                print( "新会话" )
            import hashlib
            import time
            request.session.set_expiry( 3600 * 4 )
            # md5 = hashlib.md5()
            # md5.update( (phone + password + "1258" + str( time.time() )).encode() )
            # token = md5.hexdigest()
            token=jwt.encode({"phone": phone}, "secret", algorithm="HS256")
            request.session["token"] = token
            request.session["userPhone"] = phone
            request.session["is_login"] = True
            request.session.set_expiry( 24 * 60 * 60 )
            request.session.save()
            response["token"] = token
            response["userPhone"] = user[0].userPhone
            res = HttpResponse( json.dumps( response ) )
            return res
        else:
            res = {"data": 0, "status": "error"}
            return HttpResponse( json.dumps( res ))


# 检查登录
def validToken(request):
    is_login = request.session.get('is_login')

    # 获取session中的token
    # token不存在，或者token与发送来的req_token不符合，
    # 则让客户端重新登录
    if not is_login :
        response={"data": 0, "status": "error"}
        res = HttpResponse( json.dumps( response ) )
    else:
        response={"data": 1, "status": "success"}
        res = HttpResponse( json.dumps( response ) )
    return res

