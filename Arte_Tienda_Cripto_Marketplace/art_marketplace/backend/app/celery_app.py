from celery import Celery
from app.core.config import settings

app = Celery('art_marketplace', broker=settings.REDIS_URL)
app.conf.beat_schedule = {
    'monitor-blockchain-every-15-seconds': {
        'task': 'app.tasks.blockchain_monitor.monitor_events',
        'schedule': 15.0,
    },
}
app.autodiscover_tasks(['app.tasks'])
