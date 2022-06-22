"Several metrics for the analysis of time-series data are implemented"
import pandas as pd
from typing import Tuple 

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


def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
    'Calculate Simple Moving Average'
    return prices.rolling(window=period).mean()

def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
    'Calculate Exponential Moving Average'
    return prices.ewm(span=period, adjust=False, min_periods=period).mean()

def calculate_cma(prices: pd.Series, period: int) -> pd.Series:
    'Calculate Cumulative Moving Average'
    return prices.expanding(min_periods=period).mean()

def calculate_macd_oscilators(prices: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
    'Calculate Moving Average Convergence Divergence'
    short_ema = calculate_ema(prices, 12)
    long_ema = calculate_ema(prices, 26)
    macd = short_ema - long_ema
    
    # get the 9-day EMA of the MACD from the trigger line
    signal = calculate_ema(macd, 9)
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    conv_val = macd - signal
    return macd, signal, conv_val

def calculate_rsi(prices: pd.Series, period: int) -> pd.Series:
    'Calculate Relative Strength Index'
    delta = prices.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=period).mean()
    roll_down = down.abs().rolling(window=period).mean()
    rsi = 100 - (100 / (1 + roll_up / roll_down))
    return rsi

def calculate_mom(prices: pd.Series, period: int) -> pd.Series:
    'Calculate Momentum'
    return prices.diff(period)

    