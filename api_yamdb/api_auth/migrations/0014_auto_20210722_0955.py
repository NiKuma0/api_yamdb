# Generated by Django 2.2.6 on 2021-07-22 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0013_auto_20210722_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='5905', max_length=128, verbose_name='confirmation_code'),
        ),
    ]