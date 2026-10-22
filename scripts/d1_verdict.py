"""d1_verdict: the D1-topics replication rule (jobs/d1/*d1_topics_*.yaml, amended 2026-10-22 17:36 +0200 before any
result was opened) applied to a map run and its parts run.

  cell     the decisive lookup cell, from the lens-free map alone: among the lookup family's statement cells
           (bind_bridge, bridge_word, context) in transit at the coarse layers in [32, onset), the one where C's whole
           copy flips the most lookups (point estimate; ties: the earlier layer, then bind_bridge, bridge_word, context)
  verdict  replicates iff at that cell, pooled over topics, the lens-readable part alone (jspace) switches <= 0.10 of
           lookups and everything else (not_jspace) >= 0.50, while the recall family's lens-readable part switches
           >= 0.30 there (the positive control); no recall row at the cell, or a failing positive control: not
           interpretable. Otherwise: does not replicate.
  reported per topic and by number style (digits / words; tasks_v2 sets), and the nulls (the lens-readable part's
           random-direction null, the OMP over a random dictionary), not decisive.
"switches" = the read's top token is the C bridge's answer (role b); items: every parts row of the cell (the parts
stage ran only on items the model answers right).

uv run python scripts/d1_verdict.py --map M --parts P [--lookup PP --recall PM] [--tasks-set S] [--onset 44]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import wilson

SP = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "d1_verdict"
SETS = ("bind_bridge", "bridge_word", "context")
JSPACE_MAX, REST_MIN, POSITIVE_MIN = 0.10, 0.50, 0.30


def decisive_cell(rates: list[dict], lookup: str, lo: int, onset: int) -> dict | None:
    cands = [r for r in rates if r["family"] == lookup and r["set"] in SETS and r["transit"] and lo <= r["layer"] < onset
             and r["layer"] % 4 == 0]  # fmt: skip  # the coarse grid: every 4th layer
    if not cands:
        return None
    best = min(cands, key=lambda r: (-r["cf"]["flips"][0], r["layer"], SETS.index(r["set"])))
    return {"set": best["set"], "layer": best["layer"], "map_flips": best["cf"]["flips"]}


def rate(rows: list[dict]) -> list[float]:
    return list(wilson(sum(r["role"] == "b" for r in rows), len(rows)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True)
    ap.add_argument("--parts", required=True)
    ap.add_argument("--lookup", default="PP")
    ap.add_argument("--recall", default="PM")
    ap.add_argument("--tasks-set", default=None, help="tasks_v2 set: topic and number style per item")
    ap.add_argument("--onset", type=int, default=44)
    ap.add_argument("--lo", type=int, default=32)
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new verdict folder")
    a = ap.parse_args()
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    cell = decisive_cell(rates, a.lookup, a.lo, a.onset)
    assert cell, "no lookup statement cell in transit in the primary layers"
    rows = [json.loads(x) for x in (SP / a.parts / "outcomes.jsonl").read_text().splitlines()]
    at = [r for r in rows if r["set"] == cell["set"] and r["layer"] == cell["layer"] and r["source"] == "cf"
          and not r["null"]]  # fmt: skip
    nulls = [r for r in rows if r["set"] == cell["set"] and r["layer"] == cell["layer"] and r["source"] == "cf"
             and r["null"]]  # fmt: skip
    meta: dict[str, dict] = {}
    if a.tasks_set:
        for line in (pins.DATA_DIR / "tasks_v2" / a.tasks_set / "items.jsonl").read_text().splitlines():
            it = json.loads(line)
            meta[it["id"]] = {"topic": it["domain"], "numbers": it["numbers"]}

    def part(fam: str, p: str, pool: list[dict] = at, key: str | None = None, value: str | None = None) -> list[float]:
        sel = [r for r in pool if r["family"] == fam and r["part"] == p
               and (key is None or meta.get(r["name"], {}).get(key) == value)]  # fmt: skip
        return [*rate(sel), len(sel)]

    out = {"map": a.map, "parts": a.parts, "cell": cell,
           "lookup": {p: part(a.lookup, p) for p in ("full", "jspace", "not_jspace", "rand_omp")},
           "recall": {p: part(a.recall, p) for p in ("full", "jspace", "not_jspace", "rand_omp")},
           "nulls": {"lookup_jspace_null": part(a.lookup, "jspace", nulls), "recall_jspace_null": part(a.recall, "jspace", nulls)}}  # fmt: skip
    lk, rc = out["lookup"], out["recall"]
    if not rc["jspace"][3]:
        verdict = "not interpretable: no recall row at the decisive cell"
    elif rc["jspace"][0] < POSITIVE_MIN:
        verdict = "not interpretable: the positive control fails"
    elif lk["jspace"][0] <= JSPACE_MAX and lk["not_jspace"][0] >= REST_MIN:
        verdict = "replicates"
    else:
        verdict = "does not replicate"
    out["verdict"] = verdict
    for key in ("topic", "numbers"):
        values = sorted({m[key] for m in meta.values()})
        out[f"by_{key}"] = {v: {f"{fam}_{p}": part(fam, p, at, key, v) for fam in (a.lookup, a.recall)
                                for p in ("full", "jspace", "not_jspace")} for v in values}  # fmt: skip
    d = Path(a.out) / f"{a.parts}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    lines = [f"# d1_verdict / {a.parts}", "", f"Decisive cell (map {a.map}): {cell['set']} at layer {cell['layer']} "
             f"(C's whole copy flips {100 * cell['map_flips'][0]:.0f}% of lookups)", "", f"**Verdict:** {verdict}", "",
             "| family | part | switched [95%] | n |", "|---|---|---|---|"]  # fmt: skip
    for fam, block in ((a.lookup, lk), (a.recall, rc)):
        for p, v in block.items():
            lines.append(f"| {fam} | {p} | {100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}] | {v[3]} |")
    for key in ("topic", "numbers"):
        lines += [
            "",
            f"By {key} (reported, not decisive):",
            "",
            "| " + key + " | cell | switched | n |",
            "|---|---|---|---|",
        ]
        for v, cells in out[f"by_{key}"].items():
            for c, r in cells.items():
                if r[3]:
                    lines.append(f"| {v} | {c} | {100 * r[0]:.0f}% [{100 * r[1]:.0f}, {100 * r[2]:.0f}] | {r[3]} |")
    (d / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
