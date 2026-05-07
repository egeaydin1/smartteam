from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base, TaskPriority, TaskStatus, TimestampMixin

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.project import Project
    from app.models.user import User


class Task(Base, TimestampMixin):
    """A unit of work inside a project, assignable to a team member."""

    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(200), nullable=False)
    status: TaskStatus = Column(
        Enum(TaskStatus, name="taskstatus"),
        nullable=False,
        default=TaskStatus.TO_DO,
    )
    priority: TaskPriority = Column(
        Enum(TaskPriority, name="taskpriority"),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    deadline: date | None = Column(Date, nullable=True)
    project_id: int = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assigned_to: int | None = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    project: Project = relationship("Project", back_populates="tasks")
    assignee: User | None = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assigned_to]
    )
    comments: list[Comment] = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )

    # ------------------------------------------------------------------
    # Domain helpers
    # ------------------------------------------------------------------

    def is_overdue(self) -> bool:
        if self.deadline is None or self.status == TaskStatus.DONE:
            return False
        return date.today() > self.deadline

    def advance_status(self) -> TaskStatus:
        """Move the task to the next logical status and return it."""
        transitions = {
            TaskStatus.TO_DO: TaskStatus.IN_PROGRESS,
            TaskStatus.IN_PROGRESS: TaskStatus.DONE,
            TaskStatus.DONE: TaskStatus.DONE,
        }
        self.status = transitions[self.status]
        return self.status

    def __repr__(self) -> str:
        return (
            f"<Task id={self.id} title={self.title!r} "
            f"status={self.status} priority={self.priority}>"
        )
