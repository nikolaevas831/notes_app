import asyncio
from collections.abc import Generator

import pytest
from testcontainers.kafka import KafkaContainer

from notes_app.infrastructure.config import Config
from notes_app.infrastructure.notifier.init_topics import init_notifier_topics


@pytest.fixture(scope="session")
def kafka() -> Generator[KafkaContainer]:
    with KafkaContainer(image="confluentinc/cp-kafka:7.6.0") as kafka:
        kafka.env.update({      "KAFKA_BROKER_ID": "1",
        "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
        "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "PLAINTEXT:PLAINTEXT",
        "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://kafka:9092",
        "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1",
        "KAFKA_AUTO_CREATE_TOPICS_ENABLE": "false"})
        yield kafka

@pytest.fixture(scope="session")
def kafka_bootstrap_server(kafka: KafkaContainer) -> str:
    return kafka.get_bootstrap_server()

@pytest.fixture(scope="session")
def kafka_host(kafka_bootstrap_server: str) -> str:
    return kafka_bootstrap_server.split(":")[0]

@pytest.fixture(scope="session")
def kafka_port(kafka_bootstrap_server: str) -> int:
    return int(kafka_bootstrap_server.split(":")[1])

@pytest.fixture(scope="session")
def notifier_topics(config: Config) -> None:
    asyncio.run(init_notifier_topics(config = config))