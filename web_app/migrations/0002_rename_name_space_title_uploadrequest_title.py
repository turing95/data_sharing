# Generated by Django 4.2.7 on 2023-11-30 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='space',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='uploadrequest',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]