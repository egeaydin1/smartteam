from datetime import datetime

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentRead(CommentBase):
    id: int
    user_id: int
    task_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
