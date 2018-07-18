from django.conf.urls import url

from shop import views

urlpatterns = [
    # 首页
    url(r'^home/',views.home,name='home'),

    # 个人中心
    url(r'^login/',views.login,name='login'),
    url(r'^regist/',views.regist,name='regist'),
    url(r'^mine/',views.mine,name='mine'),
    url(r'^logout/',views.logout,name='logout'),

    # 闪购
    # url(r'^market/$',views.market,name='market'),
    # url(r'^market/(\d+)/(\d+)/(\d+)/',views.goods,name='goods'),
    url(r'^market/$',views.market,name='market'),
    url(r'^goods/(\d+)/(\d+)/(\d+)/',views.goods,name='goods'),

    # 添加购物车
    url(r'^addgoods/',views.addgoods,name='addgoods'),
    url(r'^subgoods/',views.subgoods,name='subgoods'),

    # 购物车
    url(r'^cart/',views.cart,name='cart'),
    # 修改购物车商品的选择
    url(r"^change/",views.change,name='change'),

    # 下单
    url(r'^order/',views.order,name='order'),

    # 付款
    url(r'^payorder/(\d+)/',views.payorder,name='payorder'),
    # 确认付款
    url(r'^pay/(\d+)/',views.pay,name='pay'),

    # 待付款
    url(r'^waitpay/',views.waitpay,name='waitpay'),
    # 待收货
    url(r'^endpay/',views.endpay,name='endpay'),
]
