import os
from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from notes_app.api.routers.auth import router as auth_router
from notes_app.api.routers.note import router as note_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOKafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(note_router)


def main():
    uvicorn.run(
        "notes_app.__main__:app",
        host=os.getenv("UVICORN_FASTAPI_HOST"),
        port=int(os.getenv("UVICORN_FASTAPI_PORT")),
        reload=True,
    )


if __name__ == "__main__":
    main()
