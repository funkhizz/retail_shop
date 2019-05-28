from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import stripe
from django.utils.http import is_safe_url
stripe.api_key = "sk_test_KTD8bZQe1jHFF1tLelcTZPgr00PZpIFVwV"
STRIPE_PUB_KEY = 'pk_test_O5HC5E5txvOnI4WBbwPregB400xCMlbyq6'


def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url })

def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Success! Your card was added!"})
    return HttpResponse("error", status=401)
