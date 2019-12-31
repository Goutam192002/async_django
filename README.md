## Sample periodic async task of django Application

In a web framework like Django, usually there is a main thread which listens to the HTTP connections and sends responses accordingly.
Sometimes the application might need to perform some time consuming task, eg. retrain a model, video transcoding, image transformations etc. These are supposed to be done asynchronously so that it does not affect the latency of the application.


### How to implement async tasks in Django?

Using celery we can create async tasks in Django.
In an existing django project, install celery by using the following command
```
pip install Celery
```

We need to use redis database for intermediate data storage because it is an in-memory database it is faster hence reducing latencies
A running redis server is also required and redis package has to be installed using `pip`

Next we setup celery configuration by creating a `celery.py` file in the project directory as follows:

```
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
```

This sets the environment to Django and discovers tasks present in all the django applicaitons
We have also set up a schedule for running the tasks. Which runs every minute.

To run this, open a terminal window and run the following command.
```
celery -A async_django beat -l info
```

In another terminal window, run the following command
```
celery -A async_django worker -l info
```