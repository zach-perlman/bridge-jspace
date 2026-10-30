"""ptr_intervals: 95% intervals for the r4 figure's rows 2-5 (Dan 30 Oct), from per-item rows already in results/.

r4_pointer plots, per model, five transfers in points (donor - third answers, over items right unedited, the memory
families pooled): the entity's own passage (ptr.*.swap, which has an interval), one neutral sentence about it, the swap
without the entity's own-word directions, the rotated neutral donor (control), and a probe's subspace on the probe-valid
relations. The CSV stored ratios (neutral / own, noown / own) or points without intervals; here each is recomputed from
the run's rows.jsonl with scripts.jswap.score (the one the runs use: a 95% bootstrap over bridges, 1000 draws, seed 0),
checked against the run's summary.json, and written as new rows of docs/breadth/data.csv with lo / hi:

  ptr.<m>.neutral_pts, ptr.<m>.noown_pts, ptr.<m>.rot_pts, probe.<m>.probe_pts      transfer in points [lo, hi]
  ptr.<m>.neutral_minus_swap                                                      the paired difference, neutral - own
  pos.<m>.all.{all,bridge,context,question}.rot                                   the middle band's rotated control, M - K
                                                                                  (stored in jsuite2_score, never emitted)

scripts/report_breadth.py emits the same rows when it runs in a checkout that has every result (its clean-checkout check
runs are not here), so this script appends them to docs/breadth/data.csv instead of regenerating the file.

uv run python scripts/ptr_intervals.py            # recompute, check against summary.json, print
uv run python scripts/ptr_intervals.py --write    # and write the rows into docs/breadth/data.csv
"""

from __future__ import annotations

import collections
import csv
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from scripts import jswap as JS  # noqa: E402

CSV = REPO / "docs" / "breadth" / "data.csv"
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")
RUNS = {  # model key -> (pointer run, probe-ceiling run)
    "q27": ("jswap/jswap_pointer_v2_s150_v1", "probe_ceiling/probe_ceiling_L32-40_v1"),
    "q9": ("jswap/qwen35_9b_jswap_pointer_v2_s150_v1", "probe_ceiling/qwen35_9b_probe_ceiling_L12-16_v1"),
    "nl": ("jswap/nem35l_jswap_pointer_v2_s150_v1", "probe_ceiling/nem35l_probe_ceiling_L27-33_v1"),
}  # fmt: skip


def rows_of(run: str) -> list[dict]:
    return [json.loads(line) for line in (REPO / "results" / run / "rows.jsonl").read_text().splitlines()]


def pooled(rows: list[dict], cell: str, rels: list[str] | None = None) -> dict:
    sel = [{**r, "family": "memory"} for r in rows if r["family"] in MEMORY and (rels is None or r["rel"] in rels)]
    return JS.score(sel)[f"memory/{cell}"]


def paired_diff(rows: list[dict], a: str, b: str, draws: int = 1000) -> list[float]:
    """The transfer of condition a minus condition b over the same items (the memory families pooled), a 95% bootstrap
    over bridges as JS.score (same seed, same draws): [point, lo, hi], in points."""
    mem = [r for r in rows if r["family"] in MEMORY]
    ok = {r["id"] for r in mem if r["condition"] == "none" and r["cls"] == "kept"}
    cls = {c: {r["id"]: r for r in mem if r["condition"] == c and r["id"] in ok and r["third"]} for c in (a, b)}
    ids = sorted(set(cls[a]) & set(cls[b]))
    val = {i: 100 * (((cls[a][i]["cls"] == "donor") - (cls[a][i]["cls"] == "third"))
                     - ((cls[b][i]["cls"] == "donor") - (cls[b][i]["cls"] == "third"))) for i in ids}  # fmt: skip
    by = collections.defaultdict(list)
    for i in ids:
        by[cls[a][i]["x"]].append(i)
    keys, rng = sorted(by), random.Random(0)
    mean = lambda xs: sum(val[i] for i in xs) / max(1, len(xs))  # noqa: E731
    bs = sorted(mean([i for k in (rng.choice(keys) for _ in keys) for i in by[k]]) for _ in range(draws))
    return [round(mean(ids), 1), round(bs[25], 1), round(bs[974], 1)]


def compute() -> dict[str, dict]:
    out = {}
    for m, (ptr_run, probe_run) in RUNS.items():
        rows, summ = rows_of(ptr_run), json.loads((REPO / "results" / ptr_run / "summary.json").read_text())
        prows, psumm = rows_of(probe_run), json.loads((REPO / "results" / probe_run / "summary.json").read_text())
        cells = {"neutral": ("swap_neutral", rows, summ, ptr_run, None), "noown": ("swap_noown", rows, summ, ptr_run, None),
                 "rot": ("swap_neutral_rot", rows, summ, ptr_run, None)}  # fmt: skip
        for key, (cond, rs, sm, run, _) in cells.items():
            c = pooled(rs, cond)
            assert c == sm[f"memory/{cond}"], (m, cond, c, sm[f"memory/{cond}"])  # recomputed == the run's own summary
            out[f"{m}.{key}"] = {"v": c["transfer"], "ci": c["ci"], "n": c["n"], "src": f"results/{run}/summary.json"}
        valid = psumm["probe_valid_relations"]
        c = pooled(prows, "swap_probe", valid)
        assert c == psumm["memory_valid/swap_probe"], (m, c)
        out[f"{m}.probe"] = {"v": c["transfer"], "ci": c["ci"], "n": c["n"], "src": f"results/{probe_run}/summary.json"}
        d = paired_diff(rows, "swap_neutral", "swap")
        out[f"{m}.diff"] = {"v": d[0], "ci": d[1:], "n": summ["memory/swap"]["n"], "src": f"results/{ptr_run}/rows.jsonl"}
    return out


KEYS = {"neutral": "ptr.{m}.neutral_pts", "noown": "ptr.{m}.noown_pts", "rot": "ptr.{m}.rot_pts",
        "probe": "probe.{m}.probe_pts", "diff": "ptr.{m}.neutral_minus_swap"}  # fmt: skip
WHAT = {"neutral": "neutral-sentence donor, transfer", "noown": "without own-word directions, transfer",
        "rot": "neutral donor, rotated, transfer", "probe": "probe-subspace swap, transfer (probe-valid relations)",
        "diff": "neutral-sentence donor minus same-passage swap, transfer (paired)"}  # fmt: skip


POS = {"q27": "", "q9": "qwen35_9b_", "nl": "nem35l_"}
MODES = {"all": "", "bridge": "_posbridge", "context": "_poscontext", "question": "_posquestion"}


def pos_rot() -> list[dict]:
    """The middle band's rotated control of every position-limited removal: M - K with its interval, as stored in the scored
    runs (paper10_rot, start = all); the all-token one equals ko.<m>.rot."""
    out = []
    for m, pre in POS.items():
        for mode, suf in MODES.items():
            run = f"{pre}jsuite_v2_test_chat_ko_cand2{suf}_v1"
            path = REPO / "results" / "ablate_v2" / "jsuite2_score" / f"{run}.json"
            c = json.loads(path.read_text())["facts"]["paper10_rot/start=all"]["contrasts"]["M-K"]
            out.append({"key": f"pos.{m}.all.{mode}.rot", "figure": "positions", "model": m,
                        "quantity": f"M - K, start all, {'every token' if mode == 'all' else 'pos' + mode} (paper10_rot)",
                        "value": c["diff"], "lo": c["ci"][0], "hi": c["ci"][1], "n": "", "unit": "points",
                        "source": f"results/ablate_v2/jsuite2_score/{run}.json"})  # fmt: skip
    return out


def write(res: dict) -> None:
    with CSV.open() as f:
        reader = csv.DictReader(f)
        head, rows = reader.fieldnames, list(reader)
    extra = pos_rot()
    drop = {KEYS[k].format(m=m) for m in RUNS for k in KEYS} | {r["key"] for r in extra}
    rows = [r for r in rows if r["key"] not in drop]
    at = max(i for i, r in enumerate(rows) if r["key"].startswith("ptr.nl."))
    new = []
    for m in RUNS:
        for k, tmpl in KEYS.items():
            c = res[f"{m}.{k}"]
            new.append({"key": tmpl.format(m=m), "figure": "pointer" if tmpl.startswith("ptr") else "probe", "model": m,
                        "quantity": WHAT[k], "value": c["v"], "lo": c["ci"][0], "hi": c["ci"][1], "n": c["n"],
                        "unit": "points", "source": c["src"]})  # fmt: skip
    rows[at + 1 : at + 1] = new
    last = max(i for i, r in enumerate(rows) if r["key"].startswith("pos.nl."))
    rows[last + 1 : last + 1] = extra
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=head, lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    res = compute()
    for k, c in res.items():
        print(f"{k:12s} {c['v']:6.1f} [{c['ci'][0]:6.1f}, {c['ci'][1]:6.1f}]  n {c['n']}")
    if "--write" in sys.argv:
        write(res)
        print(f"wrote {len(res)} rows into {CSV.relative_to(REPO)}")
