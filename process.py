from db_crud import create_db, Crypto
from price_api import get_usdt_data, get_kline_data

create_db('Crypto')

cryptos = get_usdt_data()

for symbol in cryptos:
    print(symbol)
    crypto_items = Crypto(symbol)
    data = get_kline_data(symbol, '1h', limit=500, startTime=None, endTime=None)
    print(data)
    print(data[0])
    Crypto.add_data(data[0], data[3], data[2], data[5])
