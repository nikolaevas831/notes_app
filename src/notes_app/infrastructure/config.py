import os
from dataclasses import dataclass

from environs import Env

from notes_app.api.config import APIConfig
from notes_app.infrastructure.auth.config import AuthConfig
from notes_app.infrastructure.database.config import DBConfig
from notes_app.infrastructure.logging.config import LoggingConfig
from notes_app.infrastructure.notifier.config import (
    KafkaTopicItem,
    KafkaTopicNames,
    NotifierConfig,
)
from notes_app.infrastructure.task_queue.config import TaskQueueConfig


@dataclass
class Config:
    auth: AuthConfig
    db: DBConfig
    task_queue: TaskQueueConfig
    notifier: NotifierConfig
    api: APIConfig
    logging: LoggingConfig


def load_config() -> Config:
    env = Env()
    kafka_topics = {
        item["name"]: KafkaTopicItem(
            name=item["name"],
            num_partitions=item["num_partitions"],
            replication_factor=item["replication_factor"],
        )
        for item in env.json("KAFKA_TOPICS")
    }

    return Config(
        auth=AuthConfig(
            secret_token=os.environ["AUTH_JWT_SECRET_KEY"],
            algorithm=os.environ["AUTH_JWT_ALGORITHM"],
            access_token_expire_minutes=int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"]),
        ),
        db=DBConfig(
            database_name=os.environ["POSTGRES_DB"],
            host=os.environ["POSTGRES_HOST"],
            port=int(os.environ["POSTGRES_PORT"]),
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        ),
        task_queue=TaskQueueConfig(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.environ["REDIS_PASSWORD"],
        ),
        notifier=NotifierConfig(
            host=os.environ["KAFKA_HOST"],
            port=int(os.environ["KAFKA_PORT"]),
            kafka_topics=kafka_topics,
            kafka_topics_names=KafkaTopicNames(topics=kafka_topics),
        ),
        api=APIConfig(
            host=os.environ["UVICORN_FASTAPI_HOST"], port=int(os.environ["UVICORN_FASTAPI_PORT"])
        ),
        logging=LoggingConfig(
            level=os.environ["LOG_LEVEL"],
        ),
    )
