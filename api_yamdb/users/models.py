from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import DateField

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    is_staff= models.BooleanField(null=True)
    is_active = models.BooleanField(null=True)
    date_joined = models.DateTimeField(null=True)
    password = models.TextField(null=True)
    is_superuser = models.BooleanField(null=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(default='user', max_length=30, choices=CHOICES)
    email = models.EmailField(max_length=254, unique=True, blank=False)
