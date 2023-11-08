from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db.models import Q , F
from store.models import Product
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
# Create your views here.
# request -> response
# request handler

def say_hello(request):
    # quey = Product.objects.filter(id__range=(1,5))
    
    # query = Product.objects.filter(last_updated__year=2023)

    # complex quries

    # query = Product.objects.filter(Q(last_updated__year=2023) & Q(unit_price__gt = 10))
    #compairing with fields

    # query = Product.objects.filter(inventory=F('unit_price'))
    #annocated,aggregate ,selected_related, F , Value , ExpressionWrapper
    

    query = Product.objects.order_by('title')
    #create ,Update ,Delete , raw ,transcation,new
    return render(request, 'hello.html',{'quey':'ravi','products':list(query)}) 
