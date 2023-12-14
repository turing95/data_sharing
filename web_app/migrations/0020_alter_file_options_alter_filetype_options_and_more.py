# Generated by Django 5.0 on 2023-12-13 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0019_file_google_drive_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='filetype',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='googledrive',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='sender',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='senderevent',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='uploadrequestfiletype',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='senderevent',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='web_app.uploadrequest'),
        ),
        migrations.AlterField(
            model_name='senderevent',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='web_app.sender'),
        ),
    ]