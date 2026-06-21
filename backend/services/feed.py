import logging

from backend.models.feed_schemas import FeedPost
from backend.services.openai import OpenAIService
from backend.services.reddit import RedditService
from backend.services.x import XService

logger = logging.getLogger(__name__)


class FeedService:
    def __init__(
        self,
        reddit_service: RedditService,
        x_service: XService,
        openai_service: OpenAIService,
    ) -> None:
        self._reddit_service = reddit_service
        self._x_service = x_service
        self._openai_service = openai_service
        self._cache: list[FeedPost] = []

    def fetch(self) -> list[FeedPost]:
        return self._cache

    async def refresh(self) -> None:
        logger.info("Feed refresh started")
        try:
            x_posts = await self._x_service.fetch_all()
            processed_x = await self._openai_service.process(x_posts)

            processed_reddit: list[FeedPost] = []
            async for batch in self._reddit_service.fetch_batches():
                logger.info("Processing batch of %d Reddit posts", len(batch))
                processed_reddit.extend(await self._openai_service.process(batch))
                self._cache = [*processed_reddit, *processed_x]
                logger.info("Cache updated — %d posts available", len(self._cache))

            logger.info("Feed refresh complete — %d posts cached", len(self._cache))
        except Exception:
            logger.exception("Feed refresh failed — previous cache retained")
