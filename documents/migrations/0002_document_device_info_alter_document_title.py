# Generated by Django 5.0.4 on 2024-04-10 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='device_info',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
