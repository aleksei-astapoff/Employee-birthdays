from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emploe_birthdays.settings')

app = Celery('emploe_birthdays')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_birthday_email': {
        'task': 'users.tasks.send_birthday_email',
        # 'schedule': crontab(minute=0, hour=21),
        'schedule': crontab(minute='*/1'),
    }
}
