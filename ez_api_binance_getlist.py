import requests
import json

def get_market_list_binance():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        symbols = [item['symbol'] for item in data if 'symbol' in item]
        symbols.sort()
        with open('market_list_binance.txt', 'w', encoding='utf-8') as f:
            for symbol in symbols:
                f.write(f"{symbol}\n")
        print(f'API response saved to market_list_binance.txt. \nBinance {len(symbols)} pairs written.')
    else:
        print(f'Error fetching data: {response.status_code}')

get_market_list_binance()
