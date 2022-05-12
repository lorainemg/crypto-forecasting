import json
import pandas as pd


def load_tweets(file_name: str) -> pd.DataFrame:
    'Load tweets to a dataframe'
    with open(file_name, 'r', encoding='utf-8') as inp:
        tweets = json.load(inp)
        return pd.DataFrame(tweets)
    
    
def save_tweets(df: pd.DataFrame):
        'Save tweets in a json file.'
        df['created_at'] = df['created_at'].astype(str)
        tweets = df.to_dict()
        with open('src/data/tweets.json', 'w', encoding='utf-8') as out:
            json.dump(tweets, out, ensure_ascii=False)
    