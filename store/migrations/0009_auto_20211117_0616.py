# Generated by Django 3.2.9 on 2021-11-17 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_ordermodel_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='total',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=24, null=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='total_quantity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, null=True),
        ),
    ]
