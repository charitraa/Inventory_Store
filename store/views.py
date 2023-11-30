from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
# Create your views here.
@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        querset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(querset, many=True ,context ={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        seralizer = ProductSerializer(product)
        return Response(seralizer.data)
    elif request.method =='PUT':
        seralizer = ProductSerializer(product,data=request.data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(seralizer.validated_data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)

@api_view()
def Collection_details(request, pk):
    return Response ('ok')