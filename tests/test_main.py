import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, delete

from app.main import app
from app.crud import CostsInfoActions
from app.models import async_session_maker, CostInfo


@pytest.fixture(scope="module")
def test_client():
    # создание тестового экземпляра api
    with TestClient(app) as client:
        yield client


def test_currencies_price_btc_usd_latest(test_client):
    resp = test_client.get("/currencies_price/btc_usd/latest")
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json["ticker"] == "btc_usd"
    if resp_json["timestamp"] == 1730110547:
        assert resp_json["cur_cost"] == 68493.14


def test_ticker_name(test_client):
    resp = test_client.get("/currencies_price/eth_usd")
    resp_json = resp.json()
    assert resp.status_code == 200
    assert set(map(lambda elem: elem["ticker"], resp_json)) == {"eth_usd"}


def test_dates_filter(test_client):
    resp = test_client.get("/currencies_price/btc_usd/date_filter", params={"dates": "2024-10-27"})
    resp_json = resp.json()
    assert resp.status_code == 200
    assert len(resp_json) == 2
    if resp_json[0]["ticker"] == "btc_usd" and resp_json[0]["timestamp"] == 1730040225:
        assert resp_json[0]["cur_cost"] == 68554.0


def test_date_range_filter(test_client):
    resp = test_client.get("/currencies_price/btc_usd/date_range_filter",
                           params={"date_beginning": "2024-10-27",
                                   "date_ending": "2024-10-27"})
    resp_json = resp.json()
    assert resp.status_code == 200
    assert len(resp_json) == 2
    if resp_json[0]["ticker"] == "btc_usd" and resp_json[0]["timestamp"] == 1730040225:
        assert resp_json[0]["cur_cost"] == 68554.0

    resp = test_client.get("/currencies_price/btc_usd/date_range_filter",
                           params={"date_beginning": "2024-10-27",
                                   "date_ending": "2024-10-28"})
    resp_json = resp.json()
    assert resp.status_code == 200
    assert len(resp_json) > 2


@pytest.mark.asyncio
async def test_database():
    costs_info_acts = CostsInfoActions()
    ticker_test_res = await costs_info_acts.check_ticker_in_database("test_ticker")
    ticker_btc_res = await costs_info_acts.check_ticker_in_database("btc_usd")
    assert not ticker_test_res
    assert ticker_btc_res

    async with async_session_maker() as session:
        query_result = await session.execute(select(CostInfo))
        count_all_before_add = len(query_result.scalars().all())
        query_result = await session.execute(select(CostInfo).where(CostInfo.ticker == "test_ticker"))
        count_test_before_add = len(query_result.scalars().all())
        assert count_test_before_add == 0

        await costs_info_acts.add_new_data_about_costs("test_ticker", 150.5)
        query_result = await session.execute(select(CostInfo).where(CostInfo.ticker == "test_ticker"))
        assert len(query_result.scalars().all()) == 1
        query_result = await session.execute(select(CostInfo))
        assert len(query_result.scalars().all()) == count_all_before_add + 1
        # удаление тестовых данных
        await session.execute(delete(CostInfo).where(CostInfo.ticker == "test_ticker"))
        await session.commit()
        query_result = await session.execute(select(CostInfo).where(CostInfo.ticker == "test_ticker"))
        assert len(query_result.scalars().all()) == 0
