import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.database.main import (
    DBConnection,
)
from notes_app.infrastructure.logging.main import setup_logging
from notes_app.infrastructure.notifier.main import NotifierImpl

logger = logging.getLogger(__name__)


def main() -> None:
    config = load_config()
    setup_logging(config.logging)
    db_connection = DBConnection(db_config=config.db)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.notifier = NotifierImpl(notifier_config=config.notifier)
        app.state.db_engine = db_connection.async_engine
        app.state.db_session_factory = db_connection.async_session_factory
        app.state.passlib_hasher = PasslibHasherImpl()
        app.state.jwt_token = JwtTokenImpl(auth_config=config.auth)
        await app.state.notifier.start()
        try:
            yield
        finally:
            await app.state.notifier.stop()
            await app.state.db_engine.dispose()

    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router)
    app.include_router(note_router)
    uvicorn.run(
        app=app,
        host=config.api.host,
        port=config.api.port,
        reload=False,
        log_config=None,
    )


if __name__ == "__main__":
    main()
