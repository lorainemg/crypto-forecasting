import pandas as pd
from extract_data import get_market_chart

from metrics import calculate_sma


def get_data_metrics(data: pd.Dataframe):
    result = calculate_sma(data.prices, period=10)
    
    
if __name__ == '__main__':
    data = get_market_chart('btc', 1)
    get_data_metrics(data)