<<<<<<< HEAD
# Generated by Django 3.2.9 on 2021-11-24 16:48
=======
# Generated by Django 3.2.8 on 2021-12-01 11:46
>>>>>>> 239e3a10c8a9a3d18f025f66adff3b91b3596839

from django.db import migrations


class Migration(migrations.Migration):
<<<<<<< HEAD

=======
>>>>>>> 239e3a10c8a9a3d18f025f66adff3b91b3596839
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
