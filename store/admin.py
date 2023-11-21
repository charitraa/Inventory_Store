from django.contrib import admin
from . import models
from .models import Promotion, Product, Address,Cart,CartItem,Collection,Customer,Order,OrderItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inventory_status','collection','unit_price']
    list_editable = ['unit_price']
    list_per_page = 5

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

# Register your models here.
admin.site.register(Promotion)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Collection)
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 5

admin.site.register(Order)
admin.site.register(OrderItem)

