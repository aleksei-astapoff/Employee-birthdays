from django.contrib.auth import password_validation as validators
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractUser

from emploe_birthdays.constant import (MAX_LENGTH_EMAIL_FIELD, USERNAME,
                                       MAX_LENGTH_CHAR_FIELD)


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = USERNAME
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'date_of_birth')

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LENGTH_EMAIL_FIELD,
        unique=True,
        validators=[validate_email],
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH_CHAR_FIELD,
        unique=True
    )

    date_of_birth = models.DateField(
        'Дата рождения',
        blank=False,
        null=False
    )

    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_CHAR_FIELD
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_CHAR_FIELD
    )

    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH_CHAR_FIELD,
        validators=[validators.validate_password],
        help_text='Придумайте пароль',
    )
    department = models.CharField(
        'Отдел',
        max_length=MAX_LENGTH_CHAR_FIELD,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
    )

    birthday_person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Именинник',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'birthday_person'],
                name='unique_subscription',
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.birthday_person}'
