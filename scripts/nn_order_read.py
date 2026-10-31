"""nn_order_read (Zach, 2026-10-29, prereg amendment 59 note 27): v4's knock-out with the question first against passage first.
  1 the split with the question first: MM - MP paper10 loss gap (as note 20), bootstrap over items (2000, seed 0)
  2 order effect: items gated in both orders, per-item paper10 loss (none minus paper10), question first minus passage first;
    cluster bootstrap over bridges. MP: "leans more on the J-space with the question first" if >= 10 points with its interval
    above 0; "no order effect" if the interval lies within +-10; else unclear. MM beside.
  3 competence by order.
python scripts/nn_order_read.py PREFIX
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def rows(run: str) -> dict:
    acc = collections.defaultdict(dict)
    for line in (RES / "ablate_v2" / run / "rows.jsonl").open():
        r = json.loads(line)
        acc[(r["family"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
    return acc


def main(P: str) -> None:
    items = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "tasks_v2" / "jsuite_v4_test_chat" / "items.jsonl").open()}
    pf, qf = rows(f"{P}jsuite_v4_test_chat_ko_cand2_v1"), rows(f"{P}jsuite_v4qf_test_chat_ko_cand2_v1")
    out: dict = {"prefix": P, "split_qf": {}, "order": {}, "competence": {}}
    rng = random.Random(0)

    def loss(acc, fam, cond, sel):
        return 100 * (sum(acc[(fam, "none")][i] for i in sel) - sum(acc[(fam, cond)][i] for i in sel)) / len(sel)

    for cond in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize"):
        mm, mp = sorted(qf.get(("MM", "none"), {})), sorted(qf.get(("MP", "none"), {}))
        if not mm or not mp or ("MM", cond) not in qf:
            continue
        bs = sorted(loss(qf, "MM", cond, [rng.choice(mm) for _ in mm]) - loss(qf, "MP", cond, [rng.choice(mp) for _ in mp]) for _ in range(2000))
        out["split_qf"][cond] = {"n_MM": len(mm), "n_MP": len(mp), "loss_MM": round(loss(qf, "MM", cond, mm), 1), "loss_MP": round(loss(qf, "MP", cond, mp), 1),
                                 "gap": round(loss(qf, "MM", cond, mm) - loss(qf, "MP", cond, mp), 1), "gap_ci": [round(bs[50], 1), round(bs[1949], 1)]}  # fmt: skip
    for fam in ("MP", "MM"):
        both = sorted(set(pf.get((fam, "none"), {})) & set(qf.get((fam, "none"), {})))
        by = collections.defaultdict(list)
        for i in both:
            d = (qf[(fam, "none")][i] - qf[(fam, "paper10")][i]) - (pf[(fam, "none")][i] - pf[(fam, "paper10")][i])
            by[items[i]["bridge"]].append(d)
        keys, draws = sorted(by), []
        for _ in range(2000):
            xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
            draws.append(100 * sum(xs) / len(xs))
        draws.sort()
        est = 100 * sum(x for v in by.values() for x in v) / max(1, len(both))
        ci = [round(draws[50], 1), round(draws[1949], 1)]
        rec = {"n_both": len(both), "n_pf_only": len(set(pf.get((fam, "none"), {})) - set(both)), "n_qf_only": len(set(qf.get((fam, "none"), {})) - set(both)),
               "loss_pf": round(loss(pf, fam, "paper10", both), 1) if both else None, "loss_qf": round(loss(qf, fam, "paper10", both), 1) if both else None,
               "diff_qf_minus_pf": round(est, 1), "ci": ci}  # fmt: skip
        if fam == "MP":
            rec["reading"] = ("leans more on the J-space with the question first" if est >= 10 and ci[0] > 0 else
                              "no order effect" if ci[0] > -10 and ci[1] < 10 else "unclear")  # fmt: skip
        out["order"][fam] = rec
    for tag, run in (("passage_first", f"{P}jsuite_v4_test_chat_competence_cand2_v1"), ("question_first", f"{P}jsuite_v4qf_test_chat_competence_cand2_v1")):
        parts = collections.defaultdict(dict)
        for line in (RES / "tasks_v2" / run / "items.jsonl").open():
            r = json.loads(line)
            parts[r["id"]][r["part"]] = bool(r["correct"])
        for w in ("MP", "MM"):
            ids = [i for i in parts if f":{w}-" in i]
            out["competence"][f"{tag}/{w}"] = {k: round(100 * sum(parts[i].get(k, False) for i in ids) / len(ids), 1) for k in ("whole", "step1", "step2")}
    d = RES / "ablate_v2" / "nn_order_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}v4qf_n27.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    print("reading:", out["order"].get("MP", {}).get("reading"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
