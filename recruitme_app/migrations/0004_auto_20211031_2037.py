# Generated by Django 3.2.8 on 2021-10-31 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitme_app', '0003_auto_20211031_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
