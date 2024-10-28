from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, Column, TIMESTAMP, func, cast
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from datetime import datetime

from app.config import settings


engine = create_async_engine(f"sqlite+aiosqlite:///{settings.DATABASE_URL}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class CostInfo(Base):
    __tablename__ = "costs_info"

    ticker: Mapped[str] = mapped_column(String, nullable=False)
    cur_cost: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    @hybrid_property
    def date(self) -> datetime.date:
        # Вычисляемое поле, возвращающее дату на основе timestamp
        return datetime.fromtimestamp(self.timestamp).date()

    @date.expression
    def date(cls) -> expression.ColumnElement:
        # Вычисляемое поле, возвращающее дату на основе timestamp
        # использование date.expression позволяет использовать поле в sql запросах
        return func.date(func.from_unixtime(cast(cls.timestamp, Float)))
