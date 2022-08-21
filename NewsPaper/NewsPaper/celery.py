import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_newsmail_every_monday_8am': {
        'task': 'news.tasks.weekly_mails',
        'schedule': crontab(hour=0, minute=20, day_of_week='monday'),
    },

#     'send_newsmail_every_2min': {
#         'task': 'news.tasks.weekly_mails',
#         'schedule': crontab(minute='*/2'),
#     },
}
