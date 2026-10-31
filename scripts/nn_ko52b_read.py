"""nn_ko52b_read (Zach, 2026-10-30, prereg amendment 80 note 52b): note 52's spans against energy-matched random keeps, read (CPU).

Run (scripts/queues/h200_n52b_1030.sh), per model prefix P: {P}jsuite_v5kn2c_test_chat_ko52b_cand2_v1 (note 52's settings: note
44's set, gate, band, batch, words MC MC0, kinds clean step2) under paper10, paper10_rot, paper10_keepShared / keepCapPerp /
keepCtyPerp (rerun), paper10_keepRShared / keepRCapPerp / keepRCtyPerp (random letter-token keeps, the first k rows of note 44's Rcap
pool, k per item the smallest whose share of paper10's removal energy reaches the span's, in paper10's forward) and
paper10_keepSharedNoLit (Shared projected off the item's rows literally in both the capital and the country sets). keeplog.jsonl:
E, rank, the matched sizes; every row carries edit_rel.
Rescue(X) = note 44's (scripts/nn_ko44_read.rescue): 1 - contrast(keepX) / contrast(paper10) on MC0's gated items (contrast = the
whole question's loss minus its step 2's); rescue(X) - rescue(RX) = (c(RX) - c(X)) / c(paper10), bridge bootstrap (2000, seed 0).
Readings (MC0, all gated): "the shared part carries it at matched energy" if rescue(Shared) - rescue(RShared) >= 0.33 with the lower
end > 0; the same rule for CapPerp ("the capital-only part ...") and CtyPerp ("the country-only part ..."); otherwise "not shown at
matched energy" ("not read" if MC0's paper10 contrast is <= 0). keepSharedNoLit's rescue beside.
Writes results/ablate_v2/nn_v5_read/{P}note52b.json (or --out-dir) and prints one "reading ..." line per span.

python scripts/nn_ko52b_read.py PREFIX [--run-dir DIR] [--out-dir DIR]   (PREFIX "" for the 27B, qwen35_9b_, nem35l_)
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
from scripts.nn_ko52_read import ko_rows_at  # noqa: E402
from scripts.nn_v5_mc_read import per_item  # noqa: E402
from scripts.nn_v5_read import boot_ci, items_of  # noqa: E402

RES = ROOT / "results"
MC_SET = "jsuite_v5kn2c_test_chat"
SPANS = {"Shared": "the shared part", "CapPerp": "the capital-only part", "CtyPerp": "the country-only part"}


def diff(acc, items, x: str, keep) -> dict:
    """rescue(keepX) - rescue(keepRX) on MC0 = (c(RX) - c(X)) / c(paper10), per-item contrasts, bridge bootstrap."""
    p, kx, kr = (per_item(acc, "MC0", c, keep) for c in ("paper10", f"paper10_keep{x}", f"paper10_keepR{x}"))
    by = collections.defaultdict(list)
    for i in p:
        if i in kx and i in kr:
            by[items[i]["bridge"]].append((p[i][0] - p[i][1], kx[i][0] - kx[i][1], kr[i][0] - kr[i][1]))
    us = [u for v in by.values() for u in v]
    if not us:
        return {}

    def f(xs):
        cp = sum(u[0] for u in xs) / len(xs)
        return (sum(u[2] for u in xs) - sum(u[1] for u in xs)) / len(xs) / cp if cp > 0 else float("nan")

    v = f(us)
    return {"n": len(us), "diff": round(v, 3) if v == v else None, "ci": boot_ci(by, f)}


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    d = run_dir or RES / "ablate_v2" / f"{P}{MC_SET}_ko52b_cand2_v1"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 52b {P or '27b_'}: {d} missing")
        return out
    items, acc = items_of(MC_SET), ko_rows_at(d)
    every = lambda i: True  # noqa: E731
    tag = P or "27b_"
    lines = []
    resc = {x: rescue(acc, items, "MC0", x, every) for x in ("Shared", "CapPerp", "CtyPerp", "RShared", "RCapPerp", "RCtyPerp", "SharedNoLit")}
    out["rescue"] = resc
    R = {}
    for x, name in SPANS.items():
        dx = diff(acc, items, x, every)
        v = dx.get("diff")
        lab = ("not read: MC0's paper10 contrast <= 0 or conditions missing" if v is None else f"{name} carries it at matched energy"
               if v >= 0.33 and dx["ci"] and dx["ci"][0] > 0 else "not shown at matched energy")  # fmt: skip
        R[x] = {"label": lab, "rescue_minus_random": v, "ci": dx.get("ci"), "n": dx.get("n"), "rescue": resc[x].get("rescue"),
                "rescue_random": resc[f"R{x}"].get("rescue")}  # fmt: skip
        lines.append(f"reading note52b {x} {tag}: {lab!r} | " + json.dumps({k: v_ for k, v_ in R[x].items() if k != "label"}))
    out["readings"] = R
    lines.append(f"  beside: keepSharedNoLit rescue {resc['SharedNoLit'].get('rescue')} {resc['SharedNoLit'].get('rescue_ci')} "
                 f"(n {resc['SharedNoLit'].get('n')}); net of paper10_rot: " + ", ".join(f"{x} {r.get('rescue_net_rot')}" for x, r in resc.items()))
    # E / rank / matched sizes (MC0 whole question) and edit_rel per condition
    whole = acc.get(("MC0", "clean", "none"), {})
    E, kk = collections.defaultdict(list), collections.defaultdict(list)
    kp = d / "keeplog.jsonl"
    for line in kp.open() if kp.exists() else []:
        x = json.loads(line)
        if x["family"] == "MC0" and x["kind"] == "clean" and x["id"] in whole and x["energy"] > 0:
            for k, e in x["E"].items():
                E["E_" + k].append(e)
            for k, e in x["rank"].items():
                E["rank_" + k].append(e)
            for k, e in x.get("k52b", {}).items():
                kk[k].append(float(e))
            if "n_lit_shared_rows" in x:
                kk["n_lit_shared_rows"].append(x["n_lit_shared_rows"])
    out["energy_MC0_whole"] = {k: round(sum(v) / len(v), 4) for k, v in E.items() if v}
    out["matched_sizes_MC0_whole"] = {k: round(sum(v) / len(v), 3) for k, v in kk.items() if v}
    er = collections.defaultdict(list)
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        if r["family"] == "MC0" and r.get("kind") == "clean" and r.get("edit_rel") is not None:
            er[r["condition"]].append(r["edit_rel"])
    out["edit_rel_MC0_whole"] = {c: round(sum(v) / len(v), 6) for c, v in er.items()}
    lines.append(f"  E / rank (MC0 whole question): {json.dumps(out['energy_MC0_whole'])}")
    lines.append(f"  matched sizes (k, reached share, pool): {json.dumps(out['matched_sizes_MC0_whole'])}; edit_rel: {json.dumps(out['edit_rel_MC0_whole'])}")
    od = out_dir or RES / "ablate_v2" / "nn_v5_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note52b.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
