import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.shortcuts import get_object_or_404
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from reviews.models import Categories, Comment, Genres, Review, Titles, User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'slug': {'validators': [
                UniqueValidator(queryset=Categories.objects.all()),
                RegexValidator(r'^[-a-zA-Z0-9_]+$')
            ]}
        }


class GenresSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genres."""

    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'slug': {'validators': [
                UniqueValidator(queryset=Genres.objects.all()),
                RegexValidator(r'^[-a-zA-Z0-9_]+$')
            ]}
        }


class TitlesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов к произведениям."""

    category = serializers.SlugRelatedField(
        required=True,
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genres = serializers.SlugRelatedField(
        required=True,
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов к произведениям."""

    category = CategoriesSerializer(read_only=True)
    genres = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год произведения')
        return value

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return int(average_rating) if average_rating else None

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка от 1 до 10')
        return value

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
