# Generated by Django 5.0.4 on 2024-04-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.ImageField(upload_to='documents/'),
        ),
    ]
