import ez_api
from datetime import datetime

def format_market_data(symbol):
    market_data = ez_api.get_market_by_symbol(symbol)

    if market_data:
        # Convert updatedAt to time format
        updated_at = datetime.fromtimestamp(market_data['updatedAt'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Add "%" to changePercent
        change_percent = str(market_data['changePercent']) + " %"

        volume = market_data['volume']
        if isinstance(volume, str):
            volume = float(volume)  # or int(volume) if it's always an integer

        if volume >= 10**9:
            volume = str(volume // 10**9) + " B"
        elif volume >= 10**6:
            volume = str(volume // 10**6) + " M"
        elif volume >= 1000:
            volume = str(volume // 1000) + " K"
        else:
            volume = str(volume)


        # Extracting specific details
        formatted_data = {
            'updatedAt': updated_at,
            'symbol': market_data['symbol'],
            'lastPrice': "$ " + market_data['lastPrice'],
            'lastPriceUpDown': market_data['lastPriceUpDown'],
            'bestBid': "BID " + market_data['bestBid'],
            'bestAsk': "ASK " + market_data['bestAsk'],
            'changePercent': change_percent,
            'highPrice': "HIGH " + market_data['highPrice'],
            'lowPrice': "LOW " + market_data['lowPrice'],
            'volume': "VOL " + volume,
        }
        return formatted_data
    else:
        print(f"Failed to fetch market data for symbol {symbol}")
        return None


