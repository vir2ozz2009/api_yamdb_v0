"""Urls приложения API."""

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CategoriesViewSet, CommentViewSet, GenresViewSet, RegistrationAPIView,
    ReviewViewSet, TitlesViewSet,
)

router = DefaultRouter()

router.register('titles', TitlesViewSet)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
]
