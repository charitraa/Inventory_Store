from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
# Create your views here.
@api_view()
def product_view(request):
    querset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(querset, many=True ,context ={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id) 
    Seralizer = ProductSerializer(product)
    return Response(Seralizer.data)

@api_view() 
def Collection_details(request, pk):
    return Response ('ok')