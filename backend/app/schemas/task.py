from app.core.enums import TaskStatus
from app.schemas.base import AppBaseModel
from pydantic import ConfigDict, Field
from typing import Optional
from datetime import date
from app.schemas.category import CategoryResponse


class TaskBase(AppBaseModel):
    title: str = Field(
        ..., min_length=1, max_length=150, description="Título de la tarea."
    )
    description: str|None = Field(
        None, max_length=100, description="Descripción breve de la tarea (Opcional)."
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description=f"Estado de la tarea ({TaskStatus.PENDING.value} por defecto).",
    )
    due_date: date|None = Field(
        None, description="Fecha de vencimiento de la tarea (Opcional)."
    )

    category_id: int = Field(..., gt=0, description="Categoría de la tarea.")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(AppBaseModel):
    title: str|None = Field(None, min_length=1, max_length=30)
    description: str|None = Field(None, max_length=100)
    status: TaskStatus|None = Field(None)
    due_date: date|None = Field(None)

    category_id: int|None = Field(None, gt=0)


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategoryResponse
