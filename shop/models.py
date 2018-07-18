from django.db import models

# Create your models here.


class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)

    class Meta:
        abstract = True


class MainWheel(Main):
    # 轮播
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


# 主要展示的商品
class MainShow(Main):
    categoryid = models.CharField(max_length=16)
    # 分类名称
    brandname = models.CharField(max_length=100)
    # 图片1
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    # 名称1
    longname1 = models.CharField(max_length=100)
    # 优惠价格1
    price1 = models.FloatField(default=0)
    # 原始价格1
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = "axf_mainshow"


# 闪购--左侧类型表
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    # 分类名字
    typename = models.CharField(max_length=100)
    # 分类商品名字
    childtypenames = models.CharField(max_length=200)
    # 分类排行
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    # 商品的ID
    productid = models.CharField(max_length=16)
    # 商品的图片
    productimg = models.CharField(max_length=200)
    # 商品的名字
    productname = models.CharField(max_length=100)
    # 商品的规格
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    # 规格
    specifics = models.CharField(max_length=100)
    # 折后价格
    price = models.FloatField(default=0)
    # 原价
    marketprice = models.FloatField(default=1)
    # 分类ID
    categoryid = models.CharField(max_length=16)
    # 子分类ID
    childcid = models.CharField(max_length=16)
    # 名称
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    # 排序
    storenums = models.IntegerField(default=1)
    # 销量排序
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_goods"


class UserModel(models.Model):
    # 名称
    username = models.CharField(max_length=32, unique=True)
    # 密码
    password = models.CharField(max_length=256)
    # 邮箱
    email = models.CharField(max_length=64, unique=True)
    # 性别 Flase代表女
    sex = models.BooleanField(default=False)
    # 头像
    icon = models.ImageField(upload_to='icons')
    # 是否删除
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "axf_users"


#购物车
class CarModel(models.Model):
    # 关联用户
    user = models.ForeignKey(UserModel)
    # 关联商品
    goods = models.ForeignKey(Goods)
    # 商品的个数
    c_num = models.IntegerField(default=1)
    # 是否选择商品
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = "axf_cart"


class OrderModel(models.Model):
    # 关联用户
    user = models.ForeignKey(UserModel)
    # 购买的数量
    o_num = models.CharField(max_length=64)
    # 状态 0代表已下单但是没有付钱；1 已付款未发货； 2 已付款已发货
    o_status = models.IntegerField(default=0)
    # 创建时间
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "axf_order"


class OrderGoodsModel(models.Model):
    # 关联的商品
    goods = models.ForeignKey(Goods)
    # 关联的订单
    order = models.ForeignKey(OrderModel)
    # 商品的个数
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_order_goods"


class MainShop(Main):
    # 导航
    class Meta:
        db_table = "axf_shop"


class UserTicket(models.Model):
    # 关联用户
    user = models.ForeignKey(UserModel)
    # 密码
    ticket = models.CharField(max_length=256)
    # 过期时间
    out_time = models.DateTimeField()

    class Meta:
        db_table = "axf_user_ticket"