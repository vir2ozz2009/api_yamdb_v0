# Generated by Django 3.2 on 2023-05-16 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
