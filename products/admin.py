from django.contrib import admin
from . models import Category, Product, ProductImage

# Register your models here.
admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image']
    extra = 1
    max_num = 10
    min_num = 1
    can_delete = True
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
