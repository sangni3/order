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
#主体
# class MainShow(models.Model):
#     trackid = models.CharField(max_length=10)
#     name = models.CharField(max_length=20)
#     img = models.CharField(max_length=100)
#     categoryid = models.CharField(max_length=10)
#     brandname = models.CharField(max_length=20)
#
#     img1 = models.CharField(max_length=100)
#     childcid1 = models.CharField(max_length=10)
#     productid1 = models.CharField(max_length=10)
#     longname1 = models.CharField(max_length=50)
#     price1 = models.CharField(max_length=10)
#     marketprice1 = models.CharField(max_length=10)
#
#     img2 = models.CharField(max_length=100)
#     childcid2 = models.CharField(max_length=10)
#     productid2 = models.CharField(max_length=10)
#     longname2 = models.CharField(max_length=50)
#     price2 = models.CharField(max_length=10)
#     marketprice2 = models.CharField(max_length=10)
#
#     img3 = models.CharField(max_length=100)
#     childcid3 = models.CharField(max_length=10)
#     productid3 = models.CharField(max_length=10)
#     longname3 = models.CharField(max_length=50)
#     price3 = models.CharField(max_length=10)
#     marketprice3 = models.CharField(max_length=10)


#类型
class Category( models.Model ):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)
    def __str__(self):
        return self.typename
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '分类'  # 指定后台显示模型名称
        verbose_name_plural = '分类表'  # 指定后台显示模型复数名称

# 商品模型类
class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10,verbose_name='商品编号')
    # 商品图片
    productimg = models.CharField(max_length=150,verbose_name='图片')
    # 商品名称
    productname = models.CharField(max_length=50,verbose_name='名称')
    # 价格
    price = models.CharField(max_length=10,verbose_name='进价')
    # 超市价格
    marketprice = models.CharField(max_length=10,verbose_name='售价')
    # 组id
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='商品分类')
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
            img = mark_safe( '<img src="http://%s" width="70px" />' % href )
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
    userAccount = models.CharField(max_length=20, unique=True,verbose_name='账号')
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
    user= models.ForeignKey( User, verbose_name='用户', on_delete=models.CASCADE )
    productid = models.CharField(max_length=10,verbose_name='商品编号')
    # productid = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id' )
    productnum = models.IntegerField(verbose_name='商品数量')
    productprice = models.CharField(max_length=10,verbose_name='单价')

    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=100)
    orderid = models.CharField(max_length=20, default="0",verbose_name='订单编号')

    # object1 = CartManager1()
    # object2 = CartManager2()
    def __str__(self):
        return self.orderid
    @classmethod
    def createcart(cls, userid, productid, productnum, productprice, productimg, productname):
        c = cls(user=userid, productid=productid, productnum=productnum, productprice=productprice,
                 productimg=productimg, productname=productname)
        return c
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '销售'  # 指定后台显示模型名称
        verbose_name_plural = '销售管理'  # 指定后台显示模型复数名称
        db_table = 'shop_cart'  # 数据库表名

# 订单
class Order(models.Model):
    orderid = models.CharField(max_length=20,verbose_name='订单编号')
    user= models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    totalprice = models.IntegerField(verbose_name='总价')
    created_time = models.DateTimeField( verbose_name='创建时间', default=now)

    def __str__(self):
        return self.orderid

    @classmethod
    def createorder(cls, orderid, userAccount, totalprice,time):
        o = cls(orderid=orderid, user=userAccount, totalprice=totalprice,created_time=time)
        return o
    class Meta:
        ordering = ['-id']  # 按文章创建日期降序
        verbose_name = '订单'  # 指定后台显示模型名称
        verbose_name_plural = '订单管理'  # 指定后台显示模型复数名称
        db_table = 'shop_order'
