from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from shipping.models import Address

# Create your models here.

class CustomerProfile(models.Model):
    gender_choice = [
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    gender = models.CharField(max_length=254, blank=True, null=True)
    dob = models.DateField(default=None, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    country_code = models.CharField(default="+91", max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    old_cart = models.TextField(blank=True, null=True)
    primary_address = models.ForeignKey(Address, on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    

    class Meta:
        verbose_name = ("CustomerProfile")
        verbose_name_plural = ("CustomerProfiles")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})

    