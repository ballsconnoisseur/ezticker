import ez_api
from datetime import datetime

def format_price(price):
    price_str = str(price)
    if '.' in price_str:
        integer_part, decimal_part = price_str.split(".")
        # Remove trailing zeros
        decimal_part_trimmed = decimal_part.rstrip('0')
        # If decimal part becomes empty after trimming, remove the dot
        if decimal_part_trimmed:
            return f"{integer_part}.{decimal_part_trimmed}"
        else:
            return integer_part
    return price_str

# Function to format data later inserted into widget.
def format_market_data(exchange, symbol):
    market_data = ez_api.get_market(exchange, symbol)

    if market_data:
        if exchange == 'okx':
            volumex = market_data['volCcy24h']
            if isinstance(volumex, str):
                volumex = float(volumex)

            if volumex >= 10**9:
                volumex = "{:.1f} B".format(volumex / 10**9)
            elif volumex >= 10**6:
                volumex = "{:.1f} M".format(volumex / 10**6)
            elif volumex >= 1000:
                volumex = "{:.1f} K".format(volumex / 1000)
            else:
                volumex = str(volumex)
        else:
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

        if exchange == 'binance':
            closetime_time = datetime.fromtimestamp(market_data['closeTime'] / 1000).strftime('%H:%M:%S')
            formatted_data = {
                'updatedAt': closetime_time,
                'symbol': market_data['symbol'],
                'lastPrice': format_price(market_data['lastPrice']),
                'bestBid': format_price(market_data['bidPrice']),
                'bestAsk': format_price(market_data['askPrice']),
                'highPrice': format_price(market_data['highPrice']),
                'lowPrice': format_price(market_data['lowPrice']),
                'volume': volume + " VOL  ",
            }
            return formatted_data

        elif exchange == 'xeggex':
            updated_at_time = datetime.fromtimestamp(market_data['updatedAt'] / 1000).strftime('%H:%M:%S')
            formatted_data = {
                'updatedAt': updated_at_time,
                'symbol': market_data['symbol'],
                'lastPrice': format_price(market_data['lastPrice']),
                'bestBid': format_price(market_data['bestBid']),
                'bestAsk': format_price(market_data['bestAsk']),
                'highPrice': format_price(market_data['highPrice']),
                'lowPrice': format_price(market_data['lowPrice']),
                'volume': volume + " VOL  ",
            }
            return formatted_data
        
        elif exchange == 'okx':
            ts_time = datetime.fromtimestamp(int(market_data['ts']) / 1000).strftime('%H:%M:%S')
            formatted_data = {
                'updatedAt': ts_time,
                'symbol': market_data['instId'],
                'lastPrice': format_price(market_data['last']),
                'bestBid': format_price(market_data['bidPx']),
                'bestAsk': format_price(market_data['askPx']),
                'highPrice': format_price(market_data['high24h']),
                'lowPrice': format_price(market_data['low24h']),
                'volume': volumex + " VOL  ",
            }
            return formatted_data

        elif exchange == 'coinbase':
            fulltime = (market_data['time'])
            time_time = fulltime[11:19]
            formatted_data = {
                'updatedAt': time_time,
                'symbol': market_data['display_name'],
                'lastPrice': format_price(market_data['price']),
                'bestBid': format_price(market_data['bid']),
                'bestAsk': format_price(market_data['ask']),
                'highPrice': format_price(market_data['high']),
                'lowPrice': format_price(market_data['low']),
                'volume': volume + " VOL  ",
            }
            return formatted_data

        else:
            print(f"R- Failed to fetch market data for symbol {symbol}")
            return None