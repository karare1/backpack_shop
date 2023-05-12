from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
