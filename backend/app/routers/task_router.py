from fastapi import APIRouter,Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskResponse,TaskCreate
from app.core.enums import TaskStatus
from app.services.task_service import TaskService

router=APIRouter(prefix="/tasks",tags=["Tareas"])
DbSession = Annotated[Session, Depends(get_db)]

@router.get(
        "",
        response_model=list[TaskResponse],
        status_code=200,
        summary="Listar tareas",
        description="Devuelve todas las tareas disponibles en la base de datos"
        )
def get_tasks(db: DbSession,task_status:TaskStatus|None = None,category_id:int|None = None):
    service=TaskService(db)
    return service.list_tasks(task_status=task_status,category_id=category_id)

@router.post(
        "",
        response_model=TaskCreate,
        status_code=201,
        summary="Añadir tarea",
        description="Añade una tarea nueva a la base de datos, basada en los parámetros dados."
        )
def post_task(db: DbSession,task_data: TaskCreate):
    service=TaskService(db)
    return service.create_task(task_data)