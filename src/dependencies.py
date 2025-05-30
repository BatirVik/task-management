from typing import Annotated

from fastapi import Depends

from src.db import get_db
from src.repositories import TaskRepository


async def _get_task_repo():
    async with get_db() as db:
        yield TaskRepository(db)


TaskRepoDepends = Annotated[TaskRepository, Depends(_get_task_repo)]
