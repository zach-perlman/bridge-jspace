"""nn_ko52_read (Zach, 2026-10-30, prereg amendment 72 note 52): note 44's capital / country spans residualised, read (CPU).

Run (scripts/queues/h200_n52_1030.sh), per model prefix P: {P}jsuite_v5kn2c_test_chat_ko52_cand2_v1 (note 44's set, gate, band,
batch, words MC MC0, kinds clean step2) under paper10, paper10_rot, paper10_keepCapPerp (Cap's span projected off the item's Cty
span per layer, re-orthonormalised), paper10_keepCtyPerp (the reverse) and paper10_keepShared (bisectors of the principal vectors
of span(Cap) and span(Cty) with cosine >= 0.9). keeplog.jsonl: paper10's removal energy share E in each span, their ranks, the
number of principal cosines >= 0.9.
Rescue(X) = note 44's (scripts/nn_ko44_read.rescue): 1 - contrast(keepX) / contrast(paper10) on MC0's gated items (contrast = the
whole question's loss minus its step 2's), bridge bootstrap; the version net of paper10_rot beside.
Reading (MC0, all gated; the 27B and Lightning primary, the 9B descriptive): "the capital carries it" if rescue(CapPerp) >= 2/3 and
rescue(CtyPerp) <= 1/3; "the country carries it" the reverse; "the shared part carries it" if both <= 1/3 and rescue(Shared) >=
2/3; "either suffices" if both >= 2/3; otherwise "unclear" ("not read" if MC0's paper10 contrast is <= 0).
Beside: note 44's keepCap / keepCty rescues (its stored run, {P}jsuite_v5kn2c_test_chat_ko44_cand2_v1); MC's reading.
Writes results/ablate_v2/nn_v5_read/{P}note52.json (or --out-dir) and prints the reading line.

python scripts/nn_ko52_read.py PREFIX [--run-dir DIR] [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts.nn_ko44_read import rescue  # noqa: E402
from scripts.nn_v5_read import items_of  # noqa: E402

RES = ROOT / "results"
MC_SET = "jsuite_v5kn2c_test_chat"
KEEPS = ("CapPerp", "CtyPerp", "Shared")


def ko_rows_at(d: Path) -> dict:
    """nn_v5_read.ko_rows from a run directory: (family, kind, condition) -> id -> correct_cand2."""
    acc = collections.defaultdict(dict)
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        acc[(r["family"], r.get("kind", "clean"), r["condition"])][r["id"]] = bool(r["correct_cand2"])
    return acc


def reading(v: dict) -> str:
    if any(v.get(x) is None for x in KEEPS):
        return "not read: a rescue is undefined (MC0's paper10 contrast <= 0) or missing"
    c, t, s = v["CapPerp"], v["CtyPerp"], v["Shared"]
    if c >= 2 / 3 and t <= 1 / 3:
        return "the capital carries it"
    if t >= 2 / 3 and c <= 1 / 3:
        return "the country carries it"
    if c <= 1 / 3 and t <= 1 / 3 and s >= 2 / 3:
        return "the shared part carries it"
    if c >= 2 / 3 and t >= 2 / 3:
        return "either suffices"
    return "unclear"


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    d = run_dir or RES / "ablate_v2" / f"{P}{MC_SET}_ko52_cand2_v1"
    out: dict = {"prefix": P, "role": "descriptive" if P == "qwen35_9b_" else "primary", "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 52 {P or '27b_'}: {d} missing")
        return out
    items, acc = items_of(MC_SET), ko_rows_at(d)
    tag = P or "27b_"
    every = lambda i: True  # noqa: E731
    lines = []
    for fam in ("MC0", "MC"):
        rs = {x: rescue(acc, items, fam, x, every) for x in KEEPS}
        v = {x: rs[x].get("rescue") for x in KEEPS}
        out[fam] = {"rescue": rs, "reading": reading(v)}
    n44 = RES / "ablate_v2" / f"{P}{MC_SET}_ko44_cand2_v1"
    if (n44 / "rows.jsonl").exists():
        a44 = ko_rows_at(n44)
        out["note44_beside"] = {x: rescue(a44, items, "MC0", x, every).get("rescue") for x in ("Cap", "Cty", "CapCty", "Rcap")}
    E = collections.defaultdict(list)
    kp = d / "keeplog.jsonl"
    whole = acc.get(("MC0", "clean", "none"), {})
    for line in kp.open() if kp.exists() else []:
        x = json.loads(line)
        if x["family"] == "MC0" and x["kind"] == "clean" and x["id"] in whole and x["energy"] > 0:
            for k, e in x["E"].items():
                E["E_" + k].append(e)
            for k, e in x["rank"].items():
                E["rank_" + k].append(e)
            E["n_cos_ge_0.9"].append(x.get("n_cos_ge_shared"))
    out["energy_MC0_whole"] = {k: round(sum(v) / len(v), 4) for k, v in E.items() if v and None not in v}
    rs = out["MC0"]["rescue"]
    lines.append(f"reading note52 {tag} [{out['role']}]: MC0 {out['MC0']['reading']!r} | " + "; ".join(
        f"{x} rescue {rs[x].get('rescue')} {rs[x].get('rescue_ci')} (net of rot {rs[x].get('rescue_net_rot')}; n {rs[x].get('n')})" for x in KEEPS)
        + f"; MC beside {out['MC']['reading']!r}")  # fmt: skip
    lines.append(f"  note 44 beside (stored run): {out.get('note44_beside')}; E / rank (MC0 whole question): {json.dumps(out['energy_MC0_whole'])}")
    od = out_dir or RES / "ablate_v2" / "nn_v5_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note52.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
