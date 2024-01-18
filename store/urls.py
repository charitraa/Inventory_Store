from django.contrib import admin
from django.urls import path ,include

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections', views.CollectionVeiwSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')

product_routers = routers.NestedDefaultRouter(router,'products',lookup='product')
product_routers.register('reviews',   views.ReviewViewSet , basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items', views.CartItemViewSet , basename='cart-items-details')

urlpatterns = router.urls +product_routers.urls+cart_router.urls
