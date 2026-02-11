from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient

from notes_app.infrastructure.notifier.config import NotifierConfig


def create_kafka_admin_client(notifier_config: NotifierConfig) -> AIOKafkaAdminClient:
    return AIOKafkaAdminClient(bootstrap_servers=notifier_config.bootstrap_servers)


def create_kafka_producer(notifier_config: NotifierConfig) -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=notifier_config.bootstrap_servers,
        request_timeout_ms=notifier_config.request_timeout_ms,
        retry_backoff_ms=notifier_config.retry_backoff_ms,
        connections_max_idle_ms=notifier_config.connections_max_idle_ms,
    )
