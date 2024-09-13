from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    
    rating_choices = [
        ('1', "Bad"),
        ('2', "Below Average"), 
        ('3', "Average"),
        ('4', "Good"),
        ('5', "Excellent")
    ]
    rating = models.CharField(choices=rating_choices, max_length=30, null=True, blank=True)
    
    review = models.CharField(max_length=500, null=True, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = ("Review")
        verbose_name_plural = ("Reviews")

    def __str__(self):
        return f"{self.user.username} commented {self.review}"

    def get_absolute_url(self):
        return reverse("Review_detail", kwargs={"pk": self.pk})
