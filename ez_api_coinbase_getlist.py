import requests
import json

def get_market_list_coinbase():
    url = 'https://api.exchange.coinbase.com/products'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        ids = [item['id'] for item in data if 'id' in item]
        ids.sort()
        with open('market_list_coinbase.txt', 'w', encoding='utf-8') as f:
            for id in ids:
                f.write(f"{id}\n")
        print(f'API response saved to market_list_coinbase.txt. \nCoinbase {len(ids)} pairs written.')
    else:
        print(f'Error fetching data: {response.status_code}')

get_market_list_coinbase()


# Coinbase instead of using 'symbol' uses 'id'
