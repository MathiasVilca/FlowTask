from app.repositories.task_repository import TaskRepository
from app.repositories.category_repository import CategoryRepository
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from app.core.enums import TaskStatus
from fastapi import HTTPException


class TaskService:
    def __init__(self, db: Session) -> None:
        self.task_repo = TaskRepository(db)
        self.cat_repo = CategoryRepository(db)

    def list_tasks(
        self, task_status: TaskStatus | None = None, category_id: int | None = None
    ) -> list[Task]:
        return self.task_repo.get_all(task_status, category_id)

    def get_task_by_id(
        self,
        task_id: int,
    ) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        else:
            return task

    def create_task(self, task_data: TaskCreate) -> Task:
        if not self.cat_repo.get_by_id(task_data.category_id):
            raise HTTPException(status_code=404, detail="Categoría inválida")
        else:
            return self.task_repo.create_task(task_data)

    def update_task(self, task_id: int, task_data: TaskUpdate):
        db_task = self.get_task_by_id(task_id)
        if task_data.category_id is not None and not self.cat_repo.get_by_id(
            task_data.category_id
        ):
            raise HTTPException(status_code=404, detail="Categoría inválida")
        else:
            return self.task_repo.update_task(db_task=db_task, task_data=task_data)

    def delete_task(self, task_id: int):
        db_task = self.get_task_by_id(task_id)
        return self.task_repo.delete_task(db_task)
