from .views import MarketingPreferenceUpdateView, MailchimpWebhookView
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name="webhook"),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name="marketing"),
]
