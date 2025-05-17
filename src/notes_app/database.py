import os

from sqlalchemy import create_engine, Integer, String, select, ForeignKey
from sqlalchemy.orm import (
    sessionmaker, Mapped, mapped_column, Session, relationship, DeclarativeBase
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

current_session = sessionmaker(autocommit=False, autoflush=False,
                               expire_on_commit=False, bind=engine)


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
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_note(self, note: Note) -> None:
        self._session.add(note)

    def get_note(self, note_id: int) -> Note:
        stmt = select(Note).where(Note.id == note_id)
        note: Note = self._session.scalars(stmt).first()
        return note

    def get_notes(self, user_id) -> list[Note]:
        stmt = select(Note).where(Note.user_id == user_id)
        notes: list[Note] = list(self._session.scalars(stmt))
        return notes

    def delete_note(self, note_id: int):
        stmt = select(Note).where(Note.id == note_id).limit(1)
        note = self._session.scalars(stmt).first()
        if note:
            self._session.delete(note)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    notes: Mapped[list["Note"]] = relationship(back_populates="user")


class UserRepo:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_user(self, user: User) -> None:
        self._session.add(user)

    def get_user_by_user_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = self._session.scalars(stmt).first()
        return user

    def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = self._session.scalars(stmt).first()
        return user
