from matplotlib.pyplot import colorbar
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
    fig.update_layout(layout, height=1600, width=1100, 
                      title_text=f"Price, Market Cap and Total Volume of {coin_symb.upper()}")
    return fig


def plot_moving_averages(data: pd.DataFrame):
    'Plots moving averages in Plotly'
    fig = go.Figure(layout_title_text="Moving Averages")
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)',
                             line=dict(width=2)))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma'], name='SMA (USD)',
                             line=dict(width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['cma'], name='CMA (USD)',
                             line=dict(width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['ema'], name='EMA (USD)',
                             line=dict(width=2, dash='dot')))
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
    colors = np.where(data['histogram'] < 0, 'blue', '#ff9900')
    fig.add_trace(go.Bar(x=data['dates'], y=data['histogram'], name='Histogram',
                         marker_color=colors))
    fig.update_layout(layout, height=600, width=1100)
    return fig


def plot_other_oscillators(data: pd.DataFrame):
    'Plot RSI and MOM'
    fig = go.Figure(layout_title_text="Other Oscillators")
    # fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['rsi'], name='RSI'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['mom'], name='MOM'))
    fig.update_layout(layout, height=600, width=1100)    
    return fig


def plot_sentiment_analysis(data: pd.DataFrame):
    'Plots sentiment analysis information in a Scatter Plot'
    fig = go.Figure(layout_title_text='Sentiment Analysis Scatter Chart')
    fig.add_trace(go.Scatter(x=data['created_at'], y=data['sentiment_score'],
                             mode='markers', text=data['text'], 
                             
                             marker=dict(
                                 color=data['sentiment_score'],
                                 cmax=1,
                                 cmin=-1, 
                                 colorscale=px.colors.sequential.RdBu,
                                 colorbar=dict(title='Sentiment Score'))))
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_layout(layout, height=600, width=1100)
    return fig


def plot_sentiment_pie(data: pd.DataFrame):
    'Plots Sentiment analysis information in Pie Chart'
    counts = data.value_counts('sentiment')
    fig = go.Figure(layout_title_text='Sentiment Analysis Pie Chart')
    fig.add_trace(go.Pie(values=counts.values, labels=counts.keys()))
    fig.update_layout(layout, height=600, width=1000)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
    return fig

def plot_sentiment_count(df: pd.DataFrame):
    'Plots sentiment analysis line chart'
    fig = go.Figure(layout_title_text='Sentiment Analysis Line Chart')
    grouped_df = df.groupby(df.created_at)['created_at'].count().rename('count').reset_index()
    fig.add_trace(go.Scatter(x=grouped_df['created_at'], y=grouped_df['count'], name='Amounts of Tweets'))
    