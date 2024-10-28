from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import uvicorn

from app.routers.currencies import currencies_router
from app.config import settings
from app.services import BackGroundTasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(settings.get_db_url())
    background_tasks = BackGroundTasks()
    # Действия перед запуском API
    background_tasks.start_background_task()  # Запуск фоновой задачи
    try:
        yield  # Переход к основному жизненному циклу
    finally:
        # Действия при завершении API
        await background_tasks.stop_background_task()  # Остановка фоновой задачи


app = FastAPI(lifespan=lifespan)
app.include_router(currencies_router)


@app.get("/")
def index():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
