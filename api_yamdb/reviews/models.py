"""Модели для произведений."""

from django.db import models

CHARS_TO_SHOW = 15


class Categories(models.Model):
    """Модель категорий (типов) произведения."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name[:CHARS_TO_SHOW]


class Genres(models.Model):
    """Модель жанров произведения."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name[:CHARS_TO_SHOW]


class Titles(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(max_length=500)
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
