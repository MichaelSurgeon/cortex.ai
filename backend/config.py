import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GETX_API_KEY = os.getenv("GETX_API_KEY", "")
