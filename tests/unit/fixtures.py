import pytest
from faker import Faker

from notes_app.application.dto.user import CreateUserDTO, UserDTO
from notes_app.application.usecases.user import create_user
from tests.mocks.hasher import HasherMock
from tests.mocks.token_service import TokenServiceMock
from tests.mocks.tx_manager import TxManagerMock
from tests.mocks.user_repo import UserRepoMock


@pytest.fixture
def user_repo() -> UserRepoMock:
    return UserRepoMock()


@pytest.fixture
def tx_manager() -> TxManagerMock:
    return TxManagerMock()


@pytest.fixture
def hasher() -> HasherMock:
    return HasherMock()


@pytest.fixture
def token_service() -> TokenServiceMock:
    return TokenServiceMock()


@pytest.fixture
async def registered_user(
    faker: Faker,
    user_repo: UserRepoMock,
    tx_manager: TxManagerMock,
    hasher: HasherMock,
) -> tuple[UserDTO, str]:
    username = faker.name()
    user_password = faker.password()
    user_data = CreateUserDTO(username=username, password=user_password)
    created_user_dto = await create_user(
        user_data=user_data, user_repo=user_repo, tx_manager=tx_manager, hasher=hasher
    )
    return created_user_dto, user_password
