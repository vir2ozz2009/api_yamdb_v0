# Generated by Django 3.2 on 2023-05-25 11:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Используйте цифры, латинские буквы, дефис, подчеркивание.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Slug категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название жанра'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Используйте цифры, латинские буквы, дефис, подчеркивание.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Slug жанра'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название тайтла'),
        ),
    ]
