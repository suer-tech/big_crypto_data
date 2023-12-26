import psycopg2
from conf_db import conn_params


def create_db(db_name):
    conn = psycopg2.connect(**conn_params)
    try:
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f'CREATE DATABASE {db_name}')
        print('success create db....')

    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

    finally:
        # Закрытие соединения
        if conn is not None:
            conn.close()


class Crypto:
    def __init__(self, symbol):
        self.symbol = symbol
        self.timestamp = None
        self.low_price = None
        self.high_price = None
        self.volume = None

    def add_data(self, timestamp, low_price, high_price, volume):
        self.timestamp = timestamp
        self.low_price = low_price
        self.high_price = high_price
        self.volume = volume

    def save_to_database(self, table_name):
        conn = psycopg2.connect(**conn_params)
        try:
            cur = conn.cursor()

            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(50),
                    timestamp TIMESTAMP,
                    low_price DECIMAL,
                    high_price DECIMAL
                )
            ''')
            print(f'sucess create table {table_name}')

            cur.execute(f'''
                INSERT INTO {table_name} (symbol, timestamp, low_price, high_price)
                VALUES (%s, %s, %s, %s)
            ''', (self.symbol, self.timestamp, self.low_price, self.high_price))

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

        finally:
            # Закрытие соединения
            if conn is not None:
                conn.close()
