# Generated by Django 3.2.9 on 2021-11-24 16:48

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
