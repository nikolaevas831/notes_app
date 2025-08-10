from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from notes_app.infrastructure.database.main import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
