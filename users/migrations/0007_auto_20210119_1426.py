# Generated by Django 3.1 on 2021-01-19 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210119_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
