"""nn_cc_read (Zach, 2026-10-29, prereg amendment 58 note 24): the cue-conflict set's three readings, split by description type
(conflict: the description's association is another nationality, the cue; aligned: it is the person's own).
  1 behaviour   MM accuracy by type among gated items (scripts/nn_swap.v4_split: H1 by cand2 or its greedy reply, hop 2, guess); among conflict
                MM errors, the share whose top answer is the cue (chance: one of 33 wrong nationalities), bootstrap over bridges
  2 answer      note 15's rule (Dan's 51.12; scripts/nn_cf_read.note15) on MM rows of each type, per cell, cf_ok pairs
  3 knock-out   note 20's loss gap (MM minus MP, paper10 and its controls) per type, bootstrap over items

python scripts/nn_cc_read.py PREFIX   (PREFIX "" for the 27B, "qwen35_9b_" for the 9B)
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts.nn_cf_read import note15  # noqa: E402

RES = ROOT / "results"
SET = "jsuite_v4cc_test_chat"


def boot_mean(by: dict[str, list[float]], seed: int = 0) -> list[float]:
    rng, keys, out = random.Random(seed), sorted(by), []
    for _ in range(1000):
        xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
        out.append(100 * sum(xs) / max(1, len(xs)))
    out.sort()
    return [round(out[25], 1), round(out[974], 1)]


def main(P: str) -> None:
    items = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "tasks_v2" / SET / "items.jsonl").read_text().splitlines()}
    comp = collections.defaultdict(dict)
    for l in (RES / "tasks_v2" / f"{P}{SET}_competence_cand2_v1" / "items.jsonl").read_text().splitlines():
        r = json.loads(l)
        comp[r["id"]][r["part"]] = r
    from scripts.nn_swap import v4_split  # the gate every other note uses: H1 (cand2 or the greedy reply with other names), hop 2, guess

    split = v4_split(f"{P}{SET}_competence_cand2_v1", f"{P}jsuite_v4cc_cv_v1", SET)
    out: dict = {"prefix": P, "behaviour": {}, "answer": {}, "knockout": {}}
    # 1 behaviour
    for word in ("MM", "MP"):
        for typ in ("conflict", "aligned"):
            ids = [i for i, it in items.items() if it["word"] == word and it["cc_type"] == typ and i in split]  # gated: ok or fail
            acc = [bool(comp[i]["whole"]["correct"]) for i in ids]
            rec = {"n_eligible": len(ids), "whole_acc": round(100 * sum(acc) / max(1, len(acc)), 1)}
            if word == "MM" and typ == "conflict":
                errs = [i for i in ids if not comp[i]["whole"]["correct"]]
                by = collections.defaultdict(list)
                for i in errs:
                    top = (comp[i]["whole"].get("read_top") or "").strip().lower()
                    cue = items[i]["cue"].split()[0].lower()
                    by[items[i]["bridge"]].append(float(bool(top) and (cue.startswith(top) or top.startswith(cue))))
                n_cue = sum(sum(v) for v in by.values())
                rec.update({"n_errors": len(errs), "cue_share_of_errors": round(100 * n_cue / max(1, len(errs)), 1),
                            "cue_share_ci": boot_mean(by) if by else None, "chance": round(100 / 33, 1),
                            "shortcut_taken": bool(by) and boot_mean(by)[0] > 3 * 100 / 33})  # fmt: skip
            out["behaviour"][f"{word}/{typ}"] = rec
    # 2 the answer reading, per type and cell
    runs = sorted(p for p in (RES / "nn_swap").glob(f"{P}nn_n24_*_s?_v1") if (p / "summary.json").exists())
    cells = collections.defaultdict(lambda: collections.defaultdict(dict))
    bridge = {}
    for ri, p in enumerate(runs):
        site = json.loads((p / "manifest.json").read_text())["site"]
        for l in (p / "rows.jsonl").read_text().splitlines():
            r = json.loads(l)
            if r.get("cf_ok") is False:
                continue
            key = f"{ri}:{r['id']}"
            typ = items[r["id"]]["cc_type"]
            cells[(site, r["band"], typ)][key][r["condition"]] = r["cls"]
            bridge[key] = r["x"]
    for (site, band, typ), by in sorted(cells.items()):
        bb = collections.defaultdict(list)
        for k, d in by.items():
            bb[bridge[k]].append(d)
        rec = {"n": len(by)}
        for A in ("own", "rel"):
            rec[A] = note15(bb, [], A)
        out["answer"][f"{site}/{band}/{typ}"] = rec
    # 3 knock-out gap per type
    ko = RES / "ablate_v2" / f"{P}{SET}_ko_cand2_v1" / "rows.jsonl"
    if ko.exists():
        acc = collections.defaultdict(dict)
        for l in ko.read_text().splitlines():
            r = json.loads(l)
            acc[(r["family"], items[r["id"]]["cc_type"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
        rng = random.Random(0)
        for typ in ("conflict", "aligned"):
            mm = sorted(acc.get(("MM", typ, "none"), {}))
            mp = sorted(acc.get(("MP", typ, "none"), {}))
            if not mm or not mp:
                continue

            def loss(fam, cond, sel, typ=typ):
                return 100 * (sum(acc[(fam, typ, "none")][i] for i in sel) - sum(acc[(fam, typ, cond)][i] for i in sel)) / len(sel)

            for cond in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize"):
                if (("MM", typ, cond)) not in acc:
                    continue
                bs = sorted(loss("MM", cond, [rng.choice(mm) for _ in mm]) - loss("MP", cond, [rng.choice(mp) for _ in mp]) for _ in range(2000))
                out["knockout"][f"{typ}/{cond}"] = {"n_MM": len(mm), "n_MP": len(mp), "loss_MM": round(loss("MM", cond, mm), 1),
                                                     "loss_MP": round(loss("MP", cond, mp), 1),
                                                     "gap": round(loss("MM", cond, mm) - loss("MP", cond, mp), 1), "gap_ci": [round(bs[50], 1), round(bs[1949], 1)]}  # fmt: skip
    d = RES / "nn_swap" / "nn_cf_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}v4cc_note24.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out["behaviour"], indent=1))
    for k, v in out["answer"].items():
        print(k, "n", v["n"], "| own:", v["own"]["verdict"], v["own"]["e1"], v["own"]["e2"], v["own"]["e3"], "| rel:", v["rel"]["verdict"])
    print(json.dumps(out["knockout"], indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
