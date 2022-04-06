from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabrique_test.settings')

app = Celery('fabrique_test')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
