import uvicorn

from src.app import app
from src.config import config

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
