from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.v1 import tasks

app = FastAPI(
    title="TaskManagment",
    description="Manage tasks with background processing capabilities",
)


app.include_router(tasks.router, prefix="/v1")


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
