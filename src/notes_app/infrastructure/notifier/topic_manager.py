from types import TracebackType
from typing import Self

from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from notes_app.infrastructure.notifier.config import NotifierConfig


class NotifierTopicManager:
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
        await self._admin_client.create_topics(
            [
                NewTopic(
                    name=self._config.note_created_topic_name,
                    num_partitions=self._config.note_created_topic_num_partitions,
                    replication_factor=self._config.note_created_topic_replication_factor,
                ),
                NewTopic(
                    name=self._config.note_deleted_topic_name,
                    num_partitions=self._config.note_deleted_topic_num_partitions,
                    replication_factor=self._config.note_deleted_topic_replication_factor,
                ),
            ]
        )
