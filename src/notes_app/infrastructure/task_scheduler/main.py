from celery import Celery
from celery.schedules import crontab

from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.database.main import build_sync_engine, build_sync_session_factory
from notes_app.infrastructure.task_scheduler.config import TaskSchedulerConfig


class TaskSchedulerService:
    def __init__(self, task_schedule_config: TaskSchedulerConfig):
        self.config = task_schedule_config
        self.celery_app = Celery(
            broker=self.config.broker_url,
            backend=self.config.backend_url,
            timezone=self.config.timezone,
        )
        self._configure_celery()

    def autodiscover_tasks(self):
        self.celery_app.autodiscover_tasks(["notes_app.infrastructure.task_scheduler"])

    def beat_schedule(self):
        self.celery_app.conf.beat_schedule = {
            "delete-notes-task": {
                "task": "notes_app.infrastructure.task_scheduler.tasks.delete_notes_task",
                "schedule": crontab(),
            },
        }

    def _configure_celery(self):
        self.autodiscover_tasks()
        self.beat_schedule()

    def get_celery_app(self):
        return self.celery_app


def init_celery_service():
    config = load_config()
    task_scheduler_service = TaskSchedulerService(task_schedule_config=config.task_scheduler)
    celery_app = task_scheduler_service.get_celery_app()
    return celery_app

config = load_config()
db_engine = build_sync_engine(db_config=config.db)
db_session_factory = build_sync_session_factory(engine=db_engine)
celery_app = init_celery_service()
