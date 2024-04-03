# Generated by Django 5.0 on 2024-04-02 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0085_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='textrequest',
            name='target',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='web_app.companytextfield'),
        ),
        migrations.DeleteModel(
            name='Target',
        ),
    ]
