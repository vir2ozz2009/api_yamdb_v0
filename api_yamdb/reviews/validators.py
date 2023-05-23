"""Валидаторы."""

from django.core.validators import RegexValidator

regex_validator = [
    RegexValidator(
        regex=r'^[-a-zA-Z0-9_]+$',
        message='Используйте цифры, латинские буквы, дефис, подчеркивание.'
    )
]
