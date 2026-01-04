import os
from dataclasses import dataclass

from notes_app.api.config import APIConfig
from notes_app.infrastructure.auth.config import AuthConfig
from notes_app.infrastructure.database.config import DBConfig
from notes_app.infrastructure.logging.config import LoggingConfig
from notes_app.infrastructure.notifier.config import NotifierConfig
from notes_app.infrastructure.task_scheduler.config import TaskSchedulerConfig


@dataclass
class Config:
    auth: AuthConfig
    db: DBConfig
    task_scheduler: TaskSchedulerConfig
    notifier: NotifierConfig
    api: APIConfig
    logging: LoggingConfig


def load_config() -> Config:
    return Config(
        auth=AuthConfig(
            secret_token=os.environ["AUTH_JWT_SECRET_KEY"],
            algorithm=os.environ["AUTH_JWT_ALGORITHM"],
            access_token_expire_minutes=int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"]),
        ),
        db=DBConfig(
            database=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        ),
        task_scheduler=TaskSchedulerConfig(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.environ["REDIS_PASSWORD"],
        ),
        notifier=NotifierConfig(bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"]),
        api=APIConfig(
            host=os.environ["UVICORN_FASTAPI_HOST"], port=int(os.environ["UVICORN_FASTAPI_PORT"])
        ),
        logging=LoggingConfig(
            level=os.environ["LOG_LEVEL"],
        ),
    )
