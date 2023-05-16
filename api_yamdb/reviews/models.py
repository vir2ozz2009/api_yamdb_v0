from django.contrib.auth.models import AbstractUser
from django.db import models

CHARS_TO_SHOW = 15


class Review(models.Model):
    """Модели для отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:CHARS_TO_SHOW]
