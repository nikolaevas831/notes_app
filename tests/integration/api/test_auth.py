import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from tests.fixtures.user import UserSchemaDict


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_schema: UserSchemaDict) -> None:
    response = await client.post(url="/auth/register", json=user_schema)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_schema["username"]


@pytest.mark.asyncio
async def test_register_user_duplicate_username(
    client: AsyncClient, user_schema: UserSchemaDict
) -> None:
    response = await client.post(url="/auth/register", json=user_schema)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_schema["username"]

    response = await client.post(url="/auth/register", json=user_schema)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Conflict" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login(client: AsyncClient, registered_user_schema: UserSchemaDict) -> None:
    response = await client.post(url="/auth/token", data=registered_user_schema)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token_type"] == "bearer"  # noqa: S105


@pytest.mark.asyncio
async def test_login_unregistered_user(client: AsyncClient, user_schema: UserSchemaDict) -> None:
    response = await client.post(url="/auth/token", data=user_schema)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Username not found"


@pytest.mark.asyncio
async def test_login_incorrect_password(
    client: AsyncClient, registered_user_schema: UserSchemaDict, faker: Faker
) -> None:
    user_schema_incorrect_password = UserSchemaDict(
        username=registered_user_schema["username"], password=faker.password()
    )

    response = await client.post(url="/auth/token", data=user_schema_incorrect_password)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect password"
