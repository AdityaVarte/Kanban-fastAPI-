# app/models/column.py
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[int] = mapped_column(default=0)

    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"))
    board: Mapped["Board"] = relationship(back_populates="columns")

    cards: Mapped[list["Card"]] = relationship(
        back_populates="column", cascade="all, delete-orphan"
    )