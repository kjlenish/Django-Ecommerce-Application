# Generated by Django 4.2.15 on 2024-08-17 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(blank=True, max_length=254, unique=True),
        ),
    ]
