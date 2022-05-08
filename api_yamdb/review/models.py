from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    autor = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг'
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        pass


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    autor = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        pass
