from typing import List
from flair.models import TextClassifier
from flair.data import Sentence

import json

class SentimentAnalyzer:
    '''Sentiment analyzer that uses Flair as background to analyze tweets'''
    def __init__(self) -> None:
        self.classifier = TextClassifier.load('en-sentiment')
        
    def preprocess_tweets(self, twitter_data: List[dict]):
        'Proprocess tweets from Twitter'
        tweets = [t for t in twitter_data if t['lang'] == 'en']
        sentences = [Sentence(tweet['text']) for tweet in twitter_data] 
        return tweets, sentences
        
    def predict(self, twitter_data: List[dict]):
        'Predict Sentiment Analysis from Twitter and return the sentences with the labels'
        tweets, sentences = self.preprocess_tweets(twitter_data)
        self.classifier.predict(sentences, mini_batch_size=32)
        tweets = self.add_labels_data(tweets, sentences)
        return tweets
    
    def add_labels_data(self, twitter_data: List[dict], sentences: List[Sentence]):
        'Add information of the sentiment analysis labels to the tweets'
        for idx in range(len(twitter_data)):
            twitter_data[idx] = {**twitter_data[idx], 
                                 'sentiment': sentences[idx].labels[0].value,
                                 'sentiment_score': sentences[idx].labels[0].score}
        return twitter_data
    
    def save_tweets(self, tweets: List[dict]):
        'Save tweets in a json file.'
        with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
            json.dump(tweets, out, ensure_ascii=False)
    
    
if __name__ == '__main__':
    sa = SentimentAnalyzer()
    tweets = json.load(open('src/data/tweets.json'))
    tweets = sa.predict(tweets)
    sa.save_tweets(tweets)
    print(tweets)
    
        
        