from celery import Celery
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_sharing.settings")

app = Celery('web_app')
app.config_from_object('config.celery', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
