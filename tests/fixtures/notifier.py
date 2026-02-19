from collections.abc import AsyncGenerator

import pytest
from aiokafka import AIOKafkaConsumer

from notes_app.infrastructure.config import Config
from notes_app.infrastructure.notifier.main import create_kafka_producer
from notes_app.infrastructure.notifier.producer import NotifierImpl


@pytest.fixture
async def notifier(config: Config) -> NotifierImpl:
    producer = create_kafka_producer(config.notifier)
    return NotifierImpl(producer=producer, notifier_config=config.notifier)


@pytest.fixture
async def consumer(config: Config) -> AsyncGenerator[AIOKafkaConsumer]:
    consumer = AIOKafkaConsumer(bootstrap_servers=f"{config.notifier.host}:{config.notifier.port}")
    await consumer.start()
    yield consumer
    await consumer.stop()
