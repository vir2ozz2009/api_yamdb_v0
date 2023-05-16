from rest_framework import serializers

from reviews.models import Review


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
