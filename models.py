from pydantic import BaseModel
from typing import List


class TwitterRequest(BaseModel):
    keywords: str
    csv_fields: List[str] = ["text"]
    polarity: bool = False
    retweets: bool = False
    remove_urls: bool = False


class RedditRequest(BaseModel):
    keywords: str
