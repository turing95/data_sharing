# Generated by Django 4.2.9 on 2024-02-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0022_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]