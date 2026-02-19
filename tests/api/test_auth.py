import httpx
import pytest
from fastapi import status

from notes_app.api.models.user import UserSchema

pytestmark = pytest.mark.api

@pytest.mark.asyncio
async def test_register_user(client: httpx.AsyncClient, user_schema: UserSchema) -> None:
    response = await client.post(url="/auth/register", json=user_schema.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_schema.username


@pytest.mark.asyncio
async def test_login(client: httpx.AsyncClient, registered_user_schema: UserSchema) -> None:
    response = await client.post(url="/auth/token", data=registered_user_schema.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"  # noqa: S105
