from os import environ

from celery import Celery
from django.conf import settings

environ.setdefault("DJANGO_SETTINGS_MODULE", "readable.settings.development")

application = Celery("readable")
application.config_from_object(settings, namespace="CRONTAB")
application.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
