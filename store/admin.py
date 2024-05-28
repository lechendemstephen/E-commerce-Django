from django.contrib import admin # type: ignore
from .models import Product
# Register your models here.
# prepopulating the slug 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    
admin.site.register(Product, ProductAdmin)