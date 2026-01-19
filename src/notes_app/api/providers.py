from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from notes_app.application.dto.user import UserDTO
from notes_app.application.mappers.user import UserMapper
from notes_app.infrastructure.auth.jwt_token import JwtTokenImpl
from notes_app.infrastructure.auth.passlib_hasher import PasslibHasherImpl
from notes_app.infrastructure.database.repositories.note import NoteRepo
from notes_app.infrastructure.database.repositories.user import UserRepo
from notes_app.infrastructure.database.tx_manager import TxManagerImlp
from notes_app.infrastructure.notifier.main import NotifierImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_token(request: Request) -> JwtTokenImpl:
    return request.app.state.jwt_token


async def get_hasher(request: Request) -> PasslibHasherImpl:
    return request.app.state.passlib_hasher


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async_session_factory = request.app.state.db_session_factory
    async with async_session_factory() as session:
        yield session


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserRepo:
    return UserRepo(session=session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
    token_service: Annotated[JwtTokenImpl, Depends(get_token)],
) -> UserDTO:
    try:
        user_id = token_service.decode_token(token)
    except Exception as err:
        raise HTTPException(status_code=401, detail="Invalid credentials") from err
    user = await user_repo.get_user_by_user_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return UserMapper.map_user_entity_to_dto(user_entity=user)


async def get_tx_manager(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TxManagerImlp:
    return TxManagerImlp(session)


async def get_note_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> NoteRepo:
    return NoteRepo(session=session)


async def get_notifier(
    request: Request,
) -> NotifierImpl:
    return request.app.state.notifier
