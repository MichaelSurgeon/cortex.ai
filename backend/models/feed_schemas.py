from datetime import datetime

from pydantic import BaseModel, HttpUrl


class FeedPost(BaseModel):
    id: str
    title: str
    author: str
    url: HttpUrl
    created_at: datetime
    source: str
    clean_body_text: str
    generated_title: str | None = None
    category: str | None = None
    confidence: float | None = None
    summary_engineer: str | None = None
    summary_enthusiast: str | None = None


class FeedPostResponse(FeedPost):
    """API response model — summaries are guaranteed to be present after processing."""

    summary_engineer: str = ""
    summary_enthusiast: str = ""
