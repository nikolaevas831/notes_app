import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router
from notes_app.infrastructure.auth.jwt_token_service import JwtTokenService
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherService
from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.database.main import build_async_engine, build_async_session_factory
from notes_app.infrastructure.logging.main import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    config = load_config()
    setup_logging(config.logging)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=config.notifier.bootstrap_servers
        )
        app.state.db_engine = build_async_engine(db_config=config.db)
        app.state.db_session_factory = build_async_session_factory(engine=app.state.db_engine)
        app.state.passlib_hasher_service = PasslibHasherService()
        app.state.jwt_service = JwtTokenService(auth_config=config.auth)
        await app.state.kafka_producer.start()
        try:
            yield
        finally:
            await app.state.kafka_producer.stop()
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
