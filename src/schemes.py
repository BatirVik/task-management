from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Status(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    title: str = Field(max_length=250)
    description: str
    priority: int
    status: Status


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=250)
    description: str | None = None
    priority: int | None = None
    status: Status | None = None


class TaskDetails(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
