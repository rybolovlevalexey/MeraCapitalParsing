from pprint import pprint
import aiohttp
import asyncio

from crud import CostsInfoActions


class Parsing:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def get_current_cost(self, ticker: str = "btc_usd",
                               url: str = "wss://www.deribit.com/ws/api/v2") -> float:
        """
        Получение ответа от Deribit
        :param ticker: название индекса
        :param url: ссылка
        :return: цена переданного тикера
        """
        send_msg: dict = {
            "jsonrpc": "2.0",
            "method": "public/get_index_price",
            "id": 42,
            "params": {
                "index_name": f"{ticker}"
            }
        }
        # открытие веб-сокета
        async with self.session.ws_connect(url) as web_socket:
            # отправка запроса
            await web_socket.send_json(send_msg)
            result = await web_socket.receive()
            # общий результат в формате json
            result_json = result.json()
            cur_index_price = result_json["result"]["index_price"]
            return cur_index_price


class BackGroundTasks:
    def __init__(self):
        self.parsing_acts = Parsing()
        self.default_tickers_list: list[str] = ["btc_usd", "eth_usd"]
        self._task: None | asyncio.Task = None  # хранение фоновой задачи

    async def parse_and_save(self, tickers_list: list[str] | None = None):
        if tickers_list is None:
            tickers_list = self.default_tickers_list.copy()

        # ежеминутный парсинг и сохранение информации
        while True:
            print("in updated while true")
            for ticker in tickers_list:
                cur_cost = await self.parsing_acts.get_current_cost(ticker)
                await CostsInfoActions().add_new_data_about_costs(ticker, cur_cost)
            await asyncio.sleep(60)

    def start_background_task(self):
        # запуск фоновой задачи
        self._task = asyncio.create_task(self.parse_and_save())

    async def stop_background_task(self):
        # остановка фоновой задачи
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass


# Тестовые запуски
if __name__ == "__main__":
    async def main():
        parser = Parsing()
        resp = await parser.get_current_cost("eth_usd")
        pprint(resp)
        await parser.session.close()


    asyncio.run(main())
