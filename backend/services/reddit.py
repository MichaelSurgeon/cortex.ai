import asyncio
import logging
from datetime import UTC, datetime

import feedparser
from bs4 import BeautifulSoup

from backend.models.feed_schemas import FeedPost

logger = logging.getLogger(__name__)

SUBREDDITS = ["MachineLearning", "ArtificialIntelligence"]
DEFAULT_LIMIT = 25


class RedditService:
    def _parse_entry(self, entry) -> FeedPost:
        raw_html = entry.get("summary", "")
        clean_text = (
            BeautifulSoup(raw_html, "html.parser").get_text(separator="\n").strip()
        )

        return FeedPost(
            id=entry.get("id", ""),
            title=entry.get("title", "Untitled"),
            author=entry.get("author", "Unknown"),
            url=entry.get("link", ""),
            created_at=entry.get("updated", datetime.now(UTC).isoformat()),
            clean_body_text=clean_text,
            source="reddit",
        )

    async def fetch_batches(self):
        """Async generator that yields one batch per subreddit as each finishes."""
        for i, sub in enumerate(SUBREDDITS):
            if i > 0:
                await asyncio.sleep(61)
            batch: list[FeedPost] = []
            try:
                feed = feedparser.parse(
                    f"https://www.reddit.com/r/{sub}/.rss?limit={DEFAULT_LIMIT}",
                    agent="CortexAI/1.0 by u/MouseyfJR",
                )
                logger.info(
                    "%s: status=%s, entries=%d", sub, feed.status, len(feed.entries)
                )
                for entry in feed.entries:
                    try:
                        batch.append(self._parse_entry(entry))
                    except Exception:
                        logger.warning(
                            "Skipping malformed entry in r/%s", sub, exc_info=True
                        )
            except Exception:
                logger.exception("Failed to fetch r/%s — skipping", sub)
            if batch:
                yield batch
