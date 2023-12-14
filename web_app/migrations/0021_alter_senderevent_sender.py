# Generated by Django 5.0 on 2023-12-14 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0020_alter_file_options_alter_filetype_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='senderevent',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='web_app.sender'),
        ),
    ]
