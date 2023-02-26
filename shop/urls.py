from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [

    # 购物车
    url(r'paysuc/',views.paysuc),

    # 添加到购物车(添加、删除、修改是否选中)
    url(r'^addcart/', views.update_cart),
    #删除商品
    url(r'subcart',views.subcart),

    # 提交订单
    url(r'^saveorder/$', views.saveorder),
    #查看购物车
    url(r'orderlist',views.orderlist),
    # 我的
    url(r'^profile/$', views.profile, name='profile'),
    # 注册
    url(r'^register/$', views.register),
    # 保存用户
    url(r'^saveuser/$', views.saveuser),
    # 验证用户id是否可用
    url(r'^checkuserphone/$', views.checkuserphone),
    # 退出登陆

    # 登陆
    url(r'^login/$', views.login),
    # 验证用户登录
    url(r'^validToken/$', views.validToken),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
