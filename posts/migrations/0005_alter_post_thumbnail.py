# Generated by Django 5.0 on 2024-01-23 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_description_alter_post_favicon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.URLField(blank=True, default='null', max_length=500, null=True),
        ),
    ]
