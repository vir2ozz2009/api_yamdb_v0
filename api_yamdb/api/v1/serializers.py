from rest_framework import serializers

import datetime as dt

from django.core.validators import RegexValidator
from reviews.models import Categories, Genres, Titles, Review, User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug')
        extra_kwargs = {
            'slug': {'validators': [RegexValidator(r'^[-a-zA-Z0-9_]+$')]}
        }


class GenresSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genres."""

    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Genres
        fields = ('id', 'name', 'slug')
        extra_kwargs = {
            'slug': {'validators': [RegexValidator(r'^[-a-zA-Z0-9_]+$')]}
        }


class TitlesSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, required=True)
    year = serializers.IntegerField(required=True)
    category = serializers.SlugRelatedField(
        read_only=False,
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=True
    )
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all(),
        required=True
    )

    def validate_year(self, value):
        year = dt.date.today().year
        if (year < value):
            raise serializers.ValidationError('Проверьте год произведения')
        return value

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genres', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'pub_date')

    def validate(self, data):
        title = data.get('title')
        author = data.get('author')

        if title and author:
            existing_reviews = Review.objects.filter(
                title=title, author=author
            )
            if existing_reviews.exists():
                raise serializers.ValidationError(
                    'Отзыв на произведение уже написан'
                )
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    '''Регистрация нового пользователя.'''

    password = serializers.CharField(required=False, write_only=True)
    username = serializers.CharField(
        required=True, max_length=150,
        validators=[RegexValidator(r'^[\w.+-]+\Z', 'Enter a valid username.')])
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'password'
        )
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'bio': {'write_only': True},
        }

    def validate_username(self, value):
        '''Проверка что имя пользователя не равно me.'''

        if value == 'me':
            raise serializers.ValidationError('Имя "me" недопускается!')
        return value

    def create(self, validated_data):
        '''Создаем нового пользователя с валидированными данными.'''

        return User.objects.create_user(**validated_data)
