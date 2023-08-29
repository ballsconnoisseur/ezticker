import ez_api_xeggex_getlist as xeggex
import ez_api_binance_getlist as binance
import ez_api_okx_getlist as okx
import ez_api_coinbase_getlist as coinbase


def get_all():
    xeggex.get_market_list_xeggex
    binance.get_market_list_binance
    okx.get_market_list_okx
    coinbase.get_market_list_coinbase
    print("Successfully optained all possible pair data!")