from pprint import pprint
from typing import List
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


def get_tweets(cryptocurrency: str, max_results: int, start_time: datetime = None, end_time: datetime = None) -> List[tweepy.Tweet]:
    'Get tweets related to a specific cryptocurrency.'
    tweets = client.search_all_tweets(query=cryptocurrency, max_results=max_results, 
                                      start_time=start_time, end_time=end_time,
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


def get_recent_tweets(cryptocurrency: str, max_results: int) -> List[tweepy.Tweet]:
    'Get recent tweets related to a specific cryptocurrency.'
    tweets = client.search_recent_tweets(query=cryptocurrency, max_results=max_results, 
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


def save_tweets(tweets: List[tweepy.Tweet]):
    'Save tweets in a json file.'
    tweets_data = [t.data for t in tweets]
    with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
        json.dump(tweets_data, out, ensure_ascii=False)
    

if __name__ == '__main__':
    tweets = get_tweets('bitcoin', 30, datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31))
    save_tweets(tweets)