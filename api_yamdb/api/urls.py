from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]
