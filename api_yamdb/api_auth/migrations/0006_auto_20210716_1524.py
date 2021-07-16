# Generated by Django 2.2.6 on 2021-07-16 15:24

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0005_auto_20210716_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=150, verbose_name='О себе.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Обязательное поле! Пример: name@fake.com', max_length=254, unique=True, verbose_name='email адресс'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'Пользователь с таким никнеймом уже существует.'}, help_text='Обязательное поле! 150 символов или меньше. Буквы, цифры и @ /./+/-/_', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='никнейм'),
        ),
    ]