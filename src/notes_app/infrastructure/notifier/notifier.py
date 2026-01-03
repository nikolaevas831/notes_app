import json

from aiokafka import AIOKafkaProducer

from notes_app.application.dto.note import NoteDTO
from notes_app.application.interfaces.notifier import NotifierInterface


class Notifier(NotifierInterface):
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def notify_note_created(self, note: NoteDTO) -> None:
        self.topic = "note.created"
        message = json.dumps(
            {
                "id": note.id,
                "head": note.head,
                "body": note.body,
                "user_id": note.user_id,
            }
        ).encode("utf-8")
        await self.producer.send_and_wait(self.topic, message)

    async def notify_note_deleted(self, note: NoteDTO) -> None:
        self.topic = "note.deleted"
        message = json.dumps(
            {
                "id": note.id,
                "head": note.head,
                "body": note.body,
                "user_id": note.user_id,
            }
        ).encode("utf-8")
        await self.producer.send_and_wait(self.topic, message)
