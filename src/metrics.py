"Several metrics for the analysis of time-series data are implemented"
from this import d
import numpy as np
import pandas as pd

# def calculate_sma(prices: list, period: int) -> list:
#     'Simple moving average'
#     return[sum(prices[i:i+period]) / period for i in range(len(prices) - period + 1)]

# def calculate_ema(prices: list, period: int, smothing:int=2) -> list:
#     'Exponential moving average'
#     ema = [sum(prices[:period]) / period]
#     smothing = smothing / (1 + period)
#     for price in prices[period:]:
#         ema.append((price * smothing)) + (ema[-1] * (1 - smothing))
#     return ema


def calculate_sma(prices: pd.Series, period: int) -> list:
    'Calculate Simple Moving Average'
    return prices.rolling(window=period).mean()

def calculate_ema(prices: pd.Series, period: int) -> list:
    'Calculate Exponential Moving Average'
    return prices.ewm(span=period, adjust=False, min_periods=period).mean()

def calculate_cma(prices: pd.Series, period: int) -> list:
    'Calculate Cumulative Moving Average'
    return prices.expanding(min_periods=period).mean()

def calculate_macd_oscilators(prices: pd.Series):
    short_ema = calculate_ema(prices, 12)
    long_ema = calculate_ema(prices, 26)
    macd = short_ema - long_ema
    
    # get the 9-day EMA of the MACD fron the trigger line
    trigger_line = calculate_ema(macd, 9)
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    conv_val = macd - trigger_line
    return macd, trigger_line, conv_val


    