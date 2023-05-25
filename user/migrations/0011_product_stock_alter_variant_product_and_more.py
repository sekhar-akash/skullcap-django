# Generated by Django 4.2.1 on 2023-05-19 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_product_deleted_at_remove_product_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='user.product'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='variant_name',
            field=models.CharField(max_length=200),
        ),
    ]