# Generated by Django 4.2.9 on 2024-02-08 21:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0009_sendernotificationssettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharePoint',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('folder_id', models.CharField(max_length=255)),
                ('site_id', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
