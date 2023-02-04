from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from api.serializers import (CategorySerializer, GenreSerializer,
                             ReadTitleSerializer, WriteTitleSerializer)


class ListCreateDelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # to be updated
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class CategoryViewSet(ListCreateDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


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
