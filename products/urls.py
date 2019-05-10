
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

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<slug>/', ProductDetailSlugView.as_view(), name='products'),
]


