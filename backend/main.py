import asyncio
import logging
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.dependencies import get_feed_service, get_x_service
from backend.endpoints.feed import feed_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    feed = get_feed_service()
    x_service = get_x_service()

    asyncio.create_task(feed.refresh())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(feed.refresh, "interval", minutes=10)
    scheduler.start()

    yield

    scheduler.shutdown()
    await x_service.close()


app = FastAPI(title="Cortex AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "http://localhost:8501")],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(feed_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
