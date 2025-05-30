
from fastapi.testclient import TestClient

from src.repositories import TaskRepository
from src.schemes import Status, TaskCreate

MOCK_TASKS_CREATE = [
    TaskCreate(title="super_cat", description="...", priority=1, status=Status.PENDING),
    TaskCreate(title="happy_cat", description="...", priority=2, status=Status.PENDING),
    TaskCreate(
        title="happy_test", description="...", priority=2, status=Status.IN_PROGRESS
    ),
    TaskCreate(
        title="evil_cat", description="...", priority=3, status=Status.COMPLETED
    ),
]


async def test_create_new_task(client: TestClient, task_repo: TaskRepository):
    resp = client.post("v1/tasks", json=MOCK_TASKS_CREATE[0].model_dump())

    assert resp.status_code == 201
    data = resp.json()
    assert data.keys() == {"id"}

    assert await task_repo.get(data["id"])


async def test_get_task(client: TestClient, task_repo: TaskRepository):
    task_id = await task_repo.add(MOCK_TASKS_CREATE[0])

    resp = client.get(f"v1/tasks/{task_id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data.keys() == {
        "id",
        "title",
        "description",
        "priority",
        "status",
        "updated_at",
        "created_at",
    }

    task = await task_repo.get(task_id)
    assert task


async def test_get_task__not_found(client: TestClient, task_repo: TaskRepository):
    resp = client.get("v1/tasks/111")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Task not found"}


async def test_get_all_tasks__no_params(client: TestClient, task_repo: TaskRepository):
    tasks_ids = await task_repo.add_many(MOCK_TASKS_CREATE)

    resp = client.get("v1/tasks")

    assert resp.status_code == 200
    data = resp.json()
    assert data.keys() == {"tasks"}

    for task in data["tasks"]:
        assert task.keys() == {
            "id",
            "title",
            "description",
            "priority",
            "status",
            "updated_at",
            "created_at",
        }
        assert task["id"] in tasks_ids

    assert {t["id"] for t in data["tasks"]} == set(tasks_ids)


async def test_get_all_tasks__filter_by_title(
    client: TestClient, task_repo: TaskRepository
):
    await task_repo.add_many(MOCK_TASKS_CREATE)

    resp = client.get("v1/tasks", params={"title": "evil_cat"})

    assert resp.status_code == 200
    data = resp.json()
    assert data.keys() == {"tasks"}
    assert len(data["tasks"]) == 1


async def test_get_all_tasks__filter_by_status(
    client: TestClient, task_repo: TaskRepository
):
    await task_repo.add_many(MOCK_TASKS_CREATE)

    resp = client.get("v1/tasks", params={"status": "pending"})

    assert resp.status_code == 200
    data = resp.json()
    assert data.keys() == {"tasks"}
    assert len(data["tasks"]) == 2


async def test_get_all_tasks__pagination(client: TestClient, task_repo: TaskRepository):
    await task_repo.add_many(MOCK_TASKS_CREATE)

    resp = client.get("v1/tasks", params={"page": 2, "per_page": 2})
    assert resp.status_code == 200

    data = resp.json()
    assert data.keys() == {"tasks"}
    assert {t["title"] for t in data["tasks"]} == {"happy_test", "evil_cat"}


async def test_update_task(client: TestClient, task_repo: TaskRepository):
    task_id = await task_repo.add(MOCK_TASKS_CREATE[0])

    resp = client.patch(f"v1/tasks/{task_id}", json={"description": "Balatro"})
    assert resp.status_code == 204

    task = await task_repo.get(task_id)
    assert task
    assert task.description == "Balatro"
    assert task.created_at != task.updated_at


async def test_update_task__not_found(client: TestClient):
    resp = client.patch("v1/tasks/1111", json={"description": "Balatro"})
    assert resp.status_code == 404


async def test_remove_task(client: TestClient, task_repo: TaskRepository):
    task_id = await task_repo.add(MOCK_TASKS_CREATE[0])

    resp = client.delete(f"v1/tasks/{task_id}")

    assert resp.status_code == 204

    task = await task_repo.get(task_id)
    assert task is None


async def test_remove_task__not_found(client: TestClient, task_repo: TaskRepository):
    resp = client.delete("v1/tasks/1111")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Task not found"}


async def test_start_task_processing(client: TestClient, task_repo: TaskRepository):
    task_id = await task_repo.add(MOCK_TASKS_CREATE[0])

    resp = client.post(f"v1/tasks/{task_id}/process")

    assert resp.status_code == 202  # ACCEPTED


async def test_start_task_processing__not_found(client: TestClient):
    resp = client.post("v1/tasks/1111/process")
    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Task not found"}, resp.json()
