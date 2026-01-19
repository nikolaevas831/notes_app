from typing import Final

from celery import Celery
from celery.schedules import crontab
from dishka.integrations.celery import DishkaTask, setup_dishka

from notes_app.infrastructure.config import Config, load_config
from notes_app.infrastructure.task_scheduler.providers import setup_di_container


def create_celery_app() -> Celery:
    config = load_config()
    celery_app = Celery(
        broker=config.task_scheduler.broker_url,
        backend=config.task_scheduler.backend_url,
        timezone=config.task_scheduler.timezone,
        task_cls=DishkaTask,
    )
    container = setup_di_container(context={Config: config})
    celery_app.autodiscover_tasks(["notes_app.infrastructure.task_scheduler"])
    celery_app.conf.beat_schedule = {
        "delete-notes-task": {
            "task": "notes_app.infrastructure.task_scheduler.tasks.delete_notes_task",
            "schedule": crontab(),
        },
    }
    setup_dishka(container=container, app=celery_app)
    return celery_app


celery_app: Final[Celery] = create_celery_app()
