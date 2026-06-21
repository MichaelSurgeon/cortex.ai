from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.models.feed_schemas import FeedPost
from backend.services.feed import FeedService


@pytest.fixture
def mock_reddit_service(sample_post: FeedPost) -> MagicMock:
    service = MagicMock()

    async def _batches():
        yield [sample_post]

    service.fetch_batches = _batches
    return service


@pytest.fixture
def mock_x_service() -> MagicMock:
    service = MagicMock()
    service.fetch_all = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_openai_service(sample_post: FeedPost) -> MagicMock:
    service = MagicMock()
    service.process = AsyncMock(return_value=[sample_post])
    return service


@pytest.fixture
def feed_service(
    mock_reddit_service: MagicMock,
    mock_x_service: MagicMock,
    mock_openai_service: MagicMock,
) -> FeedService:
    return FeedService(
        reddit_service=mock_reddit_service,
        x_service=mock_x_service,
        openai_service=mock_openai_service,
    )


def test_fetch_returns_empty_before_refresh(feed_service: FeedService):
    assert feed_service.fetch() == []


@pytest.mark.asyncio
async def test_refresh_populates_cache(feed_service: FeedService):
    await feed_service.refresh()

    assert len(feed_service.fetch()) > 0


@pytest.mark.asyncio
async def test_refresh_retains_cache_on_error(
    feed_service: FeedService,
    mock_x_service: MagicMock,
):
    await feed_service.refresh()
    cached = list(feed_service.fetch())

    mock_x_service.fetch_all.side_effect = Exception("network error")
    await feed_service.refresh()

    assert feed_service.fetch() == cached
