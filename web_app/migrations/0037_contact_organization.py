# Generated by Django 4.2.9 on 2024-03-02 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0036_space_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='web_app.organization'),
        ),
    ]