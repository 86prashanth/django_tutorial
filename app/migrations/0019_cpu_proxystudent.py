# Generated by Django 4.1.4 on 2023-01-06 17:38

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_begin_contractor_examcenter_human_invigilator_meraexamcenter_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('roll', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProxyStudent',
            fields=[
            ],
            options={
                'ordering': ['id'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app.cpu',),
            managers=[
                ('barking', django.db.models.manager.Manager()),
            ],
        ),
    ]
