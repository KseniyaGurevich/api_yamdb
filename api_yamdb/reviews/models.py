from django.db import models
from .validators import validate_year


class Review(models.Model):
    pass


class Comments(models.Model):
    pass


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
