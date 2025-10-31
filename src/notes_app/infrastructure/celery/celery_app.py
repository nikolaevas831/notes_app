from celery import Celery
from notes_app.infrastructure.celery.config import redis_url


celery_app = Celery(
    broker=redis_url,
    backend=redis_url,
    timezone="UTC"
)

celery_app.autodiscover_tasks(["notes_app.infrastructure.celery"])

celery_app.conf.beat_schedule = {
    "delete-notes-task": {
        "task": "notes_app.infrastructure.celery.tasks.delete_notes_task",
        "schedule": 60.0,
    },
}

