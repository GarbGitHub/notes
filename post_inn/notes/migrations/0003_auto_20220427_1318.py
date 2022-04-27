# Generated by Django 3.2.9 on 2022-04-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='tests',
            field=models.TextField(blank=True, verbose_name='тесты'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, to='notes.Tag', verbose_name='Тэг'),
        ),
    ]
