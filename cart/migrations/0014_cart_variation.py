# Generated by Django 4.2.1 on 2023-06-26 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0007_size_size'),
        ('cart', '0013_order_product_qty_alter_cart_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='variation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admindashboard.variation'),
            preserve_default=False,
        ),
    ]
