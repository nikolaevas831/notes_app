from typing import TypedDict

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient


class UserSchemaDict(TypedDict):
    username: str
    password: str


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
