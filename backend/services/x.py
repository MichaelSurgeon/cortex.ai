import logging
from datetime import UTC, datetime

import httpx

from backend.config import GETX_API_KEY
from backend.models.feed_schemas import FeedPost

logger = logging.getLogger(__name__)

GETX_BASE_URL = "https://api.getxapi.com"
SEARCH_QUERY = (
    '"artificial intelligence" OR "machine learning" OR "LLM" lang:en min_faves:50'
)


class XService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=GETX_BASE_URL,
            headers={"Authorization": f"Bearer {GETX_API_KEY}"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    def _parse_tweet(self, tweet: dict) -> FeedPost:
        author = tweet.get("author", {})
        text = tweet.get("text", "")

        return FeedPost(
            id=tweet["id"],
            title=text[:100],
            author=author.get("userName", "Unknown"),
            url=tweet["url"],
            created_at=datetime.strptime(
                tweet["createdAt"], "%a %b %d %H:%M:%S +0000 %Y"
            ).replace(tzinfo=UTC),
            clean_body_text=text,
            source="x",
        )

    async def fetch_all(self) -> list[FeedPost]:
        try:
            response = await self._client.get(
                "/twitter/tweet/advanced_search",
                params={"q": SEARCH_QUERY, "product": "Latest"},
            )
            response.raise_for_status()
            data = response.json()
        except Exception:
            logger.exception("X fetch failed")
            return []

        posts: list[FeedPost] = []
        for tweet in data.get("tweets", []):
            try:
                posts.append(self._parse_tweet(tweet))
            except Exception:
                logger.warning(
                    "Skipping malformed tweet id=%s", tweet.get("id"), exc_info=True
                )
        return posts
