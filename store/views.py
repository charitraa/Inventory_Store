from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin ,RetrieveModelMixin , UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .permissions import ISAdminOrReadOnly,ViewCustomerHistoryPermission
from .models import Product , Collection , OrderItem , Review ,Cart,CartItem, Customer, Order, ProductImage
from .serializers import ProductSerializer , CollectionSerializer, ReviewSerializer, CartSerializer,CartItemSerializer, ADDCartItemSerializer, updateCartItemSerializer ,CustomerSerializer, orderSerializer,CreateOrderSerializer,UpdateOrderSerializer, ProductImageSerializer
from .filters import ProductFilter
from store.pagination import DEfaultPagination
# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    pagination_class = DEfaultPagination
    permission_classes = [ISAdminOrReadOnly]
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
    permission_classes = [ISAdminOrReadOnly]
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
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission ])
    def history(self,request,pk):
        return Response('ok')

    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            Serializer = CustomerSerializer(customer)
            return Response(Serializer.data)
        elif request.method =='PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        


class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','options']

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,context = {'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = orderSerializer(order)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return orderSerializer
    
    def get_queryset(self):  
        if self.request.user.is_staff:
            return Order.objects.all()
        customerid =Customer.objects.only('id').get(user_id=self.request.user.id)
        return Order.objects.filter(customer_id=customerid)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    def get_queryset(self):
        #geeting the primary key of product from the url of API
        #and return the image of product of it's
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])