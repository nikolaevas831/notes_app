import httpx
import pytest
from fastapi import status

from notes_app.api.models.note import NoteCreateSchema
from notes_app.api.models.user import LoggedInUserResponseSchema

pytestmark = pytest.mark.api


@pytest.mark.asyncio
async def test_create_note(
    client: httpx.AsyncClient,
    note_create_schema: NoteCreateSchema,
    logged_user_schema: LoggedInUserResponseSchema,
) -> None:
    headers = {"Authorization": f"Bearer {logged_user_schema.access_token}"}

    response = await client.post(
        url="/notes/", json=note_create_schema.model_dump(), headers=headers
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["user_id"], int)
    assert response.json()["head"] == note_create_schema.head
    assert response.json()["body"] == note_create_schema.body
