from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, Http404, reverse
from products.models import Product

class SearchProductView(ListView): # class based view
    # model = Product // same way that queryset
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query) # not to include repeated products
        else:
            return Product.objects.none()

    '''
    __icontains = field contains smtg
    __iexact = field is exatly this
    '''
