from typing import List
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json
import pandas as pd

from tweets.utils import load_tweets

class SentimentAnalyzer:
    '''Sentiment analyzer that uses Flair as background to analyze tweets'''
    def __init__(self) -> None:
        self.classifier = SentimentIntensityAnalyzer()
        
    def preprocess_tweets(self, twitter_data: pd.DataFrame):
        'Proprocess tweets from Twitter'
        tweets = twitter_data[twitter_data.lang == 'en']
        sentences = tweets.text
        return tweets, sentences
        
    def predict(self, twitter_data: pd.DataFrame):
        'Predict Sentiment Analysis from Twitter and return the sentences with the labels'
        tweets, sentences = self.preprocess_tweets(twitter_data)
        sentiment_dict = [self.classifier.polarity_scores(sent) for sent in sentences]
        tweets = self.add_labels_data(tweets, sentiment_dict)
        return tweets
    
    def add_labels_data(self, twitter_data: pd.DataFrame, sentiment_dict: List[dict]):
        'Add information of the sentiment analysis labels to the tweets'
        twitter_data['sentiment_neg'] = [sent['neg'] for sent in sentiment_dict]
        twitter_data['sentiment_neu'] = [sent['neu'] for sent in sentiment_dict]
        twitter_data['sentiment_pos'] = [sent['pos'] for sent in sentiment_dict]
        twitter_data['sentiment_score'] = [sent['compound'] for sent in sentiment_dict]
        return twitter_data
    
    def convert_tweets_to_df(self, tweets: List[dict]):
        'Converts the tweets list to a dataframe'
        df = pd.DataFrame.from_records(tweets)
        df['created_at'] = df['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z')) 
        df['sentiment'] = ['Positive' if t['sentiment_score'] >= 0.05 else 'Negative' if t['sentiment_score'] <= -0.05 else 'Neutral'
                                for t in tweets]
        return df

    
if __name__ == '__main__':
    sa = SentimentAnalyzer()
    tweets = load_tweets('src/data/tweets.json')
    df = sa.predict(tweets)
    sa.save_tweets(df)
        
    df = load_tweets('src/data/tweets.json') 
