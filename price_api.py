import requests


def get_kline_data(symbol, interval, limit=500, startTime=None, endTime=None):
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": startTime,
        "endTime": endTime
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None


def get_symbol_price_ticker():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None


def get_usdt_data():
    symb_index = get_symbol_price_ticker()
    return [symb['symbol'] for symb in symb_index if symb['symbol'].endswith('USDT')]



