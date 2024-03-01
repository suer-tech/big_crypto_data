import asyncio

import aiohttp


total_requests = 0


async def get_symbol_kline_data(session, symbol, params):
    global total_requests
    url = "https://fapi.binance.com/fapi/v1/klines"
    async with session.get(url, params=params) as response:
        total_requests += 1
        if response.status == 200:
            return {symbol: await response.json()}
        elif response.status == 429:
            print("Max requests is out:", response.text)
            retry_after = int(response.headers.get('Retry-After',
                                                   60))  # В случае отсутствия заголовка Retry-After, устанавливаем время ожидания по умолчанию в 60 секунд
            print("Error occurred while retrieving Kline data:", response.text)
            await asyncio.sleep(retry_after)  # Устанавливаем время ожидания до следующей попытки запроса
            return None
        else:
            print("Error occurred while retrieving Kline data:", response.text)
            return None


async def get_symbol_price_ticker():
    global total_requests
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            total_requests += 1
            if response.status == 200:
                sym_index = await response.json()
                return [sym['symbol'] for sym in sym_index if sym['symbol'].endswith('USDT')]
            else:
                print("Error occurred while retrieving Kline data:", await response.text())
                return None
