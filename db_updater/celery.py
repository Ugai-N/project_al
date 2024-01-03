from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

app = Celery('db_updater', include=['db_updater.tasks'])
# app.config_from_object('db_updater.celeryconfig')
app.config_from_object('core.settings')

app.conf.beat_schedule = {
    'update_db_every_hr': {
        'task': 'db_updater.tasks.testing_celery',
        'schedule': timedelta(hours=1)
        # 'schedule': crontab(minute=0)
        # 'schedule': crontab()
    },
}
