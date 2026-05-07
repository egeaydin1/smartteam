from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class Comment(Base, TimestampMixin):
    """A textual note attached to a task by a team member."""

    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(Text, nullable=False)
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    task_id: int = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    author: User = relationship("User", back_populates="comments")
    task: Task = relationship("Task", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment id={self.id} task_id={self.task_id} user_id={self.user_id}>"
