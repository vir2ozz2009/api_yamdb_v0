from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Review, User

from .serializers import RegistrationSerializer, ReviewSerializer


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
