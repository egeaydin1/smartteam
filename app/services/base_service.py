"""Abstract generic service that concrete services inherit and specialise."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseService(ABC, Generic[ModelT]):
    """Provides common async CRUD primitives.

    Subclasses override *_query hooks to inject eager-loading or extra
    filtering without duplicating the session-management boilerplate.
    (Polymorphism via method overriding.)
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    @property
    @abstractmethod
    def _model(self) -> type[ModelT]:
        ...

    # ------------------------------------------------------------------
    # Polymorphic hooks – override in subclasses when needed
    # ------------------------------------------------------------------

    def _base_select(self) -> Any:
        return select(self._model)

    # ------------------------------------------------------------------
    # Common CRUD
    # ------------------------------------------------------------------

    async def get_by_id(self, record_id: int) -> ModelT | None:
        result = await self._db.execute(
            self._base_select().where(self._model.id == record_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        result = await self._db.execute(self._base_select().offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj: ModelT) -> ModelT:
        self._db.add(obj)
        await self._db.commit()
        await self._db.refresh(obj)
        return obj

    async def update(self, obj: ModelT, data: dict) -> ModelT:
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        await self._db.commit()
        await self._db.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self._db.delete(obj)
        await self._db.commit()
