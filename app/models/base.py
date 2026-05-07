import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class TimestampMixin:
    """Mixin that adds created_at / updated_at columns to any model."""

    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class TaskStatus(str, enum.Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
