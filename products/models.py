from django.db import models
from django.db.models import JSONField
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    slug = models.CharField(max_length=254, blank=True, unique=True)
    image = models.ImageField(upload_to='categories/', default='categories/default_category.jpg')

    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description =  models.CharField(max_length=500, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.name.replace(" ", "-"))
            
            if self.parent_category and self.parent_category.slug:
                new_slug = f"{self.parent_category.slug}-{new_slug}"
            
            self.slug = new_slug
            
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})
    

class Product(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    price = models.FloatField(null=False, blank=False)
    
    max_quantity = models.IntegerField(null=False, blank=False, default=5)
    stock = models.IntegerField(null=False, blank=False)
    delivery_charge = models.FloatField(null=False, blank=False, default=40)
    
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    is_sale = models.BooleanField(null=False, blank=False, default=False)
    sale_price = models.FloatField(null=True, blank=True)
    
    short_description =  models.CharField(max_length=500, blank=True)
    description =  models.CharField(max_length=3000, null=False, blank=False)
    specification = models.JSONField(blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"{self.product.name} Image {self.id}"
