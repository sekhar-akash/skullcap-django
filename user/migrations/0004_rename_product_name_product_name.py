# Generated by Django 4.2.1 on 2023-05-16 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_product_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='name',
        ),
    ]
