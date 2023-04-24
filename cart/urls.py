from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_cart, name='shop_cart'),
    path('add/<item_id>/', views.add_items, name='add_items'),
]
