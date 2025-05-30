from typing import Iterable

from sqlalchemy import sql
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import TaskDB
from src.schemes import Status, TaskCreate, TaskDetails, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add(self, task_create: TaskCreate, /) -> int:
        """Returns task id."""
        task_db = TaskDB(**task_create.model_dump())
        self.db.add(task_db)
        await self.db.flush()
        task_id = task_db.id
        await self.db.commit()
        return task_id

    async def add_many(self, tasks_create: Iterable[TaskCreate], /) -> list[int]:
        """Returns tasks ids."""
        tasks_db = [TaskDB(**task.model_dump()) for task in tasks_create]
        self.db.add_all(tasks_db)
        await self.db.flush()
        ids = [task.id for task in tasks_db]
        await self.db.commit()
        return ids

    async def get(self, task_id: int) -> TaskDetails | None:
        task_db = await self.db.get(TaskDB, task_id)
        if task_db:
            return TaskDetails.model_validate(task_db, from_attributes=True)

    async def get_all(
        self,
        *,
        title: str | None = None,
        status: Status | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> list[TaskDetails]:
        st = sql.select(TaskDB).offset(per_page * (page - 1)).limit(per_page)
        if title is not None:
            st = st.where(TaskDB.title.like(title))
        if status is not None:
            st = st.where(TaskDB.status == status)

        tasks_db = await self.db.scalars(st)
        return [
            TaskDetails.model_validate(task, from_attributes=True) for task in tasks_db
        ]

    async def update(self, task_id: int, task_update: TaskUpdate) -> bool:
        """Returns a boolean value indicating whether the task was found and updated or not."""
        st = (
            sql.update(TaskDB)
            .where(TaskDB.id == task_id)
            .values(task_update.model_dump(exclude_none=True))
        )
        res = await self.db.execute(st)
        await self.db.commit()
        return res.rowcount == 1

    async def remove(self, task_id: int) -> bool:
        """Returns a boolean value indicating whether the task was found and deleted or not."""
        st = sql.delete(TaskDB).where(TaskDB.id == task_id)
        res = await self.db.execute(st)
        await self.db.commit()
        return res.rowcount == 1
