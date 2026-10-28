"""nn_mp_read (Zach, 2026-10-28, prereg amendment 58 note 13): the in-context second hop, read (CPU).

nn_swap runs on jsuite_v3mp (a latent first hop into a made-up passage value). Per condition: the shares answering X's
passage value (kept), D's passage value (donor: the lookup followed the swapped-in entity), D's remembered attribute
(third: D's memory bundle), X's remembered attribute (xmem), other; each minus its share under the controls (k10_rand,
k10_rot), paired per item, 95% bootstrap over bridges; rows pooled over the runs given (donor seeds).
Readings (fixed in note 13), for the lens-part swap insert_k10:
  identity  D's passage value >= 10 points above the larger control, interval above 0, and above D's attribute share
  bundle    D's attribute >= 10 points above the larger control, interval above 0, and above D's passage-value share
  outside   neither, while full_insert (the whole state) moves >= 20 to D's passage value
  (else: none)
and note 10's decomposition on the D-passage share (full / lens / rem / remfix / lensrand).

python scripts/nn_mp_read.py NAME RUN [RUN ...] [--relations cities companies films landmarks]   (note 13 addendum)
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLS = ("kept", "donor", "third", "xmem", "other")


def boot(by: dict[str, list[float]]) -> list[float]:
    rng, keys, out = random.Random(0), sorted(by), []
    for _ in range(1000):
        xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[25], 1), round(out[974], 1)]


def main(name: str, runs: list[str], relations: list[str] | None = None) -> None:
    rows = []
    for i, run in enumerate(runs):
        for line in (ROOT / "results/nn_swap" / run / "rows.jsonl").read_text().splitlines():
            r = json.loads(line)
            if r["family"] == "MP" and (not relations or r["rel"] in relations):
                rows.append({**r, "key": f"{i}:{r['id']}"})  # one key per item and donor seed
    by = collections.defaultdict(dict)  # key -> cond -> cls
    bridge = {}
    for r in rows:
        by[r["key"]][r["condition"]] = r["cls"]
        bridge[r["key"]] = f"{r['rel']}:{r['x']}"
    conds = sorted({c for d in by.values() for c in d})
    share = {c: {k: round(100 * sum(d.get(c) == k for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for k in CLS} for c in conds}
    out: dict = {"runs": runs, "relations": relations, "n": len(by), "share": share, "vs_controls": {}}

    def contrast(cond: str, ctl: str, cls: str) -> dict:
        b = collections.defaultdict(list)
        for key, d in by.items():
            if cond in d and ctl in d:
                b[bridge[key]].append(100.0 * ((d[cond] == cls) - (d[ctl] == cls)))
        xs = [x for v in b.values() for x in v]
        return {"diff": round(sum(xs) / len(xs), 1), "ci": boot(b)} if xs else {}

    ctls = [c for c in ("insert_k10_rand", "insert_k10_rot") if c in conds]
    for cond in conds:
        if cond == "none" or cond in ctls:
            continue
        out["vs_controls"][cond] = {cls: {ctl: contrast(cond, ctl, cls) for ctl in ctls} for cls in ("donor", "third")}
    if "insert_k10" in conds and ctls:
        v = out["vs_controls"]["insert_k10"]
        worst = {cls: min((v[cls][c] for c in ctls), key=lambda z: z["diff"]) for cls in ("donor", "third")}
        s = share["insert_k10"]
        ident = worst["donor"]["diff"] >= 10 and worst["donor"]["ci"][0] > 0 and s["donor"] > s["third"]
        bund = worst["third"]["diff"] >= 10 and worst["third"]["ci"][0] > 0 and s["third"] > s["donor"]
        outside = not ident and not bund and share.get("full_insert", {}).get("donor", 0) >= 20
        out["reading"] = {"identity": ident, "bundle": bund, "outside": outside, "worst_vs_controls": worst}
    if "remove_k10" in share and "remove_k10_rot" in share:  # necessity at the site: kept under the rotated control minus kept
        b = collections.defaultdict(list)
        for key, d in by.items():
            if "remove_k10" in d and "remove_k10_rot" in d:
                b[bridge[key]].append(100.0 * ((d["remove_k10_rot"] == "kept") - (d["remove_k10"] == "kept")))
        xs = [x for v in b.values() for x in v]
        loss = round(sum(xs) / len(xs), 1)
        ci = boot(b)
        out["necessity"] = {"loss_vs_rot": loss, "ci": ci, "needs_lens_part_at_site": loss >= 10 and ci[0] > 0}
        print("necessity", json.dumps(out["necessity"]))
    if all(f"{k}_insert" in share for k in ("full", "lens", "rem", "remfix", "lensrand")):
        t = {k: share[f"{k}_insert"]["donor"] - share["none"]["donor"] for k in ("full", "lens", "rem", "remfix", "lensrand")}
        full = t["full"]
        verdict = ("not read" if full < 10 else "through" if t["lens"] >= 2 / 3 * full and t["remfix"] <= 1 / 3 * full and t["lensrand"] < 10
                   else "around" if t["rem"] >= 2 / 3 * full else "mixed")  # fmt: skip
        out["decomposition"] = {**{k: round(v, 1) for k, v in t.items()}, "verdict": verdict}
    for c in conds:
        print(f"{c:22s} " + "  ".join(f"{k} {share[c][k]:5.1f}" for k in CLS))
    print("reading", json.dumps(out.get("reading")))
    print("decomposition", json.dumps(out.get("decomposition")))
    d = ROOT / "results/nn_swap/nn_mp_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    rels = args[args.index("--relations") + 1 :] if "--relations" in args else None
    runs_ = args[1 : args.index("--relations")] if "--relations" in args else args[1:]
    main(args[0], runs_, rels)
