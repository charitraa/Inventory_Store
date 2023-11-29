from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.product_view),
    path('product/<int:id>/',views.product_detail),
    path('collection/<int:pk>/',views.Collection_details,name='Collection-details')
]
