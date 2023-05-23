"""Сериалайзеры."""

import datetime as dt

from rest_framework import serializers

from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genres."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов к произведениям."""

    category = serializers.SlugRelatedField(
        required=True,
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        required=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов к произведениям."""

    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        """Проверка чтобы дата произведения не была из будущего."""
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год произведения')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        """Валидация оценки в промежутке от 1 до 10."""
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка от 1 до 10')
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title).exists():
            raise serializers.ValidationError(
                'Отзыв на произведение уже написан.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')


class RegistrationSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя."""

    password = serializers.CharField(required=False, write_only=True)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(r'^[\w.+-]+\Z', 'Enter a valid username.')],
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'password',
        )
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'bio': {'write_only': True},
        }

    def validate_username(self, value):
        """Проверка что имя пользователя не равно me."""
        if value == 'me':
            raise serializers.ValidationError('Имя "me" недопускается!')
        return value

    def create(self, validated_data):
        """Создаем нового пользователя с валидированными данными."""
        return User.objects.create_user(**validated_data)


class GetTokenSerializer(serializers.Serializer):
    """Получение jwt токена."""

    email = serializers.EmailField(write_only=True, max_length=256),
    confirmation_code = serializers.CharField(write_only=True),
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        """Проверяем, что передан username и confirmation_code."""
        username = self.initial_data.get('username', None)
        confirmation_code = self.initial_data.get('confirmation_code', None)
        if username is None:
            raise serializers.ValidationError(
                'Требуется username!'
            )
        if (confirmation_code is None
            or confirmation_code != get_object_or_404(
                User,
                username=username).confirmation_code):
            raise serializers.ValidationError(
                'confirmation_code некорректен!'
            )
        user = get_object_or_404(User,
                                 username=username,
                                 confirmation_code=confirmation_code)
        return {'token': user.create_jwt_token}


class RetrieveUpdateUserSerializer(serializers.ModelSerializer):
    """Изменение собственных данных пользователем."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    """Изменение данных о пользователе администратором."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
