from django.urls import path
from . import views
from products.views import (ProductListView,
                        # product_list_view,
                        # ProductDetailView,
                        # product_detail_view,
                        # ProductFeaturedListView,
                        # ProductFeaturedDetailView,
                        ProductDetailSlugView,
)

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<slug>/', ProductDetailSlugView.as_view(), name='detail'),
]


