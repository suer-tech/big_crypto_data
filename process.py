import asyncio
import logging

import aiohttp
import asyncpg

from conf_db import db_name
from db_crud import create_db, Crypto, create_table
from price_api import get_symbol_price_ticker, get_symbol_kline_data
from conf_db import conn_params


interval = '1h'
limit_kline = 100


async def request_data(session, all_crypto):
    tasks = []
    for crypto in all_crypto:
        params = {
            "symbol": crypto,
            "interval": interval,
            "limit": limit_kline,
        }
        symbol_kline_data = get_symbol_kline_data(session, crypto, params)
        tasks.append(symbol_kline_data)

    return await asyncio.gather(*tasks)


async def main():
    await create_db(db_name)

    all_crypto = await get_symbol_price_ticker()

    all_crypto_kline_data = []

    async with aiohttp.ClientSession() as session:
        for i in range(2):
            print(f'iterattion {i}')
            data = await request_data(session, all_crypto)
            if data:
                if i > 0:
                    for d in data:
                        for symbol, nested_list in d.items():
                            for inner_list in nested_list:
                                for x in range(len(inner_list)):
                                    if isinstance(inner_list[x], float):
                                        inner_list[x] = str(float(inner_list[x]) * 1.1)
                                    elif isinstance(inner_list[x], int):
                                        inner_list[x] = str(int(inner_list[x]) + 1)

            all_crypto_kline_data += data


        crypto_objects = [Crypto(symbol, kline_data) for crypto_kline_data in all_crypto_kline_data for symbol, kline_data in crypto_kline_data.items()]

        pool = await asyncpg.create_pool(**conn_params)

        await create_table(pool)

        db_data_save_tasks = []
        for crypto_obj in crypto_objects:
            for i in range(limit_kline):
                crypto_data_save = crypto_obj.save_to_database(i, pool)
                db_data_save_tasks.append(crypto_data_save)

        await asyncio.gather(*db_data_save_tasks)

        await pool.close()

        from price_api import total_requests
        print("Total requests made:", total_requests)


asyncio.run(main())