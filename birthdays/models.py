from django.db import models
from django.core.exceptions import ValidationError

from users.models import User
from emploe_birthdays.constant import MAX_LENGTH_CHAR_FIELD


class Birthdays(models.Model):
    """Модель именинников."""

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='birthdays',
        verbose_name='Сотрудник',
    )

    birthday = models.DateField(
        'Дата рождения',
        blank=False,
        null=False
    )

    department = models.CharField(
        'Отдел',
        max_length=MAX_LENGTH_CHAR_FIELD,
        blank=True
    )

    class Meta:
        verbose_name = 'Именинник'
        verbose_name_plural = 'Именинники'
        ordering = ('-birthday',)

    def __str__(self):
        return self.employee.username

    def clean(self):

        if not self.employee.date_of_birth:
            raise ValidationError(
                'У сотрудника должна быть указана дата рождения.'
                )

        if not hasattr(self.employee, 'department'):
            raise ValidationError('У сотрудника должен быть указан отдел.')

    def save(self, *args, **kwargs):

        self.clean()
        self.birthday = self.employee.date_of_birth
        self.department = self.employee.department

        super().save(*args, **kwargs)
