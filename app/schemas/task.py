from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.base import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    status: TaskStatus = TaskStatus.TO_DO
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: date | None = None
    assigned_to: int | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: date | None = None
    assigned_to: int | None = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
