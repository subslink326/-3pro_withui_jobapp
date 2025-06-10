"""
FastAPI façade exposing the JobFlow engine over HTTP.

POST /run
    Form fields:
        - job_url : str
        - resume  : File (pdf/docx)

Response JSON:
    {
      "run_id": "...",
      "table": [ {step, action, description}, ... ]
    }
"""

from pathlib import Path
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from jobflow.scraper import scrape_job_post
from jobflow.resume_parser import parse_resume
from jobflow.workflow import run_workflow

app = FastAPI(
    title="JobFlow‑Web API",
    version="1.0.0",
    description="HTTP interface for the 10‑step JobFlow engine.",
)

# Allow local Vite dev server (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # For demo – tighten in prod!
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_pipeline(job_url: str = Form(...), resume: UploadFile = Form(...)):
    if resume.filename.split(".")[-1].lower() not in {"pdf", "docx", "doc"}:
        raise HTTPException(status_code=400, detail="Resume must be PDF/DOCX/DOC")

    # Save upload to a temporary file
    with tempfile.TemporaryDirectory() as td:
        file_path = Path(td) / resume.filename
        with file_path.open("wb") as f:
            shutil.copyfileobj(resume.file, f)

        job_data = scrape_job_post(job_url)
        resume_text = parse_resume(file_path)

    table_df = run_workflow(job_data, resume_text)
    return JSONResponse(
        status_code=200,
        content={
            "run_id": str(table_df.iloc[0]['description'])[:8],  # preview
            "table": table_df.to_dict(orient="records"),
        },
    )