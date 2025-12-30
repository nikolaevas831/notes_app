from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router
from notes_app.infrastructure.auth.jwt_token_service import JwtTokenService
from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.database.main import build_async_engine, build_async_session_factory


def main():
    config = load_config()
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        producer = AIOKafkaProducer(bootstrap_servers=config.notifier.bootstrap_servers)
        db_engine = build_async_engine(db_config=config.db)
        db_session_factory = build_async_session_factory(engine=db_engine)
        jwt_token_service = JwtTokenService(auth_config=config.auth)
        await producer.start()
        app.state.kafka_producer = producer
        app.state.db_engine = db_engine
        app.state.db_session_factory = db_session_factory
        app.state.jwt_service = jwt_token_service
        try:
            yield
        finally:
            await producer.stop()

    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router)
    app.include_router(note_router)
    uvicorn.run(
        app=app,
        host=config.api.host,
        port=config.api.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
