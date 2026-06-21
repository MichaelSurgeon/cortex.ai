from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.services.x import XService


@pytest.fixture
def x_service() -> XService:
    return XService()


def test_parse_tweet_maps_fields(x_service: XService):
    tweet = {
        "id": "tw-123",
        "text": "OpenAI just released GPT-5. This is huge for the industry.",
        "author": {"userName": "ai_news"},
        "url": "https://x.com/ai_news/status/123",
        "createdAt": "Sat Jun 21 12:00:00 +0000 2026",
    }

    post = x_service._parse_tweet(tweet)

    assert post.id == "tw-123"
    assert post.source == "x"
    assert post.author == "ai_news"
    assert post.created_at == datetime(2026, 6, 21, 12, 0, 0, tzinfo=UTC)


@pytest.mark.asyncio
async def test_fetch_all_returns_parsed_posts(x_service: XService):
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "tweets": [
            {
                "id": "tw-1",
                "text": "AI news tweet content here for testing.",
                "author": {"userName": "techwriter"},
                "url": "https://x.com/techwriter/status/1",
                "createdAt": "Sat Jun 21 12:00:00 +0000 2026",
            }
        ]
    }
    x_service._client = MagicMock()
    x_service._client.get = AsyncMock(return_value=mock_response)

    posts = await x_service.fetch_all()

    assert len(posts) == 1
    assert posts[0].id == "tw-1"
    assert posts[0].source == "x"


@pytest.mark.asyncio
async def test_fetch_all_returns_empty_on_http_error(x_service: XService):
    x_service._client = MagicMock()
    x_service._client.get = AsyncMock(side_effect=Exception("connection refused"))

    posts = await x_service.fetch_all()

    assert posts == []
