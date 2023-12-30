import aiohttp


async def get_symbol_kline_data(session, symbol, params):
    url = "https://fapi.binance.com/fapi/v1/klines"
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return {symbol: await response.json()}
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






