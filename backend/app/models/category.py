from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(100), nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")
