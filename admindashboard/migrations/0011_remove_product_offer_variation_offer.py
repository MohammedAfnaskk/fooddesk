# Generated by Django 4.2.1 on 2023-06-29 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0010_alter_variation_price_variant_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='offer',
        ),
        migrations.AddField(
            model_name='variation',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admindashboard.offer'),
        ),
    ]