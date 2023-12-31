# Generated by Django 4.2.1 on 2023-06-18 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0004_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('discount_amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admindashboard.offer'),
        ),
    ]
