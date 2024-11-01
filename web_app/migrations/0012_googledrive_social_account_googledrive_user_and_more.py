# Generated by Django 4.2.9 on 2024-02-10 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0006_alter_socialaccount_extra_data'),
        ('web_app', '0011_senderevent_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='googledrive',
            name='social_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialaccount.socialaccount'),
        ),
        migrations.AddField(
            model_name='googledrive',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onedrive',
            name='social_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialaccount.socialaccount'),
        ),
        migrations.AddField(
            model_name='onedrive',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sharepoint',
            name='social_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialaccount.socialaccount'),
        ),
        migrations.AddField(
            model_name='sharepoint',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
