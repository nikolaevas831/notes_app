import sys

from celery import Celery
from celery.schedules import crontab
from dishka.integrations.celery import DishkaTask, setup_dishka

from notes_app.infrastructure.config import Config, load_config
from notes_app.infrastructure.task_queue.config import TaskQueueConfig
from notes_app.infrastructure.task_queue.providers import setup_di_container


def create_celery_app(task_queue_config: TaskQueueConfig) -> Celery:
    app = Celery(
        broker=task_queue_config.broker_url,
        backend=task_queue_config.backend_url,
        timezone=task_queue_config.timezone,
    )
    app.autodiscover_tasks(task_queue_config.path_to_tasks)
    return app


def build_celery_app(task_queue_config: TaskQueueConfig, beat_schedule: dict) -> Celery:
    app = create_celery_app(task_queue_config=task_queue_config)
    app.conf.beat_schedule = beat_schedule
    return app


def get_beat_schedule(schedule_delete_task: crontab) -> dict:
    return {
        "delete-notes-task": {
            "task": "delete_notes",
            "schedule": schedule_delete_task,
        },
    }


def setup_di_for_celery_app(app: Celery, config: Config) -> None:
    container = setup_di_container(context={Config: config})
    app.conf.update(task_cls=DishkaTask)
    setup_dishka(container=container, app=app)


def run_command(log_level: str, celery_app: Celery, command: str) -> None:
    match command:
        case "worker":
            celery_app.Worker(loglevel=log_level).start()
        case "beat":
            celery_app.Beat(loglevel=log_level).run()


def main() -> None:
    config = load_config()
    beat_schedule = get_beat_schedule(
        schedule_delete_task=config.task_queue.crontab_schedule_delete_task
    )
    celery_app = build_celery_app(
        task_queue_config=config.task_queue,
        beat_schedule=beat_schedule,
    )
    setup_di_for_celery_app(app=celery_app, config=config)
    command = sys.argv[1]
    run_command(log_level=config.logging.level, celery_app=celery_app, command=command)
