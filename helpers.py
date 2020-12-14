from datetime import datetime
import re
from textblob import TextBlob
import tweepy as tw
from models import TwitterRequest, RedditRequest


def remove_urls(txt: str) -> str:
    return re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt)


def unpack_tweet(tweet: tw.Cursor, request: TwitterRequest) -> list:

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


def unpack_submission(submission, request: RedditRequest) -> list:
    result = []
    for field in request.csv_fields:
        if field == "title":
            result.append(submission.title)
        if field == "selftext":
            result.append(submission.selftext)
        if field == "num_comments":
            result.append(submission.num_comments)
        if field == "created_utc":
            result.append(datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d"))
        if field == "author":
            if submission.author:
                result.append(submission.author.name)

    return result
