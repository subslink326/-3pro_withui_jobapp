# JobFlow-Web 🖥️

Modern web UI for the 10-step **JobFlow** AI job-application engine.

##  Quick-start

```bash
# ─── clone & enter repo ──────────────────────────────────────────────────
git clone https://github.com/your-org/jobflow-web.git
cd jobflow-web

# ─── backend ─────────────────────────────────────────────────────────────
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
uvicorn backend.main:app --reload          # → http://localhost:8000/run

# ─── frontend (new terminal) ─────────────────────────────────────────────
cd ../frontend
npm install
npm run dev                               # → http://localhost:5173
```

Open the UI, paste a public job-posting URL, upload your résumé, and watch the
10-step workflow populate in real time.  All results persist in `backend/jobflow.db`.

## 🛠  Stack

* **FastAPI** + Uvicorn – typed, async JSON API
* **SQLite + SQLAlchemy** – durable memory for every step
* **React 18** + Vite + Tailwind CSS – instant hot-reload, modern UX
* **OpenAI GPT-4o-mini** – default LLM (fallback stub if key missing)

Feel free to deploy the backend as a single container (`uvicorn`) and host the
static front-end via any CDN or Netlify/Vercel.

---

© 2025 JobFlow Project – MIT-licensed