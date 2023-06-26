# Generated by Django 4.2.1 on 2023-06-08 05:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_address_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='stock',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]