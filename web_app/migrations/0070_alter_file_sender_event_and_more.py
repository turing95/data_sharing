# Generated by Django 5.0 on 2024-03-14 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0069_remove_space_is_deleted_alter_space_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='sender_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='web_app.senderevent'),
        ),
        migrations.AlterField(
            model_name='genericdestination',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destinations', to='web_app.uploadrequest'),
        ),
        migrations.AlterField(
            model_name='genericdestination',
            name='space',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destinations', to='web_app.space'),
        ),
    ]