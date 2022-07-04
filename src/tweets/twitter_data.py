import time
from typing import List

import pandas as pd
from config import *

import datetime
import tweepy
import json


# Twitter API credentials (can be found in https://developer.twitter.com/en/portal/projects-and-apps)
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY, 
    consumer_secret=TWITTER_API_KEY_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    bearer_token=TWITTER_BEARER_TOKEN
)


def get_recent_tweets(cryptocurrency: str, days: int):
    'Get tweets of the last days related to a specifuc cryptocurrency'
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=days)
    return get_tweets(cryptocurrency, max_results=None, start_time=start_time, end_time=end_time)


def get_tweets(cryptocurrency: str, max_results: int=None, start_time: datetime = None, end_time: datetime = None) -> List[tweepy.Tweet]:
    'Get tweets related to a specific cryptocurrency.'
    tweets = client.search_all_tweets(query=cryptocurrency, 
                                      start_time=start_time, end_time=end_time,
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


def get_last_tweets(cryptocurrency: str, max_results: int) -> List[tweepy.Tweet]:
    'Get recent tweets related to a specific cryptocurrency.'
    tweets = client.search_recent_tweets(query=cryptocurrency, max_results=max_results, 
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


def save_tweets(tweets: List[tweepy.Tweet], save_file: str):
    'Save tweets in a dataframe format in a json file.'
    tweets_data = [t.data for t in tweets]
    df = pd.DataFrame.from_records(tweets_data)
    with open(save_file, 'w', encoding='utf-8') as out:
        json.dump(df.to_dict(), out, ensure_ascii=False)
    

def download_tweets(coin_names: list):
    idx = 0
    while idx < len(coin_names):
        coin_name = coin_names[idx]
        try:
            tweets = get_tweets(coin_name, start_time=datetime.datetime(2018, 1, 1), end_time=datetime.datetime(2022, 1, 1))
            save_tweets(tweets, f'src/data/twitter_data/{coin_name}.json')
            idx += 1
        except Exception as e:
            time.sleep(2)
            print(e)
        

if __name__ == '__main__':
    coin_names = ['bitcoin', 'ethereum', 'tether', 'USD Coin', 'Binance Coin', 'Binance USD', 
                  'XRP', 'Cardano', 'Solana', 'Dogecoin', 'Dai', 'Polkadot', 'smooth love potion', 'slp']
    download_tweets(coin_names)