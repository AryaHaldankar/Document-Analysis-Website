# Generated by Django 5.2 on 2025-07-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='user_id',
            field=models.CharField(max_length=500),
        ),
    ]
