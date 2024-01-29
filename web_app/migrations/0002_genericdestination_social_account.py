# Generated by Django 4.2.9 on 2024-01-29 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0006_alter_socialaccount_extra_data'),
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericdestination',
            name='social_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialaccount.socialaccount'),
        ),
    ]
