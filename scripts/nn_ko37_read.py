"""nn_ko37_read (Zach, 2026-10-30, prereg amendment 64 note 37): answer kept vs answer only on v4, read (CPU).

Runs (scripts/queues/h200_n37_1030.sh), per model prefix P:
  {P}jsuite_v4_test_chat_ko37_cand2_v1     none, paper10, paper10_rot, paper10_keepA, paper10_keepA_rot, ansJ, ansJ_rot, ansU
                                           (note 20's gate, band, items and batch; paper10 / paper10_rot rerun in the same run so
                                           every comparison is within one run; checked against note 20's stored rows)
  {P}jsuite_v4cc_test_chat_ko37_cand2_v1   the same on the cue-conflict set (descriptive; checked against note 24's stored rows)
  {P}nn_readout_v4cc_v1                    note 26c's per-item readout, for the cue subset (descriptive)
Measures (nn_ko_read's conventions): loss = 100 x (accuracy unedited - accuracy edited) over the gated items (correct_cand2),
per twin and condition; gap = MM loss - MP loss with a 95% bootstrap over bridges (2000 draws, random.Random(0) per statistic,
ko_subsets_v4's clustering: every gated MM and MP item of a bridge resampled together). Beside: the loss among items right
unedited in this run; the paired-twin gap (scenes whose MP and MM are both gated; same bootstrap); dlogp = the mean change in the
answer token's log-prob (edited - unedited).
Reading (per model, v4): ratio = (MM keepA loss - MM keepA_rot loss) / (MM paper10 loss - MM paper10_rot loss)
  "the recall's J-need is its answer's directions" if ratio <= 1/3, the keepA gap < 10 and its interval's upper end < 15;
  "beyond the answer" if ratio >= 2/3, the keepA gap >= 10 and its interval's lower end > 0; otherwise "partly"
  (not read if MM's paper10 - paper10_rot loss is <= 0: the ratio is undefined).
  Beside: ansJ's gap as a share of paper10's gap, ansU's (control) likewise; the answer log-prob change.
Descriptive (v4cc): the same numbers by description type (all, conflict, aligned), and on the conflict items whose J++ readout at
the description's end (note 25's window, scripts.nn_priming_read.windows) has the cue's top-1 share above the item's own answer's
("cue_top1"; needs the readout run).
Writes results/ablate_v2/nn_ko_read/{P}note37.json and prints a table.

python scripts/nn_ko37_read.py PREFIX      (PREFIX "" for the 27B, qwen35_9b_ for the 9B, nem35l_ for Lightning)
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
CONDS = ("paper10", "paper10_rot", "paper10_keepA", "paper10_keepA_rot", "ansJ", "ansJ_rot", "ansU")
STORED = ("paper10", "paper10_rot")  # rerun here; compared with note 20's / note 24's stored rows


def rows_of(run: str) -> dict:
    """(family, condition) -> id -> (correct_cand2, logp)."""
    acc: dict = collections.defaultdict(dict)
    for line in (RES / "ablate_v2" / run / "rows.jsonl").open():
        r = json.loads(line)
        if r.get("kind", "clean") == "clean":
            acc[(r["family"], r["condition"])][r["id"]] = (bool(r["correct_cand2"]), r["logp"])
    return acc


def uid(i: str) -> str:  # j3:chat:v4:MP-w0-00000 -> w0-00000 (the scene, shared by its MP and MM twins)
    return i.split(":")[-1].split("-", 1)[1]


def boot(by: dict, fn, n: int = 2000) -> list | None:
    keys, rng, out = sorted(by), random.Random(0), []
    for _ in range(n):
        v = fn([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
        if v == v:
            out.append(v)
    out.sort()
    return [round(out[int(0.025 * len(out))], 1), round(out[int(0.975 * len(out)) - 1], 1)] if out else None


def mean100(xs: list) -> float:
    return 100 * sum(xs) / len(xs) if xs else float("nan")


def gap_fn(us: list) -> float:
    mm = [x for f, x in us if f == "MM"]
    mp = [x for f, x in us if f == "MP"]
    return mean100(mm) - mean100(mp) if mm and mp else float("nan")


def ratio_fn(us: list) -> float:
    """us: per MM item (keepA loss, keepA_rot loss, paper10 loss, paper10_rot loss), each 1 / 0 / -1."""
    den = sum(u[2] - u[3] for u in us)
    return sum(u[0] - u[1] for u in us) / den if den > 0 else float("nan")


def measures(acc: dict, items: dict, keep, conds: tuple = CONDS) -> dict:
    """Loss per twin and condition, the gap with its bridge bootstrap, the strict loss, the paired-twin gap, dlogp, the ratio."""
    base = {f: {i: v for i, v in acc.get((f, "none"), {}).items() if keep(items[i])} for f in ("MP", "MM")}
    out: dict = {"n": {f: len(v) for f, v in base.items()}, "conditions": {}}
    if not base["MP"] or not base["MM"]:
        return out
    for c in conds:  # note 41 (nn_ko41_read) passes its own conditions; note 37 uses CONDS
        if (("MM", c) not in acc) or (("MP", c) not in acc):
            continue
        ed = {f: acc[(f, c)] for f in ("MP", "MM")}
        units = collections.defaultdict(list)
        rec: dict = {}
        for f in ("MM", "MP"):
            ids = [i for i in base[f] if i in ed[f]]
            for i in ids:
                units[items[i]["bridge"]].append((f, int(base[f][i][0]) - int(ed[f][i][0])))
            right = [i for i in ids if base[f][i][0]]
            rec[f"loss_{f}"] = round(mean100([int(base[f][i][0]) - int(ed[f][i][0]) for i in ids]), 1)
            rec[f"loss_{f}_strict"] = round(mean100([1 - int(ed[f][i][0]) for i in right]), 1)  # among items right unedited here
            rec[f"n_{f}"], rec[f"n_{f}_right_unedited"] = len(ids), len(right)
            rec[f"dlogp_{f}"] = round(sum(ed[f][i][1] - base[f][i][1] for i in ids) / len(ids), 3) if ids else None
        us = [u for v in units.values() for u in v]
        rec["gap"] = round(gap_fn(us), 1)
        rec["gap_ci"] = boot(units, gap_fn)
        rec["gap_strict"] = round(rec["loss_MM_strict"] - rec["loss_MP_strict"], 1)
        # paired twins (beside): scenes whose MP and MM are both gated
        mp_by = {uid(i): i for i in base["MP"] if i in ed["MP"]}
        pairs = collections.defaultdict(list)
        for i in base["MM"]:
            j = mp_by.get(uid(i))
            if j is not None and i in ed["MM"]:
                pairs[items[i]["bridge"]].append((int(base["MM"][i][0]) - int(ed["MM"][i][0])) - (int(base["MP"][j][0]) - int(ed["MP"][j][0])))
        ps = [x for v in pairs.values() for x in v]
        rec["paired"] = {"n_pairs": len(ps), "gap": round(mean100(ps), 1), "gap_ci": boot(pairs, mean100)} if ps else None
        out["conditions"][c] = rec
    cs = out["conditions"]
    if all(c in cs for c in ("paper10", "paper10_rot", "paper10_keepA", "paper10_keepA_rot")):
        by = collections.defaultdict(list)
        for i, (ok, _) in base["MM"].items():
            if all(i in acc[("MM", c)] for c in ("paper10_keepA", "paper10_keepA_rot", "paper10", "paper10_rot")):
                by[items[i]["bridge"]].append(tuple(int(ok) - int(acc[("MM", c)][i][0]) for c in ("paper10_keepA", "paper10_keepA_rot", "paper10", "paper10_rot")))
        num = cs["paper10_keepA"]["loss_MM"] - cs["paper10_keepA_rot"]["loss_MM"]
        den = cs["paper10"]["loss_MM"] - cs["paper10_rot"]["loss_MM"]
        r = ratio_fn([u for v in by.values() for u in v])
        ci = boot(by, lambda us: 100 * ratio_fn(us))
        out["ratio"] = {"keepA_net_MM": round(num, 1), "paper10_net_MM": round(den, 1), "ratio": round(r, 3) if r == r else None,
                        "ratio_ci": [x / 100 for x in ci] if ci else None}  # fmt: skip
        k = cs["paper10_keepA"]
        if r != r:
            out["reading"] = "not read: MM's paper10 - paper10_rot loss <= 0"
        elif r <= 1 / 3 and k["gap"] < 10 and k["gap_ci"][1] < 15:
            out["reading"] = "the recall's J-need is its answer's directions"
        elif r >= 2 / 3 and k["gap"] >= 10 and k["gap_ci"][0] > 0:
            out["reading"] = "beyond the answer"
        else:
            out["reading"] = "partly"
    if "paper10" in cs:
        g = cs["paper10"]["gap"]
        out["share_of_paper10_gap"] = {c: (round(cs[c]["gap"] / g, 2) if g else None) for c in ("ansJ", "ansJ_rot", "ansU", "paper10_keepA", "paper10_keepA_rot") if c in cs}
    return out


def stored_check(new: dict, old_run: str) -> dict:
    """paper10 / paper10_rot rows of this run against the stored run's: same items, same reads, same log-probs?"""
    p = RES / "ablate_v2" / old_run / "rows.jsonl"
    if not p.exists():
        return {"stored_run": old_run, "missing": True}
    old = rows_of(old_run)
    out = {"stored_run": old_run}
    for c in ("none",) + STORED:
        for f in ("MP", "MM"):
            a, b = new.get((f, c), {}), old.get((f, c), {})
            both = set(a) & set(b)
            out[f"{f}/{c}"] = {"n_new": len(a), "n_stored": len(b), "n_both": len(both),
                               "same_correct": sum(a[i][0] == b[i][0] for i in both),
                               "same_logp_bits": sum(a[i][1] == b[i][1] for i in both),
                               "max_abs_dlogp": round(max((abs(a[i][1] - b[i][1]) for i in both), default=0.0), 6)}  # fmt: skip
    return out


def cue_ids(P: str) -> set | None:
    """Conflict items whose J++ top-1 share over the description-end window is higher for the cue than for the item's answer."""
    run = RES / "nn_readout" / f"{P}nn_readout_v4cc_v1" / "rows.jsonl"
    if not run.exists():
        return None
    from scripts.nn_priming_read import windows

    lo, hi = windows(P)["desc_end"]
    hits = collections.defaultdict(list)
    for line in run.open():
        r = json.loads(line)
        if r["site"] == "desc_end" and r["lens"] == "jlens" and lo <= r["layer"] <= hi and r["what"] in ("cue", "attr"):
            hits[(r["id"], r["what"])].append(r["rank"] == 1)
    share = {k: sum(v) / len(v) for k, v in hits.items()}
    return {i for (i, w) in share if w == "cue" and share[(i, "cue")] > share.get((i, "attr"), 0.0)}


def table(name: str, m: dict) -> list[str]:
    lines = [f"{name}: n MP {m['n'].get('MP')} MM {m['n'].get('MM')}"]
    for c, r in m.get("conditions", {}).items():
        pr = r["paired"] or {}
        lines.append(f"  {c:18s} loss MP {r['loss_MP']:6.1f} MM {r['loss_MM']:6.1f}  gap {r['gap']:6.1f} {r['gap_ci']}  "
                     f"paired {pr.get('gap')} {pr.get('gap_ci')} (n {pr.get('n_pairs')})  dlogp MP {r['dlogp_MP']} MM {r['dlogp_MM']}")  # fmt: skip
    if "ratio" in m:
        lines.append(f"  ratio (MM keepA - keepA_rot) / (paper10 - paper10_rot) = {m['ratio']}")
    if "share_of_paper10_gap" in m:
        lines.append(f"  share of paper10's gap: {m['share_of_paper10_gap']}")
    if "reading" in m:
        lines.append(f"  reading: {m['reading']}")
    return lines


def main(P: str, set_name: str | None = None) -> dict:
    """set_name (amendment 68 note 43): read one v4-format set's {P}{set}_ko37_cand2_v1 instead (v4 part only), written to
    {P}{set}_note37.json; default: v4 and v4cc, {P}note37.json."""
    out: dict = {"prefix": P, "v4": {}, "v4cc": {}}
    lines = []
    sets = (("v4", "jsuite_v4_test_chat", f"{P}jsuite_v4_test_chat_ko_cand2_v1"),
            ("v4cc", "jsuite_v4cc_test_chat", f"{P}jsuite_v4cc_test_chat_ko_cand2_v1"))  # fmt: skip
    if set_name:
        out["set"], sets = set_name, (("v4", set_name, f"{P}{set_name}_ko_cand2_v1"),)
    for tag, SET, old in sets:
        run = f"{P}{SET}_ko37_cand2_v1"
        if not (RES / "ablate_v2" / run / "rows.jsonl").exists():
            out[tag] = {"run": run, "missing": True}
            lines.append(f"{tag}: {run} missing")
            continue
        items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
        acc = rows_of(run)
        rec = {"run": run, "stored_check": stored_check(acc, old)}
        if tag == "v4":
            rec["all"] = measures(acc, items, lambda it: True)
            lines += table(f"v4 {P or '27b_'}", rec["all"])
        else:  # descriptive
            cue = cue_ids(P)
            subsets = {"all": lambda it: True, "conflict": lambda it: it.get("cc_type") == "conflict",
                       "aligned": lambda it: it.get("cc_type") == "aligned"}  # fmt: skip
            if cue is not None:
                subsets["cue_top1"] = lambda it: it["id"] in cue
            for s, keep in subsets.items():
                rec[s] = measures(acc, items, keep)
                lines += table(f"v4cc {P or '27b_'} {s} (descriptive)", rec[s])
        sc = rec["stored_check"]
        if not sc.get("missing"):
            lines.append("  stored check (" + sc["stored_run"] + "): " + "; ".join(
                f"{k} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for k, v in sc.items() if k != "stored_run"))
        out[tag] = rec
    d = RES / "ablate_v2" / "nn_ko_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / (f"{P}{set_name}_note37.json" if set_name else f"{P}note37.json")).write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--set", default=None, help="note 43: another v4-format set (e.g. jsuite_v4p4002_test_chat)")
    a = ap.parse_args()
    main(a.prefix, a.set)
