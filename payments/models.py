from django.db import models
from django.urls import reverse
from orders.models import Order
from shipping.models import Address
# Create your models here.

class Payment(models.Model):
    order = models.OneToOneField(Order, null=True, blank=True, on_delete=models.CASCADE, related_name='payment')
    razorpay_payment_id = models.CharField(max_length=254, blank=True, null=True)
    
    billing_amount =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    
    payment_method_choices = [
        ('card', 'Credit/ Debit/ ATM card'),
        ('netbanking', 'Net Banking'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
        ('Cash On Delivery', 'Cash On Delivery')
    ]
    payment_method = models.CharField(max_length=254, choices=payment_method_choices, blank=True, null=True)
    
    payment_status_choices = [
        ('Payment Initiated', 'Payment Initiated'),
        ('Payment Not Received', 'Payment Not Received'),
        ('Payment Received', 'Payment Received')
    ]
    payment_status = models.CharField(max_length=254, choices=payment_status_choices, blank=True, null=True, default='Payment Not Initiated')
        
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Payment")
        verbose_name_plural = ("Payments")

    def __str__(self):
        return f"Payment {self.id} by {self.order.customer} for {self.order.id}"

    def get_absolute_url(self):
        return reverse("Payment_detail", kwargs={"pk": self.pk})