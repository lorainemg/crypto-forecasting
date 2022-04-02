from cmath import inf
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd

cg = CoinGeckoAPI()

def get_coins():
    'Get coins from coingecko and separetes them in 3 lists: names, symbols and ids'
    coins = cg.get_coins_list()
    names, symbols, ids = [], [], []
    for coins_info in coins:
        names.append(coins_info['name'])
        symbols.append(coins_info['symbol'])
        ids.append(coins_info['id']) 
    return names, symbols, ids
    
    
def get_market_chart(coin: str, days: int):
    'Get the market chart of a coin for a specific number of days'
    _, symbols, ids = get_coins()
    try:
        coin_id = ids[symbols.index(coin)]
    except ValueError:
        raise Exception('Coin not found')
    info = cg.get_coin_market_chart_by_id(coin_id, vs_currency='usd', days=days)
    timestamps = [t / 1000 for t, _ in info['prices']]
    info['dates'] = [datetime.utcfromtimestamp(t) for t in timestamps]
    
    info['prices'] = [p for _, p in info['prices']]
    info['market_caps'] = [m for _, m in info['market_caps']]
    info['total_volumes'] = [t for _, t in info['total_volumes']]
    return info
        

def preprocess_data(coin: str, days: int):
    'Get the market chart of a coin for a specific number of days and preprocess it'
    info = get_market_chart(coin, days)
    df = pd.DataFrame(info)
    print(df.head())
    return df

if __name__ == '__main__':
    info = preprocess_data('btc', 1)
    # print(info)