import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_scheldule = {
    'action_every_monday_8am': {
        'task': 'news_portal.tasks.weekly_send_email_task',
        'scheldule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ()
    }
}
app.conf.timezone = 'UTC'