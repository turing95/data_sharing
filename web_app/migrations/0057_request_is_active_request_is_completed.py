# Generated by Django 5.0 on 2024-03-11 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0056_filesection_textsection_spacesection'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='request',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
