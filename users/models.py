from django.db import models
from django.contrib.auth.models import AbstractUser

from emploe_birthdays.constant import (MAX_LENGTH_EMAIL_FIELD, USERNAME,
                                       MAX_LENGTH_CHAR_FIELD)


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = USERNAME
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LENGTH_EMAIL_FIELD,
        unique=True
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH_CHAR_FIELD,
        unique=True
    )

    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_CHAR_FIELD
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_CHAR_FIELD
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
    