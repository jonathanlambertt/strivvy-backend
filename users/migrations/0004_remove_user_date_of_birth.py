# Generated by Django 5.0 on 2023-12-18 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
    ]
