from fastapi import APIRouter

feed_router = APIRouter()


@feed_router.get("/feed")
async def get_feed() -> str:
    return "test"
