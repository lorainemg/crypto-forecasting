from datetime import datetime
import json, pandas as pd
import streamlit as st
from extract_data import get_market_chart, get_coin_info
from plots import *
from tweets.sentiment_analyzer import SentimentAnalyzer
from tweets.twitter_data import get_recent_tweets
from tweets.utils import load_tweets

from utils import get_data_metrics

st.set_page_config(layout='wide')
st.title('Cryptocurrency App')

def plot_market_data(coin_symb: str, days: int):
    'Show data of the selected coin in a several number of days'
    st.subheader('Market charts')
    
    data = get_market_chart(coin_symb, days)

    data_fig = plot_simple_data(data, coin_symb)
    st.plotly_chart(data_fig)
    
    data = get_data_metrics(data, 10)
    averages_fig = plot_moving_averages(data)
    st.plotly_chart(averages_fig)
    
    macd_fig = plot_macd(data)
    st.plotly_chart(macd_fig)
    
    oscillators_fig = plot_other_oscillators(data)
    st.plotly_chart(oscillators_fig)


def plot_twitter_info(coin_symb: str, days: int):
    # tweets = get_recent_tweets(coin_symb, days)
    sent_analyzer = SentimentAnalyzer()
    df = load_tweets('src/data/tweets.json')
    df = sent_analyzer.predict(df)

    # df = sent_analyzer.convert_tweets_to_df(tweets)
    sent_plot = plot_sentiment_analysis(df)
    st.plotly_chart(sent_plot)
    
    sent_pie = plot_sentiment_pie(df)
    st.plotly_chart(sent_pie)
    
    sent_line = plot_sentiment_count(df)
    st.plotly_chart(sent_line)
    
    

with st.sidebar:
    _, coin_symb, _ = get_coin_info()
    coin_symb = st.selectbox('Select a coin', coin_symb)
    days = st.number_input('Number of days to get the data', min_value=1, value=1)
    
    show_data = st.button('Show Data', 
                          help='Show data of related to the selected coin')
    show_tweets = st.button('Show Tweets', 
                            help='Show the recent tweets related to the selected coin')
    
if show_data:
    plot_market_data(coin_symb, days)
elif show_tweets:
    plot_twitter_info('btc', 10)