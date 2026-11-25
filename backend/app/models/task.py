from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from app.core.database import Base
from app.core.enums import TaskStatus

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category import Category

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[TaskStatus] = mapped_column(
        String(50), default=TaskStatus.PENDING.value, index=True
    )
    due_date: Mapped[date | None] = mapped_column(Date)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), index=True
    )

    category: Mapped["Category"] = relationship("Category", back_populates="tasks")
