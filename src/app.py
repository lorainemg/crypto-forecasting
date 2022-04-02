import streamlit as st
from extract_data import get_coins, get_data
import plotly.express as px
from plotly.subplots import make_subplots

st.title('Cryptocurrency App')

with st.sidebar:
    _, coin_symb, _ = get_coins()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data')
    
if show_data:
    data = get_data(coin_symb, days)
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(px.line(data, x='dates', y='prices', title='Price'), row=1, col=1)
    fig.add_trace(px.line(data, x='dates', y='market_caps', title='Market Cap'), row=2, col=1)
    fig.add_trace(px.line(data, x='dates', y='total_volumes', title='Total Volume'), row=3, col=1)
    # fig1 = px.line(data, x='dates', y='market_caps', title='Market Cap', )
    # fig2 = px.line(data, x='dates', y='prices', title='Price')
    # fig3 = px.line(data, x='dates', y='total_volumes', title='Total Volume')
    st.plotly_chart(fig)
    