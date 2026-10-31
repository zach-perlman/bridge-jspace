"""nn_swap38_read (Zach, 2026-10-30, prereg amendment 65 note 38): the size and semantics loopholes of notes 11-13, read (CPU).

Runs (scripts/queues/h200_n38_1030.sh), per model prefix P and band B (9B 12-16, 27B 32-40, Lightning 27-33):
  {P}nn38_L{B}_v1    note 11's jobs at the band: v3 rendering 0, RM (every eligible item) and PM (80, seeded), donor seed 0,
                     the description's last token (PM: the mention). The raw arms, rerun in-run: insert_k10, insert_k10_rot,
                     insert_k10_noansrel, insert_k10_noansrelctl, clamp, clamp_null, clamp_noans. Note 38's arms:
                     insert_k10_noansrel_nm / _x2 / _x4, insert_k10_noansoff, insert_k10_noansform (people), insert_relans,
                     clamp_noans_nm.
  {P}nn38_sweep_v1   note 11's sweep windows, RM and PM 80 each: insert_k10, insert_k10_rot, insert_k10_noansrel_nm,
                     insert_relans.
Stored check: every raw arm's rows (window, word, id) against the stored rows of the same jobs: insert_k10
{P}nn_ans_L{B}_s0_v1 (note 11); insert_k10_noansrel / _noansrelctl {P}nn_ans2_L{B}_s0_v1 (note 11 addendum); clamp /
clamp_null / clamp_noans {P}nn_clampnoans_L{B}_v1 (note 13); insert_k10_rot {P}nn_swap_L{B}_v1 (note 9, seed-0 donors); the
sweep's insert_k10 {P}nn_ans_sweep_v1. A row is identical if its pick and class are; donors and thirds are compared too.
Measures (note 11's): transfer = donor - third over the items kept unedited in this run (jswap.score; third counted on items
with a third), 95% bootstrap over bridges (1000 draws, random.Random(0) per cell). Beyond rotated = transfer(cond) - transfer(insert_k10_rot);
the clamp arms beyond clamp_null. share = beyond(cond) / beyond(insert_k10) (clamp arms: / beyond(clamp)). Differences and
shares carry a paired bootstrap over bridges (1000 draws, random.Random(0); every cell on the same resample).
Readings (per model; RM, the insert donor; PM reported the same way; not read if insert_k10 beyond rotated < 10, note 11's rule):
  B1  noansrel_nm share <= 1/3: "inert at matched size"; above: "the null was partly a size effect" (the slide says "mostly")
  B2  noansoff share >= 2/3 and noansrel share <= 1/3: "the scrub is specific to the asked relation"; otherwise "not met"
  B3  relans share >= 2/3: "the answer subspace is sufficient"; otherwise "not met"
  B1 inert + B2 + B3: "necessary, sufficient, specific and size-controlled"
Descriptive: the norm shares (rows' share_rel, share_c, share_off, share_form, scrub_kept_*; clamp_ratio), as means over the
word's kept items (bridge bootstrap) and over all its items; the dose curve (noansrel x1 / nm / x2 / x4, with the edit's norm
as a multiple of the swap's: sqrt(scrub_kept_rel) x 1 / 2 / 4, nm 1); noansform on people items beside insert_k10, noansrel and
noansoff on the same items; the clamp arms; the sweep table per window (onset = the first window with transfer >= 10, note
11's sweep rule, raw and beyond rotated; note 11's stored insert_ans and insert_k10 onsets beside, from {P}nn_ans_sweep_v1).
Writes results/nn_swap/nn38_read/{P}note38.json (or --name) and prints a table.

python scripts/nn_swap38_read.py PREFIX [--band-run R] [--sweep-run R] [--name N]
       (PREFIX "" for the 27B, qwen35_9b_ for the 9B, nem35l_ for Lightning)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

RES = ROOT / "results" / "nn_swap"
WORDS = ("RM", "PM")
SWAP, ROT = "insert_k10", "insert_k10_rot"
REL, NM, X2, X4 = "insert_k10_noansrel", "insert_k10_noansrel_nm", "insert_k10_noansrel_x2", "insert_k10_noansrel_x4"
OFF, FORM, RELANS, RELCTL = "insert_k10_noansoff", "insert_k10_noansform", "insert_relans", "insert_k10_noansrelctl"
INSERT = (SWAP, ROT, REL, RELCTL, NM, X2, X4, OFF, FORM, RELANS)
CLAMP = ("clamp", "clamp_null", "clamp_noans", "clamp_noans_nm")
STORED = {SWAP: "nn_ans_L{B}_s0_v1", REL: "nn_ans2_L{B}_s0_v1", RELCTL: "nn_ans2_L{B}_s0_v1", "clamp": "nn_clampnoans_L{B}_v1",
          "clamp_null": "nn_clampnoans_L{B}_v1", "clamp_noans": "nn_clampnoans_L{B}_v1", ROT: "nn_swap_L{B}_v1"}  # fmt: skip
STATS = ("share_rel", "share_c", "share_off", "share_form", "scrub_kept_rel", "scrub_kept_off", "scrub_kept_form")


def load(run: str) -> list[dict]:
    p = RES / run / "rows.jsonl"
    return [json.loads(line) for line in p.open()] if p.exists() else []


def tr(rs: list[dict]) -> float | None:
    """jswap.score's transfer: 100 (donor - third) / n over rows with a third entity."""
    wt = [r for r in rs if r["third"]]
    return 100 * (sum(r["cls"] == "donor" for r in wt) - sum(r["cls"] == "third" for r in wt)) / len(wt) if wt else None


def ci(vals: list[float]) -> list | None:
    vals = sorted(v for v in vals if v is not None and math.isfinite(v))
    if len(vals) < 20:
        return None
    return [round(vals[int(0.025 * len(vals))], 2), round(vals[min(len(vals) - 1, int(0.975 * len(vals)))], 2)]


def boot(cells: dict[str, list[dict]], fn, n: int = 1000) -> list | None:
    """Paired bootstrap over bridges: every cell's rows of the resampled bridges; fn(transfers by cell)."""
    grouped = {c: collections.defaultdict(list) for c in cells}
    for c, rs in cells.items():
        for r in rs:
            if r["third"]:
                grouped[c][r["x"]].append(r)
    keys = sorted({k for g in grouped.values() for k in g})
    if not keys:
        return None
    rng, out = random.Random(0), []
    for _ in range(n):
        ks = [rng.choice(keys) for _ in keys]
        t = {c: tr([r for k in ks for r in grouped[c].get(k, [])]) for c in cells}
        out.append(None if any(v is None for v in t.values()) else fn(t))
    return ci(out)


def ratio(num: float | None, den: float | None) -> float | None:
    return None if num is None or den is None or den <= 0 else num / den


class Cells:
    """Rows of one run by (window, word, condition), restricted to the ids kept unedited in the window (jswap.score's set)."""

    def __init__(self, rows: list[dict]):
        self.by: dict = collections.defaultdict(list)
        ok = {(r["band"], r["id"]) for r in rows if r["condition"] == "none" and r["cls"] == "kept"}
        self.all: dict = collections.defaultdict(list)
        for r in rows:
            self.all[(r["band"], r["family"], r["condition"])].append(r)
            if (r["band"], r["id"]) in ok:
                self.by[(r["band"], r["family"], r["condition"])].append(r)

    def get(self, tag: str, word: str, cond: str, rel: str | None = None, kept: bool = True) -> list[dict]:
        rs = (self.by if kept else self.all).get((tag, word, cond), [])
        return [r for r in rs if rel is None or r["rel"] == rel]


def table(cells: Cells, tag: str, word: str, conds: tuple, base: str, ctl: str, rel: str | None = None) -> dict:
    """Per condition: n, transfer (bridge bootstrap), beyond the control (paired), and the share of base's beyond (paired)."""
    rs = {c: cells.get(tag, word, c, rel) for c in conds}
    out = {}
    t = {c: tr(v) for c, v in rs.items()}
    for c in conds:
        if not rs[c]:
            continue
        cell = {"n": len(rs[c]), "transfer": round(t[c], 1) if t[c] is not None else None, "ci": boot({"c": rs[c]}, lambda v: v["c"]),
                "kept": round(100 * sum(r["cls"] == "kept" for r in rs[c]) / len(rs[c]), 1)}  # fmt: skip
        if rs.get(ctl) and c != ctl:
            b = None if t[c] is None or t[ctl] is None else t[c] - t[ctl]
            cell["beyond"] = None if b is None else round(b, 1)
            cell["beyond_ci"] = boot({"c": rs[c], "k": rs[ctl]}, lambda v: v["c"] - v["k"])
            if rs.get(base) and c != base:
                bb = None if t[base] is None or t[ctl] is None else t[base] - t[ctl]
                cell["share"] = None if ratio(b, bb) is None else round(ratio(b, bb), 3)
                cell["share_ci"] = boot({"c": rs[c], "k": rs[ctl], "s": rs[base]}, lambda v: ratio(v["c"] - v["k"], v["s"] - v["k"]))
                cell["raw_share"] = None if ratio(t[c], t[base]) is None else round(ratio(t[c], t[base]), 3)
        out[c] = cell
    return out


def readings(tab: dict) -> dict:
    sw = tab.get(SWAP, {}).get("beyond")
    sh = {c: tab.get(c, {}).get("share") for c in (NM, OFF, REL, RELANS)}
    if sw is None or sw < 10:
        return {"swap_beyond_rot": sw, "B1": "not read (swap beyond rotated < 10)", "B2": "not read", "B3": "not read", "all": False}
    b1 = None if sh[NM] is None else "inert at matched size" if sh[NM] <= 1 / 3 else "the null was partly a size effect (slide wording: mostly)"
    b2 = None if sh[OFF] is None or sh[REL] is None else (
        "the scrub is specific to the asked relation" if sh[OFF] >= 2 / 3 and sh[REL] <= 1 / 3 else "not met")
    b3 = None if sh[RELANS] is None else "the answer subspace is sufficient" if sh[RELANS] >= 2 / 3 else "not met"
    allok = b1 == "inert at matched size" and b2 == "the scrub is specific to the asked relation" and b3 == "the answer subspace is sufficient"
    return {"swap_beyond_rot": sw, **{f"share_{k}": v for k, v in zip(("nm", "off", "rel", "relans"), sh.values())}, "B1": b1, "B2": b2, "B3": b3,
            "all": "necessary, sufficient, specific and size-controlled" if allok else False}  # fmt: skip


def mean_stat(rs: list[dict], stat: str) -> dict:
    vals = [(r["x"], r[stat]) for r in rs if r.get(stat) is not None]
    if not vals:
        return {}
    by = collections.defaultdict(list)
    for x, v in vals:
        by[x].append(v)
    keys, rng, bs = sorted(by), random.Random(0), []
    for _ in range(1000):
        s = [v for k in (rng.choice(keys) for _ in keys) for v in by[k]]
        bs.append(sum(s) / len(s))
    return {"n": len(vals), "mean": round(sum(v for _, v in vals) / len(vals), 4), "median": round(sorted(v for _, v in vals)[len(vals) // 2], 4), "ci": ci(bs)}


def compare(ours: list[dict], stored: list[dict], cond: str) -> dict:
    """Rows of cond matched by (window, word, id): how many are identical (pick and class), and with the same donor and third."""
    key = lambda r: (r["band"], r["family"], r["id"])  # noqa: E731
    mine, st = ({key(r): r for r in rs if r["condition"] == cond} for rs in (ours, stored))
    keys = [k for k in mine if k in st]
    return {"ours": len(mine), "common": len(keys), "identical": sum(mine[k]["pick"] == st[k]["pick"] and mine[k]["cls"] == st[k]["cls"] for k in keys),
            "same_donor_third": sum(mine[k]["donor"] == st[k]["donor"] and mine[k]["third"] == st[k]["third"] for k in keys),
            "mismatch": [list(k) for k in keys if mine[k]["pick"] != st[k]["pick"]][:5]}  # fmt: skip


def stored_check(ours: list[dict], P: str, band: str) -> dict:
    out = {}
    for run in sorted({P + v.format(B=band) for v in STORED.values()}):
        st = load(run)
        if not st:
            out[run] = {"missing": True}
            continue
        out[run] = {c: compare(ours, st, c) for c in ("none", *(c for c, v in STORED.items() if P + v.format(B=band) == run))}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix")
    ap.add_argument("--band-run", default=None)
    ap.add_argument("--sweep-run", default=None)
    ap.add_argument("--name", default=None)
    a = ap.parse_args()
    P = a.prefix
    out: dict = {"prefix": P}
    band_run = a.band_run or next((r.name for r in sorted(RES.glob(f"{P}nn38_L*_v1"))), None)
    if band_run and (RES / band_run / "rows.jsonl").exists():
        man = json.loads((RES / band_run / "manifest.json").read_text())
        B = man["bands"][0]
        tag = f"L{B}"
        rows = load(band_run)
        cells = Cells(rows)
        out["band"] = {"run": band_run, "band": B, "git_commit": man.get("git_commit"), "words": {}}
        out["band"]["stored_check"] = stored_check(rows, P, B)
        for w in WORDS:
            ins = table(cells, tag, w, INSERT, SWAP, ROT)
            clamp = table(cells, tag, w, CLAMP, "clamp", "clamp_null")
            n38_rows = cells.get(tag, w, NM)
            n38_all = cells.get(tag, w, NM, kept=False)
            stats = {s: {"kept_items": mean_stat(n38_rows, s), "all_items": mean_stat(n38_all, s)} for s in STATS}
            stats["clamp_ratio"] = {"kept_items": mean_stat(cells.get(tag, w, "clamp_noans_nm"), "clamp_ratio"),
                                    "all_items": mean_stat(cells.get(tag, w, "clamp_noans_nm", kept=False), "clamp_ratio")}  # fmt: skip
            sk = stats["scrub_kept_rel"]["kept_items"]
            root = (sum(math.sqrt(r["scrub_kept_rel"]) for r in n38_rows if r.get("scrub_kept_rel") is not None) / max(1, sum(r.get("scrub_kept_rel") is not None for r in n38_rows))) if sk else None
            dose = {c: {**{k: ins.get(c, {}).get(k) for k in ("n", "transfer", "beyond", "beyond_ci", "share", "share_ci")},
                        "edit_norm_vs_swap": None if root is None else round(m * root, 3) if m else 1.0}
                    for c, m in ((REL, 1), (NM, None), (X2, 2), (X4, 4))}  # fmt: skip
            people = table(cells, tag, w, (SWAP, ROT, REL, OFF, FORM), SWAP, ROT, rel="people")
            out["band"]["words"][w] = {"insert": ins, "clamp": clamp, "readings": readings(ins), "norm_shares": stats, "dose": dose, "people_form": people}
    else:
        out["band"] = {"missing": band_run}
    sweep_run = a.sweep_run or f"{P}nn38_sweep_v1"
    rows = load(sweep_run)
    if rows:
        cells = Cells(rows)
        tags = sorted({r["band"] for r in rows}, key=lambda t: int(t[1:].split("-")[0]))
        sw: dict = {"run": sweep_run, "windows": {}, "onset": {}}
        stored = load(f"{P}nn_ans_sweep_v1")
        scells = Cells(stored) if stored else None
        for w in WORDS:
            for tag in tags:
                sw["windows"][f"{tag}/{w}"] = table(cells, tag, w, (SWAP, ROT, NM, RELANS), SWAP, ROT)
            for c in (SWAP, NM, RELANS):
                ser = {k: [(tag, sw["windows"][f"{tag}/{w}"].get(c, {}).get(k)) for tag in tags] for k in ("transfer", "beyond")}
                sw["onset"][f"{w}/{c}"] = {k2: next((t for t, v in ser[k] if v is not None and v >= 10), None) for k, k2 in (("transfer", "raw"), ("beyond", "beyond_rot"))}
            if scells:
                for c in ("insert_ans", SWAP):
                    ser = [(tag, tr(scells.get(tag, w, c))) for tag in tags]
                    sw["onset"][f"{w}/stored_note11/{c}"] = {"raw": next((t for t, v in ser if v is not None and v >= 10), None),
                                                             "series": {t: None if v is None else round(v, 1) for t, v in ser}}  # fmt: skip
        sw["stored_check"] = {f"{P}nn_ans_sweep_v1": {c: compare(rows, stored, c) for c in ("none", SWAP)}} if stored else {"missing": f"{P}nn_ans_sweep_v1"}
        out["sweep"] = sw
    else:
        out["sweep"] = {"missing": sweep_run}
    d = RES / "nn38_read"
    d.mkdir(exist_ok=True)
    (d / f"{a.name or P + 'note38'}.json").write_text(json.dumps(out, indent=1) + "\n")
    # the table
    b = out["band"]
    if "words" in b:
        print(f"note 38, {b['run']} (band L{b['band']}, commit {str(b['git_commit'])[:8]})")
        for c, v in b["stored_check"].items():
            print(f"stored check {c:28s} {v}")
        for w, x in b["words"].items():
            print(f"--- {w}")
            for c, cell in {**x["insert"], **x["clamp"]}.items():
                print(f"{w} {c:26s} n {cell['n']:4d}  transfer {cell['transfer'] if cell['transfer'] is not None else float('nan'):+6.1f} {cell['ci']}"
                      f"  beyond {cell.get('beyond')} {cell.get('beyond_ci')}  share {cell.get('share')} {cell.get('share_ci')}  raw share {cell.get('raw_share')}")  # fmt: skip
            print(f"{w} reading {x['readings']}")
            print(f"{w} norm shares " + "  ".join(f"{s} {v['kept_items'].get('mean')} {v['kept_items'].get('ci')}" for s, v in x["norm_shares"].items()))
            print(f"{w} dose " + "  ".join(f"{c.split('_')[-1]}: norm x{v['edit_norm_vs_swap']} beyond {v['beyond']} share {v['share']}" for c, v in x["dose"].items()))
            print(f"{w} people " + "  ".join(f"{c}: {v['transfer']} beyond {v.get('beyond')} share {v.get('share')} (n {v['n']})" for c, v in x["people_form"].items()))
    s = out["sweep"]
    if "windows" in s:
        print(f"sweep {s['run']}; stored check {s['stored_check']}")
        for k, cellset in s["windows"].items():
            print(f"{k:12s} " + "  ".join(f"{c}: {v['transfer']} (beyond {v.get('beyond')})" for c, v in cellset.items()))
        for k, v in s["onset"].items():
            print(f"onset {k:32s} {v}")


if __name__ == "__main__":
    main()
