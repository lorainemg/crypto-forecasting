from datetime import datetime
import json
import streamlit as st
from extract_data import get_market_chart, get_coin_info
from plots import plot_macd, plot_moving_averages, plot_other_oscillators, plot_simple_data
from sentiment_analyzer import SentimentAnalyzer
from twitter_data import get_recent_tweets

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
    tweets = json.load(open('src/data/tweets.json', 'r'))
    sent_analyzer = SentimentAnalyzer()
    tweets = sent_analyzer.predict(tweets)
    df = sent_analyzer.convert_tweets_to_df(tweets)
    
    

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
# elif show_tweets:

if __name__ == '__main__':
    plot_twitter_info('btc', 10)
    
    