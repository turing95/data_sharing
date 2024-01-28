import config
broker_url = config.CELERY_BROKER_URL
result_backend = config.CELERY_BACKEND_URL
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'UTC'
include = ['web_app.tasks']
task_always_eager = False # set to True to wait for tasks as they were synchronous. For debugging
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'