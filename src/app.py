import numpy as np
import streamlit as st
from extract_data import get_market_chart, get_coin_info
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from utils import get_data_metrics

st.set_page_config(layout='wide')
st.title('Cryptocurrency App')

with st.sidebar:
    _, coin_symb, _ = get_coin_info()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data')
    
if show_data:
    st.subheader('Market charts')
    
    data = get_market_chart(coin_symb, days)
    layout = go.Layout(
    # Font Families
    font_family='Monospace',
    font_size=20,
    xaxis=dict(
        rangeslider=dict(
            visible=False
        )
    )
    )
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)', legendgroup='1'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_caps'], name='Market Cap (USD)', legendgroup='2'), 
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['total_volumes'], name='Total Volume (USD)', legendgroup='3'), 
                  row=3, col=1)
    fig.update_layout(layout, height=1600, width=1000, 
                      title_text=f"Price, Market Cap and Total Volume of {coin_symb.upper()}")
    st.plotly_chart(fig)
    
    data = get_data_metrics(data, 3)
    
    fig = go.Figure(layout_title_text="Moving Averages")
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma'], name='SMA (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['cma'], name='CMA (USD)'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['ema'], name='EMA (USD)'))
    fig.update_layout(layout, height=600, width=1100)
    st.plotly_chart(fig)
    
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

    # fig.update_layout(height=600, width=1100)
    
    # fig = go.Figure(layout_title_text="Oscilators")
    # fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)'))
    # fig.add_trace(go.Scatter(x=data['dates'], y=data['rsi'], name='Relative Strength Index (USD)'))
    # fig.add_trace(go.Scatter(x=data['dates'], y=data['mom'], name='Momentum (USD)'))
    fig.update_layout(layout, height=600, width=1100)
    
    st.plotly_chart(fig)
    
    