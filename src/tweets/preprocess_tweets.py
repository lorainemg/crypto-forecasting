import pandas as pd
import re

class TweetsPreprocessing:
    def __call__(self, tweets: pd.DataFrame) -> pd.DataFrame:
        tweets['raw_text'] = pd.Series(tweets['text'])
        tweets = self.remove_urls(tweets)
        tweets = self.remove_usernames(tweets)
        tweets = self.deal_with_hashtags(tweets)
        tweets = self.character_normalization(tweets)
        tweets = self.remove_special_characters(tweets)
        return self.to_lower_case(tweets)
        
    def remove_urls(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the url of a list of tweets'
        tweets['text'] = tweets['text'].apply(lambda x: re.sub(r'https?://[^ ]+', '', x))
        return tweets
    
    def remove_usernames(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the usernames of a list of tweets'
        tweets['text'] = tweets.text.apply(lambda x: re.sub(r'@[^ ]+', '', x))
        return tweets
    
    def deal_with_hashtags(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the character # to deal with hashtags'
        tweets['text'] = tweets.text.apply(lambda x: re.sub(r'#', '', x))
        return tweets

    def character_normalization(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Fix some uregurarly written words'
        # removes letters written more than one time (too simple)
        tweets['text'] = tweets.text.apply(lambda x: re.sub(r'#', '', x))
        return tweets

    def remove_special_characters(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Remove punctuation and single characters'
        def sub_special_char(tweet_text):
            tweet_text = re.sub(r' 0 ', 'zero', tweet_text)
            return re.sub(r'[^A-Za-z ]', '', tweet_text)
        tweets['text'] = tweets.text.apply(lambda x: sub_special_char(x))
        return tweets

    def to_lower_case(self, tweets: pd.DataFrame) -> pd.DataFrame:
        'Transforms all capital letters to their lower case equivalent'
        tweets['text'] = tweets.text.apply(lambda x: x.lower())
        return tweets