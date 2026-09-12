from __future__ import annotations

import json
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    data = data[-371:]
    by_date = {x["date"]: x["level"] for x in data}
    dates = [x["date"] for x in data]
    if not dates:
        raise RuntimeError("No contribution data")

    # Build a 53-column x 7-row calendar using the weekday of each date.
    from datetime import date
    start = date.fromisoformat(dates[0])
    start = start.fromordinal(start.toordinal() - (start.weekday() + 1) % 7)

    cells = []
    for i in range(371):
        d = start.fromordinal(start.toordinal() + i)
        col, row = i // 7, i % 7
        level = by_date.get(d.isoformat(), 0)
        cells.append(f'<rect class="cell" x="{col*18}" y="{row*18}" width="13" height="13" rx="3" fill="{COLORS[max(0,min(4,level))]}" style="--i:{i}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="190" viewBox="0 0 1000 190">
<style>
.cell {{ opacity:0; animation:reveal .35s ease-out forwards; animation-delay:calc(var(--i) * 7ms); }}
@keyframes reveal {{ from {{ opacity:0; transform:translateY(5px); }} to {{ opacity:1; transform:translateY(0); }} }}
@media (prefers-reduced-motion: reduce) {{ .cell {{ animation:none; opacity:1; }} }}
</style>
<rect width="1000" height="190" rx="18" fill="#050505" stroke="#222"/>
<text x="28" y="34" fill="#00ff88" font-family="monospace" font-size="16">ojas@github:~$ contributions --last-53-weeks</text>
<g transform="translate(28 54)">{''.join(cells)}</g>
<text x="28" y="176" fill="#666" font-family="monospace" font-size="12">less → more</text>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
