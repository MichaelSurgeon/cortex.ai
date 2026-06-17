from typing import Annotated

from fastapi import APIRouter, Depends

from backend.dependencies import get_feed_service
from backend.models.feed_schemas import FeedPostResponse
from backend.services.feed import FeedService

feed_router = APIRouter()


@feed_router.get("/feed", response_model=list[FeedPostResponse])
async def get_feed(
    feed: Annotated[FeedService, Depends(get_feed_service)],
):
    return feed.fetch()
