import pytest
from faker import Faker

from notes_app.application.dto.user import CreateUserDTO, LoggedInUserDTO, UserDTO
from notes_app.application.usecases.auth import login
from notes_app.application.usecases.user import create_user
from tests.mocks.hasher import HasherMock
from tests.mocks.token_service import TokenServiceMock
from tests.mocks.tx_manager import TxManagerMock
from tests.mocks.user_repo import UserRepoMock


@pytest.mark.asyncio
async def test_create_user(
    faker: Faker, user_repo: UserRepoMock, tx_manager: TxManagerMock, hasher: HasherMock
) -> None:
    user_data = CreateUserDTO(username=faker.name(), password=faker.password())

    result = await create_user(
        user_data=user_data, user_repo=user_repo, tx_manager=tx_manager, hasher=hasher
    )

    assert isinstance(result, UserDTO)
    assert isinstance(result.id, int)
    assert result.id > 0
    assert result.username == user_data.username
    saved_user = await user_repo.get_user_by_user_id(result.id)
    assert saved_user is not None
    assert saved_user.username == user_data.username
    user_by_username = await user_repo.get_user_by_username(user_data.username)
    assert user_by_username is not None
    assert user_by_username.id == result.id


@pytest.mark.asyncio
async def test_login_user(
    faker: Faker,
    user_repo: UserRepoMock,
    tx_manager: TxManagerMock,
    hasher: HasherMock,
    token_service: TokenServiceMock,
) -> None:
    username = faker.name()
    password = faker.password()
    user_data = CreateUserDTO(username=username, password=password)
    created_user = await create_user(
        user_data=user_data, user_repo=user_repo, tx_manager=tx_manager, hasher=hasher
    )

    result = await login(
        username=username,
        password=password,
        user_repo=user_repo,
        hasher=hasher,
        token_service=token_service,
    )

    assert isinstance(result, LoggedInUserDTO)
    assert hasattr(result, "access_token")
    assert isinstance(result.access_token, str)
    assert len(result.access_token) > 0
    assert hasattr(result, "token_type")
    assert isinstance(result.token_type, str)
    decoded_user_id = token_service.decode_token(result.access_token)
    assert decoded_user_id == created_user.id
