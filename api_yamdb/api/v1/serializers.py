from rest_framework import serializers
import datetime as dt

from django.core.validators import RegexValidator
from reviews.models import Categories, Genres, Titles


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
