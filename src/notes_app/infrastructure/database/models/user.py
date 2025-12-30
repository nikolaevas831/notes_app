from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from notes_app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from .note import Note

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
