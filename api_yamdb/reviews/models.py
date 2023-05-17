import random

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models

CHARS_TO_SHOW = 15

role_list = (
    ('admin', 'Админ'),
    ('user', 'Пользователь'),
    ('moderator', 'Модератор')
)


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


class CustomUserManager(UserManager):
    """Кастомный менеджер для создания пользователей."""

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с email, паролем, именем
        и отправляет confirmation code на почту для дальнейшего получения
        jwt токена.
        """

        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=random.randint(100000000, 999999999),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        send_mail(
            'Ключ для вашего аккаунта',
            f'Для получения токена воспользуйтесь ключём:'
            f'{user.confirmation_code}',
            'yamdb@example.com',
            [email],
            fail_silently=False
        )
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        '''
        Создает и возвращает суперпользователя с email, паролем, именем
        и присваивае суперпользователю роль admin.
        '''

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    bio = models.TextField(
        'Биография',
        blank=True,
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
    objects = CustomUserManager()

    def create_jwt_token(self):
        '''Создает и возвращает jwt токен для пользователя'''

        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)


class Review(models.Model):
    """Модели для отзывов."""

    title = models.ForeignKey(
        Titles,
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
