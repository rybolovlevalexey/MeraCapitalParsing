from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, Column, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

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

