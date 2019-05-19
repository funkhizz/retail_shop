from . import views
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('checkout_address_create', views.checkout_address_create_view, name="checkout_address_create"),
    path('checkout_address_reuse', views.checkout_address_reuse_view, name="checkout_address_reuse"),
]


