# Generated by Django 3.1 on 2020-12-16 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listanimal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='animal',
        ),
        migrations.AddField(
            model_name='animalinfo',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='listanimal.comment'),
        ),
        migrations.AddField(
            model_name='animalnews',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='listanimal.comment'),
        ),
    ]
