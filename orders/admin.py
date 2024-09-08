from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'price']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemsInline]

admin.site.register(Order, OrderAdmin)