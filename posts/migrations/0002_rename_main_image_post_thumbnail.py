# Generated by Django 5.0 on 2023-12-31 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='main_image',
            new_name='thumbnail',
        ),
    ]