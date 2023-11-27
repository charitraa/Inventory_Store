
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin , messages
from django.db.models.query import QuerySet
from . import models
from django.urls import reverse
from django.utils.html import format_html , urlencode
from django.db.models.aggregates import Count


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return  queryset.filter(inventory__lt =10)





@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # prepopulated_fields = {
    #     'slug': ['title']
    # }
    
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    # inlines = [TagInline]
    list_display = ['title','unit_price','inventory_status','collection_title','unit_price']
    list_editable = ['unit_price']
    list_filter = ['collection','last_updated', InventoryFilter]
    list_per_page = 5
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,f'{updated_count} products were sucessfully updated.', messages.ERROR
        )
# Register your models here.

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self, Collection):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(Collection.id)}))
        return format_html('<a href="{}">{}</a>',url, Collection.products_count)
    
    def get_queryset(self , request):
        return super().get_queryset(request).annotate(products_count = Count('product'))
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # display the the data in this order of customer tables
    list_display = ['first_name', 'last_name','membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 5
    # to make search the name in the admin database
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.StackedInline):
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display =['id','placed_at','customer']


