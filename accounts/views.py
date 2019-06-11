from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
from .signals import user_logged_in
from django.contrib import messages
from .models import EmailActivation
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

# @login_required
# def account_home_view(request):
#     return render(request, "accounts/login_view.html", {})

class AccountHomeView(LoginRequiredMixin ,DetailView):
    template_name  = "accounts/login_home.html"
    def get_object(self):
        return self.request.user

class AccountEmailActivateView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(request, "Your email has been confirmed. Please login.")
            return redirect("login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = """ Your email has already been confirmed.
                Do you need to <a href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("login")
        return render(request, 'registration/activation-error.html', {})

    def post(self, request, *args, **kwargs):
        pass

def guest_login_page(request):
    guest_form = GuestForm(request.POST or None)
    # context = {
    #     "form": guest_form,
    # }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if guest_form.is_valid():
        email = guest_form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    # context["form"] = LoginForm()
        else:
            return redirect("/")
    return redirect("register")

# instead using LoginView
# def login_page(request):
#     login_form = LoginForm(request.POST or None)
#     context = {
#         "form": login_form,
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if login_form.is_valid():
#         username = login_form.cleaned_data.get("username")
#         password = login_form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#         # context["form"] = LoginForm()
#             else:
#                 return redirect("/")
#         else:
#             print("Error")
#     return render(request, "accounts/login.html", context)

class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "This user is inactive")
                return super(LoginView, self).form_invalid(form)
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
        # context["form"] = LoginForm()
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = "/accounts/login/"


# instead using RegisterView
# def register(request):
#     register_form = RegisterForm(request.POST or None)
#     context = {
#         "form": register_form,
#     }
#     if register_form.is_valid():
#         print(register_form.cleaned_data)
#         register_form.save()
#     return render(request, "accounts/register.html", context)
