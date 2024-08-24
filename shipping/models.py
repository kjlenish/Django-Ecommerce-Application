from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=254, blank=True, null=True)
    last_name = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    country_code = models.CharField(default="+91", max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address_line1 = models.TextField(max_length=254, blank=True, null=True)
    address_line2 = models.TextField(max_length=254, blank=True, null=True)
    landmark = models.TextField(max_length=254, blank=True, null=True)
    city = models.TextField(max_length=254, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    state = models.TextField(max_length=254, blank=True, null=True)
    country = models.TextField(max_length=254, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)
    

    

    class Meta:
        verbose_name = ("Address")
        verbose_name_plural = ("Addresses")

    def __str__(self):
        return (f"{self.address_line1}, {self.address_line2}, {self.state}, {self.country}")

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})


