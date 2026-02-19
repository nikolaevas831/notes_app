from types import TracebackType
from typing import Self

from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from notes_app.infrastructure.notifier.config import NotifierConfig


class NotifierTopicBuilder:
    def __init__(self, notifier_config: NotifierConfig, admin_client: AIOKafkaAdminClient) -> None:
        self._config = notifier_config
        self._admin_client = admin_client

    async def __aenter__(self) -> Self:
        await self._admin_client.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._admin_client:
            await self._admin_client.close()

    async def create_all_topics(self) -> None:
        new_topics = [
            NewTopic(
                name=item.name,
                num_partitions=item.num_partitions,
                replication_factor=item.replication_factor,
            )
            for item in self._config.kafka_topics.values()
        ]
        await self._admin_client.create_topics(new_topics)
