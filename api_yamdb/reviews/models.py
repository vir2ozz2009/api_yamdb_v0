"""Модели для произведений."""

from django.core.validators import RegexValidator
from django.db import models

CHARS_TO_SHOW = 15


class Categories(models.Model):
    """Модель категорий (типов) произведения."""

    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        blank=False,
        null=False
    )
    validators = [
        RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Используйте цифры, латинские буквы, дефис, подчеркивание.'
        )
    ]

    def __str__(self):
        return self.name[:CHARS_TO_SHOW]


class Genres(models.Model):
    """Модель жанров произведения."""

    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        blank=False,
        null=False
    )
    validators = [
        RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Используйте цифры, латинские буквы, дефис, подчеркивание.'
        )
    ]

    def __str__(self):
        return self.name[:CHARS_TO_SHOW]


class Titles(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genres = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name[:CHARS_TO_SHOW]
