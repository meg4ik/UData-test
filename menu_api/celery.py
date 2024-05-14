import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_api.settings")
app = Celery("menu_api", broker_connection_retry_on_startup=True)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse-mcdonalds-menu': {
        'task': 'api.tasks.parse_mcdonalds_menu',
        'schedule': crontab(hour=0, minute=0),
    },
}