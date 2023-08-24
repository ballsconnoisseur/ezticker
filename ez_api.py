# Module for requests from api socket

import requests

def get_market_by_symbol(symbol):
    url = f'https://xeggex.com/api/v2/market/getbysymbol/{symbol}'
    headers = {'accept': 'application/json'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"A- Error fetching market data for symbol {symbol}: {response.status_code}")
        return None
