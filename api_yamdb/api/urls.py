from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router.urls)),
]
