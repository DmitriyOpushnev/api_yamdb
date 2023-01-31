from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=settings.USER_ROLES,
        default='user'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
