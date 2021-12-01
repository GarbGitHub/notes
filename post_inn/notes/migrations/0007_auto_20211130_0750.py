# Generated by Django 3.2.8 on 2021-11-30 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_note_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(blank=True, verbose_name='Текст заметки'),
        ),
    ]