from django.core.mail import send_mail
from django.utils import timezone
from celery import shared_task

from users.models import User


@shared_task
def send_birthday_email():
    today = timezone.now().date() + timezone.timedelta(days=1)
    user_date_of_birth = User.objects.filter(
        date_of_birth__day=today.day,
    )
    for user in user_date_of_birth:
        subscibers = User.objects.filter(
            follower__birthday_person=user
        ).order_by('follower__birthday_person')

        for sub in subscibers:
            department_info = (
                f' из отдела {user.department}' if user.department else ''
                )
            message = (
                f'У сотрудника {user.first_name} {user.last_name} '
                f'{department_info} завтра день рождения, '
                f'не забудь поздравить!'
            )
            send_mail(
               subject='Не забудь поздравить коллегу с днем рождения!',
               message=message,
               from_email='your-email@example.com',
               recipient_list=[sub.email],
               fail_silently=True
            )
