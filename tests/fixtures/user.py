import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from notes_app.api.models.user import LoggedInUserResponseSchema, UserSchema
from notes_app.application.dto.user import CreateUserDTO, LoggedInUserDTO, UserDTO
from notes_app.application.mappers.user import UserMapper
from notes_app.application.usecases.auth import login
from notes_app.application.usecases.user import create_user
from tests.mocks.hasher import HasherMock
from tests.mocks.token_service import TokenServiceMock
from tests.mocks.tx_manager import TxManagerMock
from tests.mocks.user_repo import UserRepoMock


@pytest.fixture
def user_schema(faker: Faker) -> UserSchema:
    return UserSchema(username=faker.name(), password=faker.password())


@pytest.fixture
async def registered_user_schema(client: AsyncClient, user_schema: UserSchema) -> UserSchema:
    response = await client.post(url="/auth/register", json=user_schema.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    return user_schema


@pytest.fixture
async def logged_user_schema(
    client: AsyncClient, registered_user_schema: UserSchema
) -> LoggedInUserResponseSchema:
    response = await client.post(url="auth/token", data=registered_user_schema.model_dump())
    assert response.status_code == status.HTTP_200_OK
    return LoggedInUserResponseSchema(
        access_token=response.json()["access_token"], token_type=response.json()["token_type"]
    )


@pytest.fixture
async def create_user_dto(faker: Faker) -> CreateUserDTO:
    return CreateUserDTO(username=faker.name(), password=faker.password())


@pytest.fixture
async def logged_user_dto(
    user_repo_mock: UserRepoMock,
    hasher_mock: HasherMock,
    token_service_mock: TokenServiceMock,
    registered_user_dto_and_password: tuple[UserDTO, str],
) -> LoggedInUserDTO:
    return await login(
        username=registered_user_dto_and_password[0].username,
        password=registered_user_dto_and_password[1],
        user_repo=user_repo_mock,
        hasher=hasher_mock,
        token_service=token_service_mock,
    )


@pytest.fixture
async def current_user_dto(
    logged_user_dto: LoggedInUserDTO,
    user_repo_mock: UserRepoMock,
    token_service_mock: TokenServiceMock,
) -> UserDTO:
    token = logged_user_dto.access_token
    user_id = token_service_mock.decode_token(token)
    user_entity = await user_repo_mock.get_user_by_user_id(user_id=user_id)
    if user_entity is None:
        msg = "User not found"
        raise ValueError(msg)
    return UserMapper.map_user_entity_to_dto(user_entity=user_entity)


@pytest.fixture
async def registered_user_dto_and_password(
    create_user_dto: CreateUserDTO,
    user_repo_mock: UserRepoMock,
    tx_manager_mock: TxManagerMock,
    hasher_mock: HasherMock,
) -> tuple[UserDTO, str]:
    user_data = CreateUserDTO(username=create_user_dto.username, password=create_user_dto.password)
    created_user_dto = await create_user(
        user_data=user_data,
        user_repo=user_repo_mock,
        tx_manager=tx_manager_mock,
        hasher=hasher_mock,
    )
    return created_user_dto, create_user_dto.password
