# Generated by Django 3.2.8 on 2021-11-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_note_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Активный'),
        ),
        migrations.AlterField(
            model_name='note',
            name='is_favorites',
            field=models.BooleanField(db_index=True, default=False, verbose_name='В избранном'),
        ),
    ]
