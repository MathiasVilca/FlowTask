from app.core.enums import TaskStatus
from app.schemas.base import AppBaseModel
from pydantic import ConfigDict,Field
from typing import Optional
from datetime import date
from app.schemas.category import CategoryResponse

class TaskBase(AppBaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Título de la tarea."
    )
    description: Optional[str] = Field(
        None,
        max_length=100,
        description="Descripción breve de la tarea (Opcional)."
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description=f"Estado de la tarea ({TaskStatus.PENDING} por defecto)."
    )
    due_date: Optional[date] = Field(
        None,
        description="Fecha de vencimiento de la tarea (Opcional)."
    )

    category_id: int = Field(
        ...,
        gt=0,
        description= "Catergoría de la tarea."
    )

class TaskCreate(TaskBase):
    pass

class TaskUpdate(AppBaseModel):
    title: Optional[str] = Field(None,min_length=1,max_length=30)
    description: Optional[str] = Field(None,max_length=100)
    status: Optional[TaskStatus] = Field(None)
    due_date: Optional[date] = Field(None)
    
    category_id: Optional[int] = Field(None,gt=0)

class TaskResponse(TaskBase):
    model_config=ConfigDict(from_attributes=True)

    id: int
    category: CategoryResponse
