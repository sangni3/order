from django.db import models
from django.utils.timezone import now
# Create your models here.
from django.contrib.auth.models import AbstractUser
# 轮播
from django.utils.safestring import mark_safe


from media.storage import ImageStorage

class Banner(models.Model):
    bannerName=models.CharField(max_length=50,verbose_name='名称')
    bannerImg=models.ImageField(upload_to='banner/',storage=ImageStorage(), default="",verbose_name='广告')
    def images(self):
        """
        预览图
        """
        href = self.bannerImg
        try:
            img = mark_safe( '<img src="http://localhost:8000/media/%s" width="150px" />' % href )
        except Exception:
            img = ''
        return img

    images.short_description = '图片预览'
    images.allow_tags = True
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '广告'  # 指定后台显示模型名称
        verbose_name_plural = '广告'  # 指定后台显示模型复数名称


#类型
class Category( models.Model ):
    typeid = models.CharField(max_length=10,primary_key=True)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)
    def __str__(self):
        return self.typename
    class Meta:
        verbose_name = '分类'  # 指定后台显示模型名称
        verbose_name_plural = '分类表'  # 指定后台显示模型复数名称

# 商品模型类
class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10,verbose_name='商品编号')
    # 商品图片
    productimg = models.ImageField(upload_to='media', default="",verbose_name='菜品图')
    # 商品名称
    productname = models.CharField(max_length=50,verbose_name='名称')
    #商品描述
    des=models.CharField(max_length=100,verbose_name='商品描述',default='')
    # 价格
    price = models.CharField(max_length=10,verbose_name='进价')
    # 超市价格
    marketprice = models.CharField(max_length=10,verbose_name='售价')
    # 组id
    category = models.ForeignKey(Category, to_field="typeid",related_name='goods_cate',on_delete=models.CASCADE,verbose_name='商品分类')
    # 库存
    storenums = models.IntegerField(verbose_name='库存')
    # 销量
    productnum = models.IntegerField(verbose_name='销量')

    def images(self):
        """
        预览图
        """
        href = self.productimg
        try:
            img = mark_safe( '<img src="http://localhost:8000/media/%s" width="70px" />' % href )
        except Exception:
            img = ''
        return img

    images.short_description = '图片预览'
    images.allow_tags = True

    def __str__(self):
        return self.productname
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '菜品'  # 指定后台显示模型名称
        verbose_name_plural = '菜单管理'  # 指定后台显示模型复数名称


# 用户模型类
class User(models.Model):
    # 用户账号，要唯一
    userAccount = models.CharField(max_length=20,verbose_name='账号')
    # 密码
    userPasswd = models.CharField(max_length=20,verbose_name='密码')
    # 昵称
    userName = models.CharField(max_length=20,verbose_name='名称')
    # 手机号
    userPhone = models.CharField(max_length=20,verbose_name='手机')
    # 地址
    userAdderss = models.CharField(max_length=100,verbose_name='地址')
    # 头像路径
    userImg =  models.ImageField(upload_to='media', default="",verbose_name='用户头像')  # 用户头像
    # 等级
    userRank = models.IntegerField(verbose_name='会员等级')


    def __str__(self):
        return self.userName
    @classmethod
    def createuser(cls, account, passwd, name, phone, address, img, rank):
        u = cls(userAccount=account, userPasswd=passwd, userName=name, userPhone=phone, userAdderss=address,
                userImg=img, userRank=rank)
        return u
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '会员'  # 指定后台显示模型名称
        verbose_name_plural = '会员管理'  # 指定后台显示模型复数名称

# 购物车表
class CartManager1(models.Manager):
    def get_queryset(self):
        return super(CartManager1, self).get_queryset().filter(isDelete=False)


class CartManager2(models.Manager):
    def get_queryset(self):
        return super(CartManager2, self).get_queryset().filter(isDelete=True)

#购物车
class Cart(models.Model):
    user= models.ForeignKey( User,verbose_name='用户', on_delete=models.CASCADE )
    # productid = models.CharField(max_length=10,verbose_name='商品编号')
    productnum = models.IntegerField(verbose_name='商品数量')
    productid = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id' )



    # object1 = CartManager1()
    # object2 = CartManager2()

    @classmethod
    def createcart(cls, userid, productid, productnum):
        c = cls(user=userid, productid=productid, productnum=productnum)
        return c
    class Meta:
        db_table = 'shop_cart'  # 数据库表名

# 订单
class Order(models.Model):
    """订单信息"""
    # 付款方式   货到付款或者阿里支付（支付宝）
    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }
    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "支付宝"),
    )
    # 订单状态
    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "FINISHED": 5
    }
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (5, "已完成"),
    )
    order_id = models.CharField( max_length=64, primary_key=True, verbose_name="订单号" )
    user = models.ForeignKey( User, on_delete=models.PROTECT, verbose_name="下单用户" )
    address = models.CharField(max_length=100,verbose_name="收货地址" )
    comment = models.CharField(max_length=100,blank=True,default='',verbose_name="备注" )
    total_count = models.IntegerField( default=1, verbose_name="商品总数" )
    total_amount = models.DecimalField( max_digits=10, decimal_places=2, verbose_name="商品总金额" )
    freight = models.DecimalField( max_digits=12, decimal_places=2, verbose_name="运费" )
    pay_method = models.SmallIntegerField( choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式" )
    status = models.SmallIntegerField( choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态" )
    created_time = models.DateTimeField( verbose_name='创建时间', default=now )
    def __str__(self):
        return self.order_id
    @classmethod
    def createorder(cls, orderid, userAccount,address,comment, total_amount, total_count,freight):
        o = cls(order_id=orderid, user=userAccount, address=address,comment=comment,
                total_amount= total_amount,total_count=total_count,freight=freight)
        return o
    class Meta:
        ordering = ['-created_time']  # 按文章创建日期降序
        verbose_name = '订单'  # 指定后台显示模型名称
        verbose_name_plural = '订单管理'  # 指定后台显示模型复数名称
        db_table = 'shop_order'

#订单商品
class OrderGoods(models.Model):
    """订单商品"""
    order = models.ForeignKey(Order, related_name='skus', on_delete=models.CASCADE, verbose_name="订单")
    goods = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.productname

    @classmethod
    def createOrderGoods(cls, order, goods,count,price):
        o = cls( order=order,goods=goods,count=count,price=price)
        return o

#评论
class comments(models.Model):
    user = models.ForeignKey( User, on_delete=models.PROTECT, verbose_name="用户" )
    goods = models.ForeignKey( Goods, on_delete=models.PROTECT, verbose_name="商品" )
    comments=models.TextField(max_length=100,verbose_name='评论',default='')
    created_time = models.DateTimeField( verbose_name='创建时间', default=now )
    class Meta:
        verbose_name = '评论'  # 指定后台显示模型名称
        verbose_name_plural = '评论管理'  # 指定后台显示模型复数名称
        db_table = 'shop_comments'