"""nn_fail_read (Zach, 2026-10-28, prereg amendment 58 note 11, item 3): composition failures, read (CPU).

a. Readout (nn_readout --items composition rows): per item, the share of the band's read layers where the bridge (or
   the answer) is the lens's top candidate at the description's end; RM_ok minus RM_fail, 95% bootstrap over bridges.
   Reading: "missing in failures" if ok - fail >= 10 points with the interval above 0 (J++; the logit lens beside).
b. Repair (nn_swap --items fail rows): the fix rate (X's answer) per condition; repair_k10 minus each control (rand, rot,
   and insert_k10: another bridge's lens part), paired per item, 95% bootstrap over bridges. Reading: "writing the
   bridge in repairs composition" if repair_k10 minus the largest control is >= 20 with its interval above 0; "through
   the bridge, not the answer" if repair_k10_noans >= 2/3 of repair_k10.
Writes results/nn_swap/nn_fail_read/<name>.json.

python scripts/nn_fail_read.py NAME --band 12-16 [--readout RUN] [--repair RUN]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEEP: set | None = None  # note 12: --order (nn_ans_read.order_ids)


def boot(by_bridge: dict[str, list[float]], reps: int = 1000) -> list[float]:
    rng, keys, out = random.Random(0), sorted(by_bridge), []
    for _ in range(reps):
        xs = [x for k in (rng.choice(keys) for _ in keys) for x in by_bridge[k]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[int(0.025 * reps)], 1), round(out[int(0.975 * reps) - 1], 1)]


def readout(run: str, lo: int, hi: int) -> dict:
    rows = [json.loads(line) for line in (ROOT / "results/nn_readout" / run / "rows.jsonl").read_text().splitlines()]
    rows = rows if KEEP is None else [r for r in rows if r["id"] in KEEP]
    score = collections.defaultdict(list)  # (lens, what, family, id, bridge) -> top-1 per band layer
    for r in rows:
        if r["site"] == "desc_end" and lo <= r["layer"] <= hi:
            score[(r["lens"], r["what"], r["family"], r["id"], r["bridge"])].append(100.0 * (r["rank"] == 1))
    out = {}
    for lens in ("jlens", "logit"):
        for what in ("bridge", "attr"):
            fam = {f: {k[3]: (k[4], sum(v) / len(v)) for k, v in score.items() if k[:3] == (lens, what, f)} for f in ("RM_ok", "RM_fail")}
            if not fam["RM_ok"] or not fam["RM_fail"]:
                continue
            m = {f: sum(s for _, s in d.values()) / len(d) for f, d in fam.items()}
            # bootstrap over bridges: resample bridges, recompute ok - fail from their items
            by_b = collections.defaultdict(lambda: {"RM_ok": [], "RM_fail": []})
            for f, d in fam.items():
                for b, s in d.values():
                    by_b[b][f].append(s)
            rng, keys, diffs = random.Random(0), sorted(by_b), []
            for _ in range(1000):
                pick = [rng.choice(keys) for _ in keys]
                ok = [s for b in pick for s in by_b[b]["RM_ok"]]
                fail = [s for b in pick for s in by_b[b]["RM_fail"]]
                if ok and fail:
                    diffs.append(sum(ok) / len(ok) - sum(fail) / len(fail))
            diffs.sort()
            ci = [round(diffs[int(0.025 * len(diffs))], 1), round(diffs[int(0.975 * len(diffs)) - 1], 1)]
            diff = m["RM_ok"] - m["RM_fail"]
            out[f"{lens}/{what}"] = {"ok": round(m["RM_ok"], 1), "fail": round(m["RM_fail"], 1), "n_ok": len(fam["RM_ok"]), "n_fail": len(fam["RM_fail"]),
                                     "ok_minus_fail": round(diff, 1), "ci": ci, "missing_in_failures": diff >= 10 and ci[0] > 0}  # fmt: skip
    return out


def repair(run: str) -> dict:
    rows = [json.loads(line) for line in (ROOT / "results/nn_swap" / run / "rows.jsonl").read_text().splitlines()]
    rows = rows if KEEP is None else [r for r in rows if r["id"] in KEEP]
    fix = collections.defaultdict(dict)  # id -> cond -> fixed
    bridge = {}
    for r in rows:
        fix[r["id"]][r["condition"]] = 100.0 * (r["cls"] == "kept")
        bridge[r["id"]] = f"{r['rel']}:{r['x']}"
    conds = sorted({c for d in fix.values() for c in d})
    rate = {c: round(sum(d[c] for d in fix.values() if c in d) / sum(c in d for d in fix.values()), 1) for c in conds}
    out: dict = {"n": len(fix), "fix_rate": rate, "vs": {}}
    for ctl in ("repair_k10_rand", "repair_k10_rot", "insert_k10"):
        if "repair_k10" not in conds or ctl not in conds:
            continue
        by_b = collections.defaultdict(list)
        for i, d in fix.items():
            if "repair_k10" in d and ctl in d:
                by_b[bridge[i]].append(d["repair_k10"] - d[ctl])
        diff = sum(x for v in by_b.values() for x in v) / sum(len(v) for v in by_b.values())
        out["vs"][ctl] = {"diff": round(diff, 1), "ci": boot(by_b)}
    if out["vs"]:
        worst = min(out["vs"].values(), key=lambda v: v["diff"])
        out["repairs"] = worst["diff"] >= 20 and worst["ci"][0] > 0
        if "repair_k10_noans" in rate and rate.get("repair_k10"):
            out["through_bridge_not_answer"] = rate["repair_k10_noans"] >= 2 / 3 * rate["repair_k10"]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--band", required=True)
    ap.add_argument("--readout", default=None)
    ap.add_argument("--repair", default=None)
    ap.add_argument("--order", choices=["after", "before"], default=None, help="note 12: only items with the relation after / before")
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    a = ap.parse_args()
    global KEEP
    if a.order:
        import sys

        sys.path.insert(0, str(ROOT))
        from scripts.nn_ans_read import order_ids

        KEEP = order_ids(a.set, a.order)
    lo, hi = (int(x) for x in a.band.split("-"))
    out = {"order": a.order}
    if a.readout:
        out["readout"] = readout(a.readout, lo, hi)
        for k, v in out["readout"].items():
            print(f"readout {k:14s} ok {v['ok']:5.1f} (n {v['n_ok']})  fail {v['fail']:5.1f} (n {v['n_fail']})  ok-fail {v['ok_minus_fail']:+5.1f} {v['ci']}  missing: {v['missing_in_failures']}")
    if a.repair:
        out["repair"] = repair(a.repair)
        print("repair", json.dumps(out["repair"]))
    d = ROOT / "results/nn_swap/nn_fail_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{a.name}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
