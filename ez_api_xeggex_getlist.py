import requests
import json

def get_market_list_xeggex():
    url = 'https://xeggex.com/api/v2/market/getlist'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        symbols = [item['symbol'] for item in data if 'symbol' in item]
        symbols.sort()
        with open('market_list_xeggex.txt', 'w', encoding='utf-8') as f:
            for symbol in symbols:
                f.write(f"{symbol}\n")
        print(f'API response saved to market_list_xeggex.txt. \nXeggeX {len(symbols)} pairs written.')
    else:
        print(f'Error fetching data: {response.status_code}')

get_market_list_xeggex()
