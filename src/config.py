import sys
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

TEST = "pytest" in sys.modules
ENV_FILENAME = ".env.test" if TEST else ".env"
ENV_PATH = Path(__file__).parent.parent / ENV_FILENAME


class Config(BaseSettings):
    DB_URL: PostgresDsn
    HOST: str = "localhost"
    PORT: int = 8000


config = Config(_env_file=ENV_PATH)  # type: ignore
