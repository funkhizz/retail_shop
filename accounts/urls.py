from . import views
from .views import RegisterView, LoginView, AccountHomeView, AccountEmailActivateView, GuestRegisterView, UserDetailUpdateView

from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('guest_login/', GuestRegisterView.as_view(), name="guest_login"),
    path('login_home/', AccountHomeView.as_view(), name="login_home"),
    path('email/confirm/<key>/', AccountEmailActivateView.as_view(), name="email_activate"),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name="resend_activation"),
    path('details/', UserDetailUpdateView.as_view(), name='details_update')
]


