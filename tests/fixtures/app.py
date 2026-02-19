from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from notes_app.api.main import build_api_app
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.notifier.producer import NotifierImpl


@pytest.fixture
async def app(
    async_session_factory: async_sessionmaker,
    passlib_hasher: PasslibHasherImpl,
    jwt_token: JwtTokenImpl,
    notifier: NotifierImpl,
    notifier_topics: None,
) -> AsyncGenerator[FastAPI]:
    app = build_api_app(lifespan=None)
    app.state.db_session_factory = async_session_factory
    app.state.passlib_hasher = passlib_hasher
    app.state.jwt_token = jwt_token
    app.state.notifier = notifier
    await app.state.notifier.start()
    yield app
    await app.state.notifier.stop()
