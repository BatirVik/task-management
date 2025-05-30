import asyncio
import random
from weakref import WeakSet

from loguru import logger

from src.schemes import TaskDetails

background_tasks_like: WeakSet[asyncio.Task] = WeakSet()


def add_task_to_process(task: TaskDetails) -> None:
    t = asyncio.create_task(process_task(task))
    background_tasks_like.add(t)


async def process_task(task: TaskDetails) -> None:
    await asyncio.sleep(random.randint(1, 10))
    logger.success("Task(id={id}) processed", id=task.id)
