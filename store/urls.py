from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.ProductList.as_view()),
    path('product/<int:pk>/',views.ProductDetail.as_view()),
    path('collection/<int:pk>/',views.collection_details.as_view()),
    path('collection/',views.collection_veiw.as_view())
]
