import time

from django.shortcuts import render, redirect
from goods.models import GoodsInfo,GoodsCategory
from .models import OrderInfo, OrderGoods


# Create your views here.
def add_cart(request):
    # 购物车是在COOKIE good_id,count
    # 获取商品ID
    goods_id = request.GET.get('id', '')
    # 把ID存到COOKIE，如果已经存在
    if goods_id:
        # 获取上一个页面的地址
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1
        response.set_cookie(goods_id, goods_count)
    return response


def show_cart(request):
    # 获取购物车商品列表
    cart_goods_list = []
    # 购物车总数量
    cart_goods_count = 0
    # 购物车总价格
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
        cart_goods_money = cart_goods_money + int(goods_num) * cart_goods.goods_price
    return render(request, "cart/cart.html", {'cart_goods_list': cart_goods_list,
                                              'cart_goods_count': cart_goods_count,
                                              'cart_goods_money': cart_goods_money, })


def remove_cart(request):
    goods_id = request.GET.get('id', '')
    # 把ID存到COOKIE，如果已经存在
    if goods_id:
        # 获取上一个页面的地址
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id, '')
        if goods_count:
            response.delete_cookie(goods_id)
    return response


def place_order(request):
    # 获取购物车商品列表
    cart_goods_list = []
    # 购物车总数量
    cart_goods_count = 0
    # 购物车总价格
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
        cart_goods_money = cart_goods_money + int(goods_num) * cart_goods.goods_price
    return render(request, "cart/place_order.html", {'cart_goods_list': cart_goods_list,
                                                     'cart_goods_count': cart_goods_count,
                                                     'cart_goods_money': cart_goods_money, })


def submit_order(request):
    addr = request.POST.get('addr')
    recv = request.POST.get('recv')
    tele = request.POST.get('phone')
    extra = request.POST.get('extra')
    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra
    order_info.order_id = str(time.time() * 1000000)[:4] + str(time.clock() * 100000000000)[:8]
    order_info.save()

    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    # 遍历购物车数据，生成对象
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue

        cart_goods = GoodsInfo.objects.get(id=goods_id)
        order_goods = OrderGoods()
        order_goods.goods_info = cart_goods
        order_goods.goods_num = goods_num
        order_goods.goods_order = order_info
        order_goods.save()
        response.delete_cookie(goods_id)
    return response


def submit_success(request):
    order_id = request.GET.get('id')
    order_info = OrderInfo.objects.get(order_id=order_id)
    order_goods_list = OrderGoods.objects.filter(goods_order=order_info)

    total_money = 0
    total_num = 0
    for goods in order_goods_list:
        goods_total_money = goods.goods_info.goods_price * goods.goods_num
        total_money += goods_total_money
        total_num += goods.goods_num

    return render(request, "cart/submit_success.html", {"order_info": order_info,
                                                        "order_goods_list": order_goods_list,
                                                        "total_money": total_money,
                                                        "total_num": total_num, })
