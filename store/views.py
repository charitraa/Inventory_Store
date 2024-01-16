from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin ,RetrieveModelMixin , UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Product , Collection , OrderItem , Review ,Cart,CartItem, Customer
from .serializers import ProductSerializer , CollectionSerializer, ReviewSerializer, CartSerializer,CartItemSerializer, ADDCartItemSerializer, updateCartItemSerializer ,CustomerSerializer
from .filters import ProductFilter
from store.pagination import DEfaultPagination
# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    pagination_class = DEfaultPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_updated']

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
        

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class CartItemViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ADDCartItemSerializer
        elif self.request.method == 'PATCH':
            return updateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin,UpdateModelMixin , GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
