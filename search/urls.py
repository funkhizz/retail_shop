from django.urls import path
from . import views
from .views import (SearchProductView,
)


urlpatterns = [
    path('', SearchProductView.as_view(), name='query'),
]
