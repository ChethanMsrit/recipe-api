from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Update this with your Redis server details
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Same as broker URL
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_TASK_ALWAYS_EAGER = True
