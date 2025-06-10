"""
10‑step JobFlow engine (unchanged from CLI edition).
"""

from __future__ import annotations

import uuid, json, textwrap
from dataclasses import dataclass
from typing import Callable
import pandas as pd
from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL
from .db import SessionLocal, WorkflowRun
from .nlp import extract_keywords, find_matches

WORKFLOW_TEMPLATE = [
    (1,  "JK",  "Analyze Job Posting & Keyword Extraction"),
    (2,  "RK",  "Résumé/Keyword & Qualification Mapping"),
    (3,  "DN",  "Differentiators & Narrative"),
    (4,  "ES",  "Experience & Skill Mapping"),
    (5,  "AH",  "Achievement & Skill Highlighting"),
    (6,  "IP",  "Ideal Profile & Persona"),
    (7,  "QB",  "Qualification Boost & Reframing"),
    (8,  "CA",  "Custom Application Materials"),
    (9,  "AO",  "ATS & Online Optimisation"),
    (10, "IQ",  "Interview Question Bank"),
]

_oai = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def _oai_chat(prompt: str, max_tokens: int = 350) -> str:
    if not _oai:
        return textwrap.shorten(prompt, 300) + " …"
    r = _oai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()


@dataclass
class WorkflowState:
    run_id: str
    step: int
    action: str
    description: str
    output: dict | str | None = None

    def as_db(self):
        return WorkflowRun(
            run_id=self.run_id,
            step=self.step,
            action=self.action,
            description=self.description,
            output=self.output,
        )


def run_workflow(job: dict, resume_text: str) -> pd.DataFrame:
    run_id = str(uuid.uuid4())
    df = pd.DataFrame(WORKFLOW_TEMPLATE, columns=["step", "action", "description"])
    session = SessionLocal()

    ctx = {
        "job": job,
        "resume": resume_text,
        "keywords_job": extract_keywords(job["full_text"], 40),
    }

    def s1(st):  # JK
        kw = ctx["keywords_job"]
        st.output = {"title": job["title"], "company": job["company"],
                     "location": job["location"], "keywords": kw}
        st.description = f"Parsed posting – {len(kw)} keywords extracted."

    def s2(st):  # RK
        present, missing = find_matches(job["full_text"], resume_text)
        ctx["present"], ctx["missing"] = present, missing
        st.output = {"present": present, "missing": missing}
        st.description = f"{len(present)} keywords matched; {len(missing)} gaps."

    def s3(st):  # DN
        prompt = f"""
        Produce JSON with:
          differentiators – 5 bullet points,
          narrative       – 70‑word professional summary.
        Résumé:
        \"\"\"{resume_text[:2000]}\"\"\"
        Job:
        \"\"\"{job['full_text'][:2000]}\"\"\"
        """
        js = json.loads(_oai_chat(prompt, 350))
        ctx["diff"], ctx["summary"] = js["differentiators"], js["narrative"]
        st.output = js
        st.description = "Differentiators & narrative drafted."

    def s4(st):  # ES
        prompt = f"""
        Return JSON {{
          exp_map: [{{responsibility, evidence}}],
          skill_ratings: {{skill: 1‑5}}
        }} linking résumé to job.
        Résumé:
        \"\"\"{resume_text[:2500]}\"\"\"
        Job:
        \"\"\"{job['full_text'][:2500]}\"\"\"
        """
        js = json.loads(_oai_chat(prompt, 500))
        ctx["exp_map"], ctx["skill_ratings"] = js["exp_map"], js["skill_ratings"]
        st.output = js
        st.description = "Experience mapped & skills rated."

    def s5(st):  # AH
        prompt = f"""
        Using skill_ratings {ctx['skill_ratings']}, provide JSON {{
          skill_bullets: 3 bullets,
          achievement_bullets: 3 bullets (quantified)
        }}
        """
        js = json.loads(_oai_chat(prompt, 300))
        ctx["skill_bullets"], ctx["achievement_bullets"] = (
            js["skill_bullets"], js["achievement_bullets"]
        )
        st.output = js
        st.description = "Skill & achievement bullets drafted."

    def s6(st):  # IP
        prompt = f"""
        (a) List ideal candidate traits.
        (b) 120‑word persona paragraph.
        Return JSON {{traits, persona}}.
        Job: \"\"\"{job['full_text'][:2000]}\"\"\"
        """
        js = json.loads(_oai_chat(prompt, 400))
        ctx["ideal_traits"], ctx["persona"] = js["traits"], js["persona"]
        st.output = js
        st.description = "Ideal traits & persona created."

    def s7(st):  # QB
        prompt = f"""
        Suggest ≤5 certifications to close gaps {ctx['missing'][:10]}.
        Reframe 3 older experiences. JSON {{certifications, reframed_exp}}.
        Résumé:
        \"\"\"{resume_text[:2000]}\"\"\"
        """
        js = json.loads(_oai_chat(prompt, 350))
        ctx["certifications"], ctx["reframed_exp"] = js["certifications"], js["reframed_exp"]
        st.output = js
        st.description = "Certifications suggested & experience reframed."

    def s8(st):  # CA
        custom_cv = "\n".join([
            ctx["summary"], "",
            "KEY DIFFERENTIATORS", *ctx["diff"], "",
            "KEY SKILLS & ACHIEVEMENTS",
            *ctx["skill_bullets"], *ctx["achievement_bullets"], "",
            resume_text,
        ])
        cover = _oai_chat(
            f"Draft ≤350‑word cover letter using persona {ctx['persona']} and "
            f"differentiators {ctx['diff']}. Job:\n{job['full_text'][:2000]}",
            450,
        )
        ctx["custom_cv"], ctx["cover_letter"] = custom_cv, cover
        st.output = {"resume_preview": custom_cv[:1500] + "…", "cover_letter": cover}
        st.description = "Custom résumé preview & cover letter drafted."

    def s9(st):  # AO
        warnings = []
        if len(ctx["missing"]) > 10:
            warnings.append("≥10 job keywords still missing from résumé.")
        if len(ctx["custom_cv"].split()) > 1000:
            warnings.append("Résumé length >1000 words.")
        about = _oai_chat(
            f"Rewrite LinkedIn About (~300 words) using persona {ctx['persona']}.", 350
        )
        ctx["linkedin_about"] = about
        st.output = {"warnings": warnings, "linkedin_about": about}
        st.description = "ATS audit & LinkedIn About prepared."

    def s10(st):  # IQ
        prompt = """
        Produce JSON with:
          behavioural_qs – 8 questions + tip,
          technical_qs   – 4 questions + tip
        """
        qbank = json.loads(_oai_chat(prompt, 600))
        ctx["interview_bank"] = qbank
        st.output = qbank
        st.description = "Interview question bank generated."

    DISPATCH: dict[int, Callable] = {
        1: s1, 2: s2, 3: s3, 4: s4, 5: s5,
        6: s6, 7: s7, 8: s8, 9: s9, 10: s10,
    }

    for idx, row in df.iterrows():
        st = WorkflowState(run_id, row.step, row.action, row.description)
        DISPATCH[st.step](st)
        session.add(st.as_db())
        session.commit()
        df.at[idx, "description"] = st.description

    session.close()
    return df