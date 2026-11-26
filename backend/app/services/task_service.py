from app.repositories.task_repository import TaskRepository
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskUpdate
from sqlalchemy.orm import Session
from app.core.enums import TaskStatus
from fastapi import HTTPException

class TaskService:
    def __init__(self,db : Session) -> None:
        self.task_repo=TaskRepository(db)
        self.cat_repo=TaskRepository(db)

    def list_tasks(
            self,
            task_id:int|None = None,
            task_status:TaskStatus|None = None,
            category_id:int|None = None
    ) -> list[Task]:
        if task_id:
            return self.task_repo.get_by_id(task_id)
        else:
            return self.task_repo.get_all(task_status,category_id)

    def create_task(self,task_data:TaskCreate)-> Task:
        if not self.cat_repo.get_by_id(task_data.category_id):
            raise HTTPException(status_code=404,detail="Categoría inválida")
        else:
            return self.task_repo.create_task(task_data)