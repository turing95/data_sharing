# Generated by Django 5.0 on 2024-04-08 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0094_filefilefield'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='grant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='space', to='web_app.grant'),
        ),
        migrations.AddField(
            model_name='space',
            name='source_grant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='linked_spaces', to='web_app.grant'),
        ),
        migrations.AddField(
            model_name='uploadrequest',
            name='target',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='web_app.filefield'),
        ),
    ]