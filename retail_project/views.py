from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth.views import LogoutView

def home_page(request):
    context = {
        "title": "Hello world!",
        "premium_content": "YEAH!"
    }
    return render(request, "home_page.html", context)

def about_page(request):

    context = {
        "title": "Hello guy! Welcome you on about page"
    }
    return render(request, "about_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
            "form": contact_form,
    }
    if contact_form.is_valid():
        context["form"] = ContactForm() # if i want blank forms after submit

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    return render(request, "contact_page.html", context)

