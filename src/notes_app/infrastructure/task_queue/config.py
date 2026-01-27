from dataclasses import dataclass

from celery.schedules import crontab


@dataclass(frozen=True)
class TaskQueueConfig:
    # redis connection
    host: str
    port: int
    password: str
    scheme: str = "redis"
    index_db: str = "0"

    # Celery app parameters
    timezone: str = "UTC"

    @property
    def broker_url(self) -> str:
        return f"{self.scheme}://:{self.password}@{self.host}:{self.port}/{self.index_db}"

    @property
    def backend_url(self) -> str:
        return f"{self.scheme}://:{self.password}@{self.host}:{self.port}/{self.index_db}"

    @property
    def path_to_tasks(self) -> str:
        return "notes_app.infrastructure.task_queue"

    # task schedule
    schedule_delete_task: str = "0_0_*_*_*"

    @property
    def crontab_schedule_delete_task(self) -> crontab:
        parts = self.schedule_delete_task.split("_")
        return crontab(*parts)
