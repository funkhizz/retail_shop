from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.

class ProductListView(ListView): # class based view
    # model = Product // same way that queryset
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

def product_list_view(request): # function based view
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
    }
    return render(request, "products/list.html", context)

class ProductDetailView(DetailView): # class based view
    queryset = Product.objects.all()
    template_name = "products/detail.html"

def product_detail_view(request, pk=None, *args, **kwargs): # function based view
    # instance = Product.objects.get(pk=pk) #or id
    instance = get_object_or_404(Product, pk=pk)
    context = {
        'object': instance,
    }
    return render(request, "products/detail.html", context)