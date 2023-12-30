import asyncio
import aiohttp
from conf_db import db_name
# from db_crud import create_db, Crypto
from price_api import get_symbol_price_ticker, get_symbol_kline_data

interval = '1h'
limit_kline = 500


async def main():
    # await create_db(db_name)

    all_crypto = await get_symbol_price_ticker()

    if all_crypto:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for crypto in all_crypto:
                params = {
                    "symbol": crypto,
                    "interval": interval,
                    "limit": limit_kline,
                }
                symbol_kline_data = get_symbol_kline_data(session, crypto, params)
                crypto_kline_data = asyncio.ensure_future(symbol_kline_data)
                tasks.append(crypto_kline_data)

            all_crypto_kline_data = await asyncio.gather(*tasks)


        # data = {symbol: await get_symbol_kline_data(symbol, '1h', limit=limit_kline) for symbol in all_crypto}
        # crypto_data = [Crypto(symbol, data_instance) for symbol, data_instance in data.items()]
        # tables = [await crypto.create_table() for crypto in crypto_data]
        # save = [await crypto_kline_data.save_to_database(i) for crypto_kline_data in crypto_data for i in range(limit_kline)]

asyncio.run(main())
