# Generated by Django 3.2.15 on 2022-09-12 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
