from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from shipping.models import Address

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=254, blank=True, null=True)
    
    status_choices = [
        ('In Cart', 'In Cart'),
        ('Order Received', 'Order Received'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Order Rejected', 'Order Rejected'),
        ('Order Cancelled', 'Order Cancelled'),
        ('Order Shipped', 'Order Shipped'),
        ('Order Delivered', 'Order Delivered')
    ]
    order_status = models.CharField(max_length=254, choices=status_choices, blank=True, null=True, default='In Cart')
    
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    date_shipped = models.DateTimeField(null=True, blank=True)
    
    date_delivered = models.DateTimeField(null=True, blank=True)        
    
    cancellation_reason = models.CharField(max_length=500, blank=True, null=True)
    date_cancelled = models.DateTimeField(null=True, blank=True)        
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})



class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    

    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")

    def get_item_price(self):
        return(self.price * self.quantity)
        
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_absolute_url(self):
        return reverse("OrderItem_detail", kwargs={"pk": self.pk})
