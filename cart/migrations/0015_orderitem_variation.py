# Generated by Django 4.2.1 on 2023-06-26 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0008_rename_pice_variant_variation_price_variant'),
        ('cart', '0014_cart_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admindashboard.variation'),
            preserve_default=False,
        ),
    ]
