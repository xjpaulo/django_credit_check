import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_credit_check.settings')

app = Celery('django_credit_check')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
