# Generated by Django 4.1.4 on 2022-12-29 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='age',
            field=models.IntegerField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='contact',
            field=models.IntegerField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(default=datetime.datetime(2022, 12, 29, 4, 2, 58, 333982, tzinfo=datetime.timezone.utc), max_length=50),
            preserve_default=False,
        ),
    ]
