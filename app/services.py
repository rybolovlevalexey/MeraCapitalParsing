from pprint import pprint
import aiohttp
import asyncio


class Parsing:
    session: aiohttp.ClientSession

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


# Тестовые запуски
if __name__ == "__main__":
    async def main():
        parser = Parsing()
        resp = await parser.get_current_cost("eth_usd")
        pprint(resp)
        await parser.session.close()


    asyncio.run(main())
