# Generated by Django 4.2.9 on 2024-02-25 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0029_remove_file__name_remove_file__url'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_organizations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='space',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spaces', to='web_app.organization'),
        ),
    ]
