"""d2_formats: findings 3 and 4 per format (prose, table, json) of a tasks_v2 attn_knockout run (jobs/d2/*d2_formats*;
the rules committed with those specs, 22 Oct, before the runs).

  late read (finding 4)  memory -> prompt (MP), items right unedited: the answer's row hidden from the last tokens in
                every attention layer leaves <= 20% right with the Wilson upper bound <= 0.30, the off-path row hidden
                there keeps >= 90% (lower bound >= 0.85), and on a hybrid, hidden in every DeltaNet layer instead keeps
                >= 90%.
  name vs digit (finding 3)  scripts/d2_parts.py's verdicts on MP: valid-split, then H-digit-final-split (decisive)
                and H-name-q-split (where the question is testable).
Reported, not decisive: prompt -> prompt (PP), MM and PM as off-path controls, per topic.

uv run python scripts/d2_formats.py --name RUN   ->  results/d2_formats/<RUN>_<stamp>/verdict.{json,md}
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import d2_parts as DP

D2 = pins.RESULTS_DIR / "attn_knockout"
OUT = pins.RESULTS_DIR / "d2_formats"
LATE_MAX, LATE_HI, OFF_MIN, OFF_LO, GDN_MIN = 0.20, 0.30, 0.90, 0.85, 0.90


def rate(rows: list[dict], ok: set, source: str, dest: str, layers: str, fam: str) -> tuple[float, float, float, int]:
    sel = [r["correct"] for r in rows if (r["family"], r["id"]) in ok and r["family"] == fam
           and r["source"] == source and r["dest"] == dest and r["layers"] == layers]  # fmt: skip
    return (*wilson(sum(sel), len(sel)), len(sel))


def late_read(rows: list[dict], ok: set, fam: str) -> dict:
    """The late-read rule on one family's rows; 'attn' (attention layers only) on a hybrid, else 'all'."""
    labels = {r["layers"] for r in rows if r["source"] == "lookup" and r["dest"] == "final"}
    lab = "attn" if "attn" in labels else "all"
    out = {"layers": lab, "lookup": rate(rows, ok, "lookup", "final", lab, fam),
           "off": rate(rows, ok, "lookup_off", "final", lab, fam)}  # fmt: skip
    if "gdn" in labels:
        out["deltanet"] = rate(rows, ok, "lookup", "final", "gdn", fam)
    lk, off = out["lookup"], out["off"]
    holds = lk[3] > 0 and lk[0] <= LATE_MAX and lk[2] <= LATE_HI and off[0] >= OFF_MIN and off[1] >= OFF_LO
    if "deltanet" in out:
        holds = holds and out["deltanet"][0] >= GDN_MIN
    out["holds"] = bool(holds)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    d = D2 / a.name
    cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
    for c in cases.values():  # cases.jsonl keeps the format in "wording" (format/numbers)
        c.setdefault("format", c["wording"].split("/")[0])
    rows = [json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()]
    ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
    n_items = collections.Counter((cases[r["id"]]["format"], r["family"]) for r in rows if r["source"] == "none")
    out: dict = {"run": a.name, "items": {f"{k[0]}/{k[1]}": v for k, v in sorted(n_items.items())}, "formats": {}}
    for fmt in sorted({c["format"] for c in cases.values()}):
        sub = [r for r in rows if cases[r["id"]]["format"] == fmt]
        cl = DP.cells(sub, cases)
        parts = DP.verdicts(cl, "MP") if all(("MP", s, dd) in cl for s in DP.PARTS for dd in ("question", "final")) else None  # fmt: skip
        out["formats"][fmt] = {
            "late_MP": late_read(sub, ok, "MP"), "late_PP": late_read(sub, ok, "PP"),
            "parts_MP": parts,
            "cells_MP": {f"{s}|{dd}": cl[("MP", s, dd)]["right"] for s in DP.PARTS + DP.SPLIT for dd in ("question", "final")
                         if ("MP", s, dd) in cl},
        }  # fmt: skip
    dest = OUT / f"{a.name}_{time.strftime('%Y%m%d-%H%M%S')}"
    dest.mkdir(parents=True)
    (dest / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")

    def pct(v) -> str:
        return f"{100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}] (n {v[3]})" if len(v) > 3 else f"{100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}]"  # fmt: skip

    lines = [f"# d2_formats / {a.name}", "", "| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | "
             "name vs digit (MP): valid-split, digit-final-split, name-q-split |", "|---|---|---|---|---|"]  # fmt: skip
    for fmt, v in out["formats"].items():
        lm = v["late_MP"]
        p = v["parts_MP"] or {}
        lines.append(f"| {fmt} | {pct(lm['lookup'])} / {pct(lm['off'])} / {pct(lm['deltanet']) if 'deltanet' in lm else '-'} | "
                     f"{lm['holds']} | {pct(v['late_PP']['lookup'])} | {p.get('valid-split')}, {p.get('H-digit-final-split')}, "
                     f"{p.get('H-name-q-split')} (testable: {p.get('question_testable')}) |")  # fmt: skip
    lines += ["", "Name vs digit cells (MP, right [95%]):", ""]
    for fmt, v in out["formats"].items():
        keep = ("lookup|question", "lookup_nodigit|question", "lookup_noname|question", "lookup_noname|final", "lookup_nodigit|final")  # fmt: skip
        lines.append(f"- {fmt}: " + "; ".join(f"{k} {pct(v['cells_MP'][k])}" for k in keep if k in v["cells_MP"]))
    (dest / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
