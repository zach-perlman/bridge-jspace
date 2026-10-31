"""nn_ko51_read (Zach, 2026-10-30, prereg amendment 72 note 51): dose x keepA on v4 seed 4001, read (CPU).

Run (scripts/queues/h200_n51_1030.sh), per model prefix P: {P}jsuite_v4_test_chat_ko51_cand2_v1 (note 20's gate, band and batch;
every position) under paper10, paper10_rot and, for K = 30 and 100: topK, topK_rot, topK_pcasize, topK_keepA, topK_keepA_rot (topK
carries paper10's protection, the clean top-10 letter rows; checked in the smoke). keeplog.jsonl: E_A at each K (the share of topK's
removal energy in A's span, per item, in topK's forward); paper10's rows carry E_A at K = 10 ("retained").
Measures: nn_ko49_read's (loss, gap, bridge bootstrap); ratio_K = (topK_keepA - topK_keepA_rot) / (topK - topK_rot) on MM's loss.
Reading (per K and model; read only where gap_K - topK_pcasize's gap >= 10): "the answer account holds at dose K" if ratio_K <= 1/3;
"beyond the answer at dose K" if ratio_K >= 2/3; otherwise "partly". K = 10 (note 37's keepA ratio, its stored run) beside.
Writes results/ablate_v2/nn_ko_read/{P}note51.json (or --out-dir) and prints one "reading ..." line per K.

python scripts/nn_ko51_read.py PREFIX [--run-dir DIR] [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts.nn_ko41_read import keep_ratio  # noqa: E402
from scripts.nn_ko49_read import ratio_of, rows_at  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"
DOSES = (30, 100)
CONDS = ("paper10", "paper10_rot") + tuple(f"top{k}{s}" for k in DOSES for s in ("", "_rot", "_pcasize", "_keepA", "_keepA_rot"))


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
    d = run_dir or RES / "ablate_v2" / f"{P}{SET}_ko51_cand2_v1"
    n37, n41 = f"{P}{SET}_ko37_cand2_v1", f"{P}{SET}_ko41_cand2_v1"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 51 {P or '27b_'}: {d} missing")
        return out
    acc = rows_at(d)
    m = K.measures(acc, items, lambda it: True, CONDS)
    cs = m["conditions"]
    out["measures"], out["stored_check"] = m, K.stored_check(acc, n41)
    tag = P or "27b_"
    lines = K.table(f"note 51 {tag}", m)
    mm = acc.get(("MM", "none"), {})
    eA = {}
    for line in (d / "keeplog.jsonl").open() if (d / "keeplog.jsonl").exists() else []:
        x = json.loads(line)
        if x["family"] == "MM" and x["id"] in mm and x["energy"] > 0:
            eA.setdefault(x["condition"], []).append(x["E"]["A"])
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        if r["condition"] == "paper10" and r["family"] == "MM" and r.get("retained", {}).get("A") is not None:
            eA.setdefault("paper10", []).append(r["retained"]["A"])
    out["E_A_MM"] = {k: round(sum(v) / len(v), 4) for k, v in eA.items()}
    R = {}
    for k in DOSES:
        t, ps = cs.get(f"top{k}"), cs.get(f"top{k}_pcasize")
        if not t or not ps:
            R[k] = {"label": "not read: conditions missing"}
            continue
        excess = round(t["gap"] - ps["gap"], 1)
        rr = ratio_of(acc, items, f"top{k}_keepA", f"top{k}_keepA_rot", base=(f"top{k}", f"top{k}_rot"))
        r = rr.get("ratio")
        if excess < 10:
            lab = f"not read: gap_K - pcasize gap_K = {excess} < 10"
        elif r is None:
            lab = "not read: topK - topK_rot <= 0 (ratio undefined)"
        else:
            lab = (f"the answer account holds at dose {k}" if r <= 1 / 3 else f"beyond the answer at dose {k}" if r >= 2 / 3 else "partly")
        R[k] = {"label": lab, "ratio": r, "ratio_ci": rr.get("ratio_ci"), "n_MM": rr.get("n_MM"), "gap": t["gap"], "gap_ci": t["gap_ci"],
                "pcasize_gap": ps["gap"], "gap_minus_pcasize": excess, "keepA_gap": cs.get(f"top{k}_keepA", {}).get("gap"),
                "E_A": out["E_A_MM"].get(f"top{k}")}  # fmt: skip
        lines.append(f"reading note51 K{k} {tag}: {lab!r} | " + json.dumps({kk: vv for kk, vv in R[k].items() if kk != "label"}))
    a37 = rows_at(RES / "ablate_v2" / n37) if (RES / "ablate_v2" / n37 / "rows.jsonl").exists() else None
    R["10_beside"] = {"ratio_n37": keep_ratio(a37, items, "A").get("ratio") if a37 else None, "E_A": out["E_A_MM"].get("paper10")}
    lines.append(f"  K = 10 beside (note 37's run): keepA ratio {R['10_beside']['ratio_n37']}, E_A {R['10_beside']['E_A']}")
    out["readings"] = R
    sc = out["stored_check"]
    if not sc.get("missing"):
        lines.append(f"  stored check ({sc['stored_run']}): " + "; ".join(
            f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for c, v in sc.items() if c != "stored_run"))
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note51.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
