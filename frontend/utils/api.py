import os

import httpx

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


def fetch_feed() -> tuple[list[dict], str | None]:
    """Fetch posts from the backend. Returns (posts, error_message)."""
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(f"{API_BASE}/feed")
            resp.raise_for_status()
            return resp.json(), None
    except httpx.ConnectError:
        return [], (
            "Cannot reach the backend. "
            "Make sure the FastAPI server is running on `localhost:8000`."
        )
    except httpx.TimeoutException:
        return [], (
            "Request timed out. The backend is running but may still be loading "
            "its initial feed — wait a moment and refresh."
        )
    except httpx.HTTPStatusError as e:
        return [], f"Backend returned an error: {e}"
    except Exception as e:
        return [], f"Unexpected error: {e}"
