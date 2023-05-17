from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import RegistrationAPIView, ReviewViewSet

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
]
