from . import views
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('register/', views.register, name="register"),
    path('guest_login/', views.guest_login_page, name="guest_login"),

]


