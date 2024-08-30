from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from datetime import datetime

@receiver(pre_save, sender=Order)
def create_profile(sender, instance, **kwargs):
    if instance.pk:
        if instance.order_Status == "Order Shipped":
            instance.date_shipped = datetime.now()
