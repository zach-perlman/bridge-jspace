"""Finding 3, recomputed from the raw rows: the last tokens read the answer's digit, not the entity's name.

Standalone: standard library only, no repo code. Reads results/attn_knockout/<run>/{rows,cases}.jsonl and compares every
cell with results/cross_model/20261023T091847Z/grid.csv (the grid README cites; --grid=STAMP for another). Run from anywhere:
    python3 verification/finding3_2026-10-23/recompute.py            # the table, OK / MISMATCH per cell
    python3 verification/finding3_2026-10-23/recompute.py --example  # the worked example of claim.md (seed 0)

Rule (scripts/d2_parts.py, 22 Oct; per format in scripts/d2_formats.py): memory -> prompt items the model answers right
unedited; "right" = top token == the answer's token. Not interpretable unless the off-path sentence without its digit
and without its name, hidden from the question's tokens and from the last tokens, keep >= 90% right (all four). Then
holds iff the sentence without its name hidden from the last tokens leaves <= 35% right and the sentence without its
digit hidden there keeps >= 70%.
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
FINDING = "The last tokens read the answer's digit, not the entity's name"
# model -> runs of draw 1, draw 2, draw 3 (None: no run) and the prose / table / JSON run (README, "Runs", finding 3)
RUNS = {
    "Qwen3.6-27B": ("d2_parts_v2_27b", "d2_parts_seed2_27b", None, "d2_formats_27b"),
    "Qwen3.5-9B": ("qwen35_9b_d2_parts_v2", "qwen35_9b_d2_parts_seed2", "qwen35_9b_d2_parts_seed3", "qwen35_9b_d2_formats"),
    "Olmo-Hybrid-7B": ("olmo_hybrid_7b_d2_parts_v2", "olmo_hybrid_7b_d2_parts_seed2", None, "olmo_hybrid_7b_d2_formats"),
    "Qwen3.5-122B": ("qwen35_122b_d2_parts", "qwen35_122b_d2_parts_seed2", None, "qwen35_122b_d2_formats"),
    "Qwen3-32B": ("qwen3_32b_d2_parts_v2", "qwen3_32b_d2_parts_seed2", "qwen3_32b_d2_parts_seed3", "qwen3_32b_d2_formats"),
    "OLMo-3-7B-I": ("olmo3_7b_instruct_d2_parts_v2", "olmo3_7b_instruct_d2_parts_seed2",
                    "olmo3_7b_instruct_d2_parts_seed3", "olmo3_7b_instruct_d2_formats"),
    "Muse 30B": ("muse30b_d2_parts", "muse30b_d2_parts_seed2", "muse30b_d2_parts_seed3", "muse30b_d2_formats"),
    "Gemma 4 31B-it": ("gemma4it_d2_parts_v2", "gemma4it_d2_parts_seed2", "gemma4it_d2_parts_seed3", "gemma4it_d2_formats"),
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


def counts(rows, cases, fam, fmt=None):
    """(source, dest) -> [right, n] over the family's items right unedited, hidden in every layer."""
    keep = lambda r: r["family"] == fam and (fmt is None or cases[r["id"]]["wording"].split("/")[0] == fmt)  # noqa: E731
    ok = {r["id"] for r in rows if keep(r) and r["source"] == "none" and r["correct"]}
    out = {}
    for r in rows:
        if keep(r) and r["id"] in ok and r["layers"] == "all" and r["source"] != "none":
            c = out.setdefault((r["source"], r["dest"]), [0, 0])
            c[0] += r["top"] == cases[r["id"]]["tok_A"]
            c[1] += 1
    return out


def judge(c):
    noname = wilson(*c.get(("lookup_noname", "final"), (0, 0)))
    n = c.get(("lookup_noname", "final"), (0, 0))[1]
    if n == 0:  # nothing to judge: the other values are placeholders, never printed
        return n, noname, (math.nan,) * 3, {"question": math.nan, "final": math.nan}, "not testable"
    nodigit = wilson(*c[("lookup_nodigit", "final")])
    offs = {
        d: min(wilson(*c[(s, d)])[0] for s in ("lookup_off_nodigit", "lookup_off_noname"))
        for d in ("question", "final")
    }
    if min(offs.values()) < 0.90:
        verdict = "not interpretable"
    else:
        verdict = "holds" if noname[0] <= 0.35 and nodigit[0] >= 0.70 else "fails"
    return n, noname, nodigit, offs, verdict


def word(v):
    return next(w for w in ("holds", "fails", "not interpretable", "not testable", "missing") if v.startswith(w))


def main():
    grid = {
        (g["model"], g["setting"]): g for g in csv.DictReader(GRID.read_text().splitlines()) if g["finding"] == FINDING
    }
    cache, bad, done = {}, 0, 0
    print(f"{'model':15s} {'setting':7s} {'n':>4s} {'right':>6s} {'95% CI':>13s}  {'no digit hidden':>15s} "
          f"{'off q/f':>9s}  {'verdict':18s} grid")  # fmt: skip
    for model, (d1, d2, d3, fmt_run) in RUNS.items():
        cells = [(f"draw {i}", run, "RL", None) for i, run in enumerate((d1, d2, d3), 1)]
        cells += [(s, fmt_run, "MP", f) for s, f in FORMATS.items()]
        for setting, run, fam, fmt in cells:
            g = grid[(model, setting)]
            if run is None:
                print(f"{model:15s} {setting:7s} {'-':>4s}  no run; grid: {g['verdict']}")
                continue
            if run not in cache:
                cache[run] = load(run)
            n, (p, lo, hi), nodigit, offs, verdict = judge(counts(*cache[run], fam, fmt))
            same = word(g["verdict"]) == verdict and (g["n"] or "0") == str(n)
            if n:
                same &= math.isclose(float(g["value"].split()[0]), round(100 * p, 1))
                glo, ghi = (float(x) for x in g["95% CI"].strip("[]").split(", "))
                same &= math.isclose(glo, round(100 * lo, 1), abs_tol=1e-9) and math.isclose(ghi, round(100 * hi, 1))
                same &= (
                    f"{100 * nodigit[0]:.0f}% [{100 * nodigit[1]:.0f}, {100 * nodigit[2]:.0f}]"
                    in g["chance or control level"]
                )
                # "off-path parts hidden: lowest": the last tokens only up to grid 20261023T104743Z (see claim.md);
                # both destinations from 20261023T105852Z on ("needs >= 90% at both places")
                both = "at both places" in g["chance or control level"]
                low = min(offs.values()) if both else offs["final"]
                same &= f"lowest {100 * low:.0f}%" in g["chance or control level"]
            bad += not same
            done += 1
            txt = "-" if not n else f"{100 * p:5.1f}% [{100 * lo:4.1f}, {100 * hi:4.1f}]  {100 * nodigit[0]:14.0f}%  {100 * offs['question']:3.0f}/{100 * offs['final']:3.0f}%"  # fmt: skip
            print(
                f"{model:15s} {setting:7s} {n:4d} {txt}  {verdict:18s} {'OK' if same else 'MISMATCH: ' + g['verdict']}"
            )
    print(f"\n{done} cells recomputed, {done - bad} match grid.csv, {bad} mismatch")
    return 1 if bad else 0


def example(seed=0):
    """One memory -> prompt item of Qwen3.6-27B's first draw, right unedited, drawn with random.Random(seed)."""
    rows, cases = load("d2_parts_v2_27b")
    ok = sorted(r["id"] for r in rows if r["family"] == "RL" and r["source"] == "none" and r["correct"])
    c = cases[random.Random(seed).choice(ok)]
    text = {
        t: c["prompt"][a:b] for t, (a, b) in zip(c["ids"], c["offsets"], strict=True)
    }  # token id -> its text in the prompt
    user = c["prompt"].split("<|im_start|>user\n")[1].split("<|im_end|>")[0]
    print(f"seed {seed}: item {c['id']} (run d2_parts_v2_27b)\nprompt (user turn): {user}\nanswer: {c['answer']}")
    for src in ("none", "lookup", "lookup_noname", "lookup_nodigit", "lookup_off_noname", "lookup_off_nodigit"):
        for r in rows:
            if r["id"] == c["id"] and r["family"] == "RL" and r["source"] == src and r["dest"] in ("-", "final"):
                hidden = c["source_text"].get(src, "nothing")
                print(f"  hidden from the last tokens: {hidden!r:55s} -> top token {text.get(r['top'], r['top'])!r}")


if __name__ == "__main__":
    sys.exit(example() if "--example" in sys.argv else main())
