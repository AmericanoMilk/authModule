# Generated by Django 3.2.4 on 2022-10-21 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authuser',
            old_name='created_time',
            new_name='creationTime',
        ),
        migrations.RenameField(
            model_name='authuser',
            old_name='updated_time',
            new_name='updatedTime',
        ),
    ]
