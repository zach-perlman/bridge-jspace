"""Finding 4, recomputed from the raw rows: a lookup ends in a late attention read of the answer's sentence.

Standalone: standard library only, no repo code. Reads results/attn_knockout/<run>/{rows,cases}.jsonl and compares every
cell with results/cross_model/20261023T091847Z/grid.csv (the grid README cites; --grid=STAMP for another). Run from anywhere:
    python3 verification/finding4_2026-10-23/recompute.py            # the table, OK / MISMATCH per cell
    python3 verification/finding4_2026-10-23/recompute.py --example  # the worked example of claim.md (seed 0)

Rule (fixed 22 Oct for the second draws, jobs/d2/d2_late_read_seed2_27b.yaml; per format jobs/d2/d2_formats_27b.yaml):
memory -> prompt items the model answers right unedited; "right" = the row's `correct`. The answer's sentence hidden from
the last tokens in every attention layer (every layer on attention-only models) leaves <= 20% right with the Wilson upper
bound <= 30%; the off-path sentence hidden there instead keeps >= 90% (lower bound >= 85%), else not interpretable; on a
hybrid, the answer's sentence hidden in every DeltaNet layer instead keeps >= 90%. Chance: 1 in 5 on the sentence lists,
1 in 3 in the prose / table / JSON scenes (3 facts each; grid.csv writes 20% for both).
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
FINDING = "A lookup ends in a late attention read of the answer's sentence"
HYBRIDS = ("Qwen3.6-27B", "Qwen3.5-9B", "Olmo-Hybrid-7B", "Qwen3.5-122B")  # attention + DeltaNet layers
# model -> runs of draw 1, draw 2, draw 3, prose / table / JSON, long context (None: no run; README, "Runs", finding 4)
RUNS = {
    "Qwen3.6-27B": ("d2_v4_late_read", "d2_late_read_seed2_27b", None, "d2_formats_27b", "d2_late_read_long_27b_r3"),
    "Qwen3.5-9B": ("qwen35_9b_d2_v4_late_read_r2", "qwen35_9b_d2_late_read_seed2", "qwen35_9b_d2_late_read_seed3",
                   "qwen35_9b_d2_formats", "qwen35_9b_d2_late_read_long"),
    "Olmo-Hybrid-7B": ("olmo_hybrid_7b_d2_v4_late_read_v3", "olmo_hybrid_7b_d2_late_read_seed2", None,
                       "olmo_hybrid_7b_d2_formats", None),
    "Qwen3.5-122B": ("qwen35_122b_d2_late_read", "qwen35_122b_d2_late_read_seed2", None, "qwen35_122b_d2_formats",
                     "qwen35_122b_d2_late_read_long"),
    "Qwen3-32B": ("qwen3_32b_d2_v4_late_read_v2_r2", "qwen3_32b_d2_late_read_seed2", "qwen3_32b_d2_late_read_seed3",
                  "qwen3_32b_d2_formats", "qwen3_32b_d2_late_read_long"),
    "OLMo-3-7B-I": ("olmo3_7b_instruct_d2_v4_late_read_v3", "olmo3_7b_instruct_d2_late_read_seed2",
                    "olmo3_7b_instruct_d2_late_read_seed3", "olmo3_7b_instruct_d2_formats",
                    "olmo3_7b_instruct_d2_late_read_long"),
    "Muse 30B": ("muse30b_d2_late_read", "muse30b_d2_late_read_seed2", "muse30b_d2_late_read_seed3", "muse30b_d2_formats",
                 "muse30b_d2_late_read_long"),
    "Gemma 4 31B-it": ("gemma4it_d2_v4_late_read_v3_r2", "gemma4it_d2_late_read_seed2", "gemma4it_d2_late_read_seed3",
                       "gemma4it_d2_formats", None),
}  # fmt: skip
FORMATS = {"prose": "prose", "table": "table", "JSON": "json"}  # grid setting -> the format in cases.jsonl "wording"


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan,) * 3
    p = k / n
    mid, half = (
        (p + z * z / (2 * n)) / (1 + z * z / n),
        z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n),
    )
    return p, mid - half, mid + half


def load(run):
    d = REPO / "results/attn_knockout" / run
    rows = [json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()]
    return rows, {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}


def cell(rows, cases, fam, hybrid, fmt=None):
    """(n, answer's sentence blocked, off-path sentence blocked, DeltaNet layers blocked instead), Wilson triples."""
    keep = lambda r: r["family"] == fam and (fmt is None or cases[r["id"]]["wording"].split("/")[0] == fmt)  # noqa: E731
    ok = {r["id"] for r in rows if keep(r) and r["source"] == "none" and r["correct"]}

    def rate(source, layers):
        sel = [r["correct"] for r in rows if keep(r) and r["id"] in ok and r["source"] == source
               and r["dest"] == "final" and r["layers"] == layers]  # fmt: skip
        return wilson(sum(sel), len(sel)), len(sel)

    (lk, n), (off, _) = rate("lookup", "attn" if hybrid else "all"), rate("lookup_off", "attn" if hybrid else "all")
    gdn = rate("lookup", "gdn")[0] if hybrid else None
    return n, lk, off, gdn


def judge(n, lk, off, gdn):
    if n == 0:
        return "not testable"
    late = lk[0] <= 0.20 and lk[2] <= 0.30
    if late and off[0] >= 0.90 and off[1] >= 0.85 and (gdn is None or gdn[0] >= 0.90):
        return "holds"
    if not (off[0] >= 0.90 and off[1] >= 0.85):
        return "not interpretable"
    return "fails"  # the read is not blocked enough, or (hybrids) the DeltaNet layers matter


def word(v):
    return next(w for w in ("holds", "fails", "not interpretable", "not testable", "missing") if v.startswith(w))


def main():
    grid = {
        (g["model"], g["setting"]): g for g in csv.DictReader(GRID.read_text().splitlines()) if g["finding"] == FINDING
    }
    cache, bad, done = {}, 0, 0
    print(f"{'model':15s} {'setting':12s} {'n':>4s} {'right':>6s} {'95% CI':>13s}  {'off-path':>17s} {'DeltaNet':>8s}  "
          f"{'verdict':18s} grid")  # fmt: skip
    for model, (d1, d2, d3, fmt_run, long) in RUNS.items():
        cells = [(f"draw {i}", run, "RL", None) for i, run in enumerate((d1, d2, d3), 1)]
        cells += [(s, fmt_run, "MP", f) for s, f in FORMATS.items()] + [("long context", long, "RL", None)]
        for setting, run, fam, fmt in cells:
            g = grid[(model, setting)]
            if run is None:
                print(f"{model:15s} {setting:12s} {'-':>4s}  no run; grid: {g['verdict']}")
                continue
            if run not in cache:
                cache[run] = load(run)
            n, lk, off, gdn = cell(*cache[run], fam, model in HYBRIDS, fmt)
            verdict = judge(n, lk, off, gdn)
            same = word(g["verdict"]) == verdict and (g["n"] or "0") == str(n)
            note = ""
            if n:
                same &= math.isclose(float(g["value"].split()[0]), round(100 * lk[0], 1))
                glo, ghi = (float(x) for x in g["95% CI"].strip("[]").split(", "))
                same &= math.isclose(glo, round(100 * lk[1], 1), abs_tol=1e-9) and math.isclose(
                    ghi, round(100 * lk[2], 1)
                )
                same &= (
                    f"keeps {100 * off[0]:.0f}% [{100 * off[1]:.0f}, {100 * off[2]:.0f}]"
                    in g["chance or control level"]
                )
                if gdn:
                    same &= f"DeltaNet layer instead: {100 * gdn[0]:.0f}%" in g["chance or control level"]
                if verdict == "fails" and lk[1] <= 0.20 <= lk[2]:
                    note = " (at chance)"
            bad += not same
            done += 1
            txt = "-" if not n else (f"{100 * lk[0]:5.1f}% [{100 * lk[1]:4.1f}, {100 * lk[2]:4.1f}]  {100 * off[0]:4.0f}% "
                                     f"[{100 * off[1]:3.0f}, {100 * off[2]:3.0f}] {'-' if gdn is None else f'{100 * gdn[0]:.0f}%':>8s}")  # fmt: skip
            print(
                f"{model:15s} {setting:12s} {n:4d} {txt}  {verdict + note:18s} {'OK' if same else 'MISMATCH: ' + g['verdict']}"
            )
    print(f"\n{done} cells recomputed, {done - bad} match grid.csv, {bad} mismatch")
    return 1 if bad else 0


def example(seed=0):
    """One memory -> prompt item of Qwen3.6-27B's second draw, right unedited, drawn with random.Random(seed)."""
    rows, cases = load("d2_late_read_seed2_27b")
    ok = sorted(r["id"] for r in rows if r["family"] == "RL" and r["source"] == "none" and r["correct"])
    c = cases[random.Random(seed).choice(ok)]
    text = {
        t: c["prompt"][a:b] for t, (a, b) in zip(c["ids"], c["offsets"], strict=True)
    }  # token id -> its text in the prompt
    user = c["prompt"].split("<|im_start|>user\n")[1].split("<|im_end|>")[0]
    print(
        f"seed {seed}: item {c['id']} (run d2_late_read_seed2_27b)\nprompt (user turn): {user}\nanswer: {c['answer']}"
    )
    for r in rows:
        if r["id"] == c["id"] and r["dest"] in ("-", "final") and r["layers"] in ("-", "attn", "gdn"):
            what = c["source_text"].get(r["source"], "nothing")
            print(
                f"  blocked from the last tokens ({r['layers']} layers): {what!r:35s} -> top token {text.get(r['top'], r['top'])!r}"
            )


if __name__ == "__main__":
    sys.exit(example() if "--example" in sys.argv else main())
