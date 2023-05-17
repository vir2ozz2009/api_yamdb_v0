"""Вьюхи к API."""

from rest_framework import filters, permissions, viewsets

from django.shortcuts import get_object_or_404

from reviews.models import Categories, Titles, Genres

from .serializers import (
    GenresSerializer, CategoriesSerializer, TitlesSerializers
)
from .permissions import AdminChangeOnly


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Titles."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializers
    permission_classes = (AdminChangeOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Genres"""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoriesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Genres"""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.AllowAny,)
