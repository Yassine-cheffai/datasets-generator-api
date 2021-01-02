import time
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import tweepy as tw
import praw
from models import TwitterRequest, RedditRequest
from helpers import unpack_tweet, unpack_submission

load_dotenv()

app = FastAPI()

origins = [
    "https://datasets-generator.herokuapp.com",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/twitter/")
def build_twitter(request: TwitterRequest):

    auth = tw.OAuthHandler(
        os.getenv("TWITTER_CONSUMER_KEY"),
        os.getenv("TWITTER_CONSUMER_SECRET"),
    )

    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )

    api = tw.API(auth, wait_on_rate_limit=True)
    query = "#" + request.keywords

    # remove retweets: to be deleted probably
    if request.retweets is False:
        query += " -filter:retweets"

    if request.polarity:
        request.csv_fields.append("polarity")

    tweets = tw.Cursor(api.search, q=query).items()

    # lang, created_at, author.screen_name, text, retweet_count
    data = []
    max_time = time.time() + 20
    for tweet in tweets:
        if time.time() <= max_time:
            data.append(unpack_tweet(tweet, request))
        else:
            break

    data.insert(0, request.csv_fields)

    return {"result": data}


@app.post("/reddit/")
def build_reddit(request: RedditRequest):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="web:datasets-generator",
    )
    results = []
    if request.search_type == "specific_subreddit":
        submissions = reddit.subreddit(request.keywords).new(limit=None)
        for submission in submissions:
            results.append(unpack_submission(submission, request))
    else:
        submissions = reddit.subreddit("all").search(request.keywords)
        for submission in submissions:
            results.append(unpack_submission(submission, request))
    results.insert(0, request.csv_fields)
    return {"result": results}
