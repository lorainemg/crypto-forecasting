import pandas as pd
import re

class TweetsPreprocessing:
    def __call__(self, tweets: pd.Dataframe) -> pd.DataFrame:
        tweets = self.remove_urls(tweets)
        print(tweets)
        
    def remove_urls(tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the url of a list of tweets'
        return tweets.apply(lambda x: re.sub(r'https?://[^ ]+', '', x.text))
    
    def remove_usernames(tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the usernames of a list of tweets'
        return tweets.apply(lambda x: re.sub(r'@[^ ]+', '', x.text))
    
    def deal_with_hashtags(tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the character # to deal with hashtags'
        return tweets.apply(lambda x: re.sub(r'#', '', x.text))

    def character_normalization(tweets: pd.DataFrame) -> pd.DataFrame:
        'Fix some uregurarly written words'
        # removes letters written more than one time (too simple)
        return tweets.apply(lambda x: re.sub(r'([A-Za-z])\1{2,}', r'\1', x.text))

    def remove_special_characters(tweets: pd.DataFrame) -> pd.DataFrame:
        'Remove punctuation and single characters'
        def sub_special_char(tweet_text):
            tweet_text = re.sub(r' 0 ', 'zero', tweet_text)
            return re.sub(r'[^A-Za-z ]', '', tweet_text)
        return tweets.apply(lambda x: sub_special_char(x.text))

    def to_lower_case(tweets: pd.DataFrame) -> pd.DataFrame:
        'Transforms all capital letters to their lower case equivalent'
        return tweets.apply(lambda x: x.text.lower())


if __name__ == '__main__':
    pass