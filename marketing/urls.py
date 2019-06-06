from .views import MarketingPreferenceUpdateView
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name="marketing"),
]
