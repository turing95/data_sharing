# Generated by Django 5.0 on 2024-01-10 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0028_alter_filetype_group_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='deadline_enforced',
            field=models.BooleanField(default=False),
        ),
    ]
