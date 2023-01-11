import json
from django.core import serializers
from django.shortcuts import render, redirect
from .models import Category, Goods, User, Cart, Order,Banner
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import time
import random
from django.conf import settings
import os
from django.contrib.auth import logout
from django.forms.models import model_to_dict

# Create your views here.




def index(request):
    return redirect("/main/")


# 主页
def main(request):
    # 获取轮播数据
    # 主要显示
    goods=Goods.objects.all().values()
    goods = [entry for entry in goods]
    leftList = Category.objects.all()
    banners =Banner.objects.all()
    # leftList = [entry for entry in leftList]
    mainList={}
    # for i in leftList:
    #     # goodsList = Goods.objects.filter( category=i )
    #     # mainList[i.id]=goodsList
    #
    #     print( i)
    return render(request, 'home/main.html',
                  {"title": "首页",
                   "mainList": json.dumps(goods),
                   "cate": leftList,
                    'banners':banners
                   }
                  )


#
def market(request, pageid, sortid):
    # 左侧数据
    leftList = Category.objects.all()
    # 右侧数据
    goodsList = Goods.objects.filter(category=pageid)[0:10]
    # 排序goodsList
    if sortid == '0':
        pass
    elif sortid == '1':
        goodsList = goodsList.order_by("productnum")
    elif sortid == '2':
        goodsList = goodsList.order_by("price")
    elif sortid == '3':
        goodsList = goodsList.order_by("-price")

    # 子类名称
    fllist = []
    # "全部分类:0#进口零食:103547#饼干糕点:103544#膨化食品:103543#坚果炒货:103542#肉干蜜饯:103546#糖果巧克力:103545"


    titlelist = [{"title": "综合排序", "index": "0"},
                 {"title": "销量排序", "index": "1"},
                 {"title": "价格最低", "index": "2"},
                 {"title": "价格最高", "index": "3"}]

    return render(request, 'home/market.html',
                  {"title": "闪送超市",
                   "leftList": leftList,
                   "goodsList": goodsList,
                   "titlelist": titlelist,
                   "id": pageid,
                   "fllist": fllist}
                  )


# 购物车
def cart(request):
    return render(request, 'home/cart.html')
def upcart(request):
    token = request.session.get( "account" )
    user = []
    cartslist = []
    if token == None:
        cartslist = []
    else:
        user = User.objects.get(userAccount=token)
        users=User.objects.filter(userAccount=token).values()
        users= [entry for entry in users]
        carts = Cart.objects.filter( user_id=user).values()

        cartslist=[entry for entry in carts]
        data = {"cartslist": json.dumps(cartslist),
                'user': json.dumps(users)}
    response =JsonResponse( data )
    return response
#加入购物车
def changcart(request, flag):
    # 判断是否登录
    userAccount = request.session.get("account")
    if userAccount is None:
        print(userAccount)
        return JsonResponse({"data": "0", "status": "error"})
    # 用户
    user = User.objects.get(userAccount=userAccount)

    # 商品id
    productid = request.POST.get("productid")
    # 商品信息
    product = Goods.objects.get(productid=productid)
    # 从购物车里取数据（用户id、商品id）
    carts = Cart.objects.filter(user=user, productid=productid,isDelete=False)

    if carts.count() == 0:
        # 没有这样的数据
        onecart = Cart.createcart(user, productid, 1, product.marketprice, True, product.productimg, product.productname, False)
        onecart.save()
        return JsonResponse({"data": 1, "status": "success"})
    else:
        c = carts[0]
        if flag == '0':
            # 增加
            if product.storenums != 0:
                c.productnum = c.productnum + 1
                product.productnum+=1
                product.storenums -= 1
                newprice = int(product.price) * c.productnum
                c.productprice = newprice
                c.save()
                product.save()
        elif flag == '1':
            # 减少
            c.productnum = c.productnum - 1
            product.productnum -= 1
            product.storenums += 1
            product.save()
            if c.productnum == 0:
                c.delete()
                return JsonResponse({"data": 0, "status": "success"})
            else:
                newprice = int(product.price) * c.productnum

                c.productprice = newprice
                c.save()
        elif flag == '2':
            c.isChose = not c.isChose
            c.save()
            if c.isChose:
                str = "√"
            else:
                str = " "
            return JsonResponse({"data": str, "status": "success"})

        return JsonResponse({"data": c.productnum, "status": "success"})


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



# 我的主页
def mine(request):
    username = request.session.get("username")
    userImg = request.session.get("userimg")
    if username==None:
        return render( request, 'home/mine.html', {"title": "我的", "username": '未登录', 'userImg': 'media/defaul.png'} )
    else:
        username=json.loads(username)
        return render(request, 'home/mine.html', {"title": "我的", "username": username,'userImg':userImg})


# 注册
def register(request):
    return render(request, 'home/register.html', {"title": "注册"})


# 保存用户
def saveuser(request):
    useraccount = request.POST.get("userAccount")
    userPass = request.POST.get("userPass")
    userName = request.POST.get("userName")
    userPhone = request.POST.get("userPhone")
    userAdderss = request.POST.get("userAdderss")
    f = request.FILES["userImg"]
    user = User.createuser(useraccount, userPass, userName, userPhone, userAdderss, f, 0)
    user.save()
    response=HttpResponseRedirect('/mine/')
    userName = json.dumps( user.userName )
    request.session['account'] = useraccount
    request.session['password'] = userPass
    request.session['username'] = userName
    request.session['userimg'] = str( user.userImg )
    request.session.set_expiry( 60 * 60 * 24 * 14 )  # 设置过期时间

    # 重定向到mine
    return response


# 验证用户id是否可用
def checkuserid(request):
    userid = request.POST.get("checkid")
    try:
        user = User.objects.get(userAccount=userid)
    except User.DoesNotExist as e:
        # 没找到用户说明可以注册
        return JsonResponse({"data": 0, "status": "success"})
    # 找到用户说明不可以注册
    return JsonResponse({"data": 0, "status": "error"})


# 退出
def quit(request):
    logout(request)
    return redirect("/mine/")


# 登录
def login(request):
    return render(request, 'home/login.html', {"title": "登陆"})


# 检查登录
def checkuserlogin(request):
    if request.method == "POST":
        useraccount = request.POST.get("ua")
        userpasswd = request.POST.get("up")
        try:
            user = User.objects.get(userAccount=useraccount)

        except User.DoesNotExist as e:

            return JsonResponse({"data": 0, "status": "error"})

        if userpasswd != user.userPasswd:

            return JsonResponse({"data": 0, "status": "error"})

        response =HttpResponseRedirect('/mine/')

        userName=json.dumps( user.userName )
        request.session['account'] = useraccount
        request.session['password'] = userpasswd
        request.session['username'] = userName
        request.session['userimg'] = str( user.userImg )
        request.session.set_expiry( 60 * 60 * 24 * 14 )  # 设置过期时间
        return response
    # return JsonResponse({"data": 0, "status": "success"})
