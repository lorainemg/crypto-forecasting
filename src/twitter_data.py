import datetime
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

def get_tweets(cryptocurrency: str, start_time: datetime, end_time: datetime, max_results: int) -> List[dict]:
    '''
    Get tweets related to a specific cryptocurrency.
    
    Example of the response:
    {
        "data": [{
            "id": "1373001119480344583",
            "text": "Looking to get started with the Twitter API but new to APIs in general? @jessicagarson will walk you through everything you need to know in APIs 101 session."
            "created_at": "2020-12-18T17:09:57.000Z"
        }],
        "meta": {
            "newest_id": "1373001119480344583",
            "oldest_id": "1364275610764201984",
            "result_count": 6
        }
    }
    '''
    tweets = client.search_all_tweets(query=cryptocurrency, lang='en', max_results=max_results, 
                                      start_time=start_time, end_time=end_time,
                                      tweet_fields=['id', 'text', 'created_at'])
    return tweets.json()


def get_recent_tweets(cryptocurrency: str, max_results: int):
    ''''
    Get recent tweets related to a specific cryptocurrency.
    
    Example of the response:
    {
        "data": [{
            "id": "1373001119480344583",
            "text": "Looking to get started with the Twitter API but new to APIs in general? @jessicagarson will walk you through everything you need to know in APIs 101 session."
            "created_at": "2020-12-18T17:09:57.000Z"
        }],
        "meta": {
            "newest_id": "1373001119480344583",
            "oldest_id": "1364275610764201984",
            "result_count": 6
        }
    }
    '''
    tweets = client.search_recent_tweets(query=cryptocurrency, lang='en', max_results=max_results, 
                                      tweet_fields=['id', 'text', 'created_at'])
    return tweets.json()