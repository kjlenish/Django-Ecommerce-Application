# Generated by Django 4.2.15 on 2024-08-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_data_sheet_alter_category_parent_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1000),
        ),
    ]
