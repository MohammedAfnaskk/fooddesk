# Generated by Django 4.2.1 on 2023-06-26 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0007_size_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='pice_variant',
            new_name='price_variant',
        ),
    ]
