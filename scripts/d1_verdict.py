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

--cell SET:LAYER (d1_topics_v2 runs, fixed 2026-10-22 evening before they ran): the decisive cell is given in advance
(context:32, the cell d1_topics_map_27b chose) instead of chosen from the map. With a tasks set, each topic also gets
the same verdict on its own rows (topic_verdicts); a topic counts only if its own positive control passes.

uv run python scripts/d1_verdict.py --map M --parts P [--lookup PP --recall PM] [--tasks-set S] [--onset 44]
                                    [--cell SET:LAYER]
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
    grid = (lambda la: la in pins.LENS_LAYERS) if pins.LENS_LAYERS else (lambda la: la % 4 == 0)  # lens layers (OLMo)
    cands = [r for r in rates if r["family"] == lookup and r["set"] in SETS and r["transit"] and lo <= r["layer"] < onset
             and grid(r["layer"])]  # fmt: skip  # the coarse grid: every 4th layer, or the lens's own layers
    if not cands:
        return None
    best = min(cands, key=lambda r: (-r["cf"]["flips"][0], r["layer"], SETS.index(r["set"])))
    return {"set": best["set"], "layer": best["layer"], "map_flips": best["cf"]["flips"]}


def fixed_cell(rates: list[dict], spec: str, lookup: str) -> dict:
    """--cell SET:LAYER, with the map's flips there when the map has that row."""
    s, layer = spec.split(":")
    assert s in SETS, f"--cell: {s} not one of {SETS}"
    row = next((r for r in rates if r["family"] == lookup and r["set"] == s and r["layer"] == int(layer)), None)
    return {"set": s, "layer": int(layer), "map_flips": row["cf"]["flips"] if row else None, "fixed": True,
            "transit": row["transit"] if row else None}  # fmt: skip


def verdict_of(lk: dict, rc: dict) -> str:
    """lk / rc: part -> [rate, lo, hi, n] of the lookup and recall families at the decisive cell."""
    if not rc["jspace"][3]:
        return "not interpretable: no recall row at the decisive cell"
    if rc["jspace"][0] < POSITIVE_MIN:
        return "not interpretable: the positive control fails"
    if lk["jspace"][0] <= JSPACE_MAX and lk["not_jspace"][0] >= REST_MIN:
        return "replicates"
    return "does not replicate"


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
    ap.add_argument("--cell", default=None, help="SET:LAYER fixed in advance (else chosen from the map)")
    a = ap.parse_args()
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    cell = fixed_cell(rates, a.cell, a.lookup) if a.cell else decisive_cell(rates, a.lookup, a.lo, a.onset)
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
    verdict = verdict_of(out["lookup"], out["recall"])
    out["verdict"] = verdict
    for key in ("topic", "numbers"):
        values = sorted({m[key] for m in meta.values()})
        out[f"by_{key}"] = {v: {f"{fam}_{p}": part(fam, p, at, key, v) for fam in (a.lookup, a.recall)
                                for p in ("full", "jspace", "not_jspace")} for v in values}  # fmt: skip
    if meta:
        out["topic_verdicts"] = {
            v: verdict_of({p: c[f"{a.lookup}_{p}"] for p in ("jspace", "not_jspace")},
                          {p: c[f"{a.recall}_{p}"] for p in ("jspace", "not_jspace")})
            for v, c in out["by_topic"].items()
        }  # fmt: skip
    d = Path(a.out) / f"{a.parts}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    flips = "no map row" if cell["map_flips"] is None else f"C's whole copy flips {100 * cell['map_flips'][0]:.0f}% of lookups"  # fmt: skip
    how = "fixed in advance" if cell.get("fixed") else f"chosen from map {a.map}"
    lines = [f"# d1_verdict / {a.parts}", "", f"Decisive cell ({how}): {cell['set']} at layer {cell['layer']} ({flips})",
             "", f"**Verdict:** {verdict}", "", "| family | part | switched [95%] | n |", "|---|---|---|---|"]  # fmt: skip
    if "topic_verdicts" in out:
        lines[6:6] = ["Per topic: " + "; ".join(f"{t}: {v}" for t, v in out["topic_verdicts"].items()), ""]
    for fam, block in ((a.lookup, out["lookup"]), (a.recall, out["recall"])):
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
