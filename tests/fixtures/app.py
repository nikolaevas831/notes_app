from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from notes_app.api.main import build_api_app
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl


@pytest.fixture
def app(
    async_session_factory: async_sessionmaker,
    passlib_hasher: PasslibHasherImpl,
    jwt_token: JwtTokenImpl,
    notifier_mock: AsyncMock,
) -> FastAPI:
    app = build_api_app(lifespan=None)
    app.state.db_session_factory = async_session_factory
    app.state.passlib_hasher = passlib_hasher
    app.state.jwt_token = jwt_token
    app.state.notifier = notifier_mock
    return app
