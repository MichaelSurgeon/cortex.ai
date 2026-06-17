import asyncio
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.dependencies import get_feed_service
from backend.endpoints.feed import feed_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    feed = get_feed_service()

    asyncio.create_task(feed.refresh())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(feed.refresh, "interval", minutes=10)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(title="Cortex AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feed_router, prefix="/api/v1")
