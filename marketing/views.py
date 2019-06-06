from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.contrib.messages.views import SuccessMessageMixin

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
