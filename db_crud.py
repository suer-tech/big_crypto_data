import asyncpg
from conf_db import conn_params, db_create_params


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

    async def create_table(self):
        conn = await asyncpg.connect(**conn_params)
        try:
            async with conn.transaction():
                await conn.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.symbol}_table (
                        id SERIAL PRIMARY KEY,
                        symbol VARCHAR(50),
                        timestamp BIGINT,
                        low_price DECIMAL,
                        high_price DECIMAL,
                        volume DECIMAL
                    )
                ''')
                print(f'success create table {self.symbol}_table')

        except asyncpg.exceptions.PostgresError as e:
            print(f"Ошибка при создании таблицы: {e}")

        finally:
            # Закрытие соединения
            if conn is not None:
                await conn.commit()

    async def save_to_database(self, i):
        self.timestamp = int(self.data[i][0])
        self.low_price = float(self.data[i][3])
        self.high_price = float(self.data[i][2])
        self.volume = float(self.data[i][5])

        conn = await asyncpg.connect(**conn_params)
        try:
            async with conn.transaction():
                await conn.execute(f'''
                    INSERT INTO {self.symbol}_table (symbol, timestamp, low_price, high_price, volume)
                    VALUES ($1, $2, $3, $4, $5)
                ''', (self.symbol, self.timestamp, self.low_price, self.high_price, self.volume))
                print(f'success add data on table {self.symbol}_table')

        except asyncpg.exceptions.PostgresError as e:
            print(f"Ошибка при загрузке данных в таблицу {self.symbol}_table: {e}")

        finally:
            # Закрытие соединения
            if conn is not None:
                await conn.commit()
