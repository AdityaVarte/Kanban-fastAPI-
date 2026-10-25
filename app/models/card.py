# app/models/card.py
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(default=0)

    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"))
    column: Mapped["Column"] = relationship(back_populates="cards")