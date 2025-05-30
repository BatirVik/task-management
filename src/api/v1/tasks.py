from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Param

from src.background_task_process import add_task_to_process
from src.dependencies import TaskRepoDepends
from src.schemes import Status, TaskCreate, TaskDetails, TaskUpdate

router = APIRouter(tags=["tasks"])

TaskNotFound = HTTPException(404, "Task not found")


@router.post("/tasks", status_code=201)
async def create_new_task(task_repo: TaskRepoDepends, task_create: TaskCreate) -> dict:
    task_id = await task_repo.add(task_create)
    return {"id": task_id}


@router.get("/tasks/{task_id}")
async def get_task_details(task_repo: TaskRepoDepends, task_id: int) -> TaskDetails:
    task = await task_repo.get(task_id)
    if task is None:
        raise TaskNotFound
    return task


@router.get("/tasks")
async def get_tasks(
    task_repo: TaskRepoDepends,
    page: int = 1,
    per_page: Annotated[int, Param(le=100)] = 10,
    title: str | None = None,
    status: Status | None = None,
) -> dict[str, list[TaskDetails]]:
    tasks = await task_repo.get_all(
        page=page, per_page=per_page, status=status, title=title
    )
    return {"tasks": tasks}


@router.patch("/tasks/{task_id}", status_code=204)
async def update_task_details(
    task_repo: TaskRepoDepends, task_id: int, task_update: TaskUpdate
) -> None:
    is_found = await task_repo.update(task_id, task_update)
    if not is_found:
        raise TaskNotFound


@router.delete("/tasks/{task_id}", status_code=204)
async def remove_task(task_repo: TaskRepoDepends, task_id: int) -> None:
    is_found = await task_repo.remove(task_id)
    if not is_found:
        raise TaskNotFound


@router.post("/tasks/{task_id}/process", status_code=202)
async def start_background_task_processing(
    task_repo: TaskRepoDepends,
    task_id: int,
) -> None:
    task = await task_repo.get(task_id)
    if task is None:
        raise TaskNotFound
    add_task_to_process(task)
