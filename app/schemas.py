from pydantic import BaseModel


# МОДЕЛИ ДЛЯ ОТВЕТА НА ЗАПРОСЫ ПОЛЬЗОВАТЕЛЯ
# модель бд записи о цене тикера в конкретный момент времени
class CurCostInfo(BaseModel):
    ticker: str
    cur_cost: float
    timestamp: int
