from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from orders.models import Order

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request) # new_or_get from CartManager
    return render(request, "carts/cart_home.html", {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart_home")
        cart_obj, new_obj = Cart.objects.new_or_get(request) # create cart object
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # add to m2m
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart_home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart_home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
        print(new_order_obj)
    return render(request, "carts/checkout.html", {"object": order_obj})
