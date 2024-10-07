from django.contrib import admin
from .models import Coupon

# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'is_active']
    search_fields = ['code']
    list_filter = ['is_active', 'valid_from', 'valid_to']
