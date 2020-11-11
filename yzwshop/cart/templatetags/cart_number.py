from django import template

register = template.Library()


@register.inclusion_tag('cart/inclusions/_cartNumber.html', takes_context=True)
def show_cart_goods_count(context):
    request = context['request']
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods_count += int(goods_num)

    return {'cart_goods_count': cart_goods_count}


