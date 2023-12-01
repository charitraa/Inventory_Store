from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product , Collection
from rest_framework import status
from .serializers import ProductSerializer , CollectionSerializer
from django.db.models.aggregates import Count
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
    
@api_view(['GET', 'POST',])
def collection_veiw(request):
    if request.method == 'GET':
        querset = Collection.objects.annotate(product_count=Count('products')).all()
        serializer = CollectionSerializer(querset,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def Collection_details(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
    if request.method == 'GET':
        seralizer = CollectionSerializer(collection)
        return Response(seralizer.data)
    elif request.method =='PUT':
        seralizer = CollectionSerializer(collection,data=request.data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(seralizer.validated_data)
    elif request.method == 'DELETE':
        # if collection.orderitems.count() > 0:
        #     return Response({'error':'collection cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)