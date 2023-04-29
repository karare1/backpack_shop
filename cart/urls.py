from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_cart, name='shop_cart'),
    path('add/<item_id>/', views.add_items, name='add_items'),
    path('amend/<item_id>/', views.amend_item, name='amend_item'),
    path('remove/<item_id>/', views.remove_item, name='remove_item'),
]
