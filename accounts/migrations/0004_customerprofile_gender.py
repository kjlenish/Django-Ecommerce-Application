# Generated by Django 4.2.15 on 2024-08-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customerprofile_country_code_customerprofile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
