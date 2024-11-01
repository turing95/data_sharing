# Generated by Django 4.2.9 on 2024-02-27 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0031_remove_userorganization_role_organizationinvitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationinvitation',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='web_app.organization'),
        ),
    ]
