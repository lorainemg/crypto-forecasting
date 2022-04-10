import streamlit as st
from extract_data import get_market_chart, get_coin_info
from plots import plot_macd, plot_moving_averages, plot_simple_data

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

    data_fig = plot_simple_data(data, coin_symb)
    st.plotly_chart(data_fig)
    
    data = get_data_metrics(data, 10)
    averages_fig = plot_moving_averages(data)
    st.plotly_chart(averages_fig)
    
    macd_fig = plot_macd(data)
    st.plotly_chart(macd_fig)
    