import asyncio
import os

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

current_session = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    head: Mapped[str] = mapped_column(String)
    body: Mapped[str | None] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="notes")


class NoteRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_note(self, note: Note) -> None:
        self._session.add(note)

    async def get_note(self, note_id: int) -> Note| None:
        stmt = select(Note).where(Note.id == note_id)
        result = await self._session.scalars(stmt)
        note: Note = result.first()
        return note

    async def get_notes(self, user_id) -> list[Note]:
        stmt = select(Note).where(Note.user_id == user_id)
        result = await self._session.scalars(stmt)
        notes: list[Note] =  list(result)
        return notes

    async def delete_note(self, note_id: int) -> None:
        stmt = select(Note).where(Note.id == note_id).limit(1)
        result = await self._session.scalars(stmt)
        note = result.first()
        if note:
            await self._session.delete(note)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    notes: Mapped[list["Note"]] = relationship(back_populates="user")


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_user(self, user: User) -> None:
        self._session.add(user)

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.scalars(stmt)
        user = result.first()
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.scalars(stmt)
        user = result.first()
        return user
