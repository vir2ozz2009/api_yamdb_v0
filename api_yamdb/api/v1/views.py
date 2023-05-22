"""Вьюхи к API."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import DestroyCreateListMixins, RetrieveUpdateViewSet
from .pagination import GenresAndCategoriesPagination
from .permissions import AdminPermission, CustomPermission, OnlyAdminPermission
from .serializers import (
    CategoriesSerializer, CommentSerializer, GenresSerializer,
    GetTokenSerializer, RegistrationSerializer, RetrieveUpdateUserSerializer,
    ReviewSerializer, TitlesGetSerializer, TitlesPostSerializer,
    UserSerializer,
)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Titles."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year')
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesPostSerializer


class GenresViewSet(DestroyCreateListMixins):
    """Вьюсет модели Genres."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = GenresAndCategoriesPagination

    def create(self, request, *args, **kwargs):
        """Создание жанров с учетом того что поле slug уникальное."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slug = serializer.validated_data['slug']

        if Genre.objects.filter(slug=slug).exists():
            return Response(
                {'error': 'Жанр с таким slug уже существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CategoriesViewSet(DestroyCreateListMixins):
    """Вьюсет модели Categories"""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = GenresAndCategoriesPagination

    def create(self, request, *args, **kwargs):
        """Создание категорий с учетом того что поле slug уникальное."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slug = serializer.validated_data['slug']

        if Category.objects.filter(slug=slug).exists():
            return Response(
                {'error': 'Категория с таким slug уже существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Список отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        """Получение отзывов."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание отзывов."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        author = self.request.user

        existing_review = title.reviews.filter(author=author).exists()
        if existing_review:
            raise serializers.ValidationError(
                'Отзыв на произведение уже написан.'
            )
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Список комментарией."""

    serializer_class = CommentSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        """Получение комментариев."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.select_related('author')

    def perform_create(self, serializer):
        """Сохранение комментариев."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class RegistrationAPIView(APIView):
    """Регистрация нового пользователя."""

    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Обработка POST-запросов для регистрации нового пользователя."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if (
                User.objects.filter(username=username).exists()
                and User.objects.filter(email=email).exists()
            ):
                return Response(
                    {
                        'error': 'Пользователь с таким username'
                        'или email уже существует'
                    },
                    status=status.HTTP_200_OK,
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Это email уже используется'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                User.objects.filter(username=username).exists()
                and not User.objects.filter(email=email).exists()
            ):
                return Response(
                    {'error': 'Неправильный email'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPIView(APIView):
    """Получение токена."""

    serializer_class = GetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Обработка POST-запросов для получения токена."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateUserViewSet(RetrieveUpdateViewSet):
    """Изменение собственных данных пользователем."""

    queryset = User.objects.all()
    serializer_class = RetrieveUpdateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(viewsets.ModelViewSet):
    """Изменение данных о пользователе администратором."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        """Обработка запросов на обновление данных о пользователе."""
        if request.method == 'PUT':
            return Response(
                {'error': 'Метод PUT не поддерживается'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
