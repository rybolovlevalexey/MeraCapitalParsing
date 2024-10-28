from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import datetime

from app.schemas import CurCostInfo
from app.crud import CostsInfoActions


currencies_router = APIRouter(prefix="/currencies_price")


@currencies_router.get("/{ticker_name}", response_model=list[CurCostInfo])
async def get_full_price_info_by_ticker(ticker_name: str):
    cost_info_acts = CostsInfoActions()
    if not await cost_info_acts.check_ticker_in_database(ticker_name):
        return JSONResponse(status_code=404, content={"message": "Ticker name not found"})

    info_by_ticker_res_json: list[dict] = await cost_info_acts.get_info_by_ticker_name(ticker_name)
    output_result = [CurCostInfo(**elem) for elem in info_by_ticker_res_json]
    return output_result


@currencies_router.get("/{ticker_name}/latest", response_model=CurCostInfo)
async def get_latest_price_info_by_ticker(ticker_name: str):
    cost_info_acts = CostsInfoActions()
    if not await cost_info_acts.check_ticker_in_database(ticker_name):
        return JSONResponse(status_code=404, content={"message": "Ticker name not found"})

    info_by_ticker_res_json: dict = await cost_info_acts.get_info_by_ticker_name_latest(ticker_name)
    output_result = CurCostInfo(**info_by_ticker_res_json)
    return output_result


@currencies_router.get("/{ticker_name}/date_filter/", response_model=list[CurCostInfo])
async def get_price_info_by_list_of_dates(ticker_name: str,
                                          dates_list: list[datetime] | None = Query(
                                              None, description="Одна или несколько дат в формате YYYY-MM-DD")):
    cost_info_acts = CostsInfoActions()
    if not await cost_info_acts.check_ticker_in_database(ticker_name):
        return JSONResponse(status_code=404, content={"message": "Ticker name not found"})

    info_by_ticker_res_json: list[dict] = await cost_info_acts.get_info_by_ticker_dates_filter(ticker_name, dates_list)
    output_result = [CurCostInfo(**elem) for elem in info_by_ticker_res_json]
    return output_result


@currencies_router.get("/{ticker_name}/date_range_filter")
async def get_price_info_by_dates_range(ticker_name: str,
                                        date_beginning: datetime | None = Query(
                                            None, description="Дата начала диапазона в формате YYYY-MM-DD"),
                                        date_ending: datetime | None = Query(
                                            None, description="Дата начала диапазона в формате YYYY-MM-DD")):
    cost_info_acts = CostsInfoActions()
    if not await cost_info_acts.check_ticker_in_database(ticker_name):
        return JSONResponse(status_code=404, content={"message": "Ticker name not found"})

    info_by_ticker_res_json: list[dict] = await cost_info_acts.get_info_by_ticker_date_range_filter(
        ticker_name, date_beginning, date_ending)
    output_result = [CurCostInfo(**elem) for elem in info_by_ticker_res_json]
    return output_result
