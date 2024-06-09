from django.contrib import admin # type: ignore
from .models import Payment, Order, OrderProduct
# Register your models here.

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)