from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth.views import LogoutView

def home_page(request):
    context = {}
    return render(request, "home_page.html", context)

def about_page(request):

    context = {
        "title": "Hello guy! Welcome you on about page"
    }
    return render(request, "about_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None) # ContactForm() refresh form after submit; or request.POST or None

    context = {
        "title": "Contact form",
        "content": "Welcome to the contact page.",
        "form": contact_form
    } # if i want blank forms after submit
    if contact_form.is_valid():
        # print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission!"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    return render(request, "contact_page.html", context)

