from typing import List
import os
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from pydantic import BaseModel
import tweepy as tw
import pandas as pd
from textblob import TextBlob

load_dotenv()

app = FastAPI()

origins = [
    "https://twitter-datasets-builder.herokuapp.com",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Request(BaseModel):
    keywords: str
    csv_fields: List[str] = ["text"]
    since: str  # date format : YYYY-MM-DD
    polarity: bool = False
    retweets: bool = False
    remove_urls: bool = False


def remove_urls(txt: str) -> str:
    return re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt)


def unpack(tweet: tw.Cursor, request: Request) -> list:

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

    return result


@app.post("/")
def build(request: Request):

    auth = tw.OAuthHandler(
        os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"),
    )

    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )

    api = tw.API(auth, wait_on_rate_limit=True)
    query = "#" + request.keywords

    # remove retweets
    if request.retweets is False:
        query += " -filter:retweets"

    if request.polarity:
        request.csv_fields.append("polarity")

    tweets = tw.Cursor(api.search, q=query, since=request.since).items()

    # lang, created_at, author.screen_name, text, retweet_count

    data = [unpack(tweet, request) for tweet in tweets]

    data_frame = pd.DataFrame(data, columns=request.csv_fields)
    data_frame.head()

    data.insert(0, request.csv_fields)

    print(data_frame)

    return {"result": data}
