# Generated by Django 5.0 on 2024-03-13 08:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0065_textrequest_instructions_uploadrequest_instructions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='senderevent',
            name='text',
        ),
        migrations.CreateModel(
            name='TextOutput',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=50)),
                ('text', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_outputs', to='web_app.company')),
                ('sender_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_outputs', to='web_app.senderevent')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]