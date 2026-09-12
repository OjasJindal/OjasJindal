from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "OjasJindal"
OUT = Path("data/contributions.json")
URL = f"https://github.com/users/{USER}/contributions"


def main() -> None:
    html = requests.get(URL, timeout=30, headers={"User-Agent": "github-profile-svg/1.0"})
    html.raise_for_status()
    soup = BeautifulSoup(html.text, "html.parser")

    cells = soup.select("td[data-date]")
    if not cells:
        cells = soup.select("[data-date][data-level]")
    if not cells:
        raise RuntimeError("GitHub contribution calendar cells were not found")

    rows = []
    for cell in cells:
        raw = cell.get("data-date")
        if not raw:
            continue
        level = int(cell.get("data-level", "0"))
        rows.append({"date": raw, "level": level})

    rows.sort(key=lambda x: x["date"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"saved {len(rows)} contribution days")


if __name__ == "__main__":
    main()
