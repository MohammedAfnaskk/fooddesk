# Generated by Django 4.2.1 on 2023-06-20 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_address_fullname_address_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
