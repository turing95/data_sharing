# Generated by Django 4.2.7 on 2023-11-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_alter_space_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
