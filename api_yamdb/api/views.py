from rest_framework import viewsets, mixins, filters
from reviews.models import Category
from api.serializers import CategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination


class ListCreateDelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDelViewSet):
    '''Viewset for Category: create, list, del - available for admin only '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, )  # to be updated
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
