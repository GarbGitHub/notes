# Generated by Django 3.2.8 on 2022-02-02 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_alter_note_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата и время создания'),
        ),
    ]
