import datetime
from pprint import pprint
from typing import List
import tweepy
from config import TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN

# Twitter API credentials (can be found in https://developer.twitter.com/en/portal/projects-and-apps)
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY, 
    consumer_secret=TWITTER_API_KEY_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    bearer_token=TWITTER_BEARER_TOKEN
)

def get_tweets(cryptocurrency: str, start_time: datetime, end_time: datetime, max_results: int) -> List[tweepy.Tweet]:
    'Get tweets related to a specific cryptocurrency.'
    tweets = client.search_all_tweets(query=cryptocurrency, max_results=max_results, 
                                    #   start_time=start_time, end_time=end_time,
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


def get_recent_tweets(cryptocurrency: str, max_results: int) -> List[tweepy.Tweet]:
    'Get recent tweets related to a specific cryptocurrency.'
    tweets = client.search_recent_tweets(query=cryptocurrency, max_results=max_results, 
                                      tweet_fields=['id', 'text', 'created_at', 'lang'])
    return tweets.data


if __name__ == '__main__':
    tweets = get_tweets('bitcoin', datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31), 10)
    pprint(tweets)