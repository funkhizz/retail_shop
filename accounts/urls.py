from . import views
from .views import RegisterView, LoginView, AccountHomeView, AccountEmailActivateView

from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('guest_login/', views.guest_login_page, name="guest_login"),
    path('login_home/', AccountHomeView.as_view(), name="login_home"),
    path('email/confirm/<key>/', AccountEmailActivateView.as_view(), name="email_activate"),

]


