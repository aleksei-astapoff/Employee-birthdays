import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

class Command(BaseCommand):
    """Команда для создания Суперпользователя."""

    help = 'Создание суперпользователя'

    def handle(self, *args, **kwargs):

        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')
        first_name = os.getenv('SUPERUSER_FIRST_NAME')
        last_name = os.getenv('SUPERUSER_LAST_NAME')
        date_of_birth = os.getenv('SUPERUSER_DATE_OF_BIRTH')
        department = os.getenv('SUPERUSER_DEPARTMENT')

        if User.objects.filter(email=email).exists():
            self.stderr.write(self.style.ERROR(
                'Суперпользователь уже существует'
            ))
            return

        try:
            user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                department=department
            )
            self.stdout.write(self.style.SUCCESS(
                f'Суперпользователь успешно создан: {user.email}'
            ))
        except IntegrityError:
            self.stderr.write(self.style.ERROR(
                'Возникла ошибка при создании Суперпользователя'
            ))
