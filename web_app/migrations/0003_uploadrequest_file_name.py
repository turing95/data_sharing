# Generated by Django 4.2.7 on 2023-11-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_uploadrequest_instructions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrequest',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
