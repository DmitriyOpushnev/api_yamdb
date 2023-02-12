from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permission import (AdminAnonPermission, AdminOnlyPermission,
                            AuthorModeratorAdminPermission)
from api.serializers import (CategorySerializer, CommentSerializers,
                             GenreSerializer, ReadTitleSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TokenSerializer, UserMeSerializer,
                             UsersSerializer, WriteTitleSerializer)
from api.viewsets import ListCreateDelViewSet
from reviews.models import Category, Genre, Review, Title, User, ADMIN


class APISignup(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            return Response(
                'Проблемы с базой данных.',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='API YaMDB!',
            message=(
                f'Добро пожаловать на сервис YaMDB, {user.username}!'
                f'\nДля дальнейшей работы с API используйте код подтверждения.'
                f'\nВаш код подтверждения - {confirmation_code}'
            ),
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователя не существует.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if default_token_generator.check_token(
            user, confirmation_code
        ):
            token = str(RefreshToken.for_user(user).access_token)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryViewSet(ListCreateDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related('category').\
        prefetch_related('genre').annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminAnonPermission, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadTitleSerializer
        return WriteTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (AuthorModeratorAdminPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnlyPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(IsAuthenticated,)
    )
    def get_users_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.role == ADMIN:
                serializer = UsersSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = UserMeSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
