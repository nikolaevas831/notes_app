import json

import pytest
from aiokafka import AIOKafkaConsumer
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

from notes_app.api.models.note import NoteCreateSchema
from notes_app.api.models.user import LoggedInUserResponseSchema
from notes_app.infrastructure.config import Config

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_note(  # noqa: PLR0913
    client: AsyncClient,
    note_create_schema: NoteCreateSchema,
    logged_user_schema: LoggedInUserResponseSchema,
    consumer: AIOKafkaConsumer,
    config: Config,
    db_session: AsyncSession,
) -> None:
    headers = {"Authorization": f"Bearer {logged_user_schema.access_token}"}
    consumer.subscribe(topics=[config.notifier.kafka_topics_names.note_created])

    response = await client.post(
        url="/notes/", json=note_create_schema.model_dump(), headers=headers
    )
    message = await consumer.getone()
    database_note = await db_session.execute(
        text("SELECT * FROM notes WHERE id = :id"),
        {"id": response.json()["id"]},
    )
    database_note = database_note.first()

    # Api response checks
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["user_id"], int)
    assert response.json()["head"] == note_create_schema.head
    assert response.json()["body"] == note_create_schema.body

    # Kafka message checks
    assert message.topic == config.notifier.kafka_topics_names.note_created
    message_value = json.loads(message.value) if message.value is not None else None
    assert message_value == {
        "id": response.json()["id"],
        "head": response.json()["head"],
        "body": response.json()["body"],
        "user_id": response.json()["user_id"],
    }

    # Database checks
    assert database_note is not None
    assert database_note.id == response.json()["id"]
    assert database_note.head == response.json()["head"]
    assert database_note.body == response.json()["body"]
    assert database_note.user_id == response.json()["user_id"]
