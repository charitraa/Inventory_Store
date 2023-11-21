from django.contrib import admin
from . import models
from .models import Promotion, Product, Address,Cart,CartItem,Collection,Customer,Order,OrderItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price' ]
# Register your models here.
admin.site.register(Promotion)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Collection)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

