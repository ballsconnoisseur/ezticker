import requests
import json

binance = True
coinbase = True
okx = True
xeggex = True

#log GL- stands for Get List
# This module is for geting list of pairs from choosen exchange

def get_list(binance, coinbase, okx, xeggex):
    if binance:
        def get_market_list_binance():
            url = 'https://api.binance.com/api/v3/ticker/24hr'
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                symbols = [item['symbol'] for item in data if 'symbol' in item]
                symbols.sort()
                with open('ez_pair_list_binance.txt', 'w', encoding='utf-8') as f:
                    for symbol in symbols:
                        f.write(f"{symbol}\n")
                print(f'GL- API response saved to ez_pair_list_binance.txt. \nBinance {len(symbols)} pairs written.')
            else:
                print(f'GL- Error fetching data: {response.status_code}')

        get_market_list_binance()
    else:
        print("GL- Skipping Binance.")


    if coinbase:
        # Coinbase instead of using 'symbol' uses 'id'
        def get_market_list_coinbase():
            url = 'https://api.exchange.coinbase.com/products'
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                ids = [item['id'] for item in data if 'id' in item]
                ids.sort()
                with open('ez_pair_list_coinbase.txt', 'w', encoding='utf-8') as f:
                    for id in ids:
                        f.write(f"{id}\n")
                print(f'GL- API response saved to ez_pair_list_coinbase.txt. \nCoinbase {len(ids)} pairs written.')
            else:
                print(f'GL- Error fetching data: {response.status_code}')

        get_market_list_coinbase()
    else:
        print("GL- Skipping Coinbase.")

    if okx:
        # OKX instead of using 'symbol' uses 'instId'
        def get_market_list_okx():
            url = 'https://www.okx.com/api/v5/public/instruments?instType=SPOT'
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)['data']  # Access the 'data' key
                instIds = [item['instId'] for item in data if 'instId' in item]
                instIds.sort()
                with open('ez_pair_list_okx.txt', 'w', encoding='utf-8') as f:
                    for instId in instIds:
                        f.write(f"{instId}\n")
                print(f'API response saved to ez_pair_list_okx.txt. \nOKX {len(instIds)} pairs written.')
            else:
                print(f'Error fetching data: {response.status_code}')

        get_market_list_okx()
    else:
        print("GL- Skipping OKX.")

    if xeggex:
        def get_market_list_xeggex():
            url = 'https://xeggex.com/api/v2/market/getlist'
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                symbols = [item['symbol'] for item in data if 'symbol' in item]
                symbols.sort()
                with open('ez_pair_list_xeggex.txt', 'w', encoding='utf-8') as f:
                    for symbol in symbols:
                        f.write(f"{symbol}\n")
                print(f'API response saved to ez_pair_list_xeggex.txt. \nXeggeX {len(symbols)} pairs written.')
            else:
                print(f'Error fetching data: {response.status_code}')

        get_market_list_xeggex()

    else:
        print("GL- Skipping OKX.")



get_list(True, True, True, True)
print("GL- Successfully optained selected exchanges pair data!")