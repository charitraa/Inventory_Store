from django.contrib import admin
from django.urls import path ,include

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections', views.CollectionVeiwSet)
router.register('carts',views.CartViewSet)

product_routers = routers.NestedDefaultRouter(router,'products',lookup='product')
product_routers.register('reviews', views.ReviewViewSet , basename='product-reviews')


urlpatterns = router.urls +product_routers.urls
