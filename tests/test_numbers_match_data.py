"""Every number README.md and STATUS.md's current block quote is in figures/story/data.csv (Dan, 25 Oct: the address /
value mix-up; README v2 moved the data file from the frozen figures/status_2026-10-25/). An interval 'v [lo, hi]' must
match one row's value, lo and hi; a lone decimal or percentage must match some row's value. Rule bars (0.05, 0.10,
0.15, 0.20, 0.30, 0.75, 0.80, 95%) and integers (counts) are skipped."""

import contextlib
import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "figures" / "story" / "data.csv"
NUM = r"[−-]?\d+\.\d+"
TRIPLE = re.compile(rf"({NUM}) \[({NUM}), ({NUM})\]")
SINGLE = re.compile(rf"(?<![\w.\[])({NUM}|\d+(?:\.\d+)?%)(?![\d\]])")
BARS = {0.05, 0.10, 0.15, 0.20, 0.30, 0.75, 0.80}


def f(s: str) -> float:
    return float(s.replace("−", "-").rstrip("%"))


def known() -> tuple[list[tuple[float, float, float]], set[float], set[float]]:
    triples, singles, pcts = [], set(), set()
    for r in csv.DictReader(DATA.open()):
        v = r["value"]
        for m in TRIPLE.finditer(v):
            triples.append(tuple(f(x) for x in m.groups()))
        if r["lo"] and r["hi"]:
            with contextlib.suppress(ValueError):
                triples.append((float(r["value"]), float(r["lo"]), float(r["hi"])))
        for m in re.finditer(rf"{NUM}|\d+(?:\.\d+)?%", v):
            (pcts if m.group().endswith("%") else singles).add(round(f(m.group()), 3))
        try:
            x = float(v)
            singles.add(round(x, 3))
            pcts.add(round(x, 1))
            pcts.add(round(100 * x, 1))
        except ValueError:
            pass
    return triples, singles, pcts


def quoted(text: str):
    for m in TRIPLE.finditer(text):
        yield "triple", tuple(f(x) for x in m.groups()), m.group()
    rest = TRIPLE.sub(" ", text)
    for m in SINGLE.finditer(rest):
        yield "single", f(m.group()), m.group()


def check(text: str) -> list[str]:
    triples, singles, pcts = known()
    bad = []
    for kind, val, raw in quoted(text):
        if kind == "triple":
            if not any(all(abs(a - b) <= 0.0051 for a, b in zip(val, t, strict=True)) for t in triples):
                bad.append(raw)
        elif raw.endswith("%"):
            if raw != "95%" and not any(abs(val - p) <= 0.51 for p in pcts):
                bad.append(raw)
        elif round(abs(val), 2) not in BARS and not any(abs(val - s) <= 0.0051 for s in singles):
            bad.append(raw)
    return bad


def test_readme_numbers_are_in_data_csv():
    assert not (bad := check((REPO / "README.md").read_text())), bad


def test_status_current_block_numbers_are_in_data_csv():
    text = (REPO / "STATUS.md").read_text()
    current = text.split("\n# ", 1)[0]  # the newest block, up to the next top-level heading
    assert not (bad := check(current)), bad
