# Generated by Django 5.0 on 2024-01-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0039_remove_space_deadline_notification_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='notified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]