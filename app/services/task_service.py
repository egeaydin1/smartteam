from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.base_service import BaseService


class TaskService(BaseService[Task]):
    """Encapsulates task CRUD with project scoping."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    @property
    def _model(self) -> type[Task]:
        return Task

    # Polymorphic override: eager-load comments
    def _base_select(self):
        return select(Task).options(selectinload(Task.comments))

    async def get_by_project(self, project_id: int) -> list[Task]:
        result = await self._db.execute(
            self._base_select().where(Task.project_id == project_id)
        )
        return list(result.scalars().all())

    async def create_task(self, data: TaskCreate, project_id: int) -> Task:
        task = Task(
            title=data.title,
            status=data.status,
            priority=data.priority,
            deadline=data.deadline,
            assigned_to=data.assigned_to,
            project_id=project_id,
        )
        return await self.create(task)

    async def update_task(
        self, task: Task, data: TaskUpdate, requester: User
    ) -> Task:
        if not requester.can_manage_task(task):
            raise PermissionError("You do not have permission to edit this task.")
        return await self.update(task, data.model_dump(exclude_none=True))

    async def delete_task(self, task: Task, requester: User) -> None:
        if not requester.can_manage_task(task):
            raise PermissionError("You do not have permission to delete this task.")
        await self.delete(task)

    async def advance_task_status(self, task: Task, requester: User) -> Task:
        if not requester.can_manage_task(task):
            raise PermissionError("You do not have permission to advance this task.")
        task.advance_status()
        await self._db.commit()
        await self._db.refresh(task)
        return task
