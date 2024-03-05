import asyncio
import itertools
import time

import aiohttp
import asyncpg

from conf_db import db_name
from db_crud import create_db, Crypto, get_names_of_tables_in_db, create_corr_data_table, \
    fetch_and_insert_data
from price_api import get_symbol_price_ticker, get_symbol_kline_data
from conf_db import conn_params

interval = '1h'
limit_kline = 500


async def create_first_crypto_data_in_db():
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

        crypto_objects = [Crypto(symbol, kline_data) for crypto_kline_data in all_crypto_kline_data for
                          symbol, kline_data in crypto_kline_data.items()]

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


async def main():
    semaphore = asyncio.Semaphore(50)
    start = time.time()
    # await create_first_crypto_data_in_db()
    await asyncio.sleep(0)
    async with await asyncpg.create_pool(**conn_params, max_size=1000) as pool:
        tables_in_db = await get_names_of_tables_in_db(pool)

        await create_corr_data_table(pool)

        tasks = []
        for x, y in itertools.permutations(tables_in_db, 2):

            task = asyncio.create_task(fetch_and_insert_data(pool, x, y))
            tasks.append(task)

        # async with semaphore:
        await asyncio.gather(*tasks)

        await pool.close()

    end = time.time()
    res = end-start
    print(res)

asyncio.run(main())