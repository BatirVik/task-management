from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import config

engine = create_async_engine(str(config.DB_URL))
get_db = async_sessionmaker(engine)

CreatedAt = Annotated[datetime, mapped_column(default=func.now())]
UpdatedAt = Annotated[datetime, mapped_column(default=func.now(), onupdate=func.now())]


class BaseDB(DeclarativeBase):
    pass


class TaskDB(BaseDB):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str]
    status: Mapped[str] = mapped_column(String(15))
    priority: Mapped[int]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    logs: Mapped[list["TaskLogDB"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )


class TaskLogDB(BaseDB):
    __tablename__ = "task_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    status: Mapped[str] = mapped_column(String(15))
    created_at: Mapped[CreatedAt]

    task: Mapped["TaskDB"] = relationship(back_populates="logs")
