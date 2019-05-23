from . import views
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('', views.cart_home, name="cart_home"),
    path('update/', views.cart_update, name="cart_update"),
    path('checkout/', views.checkout_home, name="checkout"),
    path('checkout/success', views.checkout_done_view, name="success"),
    path('api/cart/', views.cart_detail_api_view, name="api_cart")
]


