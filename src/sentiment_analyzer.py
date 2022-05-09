from typing import List
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json
import pandas as pd

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

    
    def save_tweets(self, df: pd.DataFrame):
        'Save tweets in a json file.'
        df['created_at'] = df['created_at'].astype(str)
        tweets = df.to_dict()
        with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
            json.dump(tweets, out, ensure_ascii=False)
    
    def load_tweets(self, file_name: str) -> pd.DataFrame:
        'Load tweets to a dataframe'
        with open(file_name, 'r', encoding='utf-8') as inp:
            tweets = json.load(inp)
            return pd.DataFrame(tweets)
    
if __name__ == '__main__':
    sa = SentimentAnalyzer()
    tweets = sa.load_tweets('src/data/tweets.json')
    df = sa.predict(tweets)
    sa.save_tweets(df)
        
    df = sa.load_tweets('src/data/tweets.json') 
