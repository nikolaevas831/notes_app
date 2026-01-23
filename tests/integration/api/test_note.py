import pytest
from fastapi import status
from httpx import AsyncClient

from tests.fixtures.note import NoteCreateDict
from tests.fixtures.user import LoggedInUserSchemaDict


@pytest.mark.asyncio
async def test_create_note(
    client: AsyncClient, note_create_schema: NoteCreateDict, logged_user: LoggedInUserSchemaDict
) -> None:
    headers = {"Authorization": f"Bearer {logged_user['access_token']}"}

    response = await client.post(url="/notes/", json=note_create_schema, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["user_id"], int)
    assert response.json()["head"] == note_create_schema["head"]
    assert response.json()["body"] == note_create_schema["body"]
