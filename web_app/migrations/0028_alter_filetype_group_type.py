# Generated by Django 5.0 on 2023-12-26 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0027_remove_uploadrequest_unique_request_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetype',
            name='group_type',
            field=models.ForeignKey(blank=True, limit_choices_to={'group': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_app.filetype'),
        ),
    ]