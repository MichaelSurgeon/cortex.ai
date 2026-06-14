from fastapi import FastAPI

from backend.endpoints.feed import feed_router

app = FastAPI()


app.include_router(feed_router, prefix="/api/v1")
