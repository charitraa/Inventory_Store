from django.contrib import admin
from django.urls import path ,include

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections', views.CollectionVeiwSet)

product_routers = routers.NestedDefaultRouter(router,'products',Lookup='product_pk')
product_routers.register('reviews', views.ReviewViewSet)


urlpatterns = router.urls
