"""Валидаторы."""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


regex_validator = [
    RegexValidator(
        regex=r'^[-a-zA-Z0-9_]+$',
        message='Используйте цифры, латинские буквы, дефис, подчеркивание.'
    )
]


def validate_username(value):
    if value == 'me':
        raise ValidationError("Имя пользователя 'me' недопустимо.")
