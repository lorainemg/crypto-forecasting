import pandas as pd
import re

class TweetsPreprocessing:
    def __call__(self, tweets: pd.Dataframe) -> pd.DataFrame:
        tweets = remove_urls(tweets)
        print(tweets)
        
    def remove_urls(tweets: pd.DataFrame) -> pd.DataFrame:
        'Removes the url of a list of tweets'
        return tweets.apply(lambda x: re.sub(r'https?://[^ ]+', '', x.text))
    

if __name__ == '__main__':
    