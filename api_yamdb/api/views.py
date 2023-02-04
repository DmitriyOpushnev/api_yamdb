from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from reviews.models import Category, Genre, Review, Title, Comment
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (CategorySerializer, GenreSerializer,
                             ReadTitleSerializer, ReviewSerializer, WriteTitleSerializer, CommentSerializers)



class ListCreateDelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # to be updated
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    queryset = Title.objects.annotate(  # не совсем уверен
        rating=Avg('reviews__score')    # что правильно
    ).order_by('-id')                   # но


class CategoryViewSet(ListCreateDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (AllowAny, )  # to be updated

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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny, )  # to be updated Andrey

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related('category').\
        prefetch_related('genre')
    safe_serializer_class = ReadTitleSerializer
    unsafe_serializer_class = WriteTitleSerializer

    permission_classes = (AllowAny, )  # to be updated
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadTitleSerializer
        return WriteTitleSerializer
