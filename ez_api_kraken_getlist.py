import requests
import json

def get_market_list_kraken():
    url = 'https://api.kraken.com/0/public/AssetPairs'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        symbols = [item['pair'] for item in data if 'pair' in item]
        symbols.sort()
        with open('market_list_kraken.txt', 'w', encoding='utf-8') as f:
            for symbol in symbols:
                f.write(f"{symbol}\n")
        print(f'API response saved to market_list_kraken.txt. {len(symbols)} lines written.')
    else:
        print(f'Error fetching data: {response.status_code}')

get_market_list_kraken()


# NOT WORKING !!!