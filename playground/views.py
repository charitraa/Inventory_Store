from django.shortcuts import render
from django.shortcuts import HttpResponse
from store.models import Product
# Create your views here.
# request -> response
# request handler

def say_hello(request):
    # quey = Product.objects.filter(last_updated__gt=2021)
    return render(request, 'hello.html')
