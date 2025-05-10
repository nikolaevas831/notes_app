import os

from sqlalchemy import create_engine, Integer, String, select
from sqlalchemy.orm import (
    sessionmaker, declarative_base, Mapped, mapped_column, Session
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

current_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    head: Mapped[str] = mapped_column(String)
    body: Mapped[str | None] = mapped_column(String)


def create_note(db: Session, head: str, body: str):
    new_note = Note(head=head, body=body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


def get_note(db: Session, note_id: int):
    return db.scalars(select(Note).filter_by(id=note_id).limit(1)).first()


def get_notes(db: Session):
    return db.scalars(select(Note)).all()


def delete_note(db: Session, note_id: int):
    note = db.scalars(select(Note).filter_by(id=note_id).limit(1)).first()
    if note:
        db.delete(note)
        db.commit()
