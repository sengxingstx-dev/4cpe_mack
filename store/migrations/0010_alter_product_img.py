# Generated by Django 3.2.15 on 2023-07-16 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_income_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]