# Generated by Django 5.1.5 on 2025-03-30 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_customer_balance_alter_customer_customerid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
