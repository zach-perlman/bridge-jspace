"""Checks for the deck's depth files (Dan's brief, 29 Oct): every figure and link path in docs/slides/*.md and README.md exists, and
every sourced number (`<number><!-- src: figures/story/data.csv | quantity -->` or docs/x0_numbers.json keys) equals,
at 2 decimals, a value its source holds (for a data.csv quantity: any model's row of that quantity).

uv run python scripts/check_slides.py
"""

from __future__ import annotations

import contextlib
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FILES = [*sorted((REPO / "docs" / "slides").glob("*.md")), REPO / "README.md"]
NUM = re.compile(r"((?:(?<![\d>])[−-])?\d+\.\d+)\]?\s*(?:○\s*)?<!--\s*src:\s*([^|\\]+?)\s*\\?\|\s*(.*?)\s*-->")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")


def values() -> tuple[dict[str, set[float]], dict]:
    by_q: dict[str, set[float]] = {}
    with (REPO / "figures/story/data.csv").open() as f:
        for r in csv.DictReader(f):
            for k in ("value", "lo", "hi"):
                with contextlib.suppress(TypeError, ValueError):
                    by_q.setdefault(r["quantity"], set()).add(round(float(r[k]), 2))
    return by_q, json.loads((REPO / "docs/x0_numbers.json").read_text())


def main() -> int:
    by_q, x0 = values()
    problems, n = [], 0
    for path in FILES:
        text = path.read_text()
        for link in LINK.findall(text):
            if not link.startswith("http") and not (path.parent / link).resolve().exists():
                problems.append(f"{path.name}: missing path {link}")
        for num, src, key in NUM.findall(text):
            v = round(float(num.replace("−", "-")), 2)
            n += 1
            if src == "figures/story/data.csv":
                ok = any(abs(v - x) < 0.006 for x in by_q.get(key, ()))
            elif src == "docs/x0_numbers.json":
                raw = re.findall(r"[−-]?\d+\.\d+", str(x0.get(key, "")))
                ok = any(abs(v - round(float(x.replace("−", "-")), 2)) < 0.006 for x in raw)
            else:
                continue
            if not ok:
                problems.append(f"{path.name}: {num} not in {src} | {key}")
    print(f"check_slides: {len(FILES)} files, {n} sourced numbers, {len(problems)} problem(s)")
    print("\n".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
