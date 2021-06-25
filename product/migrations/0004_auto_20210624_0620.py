# Generated by Django 3.2.4 on 2021-06-24 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210624_0531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': '8. Reviews'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='review',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='comment',
            name='ip',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
