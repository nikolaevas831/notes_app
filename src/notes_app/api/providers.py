from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from notes_app.infrastructure.auth.jwt_token_service import JwtTokenService
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherService
from notes_app.infrastructure.database.main import async_current_session
from notes_app.infrastructure.database.models.user import User
from notes_app.infrastructure.database.repositories.note import NoteRepo
from notes_app.infrastructure.database.repositories.user import UserRepo
from notes_app.infrastructure.database.tx_manager import TxManager
from notes_app.infrastructure.kafka.config import kafka_settings
from notes_app.infrastructure.kafka.notifier import Notifier

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_token_service() -> JwtTokenService:
    return JwtTokenService()


async def get_hasher_service() -> PasslibHasherService:
    return PasslibHasherService()


async def get_db_session():
    async with async_current_session() as session:
        yield session


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserRepo:
    user_repo = UserRepo(session=session)
    return user_repo


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
    token_service: Annotated[JwtTokenService, Depends(get_token_service)],
) -> User:
    try:
        user_id = token_service.decode_token(token)
    except Exception as err:
        raise HTTPException(status_code=401, detail="Invalid credentials") from err
    user = await user_repo.get_user_by_user_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def get_tx_manager(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TxManager:
    return TxManager(session)


async def get_note_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> NoteRepo:
    note_repo = NoteRepo(session=session)
    return note_repo


async def get_kafka_producer(request: Request):
    return request.app.state.kafka_producer


def get_note_created_notifier(
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> Notifier:
    return Notifier(producer=producer, topic=kafka_settings.note_created_topic)


def get_note_deleted_notifier(
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> Notifier:
    return Notifier(producer=producer, topic=kafka_settings.note_deleted_topic)
