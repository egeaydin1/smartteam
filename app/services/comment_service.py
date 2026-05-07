from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.base_service import BaseService


class CommentService(BaseService[Comment]):
    """Encapsulates comment CRUD scoped to tasks."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    @property
    def _model(self) -> type[Comment]:
        return Comment

    async def get_by_task(self, task_id: int) -> list[Comment]:
        result = await self._db.execute(
            select(Comment).where(Comment.task_id == task_id)
        )
        return list(result.scalars().all())

    async def create_comment(
        self, data: CommentCreate, task_id: int, author: User
    ) -> Comment:
        comment = Comment(
            content=data.content,
            task_id=task_id,
            user_id=author.id,
        )
        return await self.create(comment)

    async def update_comment(
        self, comment: Comment, data: CommentUpdate, requester: User
    ) -> Comment:
        if not requester.is_admin() and comment.user_id != requester.id:
            raise PermissionError("You can only edit your own comments.")
        return await self.update(comment, data.model_dump(exclude_none=True))

    async def delete_comment(self, comment: Comment, requester: User) -> None:
        if not requester.is_admin() and comment.user_id != requester.id:
            raise PermissionError("You can only delete your own comments.")
        await self.delete(comment)
