import pytest

from notes_app.api.config import APIConfig
from notes_app.infrastructure.auth.config import AuthConfig
from notes_app.infrastructure.config import Config
from notes_app.infrastructure.database.config import DBConfig
from notes_app.infrastructure.logging.config import LoggingConfig
from notes_app.infrastructure.notifier.config import NotifierConfig
from notes_app.infrastructure.task_scheduler.config import TaskSchedulerConfig


@pytest.fixture(scope="session")
def config() -> Config:
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
        task_scheduler=TaskSchedulerConfig(host="localhost", port=6379, password=""),
        notifier=NotifierConfig(bootstrap_servers="localhost:9092"),
        logging=LoggingConfig(level="DEBUG"),
    )
