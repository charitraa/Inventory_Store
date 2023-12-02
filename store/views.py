from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product , Collection
from rest_framework import status
from .serializers import ProductSerializer , CollectionSerializer
from rest_framework.views import APIView
from django.db.models.aggregates import Count
# Create your views here.

class ProductList(APIView):
    def get(self,request):
        querset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(querset, many=True ,context ={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self,request,id):
        product = get_object_or_404(Product, pk=id)
        seralizer = ProductSerializer(product)
        return Response(seralizer.data)
    def put(self, request,id):
        product = get_object_or_404(Product, pk=id)
        seralizer = ProductSerializer(product,data=request.data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(seralizer.validated_data)
    def delete(self, request,id):
        product = get_object_or_404(Product, pk=id)
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
        collection.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)