from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from datetime import datetime

@receiver(pre_save, sender=Order)
def update_date_shipped(sender, instance, **kwargs):
    if instance.pk:
        existing_order = Order.objects.get(pk=instance.pk)
        if existing_order.order_status != "Order Shipped" and instance.order_status == "Order Shipped":
            instance.date_shipped = datetime.now()
            
@receiver(pre_save, sender=Order)
def update_date_delivered(sender, instance, **kwargs):
    if instance.pk:
        existing_order = Order.objects.get(pk=instance.pk)
        if existing_order.order_status != "Order Delivered" and instance.order_status == "Order Delivered":
            instance.date_delivered = datetime.now()

@receiver(pre_save, sender=Order)
def update_date_cancelled(sender, instance, **kwargs):
    if instance.pk:
        existing_order = Order.objects.get(pk=instance.pk)
        if existing_order.order_status != "Order Cancelled" and instance.order_status == "Order Cancelled":
            instance.date_cancelled = datetime.now()

            
            