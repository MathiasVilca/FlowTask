from enum import StrEnum


class TaskStatus(StrEnum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En Progreso"
    COMPLETE = "Completada"
