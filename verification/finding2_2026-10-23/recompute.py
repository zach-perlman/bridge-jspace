"""Finding 2 on Qwen3.6-27B, recomputed from the raw rows: a lookup ignores the lens-readable part of a stated bridge.

Standalone: standard library only, no repo code. Reads results/statement_positions/<run>/outcomes.jsonl and the item
files data/tasks_v2/<set>/items.jsonl (topic, format), and compares every Qwen3.6-27B cell of this finding with
results/cross_model/20261023T091847Z/grid.csv (the grid README cites; --grid=STAMP for another). Run from anywhere:
    python3 verification/finding2_2026-10-23/recompute.py            # the table, OK / MISMATCH per cell
    python3 verification/finding2_2026-10-23/recompute.py --example  # the worked example of claim.md (seed 0)

Rule (scripts/d1_verdict.py, replication rule; the specs jobs/d1/d1_topics_parts_27b.yaml, d1_topics2_parts_27b.yaml,
d1_formats_parts_27b.yaml): rows source == "cf", not null, at the decisive cell (context, layer 32 on every 27B run).
"Switched" = role "b" (the read's top token is the changed bridge's answer). Lookups = family PP, recalls = PM.
Holds ("replicates") iff the lens-readable part (jspace) switches <= 10% of lookups and the rest (not_jspace) >= 50%,
while the lens-readable part switches >= 30% of recalls (the positive control; failing it: not interpretable).
Reported, not decisive: the whole change (full), a random part with the lens part's share of the change (jspace_matched).
"""

import csv
import json
import math
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STAMP = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--grid=")), "20261023T091847Z")
GRID = REPO / "results/cross_model" / STAMP / "grid.csv"
FINDING = "A lookup ignores the lens-readable part of a stated bridge"
CELL = ("context", 32)
PARTS = ("jspace", "not_jspace", "full", "jspace_matched")
# (grid setting, lens role, parts run, tasks_v2 set, split by: None / "domain" (topics) / "format")
CELLS = (
    ("draw 1", "main", "d1_topics_parts_27b", "d1_topics_v1", None),
    ("draw 2", "main", "d1_topics2_parts_27b", "d1_topics_v2", "domain"),
    ("draw 2", "plain J-lens", "qwen36_27b_jlens_d1_topics2_parts", "d1_topics_v2", "domain"),
    ("formats", "main", "d1_formats_parts_27b", "d1_formats_v1", "format"),
)
FORMAT_SETTING = {"table": "table", "json": "JSON"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan,) * 3
    p = k / n
    mid, half = (
        (p + z * z / (2 * n)) / (1 + z * z / n),
        z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n),
    )
    return p, mid - half, mid + half


def load(run, tasks_set):
    rows = [
        json.loads(x) for x in (REPO / "results/statement_positions" / run / "outcomes.jsonl").read_text().splitlines()
    ]
    lines = (REPO / "data/tasks_v2" / tasks_set / "items.jsonl").read_text().splitlines()
    items = {it["id"]: it for it in map(json.loads, lines)}
    at = [r for r in rows if r["source"] == "cf" and not r["null"] and (r["set"], r["layer"]) == CELL]
    return at, items


def block(at, fam):
    """part -> (rate, lo, hi, n): share of rows switched to the changed bridge's answer."""
    out = {}
    for p in PARTS:
        sel = [r["role"] == "b" for r in at if r["family"] == fam and r["part"] == p]
        out[p] = (*wilson(sum(sel), len(sel)), len(sel))
    return out


def judge(lk, rc):
    if rc["jspace"][3] == 0 or rc["jspace"][0] < 0.30:
        return "not interpretable"
    return "holds" if lk["jspace"][0] <= 0.10 and lk["not_jspace"][0] >= 0.50 else "fails"


def main():
    grid = {}
    for g in csv.DictReader(GRID.read_text().splitlines()):
        if g["finding"] == FINDING and g["model"] == "Qwen3.6-27B":
            grid[(g["setting"], "plain J-lens" if "listed beside" in g["lens"] else "main")] = g
    bad = done = 0
    pc = lambda v: f"{100 * v[0]:3.0f}%"  # noqa: E731
    print(f"{'setting':18s} {'lens':12s} {'n':>4s}  lookups: {'lens part [95% CI]':>18s} {'rest':>4s} {'full':>4s} "
          f"{'rand':>4s}  recalls: {'lens part [95% CI]':>18s} {'rest':>4s} {'full':>4s} {'rand':>4s}  {'verdict':17s} grid")  # fmt: skip
    for setting, role, run, tasks_set, split in CELLS:
        at, items = load(run, tasks_set)
        groups = [(setting, at)] if split != "format" else []
        if split:
            for v in sorted({items[r["name"]][split] for r in at}):
                sub = [r for r in at if items[r["name"]][split] == v]
                groups.append((FORMAT_SETTING[v] if split == "format" else f"{setting} · {v}", sub))
        for name, rows in groups:
            lk, rc = block(rows, "PP"), block(rows, "PM")
            verdict, g = judge(lk, rc), grid[(name, role)]
            same = g["verdict"].split(" (")[0] == verdict and g["n"] == str(lk["jspace"][3])
            same &= math.isclose(float(g["value"].split()[0]), round(100 * lk["jspace"][0], 1), abs_tol=1e-9)
            glo, ghi = (float(x) for x in g["95% CI"].strip("[]").split(", "))
            same &= math.isclose(glo, round(100 * lk["jspace"][1], 1), abs_tol=1e-9)
            same &= math.isclose(ghi, round(100 * lk["jspace"][2], 1), abs_tol=1e-9)
            rj = rc["jspace"]
            same &= f"{100 * rj[0]:.0f}% [{100 * rj[1]:.0f}, {100 * rj[2]:.0f}]" in g["chance or control level"]
            same &= (
                f"(needs >= 50%): {100 * lk['not_jspace'][0]:.0f}%; cell context at layer 32"
                in g["chance or control level"]
            )
            if "jspace_matched" in g["chance or control level"]:  # grids from 20261023T104743Z on report it
                # max(0, lo): Wilson's lower bound of 0/n is -3e-18 in floating point, which prints "-0"
                txt = lambda v: f"{100 * v[0]:.0f}% [{100 * max(0.0, v[1]):.0f}, {100 * v[2]:.0f}] n={v[3]}"  # noqa: E731
                matched = f"lookups {txt(lk['jspace_matched'])}, recalls {txt(rc['jspace_matched'])}"
                same &= f"(jspace_matched): {matched}" in g["chance or control level"]
            bad += not same
            done += 1
            ci = lambda v: f"{100 * v[0]:4.1f}% [{100 * v[1]:4.1f}, {100 * v[2]:4.1f}]"  # noqa: E731
            print(f"{name:18s} {role:12s} {lk['jspace'][3]:4d}  lookups: {ci(lk['jspace']):>18s} {pc(lk['not_jspace'])} "
                  f"{pc(lk['full'])} {pc(lk['jspace_matched'])}  recalls: {ci(rj):>18s} {pc(rc['not_jspace'])} "
                  f"{pc(rc['full'])} {pc(rc['jspace_matched'])}  {verdict:17s} {'OK' if same else 'MISMATCH: ' + g['verdict']}")  # fmt: skip
    print(f"\n{done} cells recomputed, {done - bad} match grid.csv, {bad} mismatch. rest = not_jspace, full = the whole "
          "change, rand = jspace_matched (a random part with the lens part's share of the change); % switched")  # fmt: skip
    return 1 if bad else 0


def example(seed=0):
    """One lookup scene of the pre-registered second draw (d1_topics2_parts_27b), drawn with random.Random(seed) from
    the sorted ids, with its recall twin on the same scene."""
    at, items = load("d1_topics2_parts_27b", "d1_topics_v2")
    name = random.Random(seed).choice(sorted({r["name"] for r in at if r["family"] == "PP"}))
    scene = items[name]["scene"]
    print(f"seed {seed}: scene {scene} (run d1_topics2_parts_27b, cell: the context at layer 32)")
    for it in (it for it in items.values() if it["scene"] == scene and it["word"] in ("PP", "PM")):
        print(f"  {it['word']} ({'lookup' if it['word'] == 'PP' else 'recall'}): {it['context']} {it['question']}")
        print(f"      bridge {it['bridge']} -> answer {it['answer']}; changed: {it['cf_context']}")
        print(f"      changed bridge {it['cf_bridge']} -> answer {it['cf_answer']}")
        for r in at:
            if r["name"] == it["id"] and r["part"] in PARTS:
                print(
                    f"      patch {r['part']:15s} -> {r['top_text']!r} ({'switched' if r['role'] == 'b' else r['role']})"
                )


if __name__ == "__main__":
    sys.exit(example() if "--example" in sys.argv else main())
