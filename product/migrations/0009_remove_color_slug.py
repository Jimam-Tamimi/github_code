# Generated by Django 3.2.4 on 2021-06-25 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_color_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='slug',
        ),
    ]
