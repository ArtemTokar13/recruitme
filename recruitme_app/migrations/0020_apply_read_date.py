# Generated by Django 3.2.8 on 2021-12-06 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitme_app', '0019_auto_20211206_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='read_date',
            field=models.DateTimeField(default=None),
        ),
    ]
