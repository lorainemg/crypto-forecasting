import json
import pandas as pd
from extract_data import get_market_chart

from metrics import calculate_cma, calculate_ema, calculate_macd_oscilators, calculate_mom, calculate_rsi, calculate_sma


def get_data_metrics(data: pd.DataFrame, window: int) -> pd.DataFrame:
    data['sma'] = calculate_sma(data.prices, period=window)
    data['cma'] = calculate_cma(data.prices, period=window)
    data['ema'] = calculate_ema(data.prices, period=window)
    data['macd'], data['signal'], data['histogram'] = calculate_macd_oscilators(data.prices)
    data['rsi'] = calculate_rsi(data.prices, period=window)
    data['mom'] = calculate_mom(data.prices, period=window)
    return data

def load_df(file_name: str) -> pd.DataFrame:
    'Load json file to a dataframe'
    with open(file_name, 'r', encoding='utf-8') as inp:
        info = json.load(inp)
        return pd.DataFrame(info)
    
    
def save_df(df: pd.DataFrame, file_name):
        'Save tweets in a json file.'
        if 'created_at' in df:
            df['created_at'] = df['created_at'].astype(str)
        info = df.to_dict()
        with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
            json.dump(info, out, ensure_ascii=False)
    
    
if __name__ == '__main__':
    data = get_market_chart('btc', 1)
    get_data_metrics(data, 10)