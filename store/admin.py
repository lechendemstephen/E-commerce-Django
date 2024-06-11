from django.contrib import admin # type: ignore
from .models import Product, Variations, ReviewRating
# Register your models here.
# prepopulating the slug 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin): 
      list_display = ('product', 'varation_category', 'variation_value', 'is_active', 'created_date')
      list_editable = ('is_active',)
      list_filter = ('product', 'varation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variations, VariationAdmin)
admin.site.register(ReviewRating)