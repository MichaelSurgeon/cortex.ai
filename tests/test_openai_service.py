from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.models.ai_schemas import Category, ProcessingResult
from backend.services.openai import OpenAIService


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.responses.parse = AsyncMock()
    return client


@pytest.fixture
def openai_service(mock_client: MagicMock) -> OpenAIService:
    return OpenAIService(client=mock_client)


@pytest.mark.asyncio
async def test_process_post_relevant(openai_service, mock_client, sample_post):
    mock_response = MagicMock()
    mock_response.output_parsed = ProcessingResult(
        is_relevant=True,
        title="GPT-5 Released by OpenAI",
        summary_engineer="OpenAI released GPT-5 with improved reasoning and MMLU scores.",
        summary_enthusiast="OpenAI's new model is smarter and available today.",
        category=Category.research,
    )
    mock_client.responses.parse.return_value = mock_response

    result = await openai_service._process_post(sample_post)

    assert result is not None
    assert result.generated_title == "GPT-5 Released by OpenAI"
    assert result.category == "Research"
    assert result.summary_engineer != ""
    assert result.summary_enthusiast != ""


@pytest.mark.asyncio
async def test_process_post_not_relevant(openai_service, mock_client, sample_post):
    mock_response = MagicMock()
    mock_response.output_parsed = ProcessingResult(is_relevant=False)
    mock_client.responses.parse.return_value = mock_response

    result = await openai_service._process_post(sample_post)

    assert result is None


@pytest.mark.asyncio
async def test_process_post_api_failure(openai_service, mock_client, sample_post):
    mock_client.responses.parse.side_effect = Exception("API timeout")

    result = await openai_service._process_post(sample_post)

    assert result is None


@pytest.mark.asyncio
async def test_process_filters_irrelevant_posts(
    openai_service, mock_client, sample_post
):
    mock_response = MagicMock()
    mock_response.output_parsed = ProcessingResult(is_relevant=False)
    mock_client.responses.parse.return_value = mock_response

    results = await openai_service.process([sample_post, sample_post])

    assert results == []
