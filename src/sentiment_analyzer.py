from typing import List
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json
import pandas as pd

class SentimentAnalyzer:
    '''Sentiment analyzer that uses Flair as background to analyze tweets'''
    def __init__(self) -> None:
        self.classifier = SentimentIntensityAnalyzer()
        
    def preprocess_tweets(self, twitter_data: List[dict]):
        'Proprocess tweets from Twitter'
        tweets = [t for t in twitter_data if t['lang'] == 'en']
        sentences = [tweet['text'] for tweet in tweets] 
        return tweets, sentences
        
    def predict(self, twitter_data: List[dict]):
        'Predict Sentiment Analysis from Twitter and return the sentences with the labels'
        tweets, sentences = self.preprocess_tweets(twitter_data)
        sentiment_dict = [self.classifier.polarity_scores(sent) for sent in sentences]
        tweets = self.add_labels_data(tweets, sentiment_dict)
        return tweets
    
    def add_labels_data(self, twitter_data: List[dict], sentiment_dict: List[dict]):
        'Add information of the sentiment analysis labels to the tweets'
        for idx in range(len(twitter_data)):
            twitter_data[idx] = {**twitter_data[idx], 
                                 'sentiment_neg': sentiment_dict[idx]['neg'],
                                 'sentiment_neu': sentiment_dict[idx]['neu'],
                                 'sentiment_pos': sentiment_dict[idx]['pos'],
                                 'sentiment_score': sentiment_dict[idx]['compound']}
        return twitter_data
    
    def convert_tweets_to_df(self, tweets: List[dict]):
        'Converts the tweets list to a dataframe'
        df = pd.DataFrame.from_records(tweets)
        df['created_at'] = df['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z')) 
        df['sentiment'] = ['Positive' if t['sentiment_score'] >= 0.05 else 'Negative' if t['sentiment_score'] <= -0.05 else 'Neutral'
                                for t in tweets]
        return df

    
    def save_tweets(self, tweets: List[dict]):
        'Save tweets in a json file.'
        with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
            json.dump(tweets, out, ensure_ascii=False)
    
    
if __name__ == '__main__':
    sa = SentimentAnalyzer()
    tweets = json.load(open('src/data/tweets.json'))
    tweets = sa.predict(tweets)
    sa.save_tweets(tweets)
    sa.convert_tweets_to_df(tweets)
    # print(tweets)
    
        
        