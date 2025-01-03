from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_EXTENDED = True
CELERY_worker_state_db = True
CELERY_result_persistent = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Africa/Johannesburg'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # Optional, for timeout adjustments
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACKS_LATE = True  # Ensures tasks are acknowledged after execution
CELERY_RETRY_POLICY = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.5,
}

