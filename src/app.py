from unicodedata import name
import streamlit as st
from extract_data import get_market_chart, get_coin_info
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.title('Cryptocurrency App')

with st.sidebar:
    _, coin_symb, _ = get_coin_info()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data')
    
if show_data:
    data = get_market_chart(coin_symb, days)
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], name='Price (USD)'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_caps'], name='Market Cap (USD)'), 
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=data['dates'], y=data['total_volumes'], name='Total Volume (USD)'), 
                  row=3, col=1)
    fig.update_layout(height=1200, width=800, 
                      title_text=f"Price, Market Cap and Total Volume of {coin_symb.upper()}")
    st.plotly_chart(fig)
    