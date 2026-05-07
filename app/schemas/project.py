from datetime import datetime

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None


class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
