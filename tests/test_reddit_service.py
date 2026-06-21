from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.services.reddit import RedditService


@pytest.fixture
def reddit_service() -> RedditService:
    return RedditService()


def test_parse_entry_valid(reddit_service):
    entry = {
        "id": "t3_abc123",
        "title": "New AI Benchmark Released",
        "author": "researcher42",
        "link": "https://reddit.com/r/MachineLearning/comments/abc123",
        "updated": "2026-06-21T12:00:00+00:00",
        "summary": "<p>Researchers published a new benchmark for LLMs.</p>",
    }

    post = reddit_service._parse_entry(entry)

    assert post.id == "t3_abc123"
    assert post.title == "New AI Benchmark Released"
    assert post.source == "reddit"
    assert "Researchers published" in post.clean_body_text


def test_parse_entry_missing_fields_uses_fallbacks(reddit_service):
    entry = {"link": "https://reddit.com/r/MachineLearning/comments/fallback"}

    post = reddit_service._parse_entry(entry)

    assert post.title == "Untitled"
    assert post.author == "Unknown"
    assert post.source == "reddit"


@pytest.mark.asyncio
async def test_fetch_batches_yields_parsed_posts():
    fake_entry = {
        "id": "t3_xyz",
        "title": "ML News",
        "author": "ml_fan",
        "link": "https://reddit.com/r/MachineLearning/comments/xyz",
        "updated": "2026-06-21T12:00:00+00:00",
        "summary": "<p>Some ML news.</p>",
    }
    fake_feed = MagicMock()
    fake_feed.status = 200
    fake_feed.entries = [fake_entry]

    with patch("backend.services.reddit.feedparser.parse", return_value=fake_feed):
        with patch("asyncio.sleep", new_callable=AsyncMock):
            service = RedditService()
            batches = [batch async for batch in service.fetch_batches()]

    assert len(batches) >= 1
    assert batches[0][0].id == "t3_xyz"
    assert batches[0][0].source == "reddit"


@pytest.mark.asyncio
async def test_fetch_batches_skips_subreddit_on_error():
    with patch(
        "backend.services.reddit.feedparser.parse", side_effect=Exception("timeout")
    ):
        with patch("asyncio.sleep", new_callable=AsyncMock):
            service = RedditService()
            batches = [batch async for batch in service.fetch_batches()]

    assert batches == []
