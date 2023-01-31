from django.db import models
from django.contrib.auth.models import AbstractUser

from api_yamdb.settings import USER_ROLES


class User(AbstractUser):
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
