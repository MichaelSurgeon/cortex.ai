from datetime import datetime

from pydantic import BaseModel, HttpUrl


class FeedPost(BaseModel):
    id: str
    title: str
    author: str
    url: HttpUrl
    created_at: datetime
    clean_body_text: str
    source: str
    summary: str | None = None
    is_relevant: bool = True


class FeedPostResponse(BaseModel):
    id: str
    title: str
    author: str
    url: HttpUrl
    created_at: datetime
    source: str
    summary: str
