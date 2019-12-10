from django.conf import settings
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect, HttpResponse
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.contrib.messages.views import SuccessMessageMixin
from .utils import Mailchimp
from .mixins import CsrfExemptMixin
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/marketing/settings/email/'
    success_message = 'Your email preferences have been updated!'

    def get_context_data(self, *args, **kwargs): # update context
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Update Email Preferences"
        return context

    def get_object(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            obj, created = MarketingPreference.objects.get_or_create(user=user)
            return obj

class MailchimpWebhookView(CsrfExemptMixin ,View):
    def get(self, request):
       return HttpResponse("Thank you", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get('data[email]')
            hook_type = data.get('type')
            response_status, response = Mailchimp().check_sub_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                    subscribed=is_subbed,
                    mailchimp_msg=str(data),
                    mailchimp_subscribed=mailchimp_subbed)
        return HttpResponse("Thank you", status=200)

# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         email = data.get('data[email]')
#         hook_type = data.get('type')
#         response_status, response = Mailchimp().check_sub_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(str(data),
#                 subscribed=is_subbed,
#                 mailchimp_msg=str(data),
#                 mailchimp_subscribed=mailchimp_subbed)
#     return HttpResponse("Thank you", status=200)
