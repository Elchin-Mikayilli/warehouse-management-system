# Generated by Django 4.2 on 2025-01-11 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_threshold',
            field=models.PositiveIntegerField(default=20),
        ),
    ]
