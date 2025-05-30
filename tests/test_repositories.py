from sqlalchemy import sql

from src.db import TaskDB, get_db
from src.repositories import TaskRepository
from src.schemes import Status, TaskCreate, TaskUpdate

TASK_CREATE = TaskCreate(
    title="Deadpool", description="...", priority=1, status=Status.PENDING
)
TASK_UPDATE = TaskUpdate(title="Deadpool 2", priority=2)


async def test_task_repo_add(task_repo: TaskRepository):
    task_id = await task_repo.add(TASK_CREATE)

    async with get_db() as db:
        [task] = await db.scalars(sql.select(TaskDB))
        assert task.id == task_id


async def test_task_repo_get(task_repo: TaskRepository):
    task_id = await task_repo.add(TASK_CREATE)
    task = await task_repo.get(task_id)
    assert task
    assert task.id == task_id


async def test_task_repo_get__not_found(task_repo: TaskRepository):
    task = await task_repo.get(1111)
    assert task is None


async def test_task_repo_add_many(task_repo: TaskRepository):
    tasks_ids = await task_repo.add_many([TASK_CREATE, TASK_CREATE])

    async with get_db() as db:
        tasks = await db.scalars(sql.select(TaskDB))
        tasks = list(tasks)
        assert len(tasks) == 2
        assert {task.id for task in tasks} == set(tasks_ids)


async def test_task_repo_update(task_repo: TaskRepository):
    task_id = await task_repo.add(TASK_CREATE)

    is_found = await task_repo.update(task_id, TASK_UPDATE)
    assert is_found is True

    async with get_db() as db:
        [task] = await db.scalars(sql.select(TaskDB))
        assert task.id == task_id


async def test_task_repo_update__not_found(task_repo: TaskRepository):
    is_found = await task_repo.update(111, TASK_UPDATE)
    assert is_found is False


async def test_task_repo_remove(task_repo: TaskRepository):
    task_id = await task_repo.add(TASK_CREATE)

    is_found = await task_repo.remove(task_id)
    assert is_found is True

    async with get_db() as db:
        tasks = await db.scalars(sql.select(TaskDB))
        assert list(tasks) == []


async def test_task_repo_remove__not_found(task_repo: TaskRepository):
    is_found = await task_repo.remove(1111)
    assert is_found is False
