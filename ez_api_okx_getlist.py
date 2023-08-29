import requests
import json

def get_market_list_okx():
    url = 'https://www.okx.com/api/v5/public/instruments?instType=SPOT'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)['data']  # Access the 'data' key
        instIds = [item['instId'] for item in data if 'instId' in item]
        instIds.sort()
        with open('market_list_okx.txt', 'w', encoding='utf-8') as f:
            for instId in instIds:
                f.write(f"{instId}\n")
        print(f'API response saved to market_list_okx.txt. \nOKX {len(instIds)} pairs written.')
    else:
        print(f'Error fetching data: {response.status_code}')

get_market_list_okx()


# OKX instead of using 'symbol' uses 'instId'