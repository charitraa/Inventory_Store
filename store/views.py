from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView , ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Product , Collection , OrderItem , Review
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer , CollectionSerializer, ReviewSerializer
from rest_framework.views import APIView
from django.db.models.aggregates import Count
from .filters import ProductFilter
# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() > 0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class CollectionVeiwSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count()>0:
            return Response({'error': 'Collection cannot be deleted cause collection has products'})
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
        
        serializer_class = ReviewSerializer
        def get_queryset(self):
            return Review.objects.filter(product_id=self.kwargs['product_pk'])

        def get_serializer_context(self):
            return {'product_id': self.kwargs['product_pk']}