from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from kombu import Exchange, Queue


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('recipe-api')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.task_queues = (
    Queue('high', Exchange('high priority'), routing_key='high', queue_arguments={'x-max-priority': 10}),
    Queue('medium', Exchange('medium priority'), routing_key='medium', queue_arguments={'x-max-priority': 2}),
    Queue('low', Exchange('low priority'), routing_key='low', queue_arguments={'x-max-priority': 1}),
    Queue('urgent', Exchange('urgent'), routing_key='urgent'),
    Queue('default', Exchange('default'), routing_key='default'),
)
