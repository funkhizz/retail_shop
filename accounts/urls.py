from . import views
from .views import RegisterView, LoginView
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('guest_login/', views.guest_login_page, name="guest_login"),

]


