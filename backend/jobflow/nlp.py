"""
spaCy keyword helpers.
"""

import spacy
from keyword_spacy import KeywordComponent

_nlp = spacy.load("en_core_web_lg")
_nlp.add_pipe(KeywordComponent(_nlp, top_n=40), last=True)


def extract_keywords(text: str, n: int = 25) -> list[str]:
    doc = _nlp(text)
    return [kw.text for kw in doc._.keywords][:n]


def find_matches(job_text: str, resume_text: str):
    j, r = set(extract_keywords(job_text, 40)), set(extract_keywords(resume_text, 40))
    return sorted(j & r), sorted(j - r)