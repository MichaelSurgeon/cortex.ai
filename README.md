# Cortex AI

A personal AI news aggregator that pulls posts from Reddit and X (Twitter), filters them for relevance, and generates summaries and categories using GPT-4o-mini.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (or pip)
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [GetX API key](https://getxapi.com) for X/Twitter posts

## Setup

```bash
# 1. Clone and enter the repo
git clone https://github.com/your-username/cortex.ai
cd cortex.ai

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env and fill in your API keys
```

## Running

Open two terminals from the repo root.

**Backend (FastAPI)**
```bash
uvicorn backend.main:app --reload
```

**Frontend (Streamlit)**
```bash
streamlit run frontend/streamlit_app.py
```

The frontend is available at `http://localhost:8501`. The backend API is at `http://localhost:8000/api/v1`.

The feed refreshes automatically every 10 minutes. The first batch of posts appears within ~60 seconds of starting the backend.

## Tests

```bash
python -m pytest tests/ -v
```

### LLM-as-a-Judge

`tests/test_llm_judge.py` runs an integration eval against a set of golden posts in `tests/golden_posts.py`. For each post it:

1. Calls `OpenAIService._process_post` to generate the headline, dual summaries, and category.
2. Sends the original post + generated summaries to a second GPT-4o-mini call acting as a judge.
3. The judge scores four dimensions — **relevance**, **accuracy**, **tone**, and **coherence** — each on a 0–1 scale.
4. A post passes if every dimension is ≥ 0.65. The suite passes if ≥ 85 % of posts pass.

This test hits the OpenAI API and is marked `integration`, so it is skipped if `OPENAI_API_KEY` is not set.

```bash
# Run only the LLM judge eval (verbose output shows per-post scores)
python -m pytest tests/test_llm_judge.py -v -s

# Run all integration tests
python -m pytest tests/ -v -s -m integration
```

## Architecture

- **Backend**: FastAPI + APScheduler, fetches and processes posts on a 10-minute cycle
- **Frontend**: Streamlit multi-page app
- **AI**: Single GPT-4o-mini call per post — relevance check, headline, dual summaries (engineer + enthusiast), and category
- **Sources**: Reddit RSS (`r/MachineLearning`, `r/ArtificialIntelligence`) and X via GetX API
