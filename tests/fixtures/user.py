from typing import TypedDict

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient


class UserSchemaDict(TypedDict):
    username: str
    password: str


class LoggedInUserSchemaDict(TypedDict):
    access_token: str
    token_type: str


@pytest.fixture
def user_schema(faker: Faker) -> UserSchemaDict:
    return {"username": faker.name(), "password": faker.password()}


@pytest.fixture
async def registered_user_schema(
    client: AsyncClient, user_schema: UserSchemaDict
) -> UserSchemaDict:
    response = await client.post(url="/auth/register", json=user_schema)
    assert response.status_code == status.HTTP_201_CREATED
    return user_schema


@pytest.fixture
async def logged_user(
    client: AsyncClient, registered_user_schema: UserSchemaDict
) -> LoggedInUserSchemaDict:
    response = await client.post(url="auth/token", data=registered_user_schema)
    assert response.status_code == status.HTTP_200_OK
    return LoggedInUserSchemaDict(
        access_token=response.json()["access_token"], token_type=response.json()["token_type"]
    )
