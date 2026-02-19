from dataclasses import dataclass
from functools import cached_property

from pydantic import BaseModel


class KafkaTopicItem(BaseModel):
    name: str
    num_partitions: int
    replication_factor: int


class KafkaTopicNames:
    def __init__(self, topics: dict[str, KafkaTopicItem]) -> None:
        self._topics = topics

    @cached_property
    def note_created(self) -> str:
        return self._topics["note.created"].name

    @cached_property
    def note_deleted(self) -> str:
        return self._topics["note.deleted"].name


@dataclass(frozen=True)
class NotifierConfig:
    host: str
    port: int
    kafka_topics: dict[str, KafkaTopicItem]
    kafka_topics_names: KafkaTopicNames

    @cached_property
    def bootstrap_servers(self) -> str:
        return f"{self.host}:{self.port}"

    # producer_settings
    request_timeout_ms: int = 30000
    retry_backoff_ms: int = 1000
    connections_max_idle_ms: int = 600000
