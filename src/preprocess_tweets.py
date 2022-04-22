from ast import List
from flair.models import TextClassifier
from flair.data import Sentence

import tweepy
import json


def sentiment_analysis_flair(twitter_data: List[dict]):
    classifier = TextClassifier.load('en-sentiment')
    for tweet in twitter_data:
        if tweet['lang'] != 'en':
            continue
        txt = tweet['text']
    sentence = Sentence('The food was not great!')
    classifier.predict(sentence)
    print('Sentence above is: ', sentence.labels)
    

if __name__ == '__main__':
    tweets = json.load(open('src/data/tweets.json'))
    sentiment_analysis_flair(tweets)