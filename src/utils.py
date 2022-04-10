import pandas as pd
from extract_data import get_market_chart

from metrics import calculate_cma, calculate_ema, calculate_macd_oscilators, calculate_mom, calculate_rsi, calculate_sma


def get_data_metrics(data: pd.DataFrame, window: int) -> pd.DataFrame:
    data['sma'] = calculate_sma(data.prices, period=window)
    data['cma'] = calculate_cma(data.prices, period=window)
    data['ema'] = calculate_ema(data.prices, period=window)
    data['macd'], data['signal'], data['convergence-value'] = calculate_macd_oscilators(data.prices)
    data['rsi'] = calculate_rsi(data.prices, period=window)
    data['mom'] = calculate_mom(data.prices, period=window)
    return data
    
if __name__ == '__main__':
    data = get_market_chart('btc', 1)
    get_data_metrics(data, 10)