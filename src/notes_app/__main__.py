
import json
import os
from contextlib import asynccontextmanager

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from notes_app.database import Note, NoteRepo, User, UserRepo, current_session
from notes_app.schemas import NotePydantic, UserPydantic, NoteCreateSchema

AUTH_JWT_SECRET_KEY = os.getenv("AUTH_JWT_SECRET_KEY")
AUTH_JWT_ALGORITHM = os.getenv("AUTH_JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092')
    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()

app = FastAPI(lifespan=lifespan)


async def get_session():
    async with current_session() as session:
        yield session


class TxManager:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


async def get_tx_manager(session: Annotated[AsyncSession, Depends(get_session)]) -> TxManager:
    return TxManager(session)


async def get_note_repo(session: Annotated[AsyncSession, Depends(get_session)]):
    note_repo = NoteRepo(session=session)
    return note_repo


async def get_user_repo(session: Annotated[AsyncSession, Depends(get_session)]):
    user_repo = UserRepo(session=session)
    return user_repo

async def get_kafka_producer():
    return app.state.kafka_producer



def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(form_data_password: str, hashed_password: str) -> bool:
    return password_context.verify(form_data_password, hashed_password)


def create_access_token(user_data: dict, expires_delta: timedelta):
    copied_user_data = user_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    copied_user_data.update({"exp": expire})
    encoded_jwt = jwt.encode(
        copied_user_data, AUTH_JWT_SECRET_KEY, algorithm=AUTH_JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
) -> User:
    try:
        payload = jwt.decode(
            token, AUTH_JWT_SECRET_KEY, algorithms=[AUTH_JWT_ALGORITHM]
        )
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401)
    except InvalidTokenError:
        raise HTTPException(status_code=401)
    user_id = int(sub)
    user = await user_repo.get_user_by_user_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=401)
    return user


@app.post("/users")
async def create_user(
    user_data: UserPydantic,
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
    tx_manager: Annotated[TxManager, Depends(get_tx_manager)],
):
    username_check = await user_repo.get_user_by_username(username=user_data.username)
    if username_check:
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    await user_repo.add_user(user)
    await tx_manager.commit()


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated[UserRepo, Depends(get_user_repo)],
):
    user = await user_repo.get_user_by_username(username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Username not found")
    elif not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user_data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/notes")
async def add_note(
    data: NoteCreateSchema,
    note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
    current_user: Annotated[User, Depends(get_current_user)],
    tx_manager: Annotated[TxManager, Depends(get_tx_manager)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    note = Note(head=data.head, body=data.body, user_id=current_user.id)
    await note_repo.add_note(note)
    await tx_manager.commit()
    message = json.dumps({"id": note.id, "head": note.head, "body": note.body,
                          "user_id": note.user_id}).encode("utf-8")
    await producer.send_and_wait("TestTopic", message)

@app.delete("/notes/{note_id}")
async def delete_note(
    note_id: int,
    note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
    current_user: Annotated[User, Depends(get_current_user)],
    tx_manager: Annotated[TxManager, Depends(get_tx_manager)],
) -> None:
    note = await note_repo.get_note(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403)
    await note_repo.delete_note(note_id=note_id)
    await tx_manager.commit()


@app.get("/notes/{note_id}")
async def read_note(
    note_id: int,
    note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NotePydantic:
    note = await note_repo.get_note(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403)
    pydantic_note = NotePydantic(
        id=note.id, head=note.head, body=note.body, user_id=note.user_id
    )
    return pydantic_note


@app.get("/notes")
async def get_list_notes(
    note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[NotePydantic]:
    notes = await note_repo.get_notes(user_id=current_user.id)
    pydantic_notes = [
        NotePydantic(id=n.id, head=n.head, body=n.body, user_id=n.user_id)
        for n in notes
    ]
    return pydantic_notes


def main():
    uvicorn.run("notes_app.__main__:app", reload=True)


if __name__ == "__main__":
    main()
