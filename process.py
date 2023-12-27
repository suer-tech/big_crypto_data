from conf_db import db_name
from db_crud import create_db, Crypto
from price_api import get_usdt_data, get_kline_data


limit_kline = 500

create_db(db_name)

cryptos = get_usdt_data()

data = {symbol: get_kline_data(symbol, '1h', limit=limit_kline, startTime=None, endTime=None) for symbol in cryptos}

crypto_data = [Crypto(symbol, data_instance) for symbol, data_instance in data.items()]

tables = [crypto.create_table() for crypto in crypto_data]

save = [crypto_kline_data.save_to_database(i) for crypto_kline_data in crypto_data for i in range(limit_kline)]
