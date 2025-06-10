"""
`uvicorn backend.main:app --reload`
"""

from api import app   # re‑export FastAPI instance

# Nothing else needed – uvicorn discovers `app`