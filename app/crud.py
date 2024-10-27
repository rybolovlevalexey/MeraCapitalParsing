from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

import asyncio
import time
from datetime import datetime, date

from models import CostInfo, async_session_maker


class CostsInfoActions:
    def __init__(self):
        self.session: AsyncSession

    async def add_new_data_about_costs(self, ticker: str, cur_cost: float) -> None:
        async with async_session_maker() as self.session:
            new_cost_info = CostInfo(ticker=ticker, cur_cost=cur_cost, timestamp=int(time.time()))
            self.session.add(new_cost_info)
            await self.session.commit()

    async def get_all_costs_info(self) -> list[dict]:
        async with async_session_maker() as self.session:
            costs_info = await self.session.execute(select(CostInfo))
            result = [{"ticker": elem_cost_info.ticker,
                       "cur_cost": elem_cost_info.cur_cost,
                       "timestamp": elem_cost_info.timestamp}
                      for elem_cost_info in costs_info.scalars().all()]
            return result

    async def get_info_by_ticker_name(self, ticker_name: str) -> list[dict]:
        async with async_session_maker() as self.session:
            costs_info = await self.session.execute(select(CostInfo).where(CostInfo.ticker == ticker_name))
            result = [{"ticker": elem_cost_info.ticker,
                       "cur_cost": elem_cost_info.cur_cost,
                       "timestamp": elem_cost_info.timestamp}
                      for elem_cost_info in costs_info.scalars().all()]
            return result

    async def get_info_by_ticker_name_latest(self, ticker_name: str) -> dict:
        async with async_session_maker() as self.session:
            costs_info = await self.session.execute(select(CostInfo).where(
                CostInfo.ticker == ticker_name).order_by(CostInfo.timestamp.desc).limit(1))
            cost_info_elem = costs_info.scalar()
            result = {"ticker": cost_info_elem.ticker,
                      "cur_cost": cost_info_elem.cur_cost,
                      "timestamp": cost_info_elem.timestamp}
            return result

    async def get_info_by_ticker_name_date_filter(self, ticker_name: str,
                                                  dates: list[datetime] | None = None) -> list[dict]:
        dates = list(map(lambda elem: elem.date(), dates))
        async with async_session_maker() as self.session:
            costs_info = await self.session.execute(CostInfo).where(
                and_(CostInfo.ticker == ticker_name, date.fromtimestamp(CostInfo.date.in_(dates))))
            result = [{"ticker": cost_info_elem.ticker,
                       "cur_cost": cost_info_elem.cur_cost,
                       "timestamp": cost_info_elem.timestamp}
                      for cost_info_elem in costs_info]
            return result
