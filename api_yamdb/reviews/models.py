from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role_list = (('admin', 'Админ'),
                 ('user', 'Пользователь'),
                 ('moderator', 'Модератор')
    )
    role = models.CharField(
        'Роль пользователя',
        choices=role_list,
        max_length=10,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=9,
        blank=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
