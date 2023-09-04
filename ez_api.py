import requests

def get_market(exchange, symbol):
    result = {}
    if exchange == 'binance':
        url = f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}'
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = {k: v for k, v in response.json().items() if k in ['closeTime', 'symbol', 'lastPrice', 'bidPrice', 'askPrice', 'priceChangePercent', 'highPrice', 'lowPrice', 'volume']}
        else:
            result = {'error': f"A- Error fetching market data from {exchange} for symbol {symbol}: {response.status_code}"}
    
    elif exchange == 'xeggex':
        url = f'https://xeggex.com/api/v2/market/getbysymbol/{symbol}'
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = {k: v for k, v in response.json().items() if k in ['updatedAt', 'symbol', 'lastPrice', 'bestBid', 'bestAsk', 'changePercent', 'highPrice', 'lowPrice', 'volume']}
        else:
            result = {'error': f"A- Error fetching market data from {exchange} for symbol {symbol}: {response.status_code}"}
    
    elif exchange == 'okx':
        url = f'https://www.okx.com/api/v5/market/ticker?instId={symbol}'
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()['data'][0]
            result = {k: v for k, v in data.items() if k in ['ts', 'instId', 'last', 'bidPx', 'askPx', 'high24h', 'low24h', 'volCcy24h']}
        else:
            result = {'error': f"A- Error fetching market data from {exchange} for symbol {symbol}: {response.status_code}"}
    
    elif exchange == 'coinbase':
        url_head = f'https://api.exchange.coinbase.com/products/{symbol}'
        headers = {'accept': 'application/json'}
        response_head = requests.get(url_head, headers=headers)
        url_ticker = f'https://api.exchange.coinbase.com/products/{symbol}/ticker'
        response_ticker = requests.get(url_ticker, headers=headers)
        url_stats = f'https://api.exchange.coinbase.com/products/{symbol}/stats'
        response_stats = requests.get(url_stats, headers=headers)
        
        if response_head.status_code == 200 and response_ticker.status_code == 200 and response_stats.status_code == 200:
            head_data = response_head.json()
            ticker_data = response_ticker.json()
            stats_data = response_stats.json()
            combined_data = {**head_data, **ticker_data, **stats_data}
            result = ({k: v for k, v in combined_data.items() if k in ['time', 'display_name', 'price', 'bid', 'ask', 'high', 'low', 'volume']})
        else:
            result = {'error': f"A- Error fetching market data from {exchange} for symbol {symbol}"}
    
    else:
        result = {'error': f"A- Error no exchange chosen: {exchange} {symbol}"}
    
    return result
