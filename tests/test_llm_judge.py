import asyncio
import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from backend.models.feed_schemas import FeedPost
from backend.services.openai import OpenAIService
from tests.golden_posts import GOLDEN_POSTS

pytestmark = pytest.mark.integration

load_dotenv()

ACCURACY_THRESHOLD = 0.85
DIMENSION_PASS_SCORE = 0.65

JUDGE_PROMPT = """You are a strict quality evaluator for AI-generated news summaries.

You will receive:
1. The original post title and body text.
2. Two AI-generated summaries of that post:
   - summary_engineer : intended for ML / software engineers (should be precise, technical,
     and reference specific models, architectures, benchmarks, or figures from the source).
   - summary_enthusiast : intended for curious non-technical readers (should use plain
     English, avoid jargon, and explain real-world significance).

Score the combined quality across FOUR dimensions. Each score is a float from 0.0 to 1.0.

RELEVANCE   — Do both summaries stay on-topic and accurately reflect the post's subject?
              Penalise if a summary drifts to unrelated content or omits the key point.

ACCURACY    — Are all factual claims (names, numbers, benchmarks, organisations) consistent
              with the source text? Penalise any hallucinated or contradicted facts.

TONE        — Is summary_engineer suitably technical and precise for an engineer audience?
              Is summary_enthusiast accessible and jargon-free for a general audience?
              Score low if either summary reads identically to the other or misses its audience.

COHERENCE   — Are the summaries well-structured, clear, and internally consistent?
              Penalise rambling, contradictions, or awkward phrasing.

Scoring guide:
  0.9 – 1.0 : excellent, no notable flaws
  0.7 – 0.9 : good, minor issues
  0.5 – 0.7 : adequate but noticeably flawed
  0.3 – 0.5 : poor quality
  0.0 – 0.3 : unacceptable

Also provide a brief reasoning string (1–3 sentences) explaining your scores."""


class JudgeVerdict(BaseModel):
    relevance: float = Field(ge=0.0, le=1.0)
    accuracy: float = Field(ge=0.0, le=1.0)
    tone: float = Field(ge=0.0, le=1.0)
    coherence: float = Field(ge=0.0, le=1.0)
    reasoning: str = ""

    @property
    def passed(self) -> bool:
        return all(
            score >= DIMENSION_PASS_SCORE
            for score in (self.relevance, self.accuracy, self.tone, self.coherence)
        )

    @property
    def mean_score(self) -> float:
        return (self.relevance + self.accuracy + self.tone + self.coherence) / 4


@dataclass
class EvalResult:
    post_id: str
    title: str
    verdict: JudgeVerdict | None
    service_failed: bool = False

    @property
    def passed(self) -> bool:
        return self.verdict is not None and self.verdict.passed


@pytest.fixture(scope="module")
def openai_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable is not set")
    return AsyncOpenAI(api_key=api_key)


@pytest.fixture(scope="module")
def openai_service(openai_client: AsyncOpenAI) -> OpenAIService:
    return OpenAIService(client=openai_client)


async def _judge_post(client: AsyncOpenAI, post: FeedPost) -> JudgeVerdict | None:
    content = (
        f"### Original post\n"
        f"Title: {post.title}\n"
        f"Body: {post.clean_body_text}\n\n"
        f"### Generated summaries\n"
        f"summary_engineer: {post.summary_engineer}\n"
        f"summary_enthusiast: {post.summary_enthusiast}"
    )
    try:
        response = await client.responses.parse(
            model="gpt-4o-mini",
            instructions=JUDGE_PROMPT,
            input=content,
            text_format=JudgeVerdict,
        )
        return response.output_parsed
    except Exception:
        return None


async def _run_evaluation(
    service: OpenAIService, client: AsyncOpenAI
) -> list[EvalResult]:
    processed = await asyncio.gather(
        *[service._process_post(post.model_copy(deep=True)) for post in GOLDEN_POSTS]
    )

    async def _evaluate(
        post_id: str, title: str, processed_post: FeedPost | None, failed: bool
    ) -> EvalResult:
        if processed_post is None:
            return EvalResult(
                post_id=post_id, title=title, verdict=None, service_failed=failed
            )
        verdict = await _judge_post(client, processed_post)
        return EvalResult(post_id=post_id, title=title, verdict=verdict)

    tasks = [
        _evaluate(
            orig.id,
            orig.title,
            result if result is not None else None,
            result is None,
        )
        for orig, result in zip(GOLDEN_POSTS, processed, strict=True)
    ]
    return list(await asyncio.gather(*tasks))


@pytest.mark.asyncio
async def test_llm_judge_summary_quality(
    openai_service: OpenAIService,
    openai_client: AsyncOpenAI,
) -> None:
    results = await _run_evaluation(openai_service, openai_client)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    accuracy = passed / total

    lines = []
    for r in results:
        if r.service_failed or r.verdict is None:
            lines.append(
                f"  FAIL [{r.post_id}] {r.title!r} — service returned no output"
            )
        else:
            v = r.verdict
            status = "PASS" if r.passed else "FAIL"
            lines.append(
                f"  {status} [{r.post_id}] {r.title!r}\n"
                f"       relevance={v.relevance:.2f}  accuracy={v.accuracy:.2f}  "
                f"tone={v.tone:.2f}  coherence={v.coherence:.2f}  mean={v.mean_score:.2f}\n"
                f"       {v.reasoning}"
            )

    print(
        f"\n{'=' * 68}\n"
        f"LLM-as-a-Judge  {passed}/{total} passed  ({accuracy:.0%})  "
        f"threshold={ACCURACY_THRESHOLD:.0%}\n"
        f"{'=' * 68}\n" + "\n".join(lines) + f"\n{'=' * 68}"
    )

    assert accuracy >= ACCURACY_THRESHOLD, (
        f"LLM-as-a-Judge accuracy {accuracy:.0%} ({passed}/{total}) is below the "
        f"{ACCURACY_THRESHOLD:.0%} threshold."
    )
