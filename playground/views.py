from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
# request -> response
# request handler

def say_hello(request):
    return HttpResponse('hello World')
