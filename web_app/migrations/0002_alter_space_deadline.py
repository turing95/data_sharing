# Generated by Django 4.2.7 on 2023-11-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
    ]
