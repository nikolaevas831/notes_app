import json
from typing import Final

from aiokafka import AIOKafkaProducer

from notes_app.application.dto.note import NoteDTO
from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.infrastructure.notifier.config import NotifierConfig


class NotifierImpl(NotifierInterface):
    TOPIC_NOTE_CREATED: Final[str] = "note.created"
    TOPIC_NOTE_DELETED: Final[str] = "note.deleted"

    def __init__(self, notifier_config: NotifierConfig) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=notifier_config.bootstrap_servers,
            request_timeout_ms=30000,
            retry_backoff_ms=1000,
            connections_max_idle_ms=600000,
        )
        self._config = notifier_config

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()

    async def notify_note_created(self, note: NoteDTO) -> None:
        await self._producer.send_and_wait(self.TOPIC_NOTE_CREATED, self._serialize_note(note))

    async def notify_note_deleted(self, note: NoteDTO) -> None:
        await self._producer.send_and_wait(self.TOPIC_NOTE_DELETED, self._serialize_note(note))

    def _serialize_note(self, note: NoteDTO) -> bytes:
        data = {
            "id": note.id,
            "head": note.head,
            "body": note.body,
            "user_id": note.user_id,
        }
        return json.dumps(data).encode("utf-8")
