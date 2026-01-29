import pytest

from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.config import Config


@pytest.fixture(scope="session")
def passlib_hasher() -> PasslibHasherImpl:
    return PasslibHasherImpl()


@pytest.fixture(scope="session")
def jwt_token(config: Config) -> JwtTokenImpl:
    return JwtTokenImpl(auth_config=config.auth)
