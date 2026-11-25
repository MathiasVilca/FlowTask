from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="category")
