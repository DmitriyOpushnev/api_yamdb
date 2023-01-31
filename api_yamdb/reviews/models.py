from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('US', 'user'),
    ('MOD', 'moderator'),
    ('ADM', 'admin'),
)


class User(AbstractUser):
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
