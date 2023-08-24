import ez_api
from datetime import datetime

def format_price(price):
    price_str = str(price)
    if '.' in price_str:
        integer_part, decimal_part = price_str.split(".")
        leading_zeros_count = len(decimal_part) - len(decimal_part.lstrip('0'))
        if leading_zeros_count > 3:
            compact_decimal = decimal_part.lstrip('0')
            return f"{integer_part}.0({leading_zeros_count}){compact_decimal}"
    return price_str

def format_market_data(symbol):
    market_data = ez_api.get_market_by_symbol(symbol)

    if market_data:
        # Convert updatedAt to time format
        updated_at = datetime.fromtimestamp(market_data['updatedAt'] / 1000).strftime('%H:%M:%S')

        # Add "%" to changePercent
        change_percent = str(market_data['changePercent']) + " %"

        volume = market_data['volume']
        if isinstance(volume, str):
            volume = float(volume)

        if volume >= 10**9:
            volume = "{:.1f} B".format(volume / 10**9)
        elif volume >= 10**6:
            volume = "{:.1f} M".format(volume / 10**6)
        elif volume >= 1000:
            volume = "{:.1f} K".format(volume / 1000)
        else:
            volume = str(volume)



        # Extracting specific details
        formatted_data = {
            'updatedAt': updated_at,
            'symbol': market_data['symbol'],
            'lastPrice': "$ " + format_price(market_data['lastPrice']),
            'lastPriceUpDown': market_data['lastPriceUpDown'],
            'bestBid': "BID " + format_price(market_data['bestBid']),
            'bestAsk': "ASK " + format_price(market_data['bestAsk']),
            'changePercent': change_percent,
            'highPrice': "HIGH " + format_price(market_data['highPrice']),
            'lowPrice': "LOW " + format_price(market_data['lowPrice']),
            'volume': "VOL " + volume,
        }
        return formatted_data
    else:
        print(f"R- Failed to fetch market data for symbol {symbol}")
        return None


