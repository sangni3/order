from django.contrib import admin

# Register your models here.
from django.forms.models import model_to_dict
from .models import User, Goods, Order, Category, Banner, OrderGoods, comments
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



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    def user_id (self):
        return self.user.userAccount

    user_id.short_description = "用户id"

    def order_goods(self):
        goods=OrderGoods.objects.filter(order=self)
        a=[]
        for i in goods:
            a.append(str(i)+' * '+str(i.count)+' ')
        return a

    order_goods.short_description='商品详情'

    list_editable = ['status']

    list_display = ['order_id',user_id,order_goods,'address','comment','status','pay_method','created_time']
    list_filter = ['status']
    search_fields = ['order_id',"user_id",'address']
    list_per_page = 7

@admin.register(comments)
class commentsAdmin(admin.ModelAdmin):
    list_display = ['user','goods', 'comments','created_time']

