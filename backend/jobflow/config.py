"""
Central configuration – loads environment variables and constants.
"""

from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # optional
    load_dotenv = None

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if ENV_PATH.exists() and load_dotenv:
    load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SQLITE_URL     = os.getenv("SQLITE_URL", "sqlite:///jobflow.db")
TIMEOUT        = int(os.getenv("HTTP_TIMEOUT", "15"))