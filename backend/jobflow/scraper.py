"""
Static‑HTML job‑post scraper (swap for Playwright if JS‑heavy).
"""

import re
import requests
import bs4
from .config import TIMEOUT


def _text(el):
    return re.sub(r"\s+", " ", el.get_text(strip=True)) if el else ""


def scrape_job_post(url: str) -> dict:
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    return {
        "url": url,
        "title": _text(soup.select_one("h1")),
        "company": _text(soup.select_one("[data-company], .company, .posting-category")),
        "location": _text(soup.select_one(".location, [data-location]")),
        "posted_date": _text(soup.select_one("time")),
        "full_text": _text(soup),
    }