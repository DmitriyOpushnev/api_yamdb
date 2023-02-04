from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator,)


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

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        default_related_name = 'titles'



class Comment(models.Model):
    text = models.TextField(verbose_name='text')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='review',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        verbose_name='pub_date'
    )


class Review(models.Model):
    text = models.TextField(verbose_name='text')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='title',
        related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='author'
    )
    score = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='score'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    def __str__(self):
        return self.text

