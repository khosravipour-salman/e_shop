# Generated by Django 3.2.9 on 2021-11-08 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_bookmodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=8),
        ),
    ]
