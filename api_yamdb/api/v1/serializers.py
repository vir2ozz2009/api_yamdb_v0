from rest_framework import serializers

from django.core.validators import RegexValidator

from reviews.models import Review, User


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
