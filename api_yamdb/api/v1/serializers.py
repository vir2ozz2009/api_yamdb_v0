from rest_framework import serializers

from django.core.validators import RegexValidator
from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug')
        extra_kwargs = {
            'slug': {'validators': [RegexValidator(r'^[-a-zA-Z0-9_]+$')]}
        }


class GenresSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genres."""

    class Meta:
        model = Genres
        fields = ('id', 'name', 'slug')
        extra_kwargs = {
            'slug': {'validators': [RegexValidator(r'^[-a-zA-Z0-9_]+$')]}
        }


class TitlesSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=False, slug_field='slug', queryset=Categories.objects.all()
    )
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'category', 'genres')
