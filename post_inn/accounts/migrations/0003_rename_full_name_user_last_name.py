# Generated by Django 3.2.8 on 2021-12-01 11:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_alter_user_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='last_name',
        ),
    ]
