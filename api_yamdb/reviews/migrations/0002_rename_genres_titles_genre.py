# Generated by Django 3.2 on 2023-05-19 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='genres',
            new_name='genre',
        ),
    ]