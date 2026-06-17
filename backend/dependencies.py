from backend.clients.openai_client import openai_client
from backend.services.feed import FeedService
from backend.services.openai import OpenAIService
from backend.services.reddit import RedditService
from backend.services.x import XService

_openai_service = OpenAIService(client=openai_client)
_reddit_service = RedditService()
_x_service = XService()
_feed_service = FeedService(
    reddit=_reddit_service,
    x_service=_x_service,
    openai_service=_openai_service,
)


def get_feed_service() -> FeedService:
    return _feed_service
