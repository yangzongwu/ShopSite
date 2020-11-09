from goods.models import GoodsCategory
from django import template

register = template.Library()


@register.inclusion_tag('goods/inclusions/_goodsCategory.html', takes_context=True)
def show_goodsCategory(context):
    categories = GoodsCategory.objects.all()
    return {
        'categories': categories,
    }
