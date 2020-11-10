from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .models import GoodsCategory, GoodsInfo


# Create your views here.
# 必须传一个参数request请求对象，里面有用户发送的请求信息
def goods_index(request):
    # 1查询商品的分类
    categories = GoodsCategory.objects.all()

    # 2从每个分类中获取四个商品，最新的四个商品
    for cag in categories:
        # GoodsInfo.objects.filter(goods_cag=cag)
        # 一对多关系， 查询多的一方  会在一的这一方有一个属性  多的一方的 模型类名小写_set
        # cag.goodsinfo_set.all()
        # 拿到最新的四个数据
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]

    # 3 购物车所有的商品 cookie key:value, key 商品ID，value 商品数量 cookie存的都是字符串
    # 4购物车商品总数量
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)

    return render(request, 'goods/index.html', {'categories': categories,
                                                'cart_goods_list': cart_goods_list,
                                                'cart_goods_count': cart_goods_count})


def goods_detail(request):
    # 商品分类
    categories = GoodsCategory.objects.all()

    # 购物车数据
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)

    # 当前商品数据
    goods_id = request.GET.get('id', 1)
    goods_data = GoodsInfo.objects.get(id=goods_id)

    return render(request, 'goods/detail.html', {'goods_data': goods_data,
                                                 'categories': categories,
                                                 'cart_goods_list': cart_goods_list,
                                                 'cart_goods_count': cart_goods_count})

def goods_list(request):
    # 商品分类
    categories = GoodsCategory.objects.all()

    # 购物车数据
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)


    cag_id=request.GET.get('cag',1)
    page_id=request.GET.get('page',1)
    current_cag=GoodsCategory.objects.get(id=cag_id)
    goods_data=GoodsInfo.objects.filter(goods_cag=current_cag).order_by("goods_name")
    # goods_data=GoodsInfo.objects.filter(goods_cag_id=cag_id)
    paginator=Paginator(goods_data,10)
    page_data=paginator.page(page_id)


    return render(request,'goods/list.html',{'categories':categories,
                                           'cart_goods_list': cart_goods_list,
                                           'cart_goods_count': cart_goods_count,
                                           'page_data':page_data,
                                            'paginator':paginator,
                                             'cag_id':cag_id})