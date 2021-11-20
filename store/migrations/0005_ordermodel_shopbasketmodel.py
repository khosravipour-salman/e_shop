# Generated by Django 3.2.9 on 2021-11-16 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_alter_bookmodel_age_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32)),
                ('address', models.TextField()),
                ('delivery_date', models.DateField()),
                ('phone_number', models.CharField(max_length=11)),
                ('postal_code', models.CharField(max_length=10)),
                ('national_code', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('Prepayment', 'prepayment'), ('Inprocess', 'inprocess'), ('Delivered', 'delivered'), ('Canceled', 'canceled')], max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='ShopBasketModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to='store.bookmodel')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='store.ordermodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shop_basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
