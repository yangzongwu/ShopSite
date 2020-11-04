from django.urls import path
from . import views

app_name='goods'
urlpatterns = [
    path('', views.goods_index, name='index'),
    path('detail/',views.goods_detail,name='goods_detail'),
    path('goods_list/',views.goods_list,name='goods_list'),
]
