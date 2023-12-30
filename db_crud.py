import asyncio

import asyncpg
from conf_db import db_create_params


async def create_db(db_name):
    # Устанавливаем параметры подключения к базе данных
    create_conn_params = db_create_params.copy()
    create_conn_params["database"] = "postgres"  # Подключаемся к системной базе данных PostgreSQL

    conn = await asyncpg.connect(**create_conn_params)

    try:
        await conn.execute(f'CREATE DATABASE {db_name}')
        print('success create db....')

    except asyncpg.exceptions.PostgresError as e:
        print(f"Ошибка при создании базы данных: {e}")

    finally:
        # Закрытие соединения
        if conn is not None:
            await conn.close()


class Crypto:
    def __init__(self, symbol, data):
        self.data = data
        self.symbol = symbol
        self.timestamp = None
        self.low_price = None
        self.high_price = None
        self.volume = None

    def __str__(self):
        return self.symbol

    async def create_table(self, pool):
        max_retries = 10
        async with pool.acquire() as connection:
            for attempt in range(max_retries):
                print(self.symbol)
                print(f'Попытка подключения {attempt}')
                try:

                    async with connection.transaction():
                        await connection.execute(f'''
                            CREATE TABLE IF NOT EXISTS _{self.symbol}_table (
                                id SERIAL PRIMARY KEY,
                                symbol VARCHAR(50),
                                timestamp BIGINT,
                                low_price DECIMAL,
                                high_price DECIMAL,
                                volume DECIMAL
                            )
                        ''')
                        print(f'success create table _{self.symbol}_table')
                        break

                except asyncpg.exceptions.PostgresError as e:
                    print(f"Ошибка при создании таблицы: {e}")

                    if attempt == max_retries -1:
                        raise ValueError('Максимальное количество попыток создания таблицы')

                    await asyncio.sleep(5)

    async def save_to_database(self, i, pool):
        if i < len(self.data):
            self.timestamp = int(self.data[i][0])
            self.low_price = float(self.data[i][3])
            self.high_price = float(self.data[i][2])
            self.volume = float(self.data[i][5])
        else:
            print(f'Индекс {i} выходит за пределы длины списка {self.symbol}')

        async with pool.acquire() as connection:
            try:
                async with connection.transaction():
                    await connection.execute(f'''
                        INSERT INTO _{self.symbol}_table (symbol, timestamp, low_price, high_price, volume)
                        VALUES ($1, $2, $3, $4, $5)
                    ''', self.symbol, self.timestamp, self.low_price, self.high_price, self.volume)
                    print(f'success add data on table _{self.symbol}_table')

            except asyncpg.exceptions.PostgresError as e:
                print(f"Ошибка при загрузке данных в таблицу {self.symbol}_table: {e}")
