# Generated by Django 4.2.15 on 2024-09-04 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_Status',
            new_name='order_status',
        ),
    ]