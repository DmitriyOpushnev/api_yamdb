from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

USER_ROLES = (
    ('US', 'user'),
    ('MOD', 'moderator'),
    ('ADM', 'admin'),
)

# как ревьювер учил обЪединять что можно, чтобы упростить


class AbstractModelMasterCategory(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    email = models.EmailField('E-mail пользователя',
                              unique=True, max_length=settings.LIMIT_EMAIL)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Category(AbstractModelMasterCategory):
    class Meta(AbstractModelMasterCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = "categories"


class Genre(AbstractModelMasterCategory):
    class Meta(AbstractModelMasterCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = "genres"


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name
