# Generated by Django 4.2.9 on 2024-03-04 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0037_contact_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadrequestfiletype',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='uploadrequestfiletype',
            name='upload_request',
        ),
        migrations.RemoveField(
            model_name='uploadrequest',
            name='file_types',
        ),
        migrations.DeleteModel(
            name='FileType',
        ),
        migrations.DeleteModel(
            name='UploadRequestFileType',
        ),
    ]
