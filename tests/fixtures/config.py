import pytest

from notes_app.api.config import APIConfig
from notes_app.infrastructure.auth.config import AuthConfig
from notes_app.infrastructure.config import Config, load_config
from notes_app.infrastructure.database.config import DBConfig
from notes_app.infrastructure.logging.config import LoggingConfig
from notes_app.infrastructure.notifier.config import KafkaTopicItem, KafkaTopicNames, NotifierConfig
from notes_app.infrastructure.task_queue.config import TaskQueueConfig


@pytest.fixture(scope="session")
def config_for_integration_test(kafka_host: str, kafka_port: int) -> Config:
    kafka_topics = {
        "note.created": KafkaTopicItem(name="note.created", num_partitions=1, replication_factor=1),
        "note.deleted": KafkaTopicItem(name="note.deleted", num_partitions=1, replication_factor=1),
    }
    return Config(
        api=APIConfig(host="127.0.0.1", port=8000),
        auth=AuthConfig(
            secret_token="test_secret",  # noqa:  S106
            algorithm="HS256",
            access_token_expire_minutes=30,
        ),
        db=DBConfig(
            database_name=":memory:",
            host="",
            port=0,
            user="",
            password="",
            async_driver="sqlite+aiosqlite",
            sync_driver="sqlite",
        ),
        task_queue=TaskQueueConfig(host="localhost", port=6379, password=""),
        notifier=NotifierConfig(
            host=kafka_host,
            port=kafka_port,
            kafka_topics=kafka_topics,
            kafka_topics_names=KafkaTopicNames(topics=kafka_topics),
        ),
        logging=LoggingConfig(level="DEBUG"),
    )


@pytest.fixture(scope="session")
def config_for_api_test() -> Config:
    return load_config()
