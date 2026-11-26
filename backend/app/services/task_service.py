from app.repositories.task_repository import TaskRepository
from app.repositories.category_repository import CategoryRepository
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskUpdate
from sqlalchemy.orm import Session
from app.core.enums import TaskStatus
from fastapi import HTTPException

class TaskService:
    def __init__(self,db : Session) -> None:
        self.task_repo=TaskRepository(db)
        self.cat_repo=CategoryRepository(db)

    def list_tasks(
            self,
            task_status:TaskStatus|None = None,
            category_id:int|None = None
    ) -> list[Task]:
        return self.task_repo.get_all(task_status,category_id)

    def get_task(
                self,
                task_id:int|None = None,
    ) -> Task:
        task=self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404,detail="Tarea no encontrada")
        else:
            return task

    def create_task(self,task_data:TaskCreate)-> Task:
        pass