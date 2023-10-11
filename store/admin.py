from django.contrib import admin
from .models import Promotion, Product, Address,Cart,CartItem,Collection,Customer,Order,OrderItem
# Register your models here.
admin.site.register(Promotion)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Collection)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

