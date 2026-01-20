from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.config import Config


@pytest.fixture
def app(config: Config, async_session_factory: async_sessionmaker) -> FastAPI:
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(note_router)
    passlib_hasher = PasslibHasherImpl()
    jwt_token_service = JwtTokenImpl(auth_config=config.auth)
    notifier = MagicMock()
    app.state.db_session_factory = async_session_factory
    app.state.passlib_hasher = passlib_hasher
    app.state.jwt_token = jwt_token_service
    app.state.notifier = notifier
    return app


# app.state.notifier = NotifierImpl(notifier_config=config.notifier)  # noqa: ERA001
