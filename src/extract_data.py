import time
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from typing import Tuple, List
import pandas as pd
import json
from utils import save_df

cg = CoinGeckoAPI()

def get_coins() -> Tuple[List[str], List[str], List[str]]:
    'Get coins from coingecko and separetes them in 3 lists: names, symbols and ids'
    coins = cg.get_coins_list()
    names, symbols, ids = [], [], []
    for coins_info in coins:
        names.append(coins_info['name'])
        symbols.append(coins_info['symbol'])
        ids.append(coins_info['id']) 
    return names, symbols, ids

    
def save_coin_info():
    'Save coin info in a json file'
    name, symbols, ids = get_coins()
    coin_info =  {'names': name, 'symbols': symbols, 'ids': ids}
    json.dump(coin_info, open('src/data/coin_info.json', 'w+'))
    
    
def get_coin_info() -> Tuple[List[str], List[str], List[str]]:
    'Get coin info from the saved json file'
    coin_info = json.load(open('src/data/coin_info.json'))
    return coin_info['names'], coin_info['symbols'], coin_info['ids']
    
    
def get_market_chart(coin: str, days: int) -> dict:
    'Get the market chart of a coin for a specific number of days'
    _, symbols, ids = get_coin_info()
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
    return pd.DataFrame(info)
        

def get_market_chart_range(coin: str, date_from: datetime, date_to: datetime) -> dict:
    'Get the market chart of a coin for a specific date range'
    _, symbols, ids = get_coin_info()
    try:
        coin_id = ids[symbols.index(coin)]
    except ValueError:
        raise Exception('Coin not found')
    info = cg.get_coin_market_chart_range_by_id(coin_id, vs_currency='usd',
                                                from_timestamp=date_from.timestamp(),
                                                to_timestamp=date_to.timestamp())
    timestamps = [t / 1000 for t, _ in info['prices']]
    info['dates'] = [datetime.utcfromtimestamp(t).isoformat() for t in timestamps]
    
    info['prices'] = [p for _, p in info['prices']]
    info['market_caps'] = [m for _, m in info['market_caps']]
    info['total_volumes'] = [t for _, t in info['total_volumes']]
    return pd.DataFrame(info)
    
def download_data(coins: list):
    idx = 0
    while idx < len(coins):
        coin = coins[idx]
        try:
            df = get_market_chart_range(coin, datetime(2018, 1, 1), datetime(2022, 1, 1))
            save_df(df, f'src/data/{coin}.json')
            idx += 1
        except:
            time.sleep(60)
    
if __name__ == '__main__':
    coins = ['btc', 'eth', 'usdt', 'usdc', 'bnb', 'busd', 'xrp', 'ada', 'sol', 'doge', 'dai', 'dot', 'slp']
    download_data(coins)