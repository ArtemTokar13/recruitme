# Generated by Django 3.2.8 on 2021-11-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitme_app', '0006_auto_20211106_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hiring_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]