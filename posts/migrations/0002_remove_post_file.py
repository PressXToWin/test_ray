# Generated by Django 4.2.7 on 2023-12-06 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='file',
        ),
    ]