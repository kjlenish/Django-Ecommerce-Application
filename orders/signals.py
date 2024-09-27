from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, OrderItem
from products.models import Product
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
def update_date_cancelled_and_stock(sender, instance, **kwargs):
    if instance.pk:
        existing_order = Order.objects.get(pk=instance.pk)
        if existing_order.order_status != "Order Cancelled" and instance.order_status == "Order Cancelled":
            instance.date_cancelled = datetime.now()
            order_items = OrderItem.objects.filter(order=existing_order)
            for item in order_items:
                    product = Product.objects.get(id=item.product.id)
                    product.update_stock_on_order(item.quantity, instance.order_status)            
            