# Generated by Django 4.2.1 on 2023-05-19 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=100)),
                ('stock', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
            ],
        ),
    ]
