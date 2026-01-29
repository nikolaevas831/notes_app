from collections.abc import AsyncGenerator
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Protocol

import uvicorn
from fastapi import FastAPI

from notes_app.api.config import APIConfig
from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.config import Config
from notes_app.infrastructure.database.main import DBConnection
from notes_app.infrastructure.notifier.main import NotifierImpl


class LifespanProtocol(Protocol):
    def __call__(self, app: FastAPI) -> _AsyncGeneratorContextManager[None]: ...


class APIStateDependency:
    def __init__(self, config: Config) -> None:
        self.config = config

    @property
    def db_connection(self) -> DBConnection:
        return DBConnection(db_config=self.config.db)

    @property
    def notifier(self) -> NotifierImpl:
        return NotifierImpl(notifier_config=self.config.notifier)

    @property
    def passlib_hasher(self) -> PasslibHasherImpl:
        return PasslibHasherImpl()

    @property
    def jwt_token(self) -> JwtTokenImpl:
        return JwtTokenImpl(auth_config=self.config.auth)


def create_lifespan(
    api_dependency: APIStateDependency,
) -> LifespanProtocol:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.notifier = api_dependency.notifier
        app.state.db_engine = api_dependency.db_connection.async_engine
        app.state.db_session_factory = api_dependency.db_connection.async_session_factory
        app.state.passlib_hasher = api_dependency.passlib_hasher
        app.state.jwt_token = api_dependency.jwt_token
        await app.state.notifier.start()
        try:
            yield
        finally:
            await app.state.notifier.stop()
            await app.state.db_engine.dispose()

    return lifespan


def run_api(app: FastAPI, api_config: APIConfig) -> None:
    uvicorn.run(
        app=app,
        host=api_config.host,
        port=api_config.port,
        reload=api_config.reload,
        log_config=None,
    )


def build_api_app(lifespan: LifespanProtocol | None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router)
    app.include_router(note_router)
    return app
