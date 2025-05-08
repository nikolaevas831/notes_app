import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import (
    sessionmaker, declarative_base, Mapped, mapped_column, Session
)

load_dotenv()
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
    return db.query(Note).filter(Note.id == note_id).first()


def get_notes(db: Session):
    return db.query(Note).all()


def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
