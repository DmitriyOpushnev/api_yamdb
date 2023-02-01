from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from django.db.models import Avg

from reviews.models import Category, Genre, Review, Title
from api.serializers import (CategorySerializer, GenreSerializer,
                             CommentSerializers)
from django.shortcuts import get_object_or_404


class ListCreateDelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # to be updated
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
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
