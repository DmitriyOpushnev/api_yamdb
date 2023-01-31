from rest_framework import viewsets, mixins
from reviews.models import Category
from api.serializers import CategorySerializer
from rest_framework.permissions import AllowAny


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
