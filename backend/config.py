import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GETX_API_KEY = os.getenv("GETX_API_KEY", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY is not set — AI processing will fail")
if not GETX_API_KEY:
    logger.warning("GETX_API_KEY is not set — X/Twitter feed will be disabled")
