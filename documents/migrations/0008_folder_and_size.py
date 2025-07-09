from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_remove_document_device_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='documents', to='documents.folder'),
        ),
        migrations.AddField(
            model_name='document',
            name='size',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
