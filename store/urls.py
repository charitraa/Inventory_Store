from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.ProductList.as_view()),
    path('product/<int:id>/',views.ProductDetail.as_view()),
    path('collection/<int:pk>/',views.Collection_details),
    path('collection/',views.collection_veiw)
]
