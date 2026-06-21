import asyncio
import logging
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from backend.models.ai_schemas import ProcessingResult
from backend.models.feed_schemas import FeedPost

logger = logging.getLogger(__name__)

PROCESSING_PROMPT = """You are an AI news aggregator assistant. Given a post title and body:

1. Decide if it is relevant to AI, machine learning, or the broader tech industry.

2. If relevant, write a short factual headline (max 12 words, no clickbait, no hype).

3. If relevant, write two summaries (2-3 sentences each):
   - summary_engineer: For an ML/software engineer. Be precise — name specific models,
     architectures, benchmarks, APIs, or performance figures where relevant.
   - summary_enthusiast: For a curious non-technical reader. Plain English only,
     explain why it matters in the real world, no assumed knowledge.

4. If relevant, assign exactly one category:
   - Research: academic papers, model benchmarks, scientific breakthroughs
   - Engineering: tools, frameworks, libraries, deployment, code
   - Business: funding, acquisitions, product launches, company news
   - Policy: regulation, ethics, governance, legal
   - General: anything else, enthusiast or broad AI discussion

If not relevant, leave all string fields as empty strings."""

MODEL = "gpt-4o-mini"

T = TypeVar("T", bound=BaseModel)


class OpenAIService:
    def __init__(self, client: AsyncOpenAI) -> None:
        self._client = client

    async def _parse(
        self, instructions: str, content: str, text_format: type[T]
    ) -> T | None:
        try:
            response = await self._client.responses.parse(
                model=MODEL,
                instructions=instructions,
                input=content,
                text_format=text_format,
            )
            return response.output_parsed
        except Exception:
            logger.exception(
                "OpenAI request failed for format %s", text_format.__name__
            )
            return None

    async def _process_post(self, post: FeedPost) -> FeedPost | None:
        result = await self._parse(
            PROCESSING_PROMPT,
            f"Title: {post.title}\nBody: {post.clean_body_text}",
            ProcessingResult,
        )
        if not result:
            logger.warning("Processing failed for post %s", post.id)
            return None
        if not result.is_relevant:
            logger.debug("Post %s marked not relevant", post.id)
            return None
        post.generated_title = result.title
        post.summary_engineer = result.summary_engineer
        post.summary_enthusiast = result.summary_enthusiast
        post.category = result.category.value
        return post

    async def process(self, posts: list[FeedPost]) -> list[FeedPost]:
        logger.info("Processing %d posts", len(posts))
        results = await asyncio.gather(*[self._process_post(post) for post in posts])
        relevant_posts = [post for post in results if post is not None]
        logger.info("%d/%d posts marked relevant", len(relevant_posts), len(posts))
        return relevant_posts
