import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_django.settings')

celery_app = Celery('add_numbers')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.beat_schedule = {
    'add_numbers.tasks.adding_task': {
        'task': 'add_numbers.tasks.adding_task',
        'schedule': 60.0,
        'args': (16, 16)
    }
}
