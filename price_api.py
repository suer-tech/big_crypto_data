import aiohttp


async def get_kline_data(symbol, interval, limit=500, startTime=None, endTime=None):
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": startTime,
        "endTime": endTime
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print("Error occurred while retrieving Kline data:", response.text)
                return None


async def get_symbol_price_ticker():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                sym_index = await response.json()
                return [sym['symbol'] for sym in sym_index if sym['symbol'].endswith('USDT')]
            else:
                print("Error occurred while retrieving Kline data:", await response.text())
                return None






