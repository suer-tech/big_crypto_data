import asyncio
from conf_db import db_name
from db_crud import create_db, Crypto
from price_api import get_kline_data, get_symbol_price_ticker

limit_kline = 500


async def main():
    await create_db(db_name)

    cryptos = await get_symbol_price_ticker()

    if cryptos:

        data = {symbol: await get_kline_data(symbol, '1h', limit=limit_kline) for symbol in cryptos}
        crypto_data = [Crypto(symbol, data_instance) for symbol, data_instance in data.items()]
        tables = [await crypto.create_table() for crypto in crypto_data]
        save = [await crypto_kline_data.save_to_database(i) for crypto_kline_data in crypto_data for i in range(limit_kline)]

asyncio.run(main())
