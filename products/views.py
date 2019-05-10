from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, Http404
from .models import Product

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug)
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Hmmmm")
        return instance

class ProductListView(ListView): # class based view
    # model = Product // same way that queryset
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    def get_queryset(self, *args, **kwargs):
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView): # class based view
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"
    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.featured()

def product_list_view(request): # function based view
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
    }
    return render(request, "products/list.html", context)



class ProductDetailView(DetailView): # class based view
    # model = Product // same way that queryset
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesnot exist")
        return instance

def product_detail_view(request, pk=None, *args, **kwargs): # function based view
    instance = Product.objects.get(pk=pk, featured=True) #or id
    # instance = get_object_or_404(Product, pk=pk)

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesnot exist")

    # SAME FUNCTIONALITY IN DIFF WAY

    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesnot exist")

    context = {
        'object': instance,
    }
    return render(request, "products/detail.html", context)

def product_detail_slug(request, slug):
    instance = Product.objects.get(slug=slug)
    if instance is None:
        raise Http404("Product doesnot exist")
    context = {
        'object': instance,
    }
    return render(request, "products/detail.html", context)