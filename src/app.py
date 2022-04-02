import streamlit as st
from extract_data import get_coins, get_data
import plotly.express as px
import plotly.graph_objects as go

st.title('Cryptocurrency App')

with st.sidebar:
    _, coin_symb, coin_ids = get_coins()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data')
    
if show_data:
    data = get_data(coin_symb, days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['dates'], y=data['prices'], 
                             name='Price', mode='lines'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_caps'], 
                             name='Market Cap', mode='lines'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['total_volumes'], 
                             name='Total Volume', mode='lines'))
    st.plotly_chart(fig)