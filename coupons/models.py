from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=128, unique=True)
    
    discount_type_choices = [
        ("Percentage", "Percentage"),
        ("Fixed Amount", "Fixed Amount")
    ]
    discount_type = models.CharField(max_length=128, choices=discount_type_choices)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    
    valid_from = models.DateTimeField(default=timezone.now())
    valid_to = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    minimum_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    class Meta:
        verbose_name = ("Coupon")
        verbose_name_plural = ("Coupons")

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("coupon_detail", kwargs={"pk": self.pk})
    
    def is_valid(self):
        if self.valid_to:
            now = timezone.now()
            if not (self.valid_from <= now <= self.valid_to):
                return False, "The coupon has expired"
        
        if self.is_active:
            return True, None
        
        return False, "The coupon is Inactive"
