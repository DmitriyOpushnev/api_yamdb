from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, mixins, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, User
from api.serializers import (CategorySerializer, GenreSerializer,
                             SignUpSerializer, TokenSerializer)


class ListCreateDelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # to be updated
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class CategoryViewSet(ListCreateDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class APISignup(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_mail(
            subject='API YaMDB!',
            message=(
                f'Добро пожаловать на сервис YaMDB, {user.username}!'
                f'\nДля дальнейшей работы с API используйте код подтверждения.'
                f'\nВаш код подтверждения - {user.confirmation_code}'
            ),
            from_email='api@yamdb.ru',
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователя не существует.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.data['confirmation_code'] == user.confirmation_code:
            token = str(RefreshToken.for_user(user).access_token)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST
        )
