import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_ray.settings')

app = Celery('test_ray')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-posts-about-bitcoin': {
        'task': 'posts.tasks.get_news',
        'schedule': crontab(minute='0', hour='0'),
        'args': ('bitcoin', )
    },
}
