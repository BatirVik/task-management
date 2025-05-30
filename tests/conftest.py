import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from loguru import logger

from src.app import app
from src.db import BaseDB, engine, get_db
from src.repositories import TaskRepository

TEST_LOGS_DIR = Path(__file__).parent / "logs"

logger.remove()


@pytest.fixture(scope="function", autouse=True)
def logs_to_files(request, clean_log_files):
    log_file_path: Path = TEST_LOGS_DIR / (str(request.node.name) + ".log")
    id = logger.add(log_file_path)
    yield
    logger.remove(id)


@pytest.fixture(scope="session", autouse=True)
def clean_log_files(request):
    TEST_LOGS_DIR.mkdir(exist_ok=True)
    shutil.rmtree(TEST_LOGS_DIR)
    TEST_LOGS_DIR.mkdir(exist_ok=True)


@pytest.fixture
async def db():
    async with get_db() as session:
        yield session


@pytest.fixture(autouse=True)
async def db_life():
    async with engine.connect() as conn:
        await conn.run_sync(BaseDB.metadata.create_all)
        await conn.commit()
        yield
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.commit()


@pytest.fixture
async def task_repo(db):
    return TaskRepository(db)


@pytest.fixture
async def client():
    return TestClient(app)
