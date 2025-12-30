from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from notes_app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    head: Mapped[str] = mapped_column(String)
    body: Mapped[str | None] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="notes")
