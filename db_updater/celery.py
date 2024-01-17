from datetime import timedelta

from celery import Celery

app = Celery('db_updater', include=['db_updater.tasks'])
app.config_from_object('core.settings')

app.conf.beat_schedule = {
    'update_db_every_hr': {
        'task': 'db_updater.tasks.update_db',
        'schedule': timedelta(hours=1)
        # 'schedule': crontab(minute=0)
    },
}
