# Generated by Django 3.2.15 on 2023-07-11 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_auto_20230703_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='delivery',
            field=models.CharField(blank=True, choices=[('Houng ah loun', 'Houng ah loun'), ('Ah nou sit', 'Ah nou sit')], default='Houng ah loun', max_length=30, null=True),
        ),
    ]