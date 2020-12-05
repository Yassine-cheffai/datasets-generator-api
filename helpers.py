import re
from textblob import TextBlob
import tweepy as tw
import praw
from models import TwitterRequest, RedditRequest


def remove_urls(txt: str) -> str:
    return re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt)


def unpack(tweet: tw.Cursor, request: TwitterRequest) -> list:

    result = []

    for field in request.csv_fields:
        if field == "lang":
            result.append(tweet.lang)
        if field == "created_at":
            result.append(tweet.created_at)
        if field == "author":
            result.append(tweet.author.screen_name)
        if field == "text":
            if request.remove_urls:
                result.append(remove_urls(tweet.text))
            else:
                result.append(tweet.text)
        if field == "retweet_count":
            result.append(tweet.retweet_count)
        if field == "polarity":
            polarity = TextBlob(tweet.text).polarity
            result.append(polarity)

    print(f"processing {result}")
    return result

def build_specific_subreddit(request: RedditRequest):
    subreddit_name = request.keywords
    reddit = praw.Reddit(client_id="cf1WIz3lBN8bBA",
                         client_secret="HMdgpBj3tNRn_iPN2hd1VU9Qqf95zQ",
                         user_agent="web:datasets-generator")
    subreddit = reddit.subreddit(subreddit_name)
