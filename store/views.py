from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView , ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Product , Collection
from rest_framework import status
from .serializers import ProductSerializer , CollectionSerializer
from rest_framework.views import APIView
from django.db.models.aggregates import Count
# Create your views here.

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request':self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id'
    def delete(self, request,pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)
    

class collection_veiw(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request':self.request}

class collection_details(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self,request,pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count()>0:
            return Response({'error': 'Collection cannot be deleted cause collection has products'})
        collection.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)