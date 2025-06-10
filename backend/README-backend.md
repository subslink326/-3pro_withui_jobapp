# Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# dev server (hot‑reload)
uvicorn backend.main:app --reload
```