# Generated by Django 5.0 on 2024-03-17 15:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0072_contact_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='sender',
            name='notification_task',
        ),
        migrations.AddField(
            model_name='output',
            name='feedback',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='output', to='web_app.feedback'),
        ),
    ]