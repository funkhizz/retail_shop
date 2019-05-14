from . import views
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('', views.cart_home, name="cart_home"),
    path('update/', views.cart_update, name="cart_update"),

]


