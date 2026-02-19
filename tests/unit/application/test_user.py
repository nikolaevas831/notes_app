import pytest

from notes_app.application.dto.user import CreateUserDTO, LoggedInUserDTO, UserDTO
from notes_app.application.usecases.auth import login
from notes_app.application.usecases.user import create_user
from tests.mocks.hasher import HasherMock
from tests.mocks.token_service import TokenServiceMock
from tests.mocks.tx_manager import TxManagerMock
from tests.mocks.user_repo import UserRepoMock

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


async def test_create_user(
    create_user_dto: CreateUserDTO,
    user_repo_mock: UserRepoMock,
    tx_manager_mock: TxManagerMock,
    hasher_mock: HasherMock,
) -> None:
    result = await create_user(
        user_data=create_user_dto,
        user_repo=user_repo_mock,
        tx_manager=tx_manager_mock,
        hasher=hasher_mock,
    )

    assert isinstance(result, UserDTO)
    assert isinstance(result.id, int)
    assert result.id > 0
    assert result.username == create_user_dto.username
    saved_user = await user_repo_mock.get_user_by_user_id(result.id)
    assert saved_user is not None
    assert saved_user.username == create_user_dto.username
    user_by_username = await user_repo_mock.get_user_by_username(create_user_dto.username)
    assert user_by_username is not None
    assert user_by_username.id == result.id


async def test_login_user(
    registered_user_dto_and_password: tuple[UserDTO, str],
    user_repo_mock: UserRepoMock,
    hasher_mock: HasherMock,
    token_service_mock: TokenServiceMock,
) -> None:
    user_dto, user_password = registered_user_dto_and_password

    result = await login(
        username=user_dto.username,
        password=user_password,
        user_repo=user_repo_mock,
        hasher=hasher_mock,
        token_service=token_service_mock,
    )

    assert isinstance(result, LoggedInUserDTO)
    assert hasattr(result, "access_token")
    assert isinstance(result.access_token, str)
    assert len(result.access_token) > 0
    assert hasattr(result, "token_type")
    assert isinstance(result.token_type, str)
    decoded_user_id = token_service_mock.decode_token(result.access_token)
    assert decoded_user_id == user_dto.id
