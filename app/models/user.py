from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, UserRole

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.project import Project
    from app.models.task import Task


class User(Base, TimestampMixin):
    """Represents an authenticated team member.

    Encapsulates identity, credential verification, and role-based access
    checks so callers never need to touch raw hashes or role strings.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, nullable=False, index=True)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    _password_hash: str = Column("password_hash", String(255), nullable=False)
    role: UserRole = Column(
        Enum(UserRole, name="userrole"),
        nullable=False,
        default=UserRole.MEMBER,
    )
    is_active: bool = Column(Boolean, default=True, nullable=False)

    # Relationships
    owned_projects: list[Project] = relationship(
        "Project", back_populates="owner", cascade="all, delete-orphan"
    )
    assigned_tasks: list[Task] = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assigned_to"
    )
    comments: list[Comment] = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )

    # ------------------------------------------------------------------
    # Encapsulated credential management
    # ------------------------------------------------------------------

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, hashed: str) -> None:
        self._password_hash = hashed

    # ------------------------------------------------------------------
    # Role-based access helpers (polymorphic behaviour via role enum)
    # ------------------------------------------------------------------

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def can_manage_project(self, project: "Project") -> bool:
        """Return True when the user may edit or delete the given project."""
        return self.is_admin() or project.owner_id == self.id

    def can_manage_task(self, task: "Task") -> bool:
        """Return True when the user may update or delete the given task."""
        return self.is_admin() or task.assigned_to == self.id

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role}>"
