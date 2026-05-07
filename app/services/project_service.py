from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.base_service import BaseService


class ProjectService(BaseService[Project]):
    """Encapsulates project CRUD and ownership enforcement."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    @property
    def _model(self) -> type[Project]:
        return Project

    # Polymorphic override: eager-load tasks alongside each project
    def _base_select(self):
        return select(Project).options(selectinload(Project.tasks))

    async def get_by_owner(self, owner_id: int) -> list[Project]:
        result = await self._db.execute(
            self._base_select().where(Project.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def create_project(self, data: ProjectCreate, owner: User) -> Project:
        project = Project(
            title=data.title,
            description=data.description,
            owner_id=owner.id,
        )
        return await self.create(project)

    async def update_project(
        self, project: Project, data: ProjectUpdate, requester: User
    ) -> Project:
        if not requester.can_manage_project(project):
            raise PermissionError("You do not have permission to edit this project.")
        return await self.update(project, data.model_dump(exclude_none=True))

    async def delete_project(self, project: Project, requester: User) -> None:
        if not requester.can_manage_project(project):
            raise PermissionError("You do not have permission to delete this project.")
        await self.delete(project)
