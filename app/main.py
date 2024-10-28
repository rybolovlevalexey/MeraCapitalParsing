from fastapi import FastAPI
from routers.currencies import currencies_router
from contextlib import asynccontextmanager
import asyncio
import uvicorn

from services import BackGroundTasks


app = FastAPI()
app.include_router(currencies_router)


@app.get("/")
def index():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # действия выполняемые до начала работы API
    await asyncio.create_task(BackGroundTasks().parse_and_save())  # запуск фоновой задачи
    # возвращение к основному жизненному циклу
    yield
    # выполнение действий после завершения работы API


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
