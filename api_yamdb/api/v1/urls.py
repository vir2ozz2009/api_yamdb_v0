"""Urls приложения API."""

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TitlesViewSet, CategoriesViewSet, GenresViewSet


router = DefaultRouter()

router.register('titles', TitlesViewSet)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
