# Generated by Django 4.1.4 on 2022-12-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_employee_age_employee_contact_employee_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.CharField(max_length=100)),
                ('mname', models.CharField(max_length=100)),
                ('mconn', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'mobile',
            },
        ),
    ]