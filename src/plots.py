import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

layout = go.Layout(
    # Font Families
    font_family='Monospace',
    font_size=15,
    xaxis=dict(
        rangeslider=dict(
            visible=False
        )
    ))

def plot_simple_data(data: pd.DataFrame, coin_symb: str):
    'Plots data from coingecko'
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)', legendgroup='1'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_caps'], name='Market Cap (USD)', legendgroup='2'), 
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['total_volumes'], name='Total Volume (USD)', legendgroup='3'), 
                  row=3, col=1)
    fig.update_layout(layout, height=1600, width=1000, 
                      title_text=f"Price, Market Cap and Total Volume of {coin_symb.upper()}")
    return fig

def plot_moving_averages(data: pd.DataFrame):
    'Plots moving averages in Plotly'
    fig = go.Figure(layout_title_text="Moving Averages")
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma'], name='SMA (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['cma'], name='CMA (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['ema'], name='EMA (USD)'))
    fig.update_layout(layout, height=600, width=1100)
    return fig

def plot_macd(data: pd.DataFrame):
    'Plot MACD information in Plotly'
    fig = go.Figure(layout_title_text="MACD")
    # fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['macd'], name='MCAD',
                             line=dict(color='#ff9900', width=2)))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['signal'], name='Signal', 
                             line=dict(color='blue', width=2)))
    # Colorize the histogram values
    colors = np.where(data['convergence-value'] < 0, 'blue', '#ff9900')
    fig.add_trace(go.Bar(x=data['dates'], y=data['convergence-value'], name='Histogram',
                         marker_color=colors))
    fig.update_layout(layout, height=600, width=1100)

    return fig


    