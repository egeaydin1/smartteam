from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class Project(Base, TimestampMixin):
    """A container for tasks owned by a single admin user."""

    __tablename__ = "projects"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(200), nullable=False)
    description: str | None = Column(Text, nullable=True)
    owner_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    owner: User = relationship("User", back_populates="owned_projects")
    tasks: list[Task] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )

    # ------------------------------------------------------------------
    # Domain helpers
    # ------------------------------------------------------------------

    @property
    def open_task_count(self) -> int:
        from app.models.base import TaskStatus

        return sum(1 for t in self.tasks if t.status != TaskStatus.DONE)

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r}>"
