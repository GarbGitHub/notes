# Generated by Django 3.2.8 on 2022-05-10 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='имя')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='описание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='активна')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': ('категория',),
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='краткое содержание')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='активный')),
                ('is_boxed', models.BooleanField(db_index=True, default=False, verbose_name='закрепленный')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fordev.pagecategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': ('страница',),
                'verbose_name_plural': 'страницы',
            },
        ),
    ]
