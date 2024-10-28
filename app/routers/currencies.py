from fastapi import APIRouter, Query
from datetime import datetime

currencies_router = APIRouter(prefix="/currencies_price")


@currencies_router.get("/{ticker_name}")
async def get_full_price_info_by_ticker(ticker_name: str):
    pass


@currencies_router.get("/{ticker_name}/latest")
async def get_latest_price_info_by_ticker(ticker_name: str):
    pass


@currencies_router.get("/{ticker_name}/date_filter/")
async def get_price_info_by_list_of_dates(ticker_name: str,
                                          dates_list: list[datetime] | None = Query(
                                              None, description="Одна или несколько дат в формате YYYY-MM-DD")):
    pass


@currencies_router.get("/{ticker_name}/date_range_filter")
async def get_price_info_by_dates_range(ticker_name: str,
                                        date_beginning: datetime | None = Query(
                                            None, description="Дата начала диапазона в формате YYYY-MM-DD"),
                                        date_ending: datetime | None = Query(
                                            None, description="Дата начала диапазона в формате YYYY-MM-DD")):
    pass
