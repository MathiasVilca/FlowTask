from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.task import Task
from app.core.enums import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, task_status: TaskStatus | None = None, category_id: int | None = None
    ) -> list[Task]:
        stmt = select(Task).options(joinedload(Task.category)).order_by(Task.id.asc())
        if task_status:
            stmt = stmt.where(Task.status == task_status)
        if category_id:
            stmt = stmt.where(Task.category_id == category_id)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, task_id: int) -> Task | None:
        stmt = select(Task).options(joinedload(Task.category)).where(Task.id == task_id)
        return self.db.scalar(stmt)

    def create_task(self, task_data: TaskCreate) -> Task:
        payload = task_data.model_dump()
        payload["status"] = task_data.status.value
        db_task = Task(**payload)

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return self.get_by_id(db_task.id)

    def update_task(self, db_task: Task, task_data: TaskUpdate) -> Task:
        update_fields = task_data.model_dump(exclude_unset=True)

        if "status" in update_fields and update_fields["status"] is not None:
            update_fields["status"] = task_data.status.value

        for field, value in update_fields.items():
            setattr(db_task, field, value)

        self.db.commit()
        self.db.refresh(db_task)

        return self.get_by_id(db_task.id)

    def delete_task(self, db_task: Task) -> None:
        self.db.delete(db_task)
        self.db.commit()
