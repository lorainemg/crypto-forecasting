from ast import List
from flair.models import TextClassifier
from flair.data import Sentence

import tweepy


def sentiment_analysis_flair(twitter_data: List[tweepy.Tweet]):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence('The food was not great!')
    classifier.predict(sentence)
    print('Sentence above is: ', sentence.labels)
    

if __name__ == '__main__':
    
    sentiment_analysis_flair()