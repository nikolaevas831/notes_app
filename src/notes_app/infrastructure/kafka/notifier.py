import json

from aiokafka import AIOKafkaProducer

from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.infrastructure.database.models.note import Note


class Notifier(NotifierInterface):
    def __init__(self, producer: AIOKafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    async def notify_note_created(self, note: Note) -> None:
        message = json.dumps(
            {
                "id": note.id,
                "head": note.head,
                "body": note.body,
                "user_id": note.user_id,
            }
        ).encode("utf-8")
        await self.producer.send_and_wait(self.topic, message)

    async def notify_note_deleted(self, note: Note) -> None:
        message = json.dumps(
            {
                "id": note.id,
                "head": note.head,
                "body": note.body,
                "user_id": note.user_id,
            }
        ).encode("utf-8")
        await self.producer.send_and_wait(self.topic, message)
