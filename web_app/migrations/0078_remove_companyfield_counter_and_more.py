# Generated by Django 5.0 on 2024-03-28 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0077_companyfieldgroup_counter_companytemplate_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyfield',
            name='counter',
        ),
        migrations.RemoveField(
            model_name='companyfieldgroup',
            name='counter',
        ),
    ]
