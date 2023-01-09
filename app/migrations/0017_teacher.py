# Generated by Django 3.2.15 on 2023-01-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_queryset_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('empnum', models.IntegerField(unique=True)),
                ('city', models.CharField(max_length=70)),
                ('salary', models.IntegerField()),
                ('join_date', models.DateField()),
            ],
        ),
    ]
