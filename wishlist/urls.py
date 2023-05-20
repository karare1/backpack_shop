from django.urls import path
from .import views


urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),
    path('wishlist_on/<int:product_id>/', views.wishlist_on, name='wishlist_on'),
    path('wishlist_off/<int:product_id>/', views.wishlist_off, name='wishlist_off'),
]
