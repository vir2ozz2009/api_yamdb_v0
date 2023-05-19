"""Вьюхи к API."""

from rest_framework import filters, mixins, permissions, status, viewsets

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Genres, Review, Titles, User


from .permissions import CustomPermission, OnlyAdminPermission, AdminPermission
from .serializers import (
    CategoriesSerializer, CommentSerializer, GenresSerializer,
    GetTokenSerializer, RegistrationSerializer, ReviewSerializer,
    RetrieveUpdateUserSerializer, TitlesSerializers, UserSerializer
)
from .filters import TitleFilter


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Titles."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializers
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend)
    pagination_class = None
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year')
    pagination_class = LimitOffsetPagination


class GenresViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Genres"""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Genres"""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Список отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Список комментарией."""

    serializer_class = CommentSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review_id=self.kwargs.get('review_id')
        )


class RegistrationAPIView(APIView):
    """Регистрация нового пользователя."""

    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
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
            elif User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Это email уже используется'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif (
                User.objects.filter(username=username).exists()
                and not User.objects.filter(email=email).exists()
            ):
                return Response(
                    {'error': 'Неправильный email'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GetTokenAPIView(APIView):
    """Получение токена."""

    serializer_class = GetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    '''
    Кастомный родительский ViewSet для наследования.
    '''
    def get_object(self):
        return self.request.user


class RetrieveUpdateUserViewSet(RetrieveUpdateViewSet):
    '''
    Изменение собственных данных пользователем.
    '''
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
        if request.method == 'PUT':
            return Response(
                {'error': 'Метод PUT не поддерживается'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
