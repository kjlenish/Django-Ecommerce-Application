from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order
from shipping.models import Address
# Create your models here.

class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    
    payment_method_choices = [
        ('Credit/ Debit/ ATM card', 'Credit/ Debit/ ATM card'),
        ('UPI', 'UPI'),
        ('Cash On Delivery', 'Cash On Delivery')
    ]
    payment_method = models.CharField(max_length=254, blank=True, null=True)
    
    payment_status_choices = [
        ('Payment Not Received', 'Payment Not Received'),
        ('Payment Received', 'Payment Received')
    ]
    payment_status = models.CharField(max_length=254, blank=True, null=True, default='Payment Not Initiated')
        
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Payment")
        verbose_name_plural = ("Payments")

    def __str__(self):
        return f"Payment {self.id} by {self.customer} for {self.order.id}"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})