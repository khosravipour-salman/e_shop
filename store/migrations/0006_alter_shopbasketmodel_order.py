# Generated by Django 3.2.9 on 2021-11-16 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_ordermodel_shopbasketmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopbasketmodel',
            name='order',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='store.ordermodel'),
        ),
    ]
