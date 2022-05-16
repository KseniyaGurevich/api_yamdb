from django.db import models
from .validators import validate_year

from users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )


class Genre(models.Model):
    """Модель жанры, многое к многому"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель категории одно к многим """
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    """Модель Произведение, базовая модель"""

    name = models.TextField()
    year = models.IntegerField(
        'Год релиза',
        validators=[validate_year],
        help_text='Введите год релиза'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name
  