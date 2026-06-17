import asyncio
import logging
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from backend.models.ai_schemas import ClassificationResult, SummaryResult
from backend.models.feed_schemas import FeedPost

logger = logging.getLogger(__name__)

CLASSIFIER_PROMPT = """You are a classifier for an AI news aggregator.
Given a post title and body, determine if it is relevant AI news."""

SUMMARISER_PROMPT = """You are a summariser for an AI news aggregator.
Given a post title and body, write a concise 2-3 sentence plain English summary.
No jargon, no fluff."""

MODEL = "gpt-4o-mini"

T = TypeVar("T", bound=BaseModel)


class OpenAIService:
    def __init__(self, client: AsyncOpenAI) -> None:
        self._client = client

    async def _parse(
        self, instructions: str, input: str, text_format: type[T]
    ) -> T | None:
        try:
            response = await self._client.responses.parse(
                model=MODEL,
                instructions=instructions,
                input=input,
                text_format=text_format,
            )
            return response.output_parsed
        except Exception:
            logger.exception(
                "OpenAI request failed for format %s", text_format.__name__
            )
            return None

    async def _classify(self, post: FeedPost) -> bool:
        result = await self._parse(
            CLASSIFIER_PROMPT,
            f"Title: {post.title}\nBody: {post.clean_body_text}",
            ClassificationResult,
        )
        is_relevant = result.is_relevant if result else False
        logger.debug("Classified post %s as relevant=%s", post.id, is_relevant)
        return is_relevant

    async def _summarise(self, post: FeedPost) -> str:
        result = await self._parse(
            SUMMARISER_PROMPT,
            f"Title: {post.title}\nBody: {post.clean_body_text}",
            SummaryResult,
        )
        if not result:
            logger.warning("Summarisation failed for post %s", post.id)
            return "N/A"
        return result.summary

    async def _process_post(self, post: FeedPost) -> FeedPost | None:
        if await self._classify(post):
            post.summary = await self._summarise(post)
            return post
        return None

    async def process(self, posts: list[FeedPost]) -> list[FeedPost]:
        logger.info("Processing %d posts", len(posts))
        results = await asyncio.gather(*[self._process_post(post) for post in posts])
        relevant_posts = [post for post in results if post is not None]
        logger.info("%d/%d posts marked relevant", len(relevant_posts), len(posts))
        return relevant_posts
