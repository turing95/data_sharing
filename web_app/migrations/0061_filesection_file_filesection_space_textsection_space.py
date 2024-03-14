# Generated by Django 5.0 on 2024-03-11 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0060_grant'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesection',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_app.file'),
        ),
        migrations.AddField(
            model_name='filesection',
            name='space',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_sections', to='web_app.space'),
        ),
        migrations.AddField(
            model_name='textsection',
            name='space',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_sections', to='web_app.space'),
        ),
    ]