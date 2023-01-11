from django.contrib import admin

# Register your models here.

from .models import User, Cart,Goods,Order,Category,Banner
from django.contrib.auth.models import Group

from django.utils.safestring import mark_safe



admin.site.unregister(Group)

admin.AdminSite.site_header='点菜后台管理系统'

admin.AdminSite.site_title = '管理系统'

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display =['bannerName','images']

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):

    # def get_price(self,storenums,productnum ,price ,marketprice):
    #     num=int(productnum)*int(marketprice)-int(price)*storenums
    #     return num
    #
    # get_price.short_description = '利润'

    list_display = ["images","productid","productname","storenums",'marketprice']

    search_fields = list_display
    list_filter = ['category']
    list_per_page = 5

# 用户表
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ["pk", 'userAccount', 'userName', 'userPhone', 'userAdderss', 'userRank']
    search_fields = [ 'userAccount', 'userName', 'userPhone', 'userRank']
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['typename']
    list_display = ['typeid','typename']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['productid']
    list_display = ['id','productid','productnum','productprice']

    # def get_price(self, productid):
    #     G= Goods.objects.filter(productid=productid)
    #     print(productid)
    #     num=G.productnum*G.marketprice-G.storenums*G.price
    #     return num
    # get_price.short_description = '利润'

    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    def orderid(self):
        return self.orderid

    orderid.short_description = "订单id"

    def user(self):
        return self.user

    user.short_description = "用户"



    list_display = ['orderid',"user_id",'totalprice','created_time']

    search_fields = list_display

    date_hierarchy = 'created_time'

    list_per_page = 7



