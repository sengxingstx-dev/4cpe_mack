# Generated by Django 3.2.15 on 2023-07-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20230716_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
