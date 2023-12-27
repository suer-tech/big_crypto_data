import psycopg2
from conf_db import conn_params, db_create_params


def create_db(db_name):
    conn = psycopg2.connect(**db_create_params)
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
    def __init__(self, symbol, data):
        self.data = data
        self.symbol = symbol
        self.timestamp = None
        self.low_price = None
        self.high_price = None
        self.volume = None

    def create_table(self):
        conn = psycopg2.connect(**conn_params)
        try:
            cur = conn.cursor()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.symbol.lower()}_table (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(50),
                    timestamp BIGINT,
                    low_price DECIMAL,
                    high_price DECIMAL,
                    volume DECIMAL
                )
            ''')
            print(f'success create table {self.symbol.lower()}_table')

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

        finally:
            # Закрытие соединения
            if conn is not None:
                conn.commit()

    def save_to_database(self, i):
        self.timestamp = int(self.data[i][0])
        self.low_price = float(self.data[i][3])
        self.high_price = float(self.data[i][2])
        self.volume = float(self.data[i][5])

        conn = psycopg2.connect(**conn_params)
        try:
            cur = conn.cursor()

            cur.execute(f'''
                INSERT INTO {self.symbol.lower()}_table (symbol, timestamp, low_price, high_price, volume)
                VALUES (%s, %s, %s, %s, %s)
            ''', (self.symbol, self.timestamp, self.low_price, self.high_price, self.volume))
            print(f'success add data on table {self.symbol.lower()}_table')

        except psycopg2.Error as e:
            print(f"Ошибка при загрузке данных в таблицу {self.symbol.lower()}_table: {e}")

        finally:
            # Закрытие соединения
            if conn is not None:
                conn.commit()
