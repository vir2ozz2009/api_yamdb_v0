"""Urls приложения API."""

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .routers import CustomRetrieveUpdateUserRouter
from .views import (
    CategoriesViewSet, CommentViewSet, GenresViewSet, GetTokenAPIView,
    RegistrationAPIView, RetrieveUpdateUserViewSet, ReviewViewSet, TitlesViewSet
)

router = DefaultRouter()
router_me = CustomRetrieveUpdateUserRouter()

router.register('titles', TitlesViewSet)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router_me.register(r'me', RetrieveUpdateUserViewSet, basename='me')
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
    path('users/', include(router_me.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
    path('auth/token/', GetTokenAPIView.as_view()),
]
