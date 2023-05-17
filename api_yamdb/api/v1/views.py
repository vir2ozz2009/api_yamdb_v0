"""Вьюхи к API."""

from rest_framework import filters, permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from reviews.models import Categories, Titles, Genres, Review, User

from .serializers import (
    GenresSerializer, CategoriesSerializer, TitlesSerializers, RegistrationSerializer, ReviewSerializer
)
from .permissions import AdminChangeOnly


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Titles."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializers
    permission_classes = (AdminChangeOnly,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = None
    filterset_fields = {
        'category': ['category__slug'],
        'genre': ['genres__slug'],
        'name': ['name'],
        'year': ['year'],
    }
    ordering_fields = ('name', 'year')



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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Список отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    queryset = Review.objects.select_related('title')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.request.data.get('title')
        )


class RegistrationAPIView(APIView):
    """Регистрация нового пользователя."""

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if (User.objects.filter(username=username).exists()
               and User.objects.filter(email=email).exists()):
                return Response(
                    {'error': 'Пользователь с таким username'
                     'или email уже существует'},
                    status=status.HTTP_200_OK
                )
            elif User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Это email уже используется'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif (User.objects.filter(username=username).exists()
                  and not User.objects.filter(email=email).exists()):
                return Response(
                    {'error': 'Неправильный email'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
