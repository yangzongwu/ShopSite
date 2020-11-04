from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add_cart/', views.add_cart, name='add_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('submit_success/', views.submit_success, name='submit_success'),
]
