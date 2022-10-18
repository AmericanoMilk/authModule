# Generated by Django 3.2.4 on 2022-10-18 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0002_tenant_token_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='status',
            field=models.CharField(choices=[('FORBIDDEN', 'FORBIDDEN'), ('NORMAL', 'NORMAL')], default='NORMAL', max_length=24),
        ),
    ]
