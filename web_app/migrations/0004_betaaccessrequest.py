# Generated by Django 4.2.9 on 2024-01-30 18:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0003_organization_user_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='BetaAccessRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=50)),
                ('industry', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('company', models.TextField(blank=True, null=True)),
                ('intended_use', models.TextField(blank=True, null=True)),
                ('first_touchpoint', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]