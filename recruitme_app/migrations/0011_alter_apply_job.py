# Generated by Django 3.2.8 on 2021-11-15 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitme_app', '0010_auto_20211115_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='job',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]