# Generated by Django 4.2.7 on 2023-11-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0004_sender_delete_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
