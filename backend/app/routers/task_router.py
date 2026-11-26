from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.core.enums import TaskStatus
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tareas"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[TaskResponse],
    status_code=200,
    summary="Listar tareas",
    description=(
        "Devuelve todas las tareas disponibles en la base de datos, "
        "filtrable por status y categoría."
    ),
)
def get_tasks(
    db: DbSession,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    category_id: int | None = None,
):
    service = TaskService(db)
    return service.list_tasks(task_status=task_status, category_id=category_id)


@router.get(
    "/{id}",
    response_model=TaskResponse,
    status_code=200,
    summary="Mostrar una tarea específica",
    description="Devuelve la tarea correspondiente a la id.",
)
def get_tasks_by_id(db: DbSession, id: int):
    service = TaskService(db)
    return service.get_task_by_id(task_id=id)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
    summary="Añadir tarea",
    description=(
        "Añade una tarea nueva a la base de datos, " "basada en los parámetros dados."
    ),
)
def post_task(db: DbSession, task_data: TaskCreate):
    service = TaskService(db)
    return service.create_task(task_data)


@router.patch(
    "/{id}",
    response_model=TaskResponse,
    status_code=200,
    summary="Actualizar tarea de forma parcial",
    description=(
        "Actualiza la tarea correspondiente a la id "
        "de forma parcial (no todos los campos)"
    ),
)
@router.put(
    "/{id}",
    response_model=TaskResponse,
    status_code=200,
    summary="Actualizar tarea de forma completa",
    description=(
        "Actualiza la tarea correspondiente a la id "
        "de forma completa (todos los campos)"
    ),
)
def update_task(db: DbSession, id: int, task_data: TaskUpdate):
    service = TaskService(db)
    return service.update_task(task_id=id, task_data=task_data)


@router.delete(
    "/{id}",
    status_code=200,
    summary="Eliminar tarea",
    description=(
        "Elimina la tarea correspondiente a la id. "
        "Retorna mensaje de confirmación junto a la id"
    ),
)
def delete_task(db: DbSession, id: int):
    service = TaskService(db)
    service.delete_task(task_id=id)
    return {"message": "Tarea eliminada correctamente", "id": id}
