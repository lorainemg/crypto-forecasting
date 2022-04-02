import streamlit as st
from extract_data import get_coins, get_data


st.title('Cryptocurrency App')

with st.sidebar:
    _, coin_symb, coin_ids = get_coins()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    coin_id = coin_ids[coin_symb.index(coin_symb)]
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data')
    
if show_data:
    data = get_data(coin_id, days)