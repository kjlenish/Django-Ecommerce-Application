# Generated by Django 4.2.15 on 2024-09-04 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_order_status_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]