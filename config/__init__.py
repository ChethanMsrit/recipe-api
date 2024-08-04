from config.settings.base import *
from config.settings.development import *
from celery import app as celery_app


__all__ = ['celery_app']
