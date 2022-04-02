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
    fig1 = px.line(data, x='dates', y='market_caps', title='Market Cap')
    fig2 = px.line(data, x='dates', y='prices', title='Price')
    fig3 = px.line(data, x='dates', y='total_volumes', title='Total Volume')
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)