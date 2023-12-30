import asyncio
import aiohttp
import asyncpg

from conf_db import db_name
from db_crud import create_db, Crypto
from price_api import get_symbol_price_ticker, get_symbol_kline_data
from conf_db import conn_params


interval = '1h'
limit_kline = 500


async def main():
    await create_db(db_name)

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
                tasks.append(symbol_kline_data)

            all_crypto_kline_data = await asyncio.gather(*tasks)

        crypto_objects = [Crypto(symbol, kline_data) for crypto_kline_data in all_crypto_kline_data for symbol, kline_data in crypto_kline_data.items()]

        pool = await asyncpg.create_pool(**conn_params)

        db_table_create_tasks = []
        for crypto_obj in crypto_objects:
            crypto_table_create = crypto_obj.create_table(pool)
            db_table_create_tasks.append(crypto_table_create)

        await asyncio.gather(*db_table_create_tasks)

        db_data_save_tasks = []
        for crypto_obj in crypto_objects:
            for i in range(limit_kline):
                crypto_data_save = crypto_obj.save_to_database(i, pool)
                db_data_save_tasks.append(crypto_data_save)

        await asyncio.gather(*db_data_save_tasks)

        await pool.close()

asyncio.run(main())
