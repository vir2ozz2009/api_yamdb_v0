"""Urls приложения API."""

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TitlesViewSet, CategoriesViewSet, GenresViewSet, RegistrationAPIView, ReviewViewSet


router = DefaultRouter()

router.register('titles', TitlesViewSet)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
]
