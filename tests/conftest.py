from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl

from backend.models.feed_schemas import FeedPost


@pytest.fixture
def sample_post() -> FeedPost:
    return FeedPost(
        id="post-1",
        title="GPT-5 Released",
        author="user123",
        url=HttpUrl("https://reddit.com/r/MachineLearning/comments/post-1"),
        created_at=datetime(2026, 6, 21, 12, 0, 0, tzinfo=UTC),
        source="reddit",
        clean_body_text="OpenAI has released GPT-5 with major improvements.",
    )
