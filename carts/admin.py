from django.contrib import admin # type: ignore
from .models import Cart, CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin): 
    list_display = ('cart_id', 'date_added')
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product',  'cart', 'quantity', 'is_active')
    list_editable = ('is_active',)



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)