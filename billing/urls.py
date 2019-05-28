from django.urls import path, include
from . import views


urlpatterns = [
    path('payment-method/', views.payment_method_view, name='payment'),
    path('payment-method/create', views.payment_method_create_view, name='payment-endpoint'),

]

