# Generated by Django 5.0 on 2024-03-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0049_alter_request_title_alter_textrequest_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputrequest',
            name='position',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
