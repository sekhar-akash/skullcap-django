# Generated by Django 4.2.1 on 2023-06-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('min_amount', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
