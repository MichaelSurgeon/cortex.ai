from backend.models.feed_schemas import FeedPost
from backend.services.openai import OpenAIService
from backend.services.reddit import RedditService
from backend.services.x import XService


class FeedService:
    _cache: list[FeedPost] = []

    def __init__(
        self,
        reddit: RedditService,
        x_service: XService,
        openai_service: OpenAIService,
    ) -> None:
        self._reddit = reddit
        self._x_service = x_service
        self._openai_service = openai_service

    def fetch(self) -> list[FeedPost]:
        return self._cache

    async def refresh(self) -> None:
        reddit_posts = await self._reddit.fetch_all()
        x_posts = await self._x_service.fetch_all()
        all_posts: list[FeedPost] = [*reddit_posts, *x_posts]
        self._cache = await self._openai_service.process(all_posts)
