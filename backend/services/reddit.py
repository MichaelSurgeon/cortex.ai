import asyncio
from datetime import UTC, datetime

import feedparser
from bs4 import BeautifulSoup

from backend.models.feed_schemas import FeedPost

SUBREDDITS = ["MachineLearning", "ArtificialInteligence"]
DEFAULT_LIMIT = 25


class RedditService:
    def _parse_entry(self, entry, subreddit: str) -> FeedPost:
        raw_html = entry.get("summary", "")
        clean_text = (
            BeautifulSoup(raw_html, "html.parser").get_text(separator="\n").strip()
        )

        return FeedPost(
            id=entry.id,
            title=entry.title,
            author=entry.get("author", "Unknown"),
            url=entry.link,
            created_at=entry.get("updated", datetime.now(UTC).isoformat()),
            clean_body_text=clean_text,
            source="reddit",
        )

    async def fetch_all(self) -> list[FeedPost]:
        all_posts: list[FeedPost] = []

        for i, sub in enumerate(SUBREDDITS):
            feed = feedparser.parse(
                f"https://www.reddit.com/r/{sub}/.rss?limit={DEFAULT_LIMIT}",
                agent="CortexAI/1.0 by u/MouseyfJR",
            )
            print(f"{sub}: status={feed.status}, posts={len(feed.entries)}")
            all_posts.extend(self._parse_entry(entry, sub) for entry in feed.entries)

            if i < len(SUBREDDITS) - 1:
                await asyncio.sleep(61)

        return all_posts
