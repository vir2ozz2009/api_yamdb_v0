from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Review

from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Список отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    queryset = Review.objects.select_related('title')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.request.data.get('title')
        )
