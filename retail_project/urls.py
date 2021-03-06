"""retail_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView



urlpatterns = [
    path('', views.home_page, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search/', include('search.urls')),
    path('cart/', include('carts.urls')),
    path('addresses/', include('addresses.urls')),
    path('billing/', include('billing.urls')),
    path('marketing/', include('marketing.urls')),
    # paths for user account settings
    path('account/', RedirectView.as_view(url='/accounts/login_home')),
    path('settings/', RedirectView.as_view(url='/accounts/login_home')),
    path('accounts/', include('accounts.passwords.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

