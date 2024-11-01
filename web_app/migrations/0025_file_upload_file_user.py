# Generated by Django 4.2.9 on 2024-02-18 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import web_app.storage_backends.backends


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0024_notificationssettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='upload',
            field=models.FileField(blank=True, null=True, storage=web_app.storage_backends.backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL),
        ),
    ]
