from datetime import UTC, datetime

import httpx

from backend.config import GETX_API_KEY
from backend.models.feed_schemas import FeedPost

GETX_BASE_URL = "https://api.getxapi.com"  # replace with actual base URL
SEARCH_QUERY = (
    '"artificial intelligence" OR "machine learning" OR "LLM" lang:en min_faves:50'
)


class XService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=GETX_BASE_URL,
            headers={"Authorization": f"Bearer {GETX_API_KEY}"},
        )

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
            return [self._parse_tweet(tweet) for tweet in data.get("tweets", [])]
        except Exception as e:
            print(f"X fetch error: {e}")
            return []
