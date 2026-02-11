import json

from aiokafka import AIOKafkaProducer

from notes_app.application.dto.note import NoteDTO
from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.infrastructure.notifier.config import NotifierConfig


class NotifierImpl(NotifierInterface):
    def __init__(self, notifier_config: NotifierConfig, producer: AIOKafkaProducer) -> None:
        self._config = notifier_config
        self._producer = producer

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()

    async def notify_note_created(self, note: NoteDTO) -> None:
        await self._producer.send_and_wait(
            topic=self._config.note_created_topic_name, value=self._serialize_note(note)
        )

    async def notify_note_deleted(self, note: NoteDTO) -> None:
        await self._producer.send_and_wait(
            topic=self._config.note_deleted_topic_name, value=self._serialize_note(note)
        )

    def _serialize_note(self, note: NoteDTO) -> bytes:
        data = {
            "id": note.id,
            "head": note.head,
            "body": note.body,
            "user_id": note.user_id,
        }
        return json.dumps(data).encode("utf-8")
