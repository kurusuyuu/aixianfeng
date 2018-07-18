import random
from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse

from shop.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, UserTicket, FoodType, Goods, \
    CarModel, OrderModel, OrderGoodsModel


def home(request):
    if request.method == 'GET':
        datawheels = MainWheel.objects.all()
        datanavs = MainNav.objects.all()
        datamustbuys = MainMustBuy.objects.all()
        datashops = MainShop.objects.all()
        datamainshows = MainShow.objects.all()[0]
        data = {
            'datawheels': datawheels,
            'datanavs': datanavs,
            'datamustbuys': datamustbuys,
            'datashops': datashops,
            'datamainshows':datamainshows,
        }
    return render(request,'home/home.html',data)




def login(request):
    if request.method == 'GET':
        return render(request,'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户是否存在
        users = UserModel.objects.filter(username=username)
        if users:
            # 校验密码
            if check_password(password,users[0].password):
                ticket = ''
                s = 'qwertyuiopasdfghjklzxcvbnm0123456789'
                for i in range(15):
                    ticket += random.choice(s)
                # 设置cookie
                response = HttpResponseRedirect(reverse('shop:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket',ticket,expires=out_time)

                # 服务端存时间
                UserTicket.objects.create(user=users[0],
                                          ticket=ticket,
                                          out_time=out_time)
                return response


def regist(request):
    if request.method == 'GET':
        return render(request,'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        password = make_password(password)

        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            icon=icon,
        )
        return HttpResponseRedirect('/shop/login/')

def mine(request):
    if request.method == 'GET':

        user = request.user
        data = {}
        if user.id:
           orders = user.ordermodel_set.all()

           wait_pay,payed = 0,0

           for order in orders:
                if order.o_status == 0:
                    wait_pay +=1
                elif order.o_status == 1:
                    payed += 1
           data['wait_pay'] = wait_pay
           data['payed'] = payed
        return render(request,'mine/mine.html',data)

def logout(request):
    if request.method == 'GET':
        # 删除cookie
        response = HttpResponseRedirect(reverse('shop:home'))
        response.delete_cookie('ticket')
        # 删除userticket
        ticket = request.COOKIES.get('ticket')
        UserTicket.objects.filter(ticket=ticket).delete()

        return response


def market(request):

    return HttpResponseRedirect(reverse('shop:goods',args=('104749','0','0')))


def goods(request, typeid, cid, sort_id):
    if request.method == 'GET':
        # 获取类型
        foodtype = FoodType.objects.all()

        # 获取商品
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)

        # 商品的分类
        if sort_id == '0':
            pass
        elif sort_id == '1':
            goods = goods.order_by('productnum')
        elif sort_id == '2':
            goods = goods.order_by('-price')
        elif sort_id == '3':
            goods = goods.order_by('price')

        # 获取分类的全部类型
        foodtypes = FoodType.objects.filter(typeid=typeid).first()

        childtypenames = foodtypes.childtypenames
        typeclass = childtypenames.split('#')

        typelist = []
        for i in typeclass:
             typelist.append(i.split(':'))

        data = {'foodtype':foodtype,
                'goods':goods,
                'foodtypes':foodtypes,
                'typelist':typelist,
                'typeid':typeid,
                'cid':cid,
                'sort_id':sort_id,
                }

    return render(request,'market/market.html',data)


def cart(request):
    if request.method == 'GET':

        user = request.user

        if user and user.id:
            # 如果用户已经登录，则加载购物车的数据
            cart = CarModel.objects.filter(user=user)

            return render(request, 'cart/cart.html', {'cart': cart})

        else:
            return HttpResponseRedirect(reverse('shop:login'))


def change(request):
    if request.method == 'POST':

        cart_id = request.POST.get('cart_id')
        user = request.user
        data = {
            'code':'200',
            'msg':'请求成功'
        }

        if user and user.id:
            cart = CarModel.objects.filter(pk=cart_id).first()

            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select
        return JsonResponse(data)


def addgoods(request):
    if request.method == 'POST':
        data = {
            'cood': '200',
            'msg': '请求成功'
        }
        user = request.user

        if user and user.id:

            goods_id = request.POST.get('goods_id')

            # 获取购物车信息
            usercart = CarModel.objects.filter(user=user,
                                               goods_id=goods_id).first()

            # 如果用户选了商品
            if usercart:
                usercart.c_num += 1
                usercart.save()
                data['c_num'] = usercart.c_num
            else:
                # 如果用户没选商品，就创建
                CarModel.objects.create(user=user,
                                        goods_id=goods_id,
                                        c_num=1
                                        )
                data['c_num'] = 1
        return JsonResponse(data)


def subgoods(request):
    if request.method == 'POST':
        data = {
            'cood': '200',
            'msg': '请求成功'
        }

        user= request.user
        goods_id = request.POST.get('goods_id')

        # 查看当前商品是否已经在购物车中
        if user and user.id:
            usercart = CarModel.objects.filter(user=user,
                                               goods_id=goods_id).first()

            #如果存在，则减一
            if usercart:
                # 如果商品的数量为1，则删除
                if usercart.c_num == 1:
                    usercart.delete()
                    data['c_num'] = 0
                else:
                    # 如果商品数量不为1，则减一
                    usercart.c_num -=1
                    usercart.save()
                    data['c_num'] = usercart.c_num
        return JsonResponse(data)



def order(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 先查询is_select为True的购物车的数据
            cartgoods = CarModel.objects.filter(is_select=True)

            # 创建订单,0是未付款 1是已付款
            order = OrderModel.objects.create(user=user,o_status=0)

            # 创建订单详情信息
            for cart in cartgoods:
                OrderGoodsModel.objects.create(goods=cart.goods,
                                               order=order,
                                               goods_num=cart.c_num)
                #cart.delete()
            cartgoods.delete()
            return HttpResponseRedirect(reverse('shop:payorder',args=(str(order.id),)))


def payorder(request,order_id):
    if request.method == 'GET':

        orders = OrderModel.objects.filter(pk=order_id).first()
        data = {
            'orders':orders,
            'order_id':order_id,
        }
        return render(request,'order/order_info.html',data)


def pay(request,order_id):
    # 修改订单的付款状态，o_status=1
    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)

        return HttpResponseRedirect(reverse('shop:mine'))


def waitpay(request):
    if request.method == 'GET':
        user = request.user

        if user and user.id:
            orders = OrderModel.objects.filter(user=user,o_status=0)

            return render(request,'order/order_list_wait_pay.html',{'orders':orders})


def endpay(request):
    if request.method == 'GET':
        user = request.user

        if user and user.id:
            orders = OrderModel.objects.filter(user=user,o_status=1)

            return render(request,'order/order_list_wait_pay.html',{'orders':orders})