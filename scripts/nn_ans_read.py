"""nn_ans_read (Zach, 2026-10-28, prereg amendment 58 note 11): bridge or answer, read (CPU).

Band runs (one per donor seed): per word and donor (insert, latent), the transfer (jswap.score: donor - third, 95%
bootstrap over bridges) under k10, noans, noansctl, ans, ansctl, rand and rot, with rows pooled over the seeds and per
seed; the removal's kept share under remove_k10, remove_k10_noans and remove_k10_rot. Note 11's readings (RM, per donor;
not read if k10 < 10): "bridge" if noans >= 2/3 k10; "answer" if noans <= 1/3 k10 and noansctl >= 2/3 k10; else
"mixed". The answer alone "suffices" if ans >= 2/3 k10 with ansctl < 10.
Note 11 addendum: the same rule at the narrower scrubs, noansrel (the relation's answers) and noansown (X's and D's
own), each against its own same-size control (pass the addendum runs with the note 11 runs; rows are pooled).
Sweep run: per word and condition, the transfer by window and its onset (the first window with transfer >= 10); "the
bridge acts before the answer" if {src}_k10_noans's onset is at least one window earlier than {src}_ans's.
Writes results/nn_swap/nn_ans_read/<name>.json.

python scripts/nn_ans_read.py NAME --band RUN [RUN ...] [--sweep RUN]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
from scripts import jswap as JS  # noqa: E402

RES = ROOT / "results" / "nn_swap"
KEEP: set | None = None  # note 12: --order keeps the items whose question puts the relation after (or before) the bridge


def order_ids(set_name: str, order: str) -> set:
    """Note 12: ids whose question names the relation after the bridge or its description ("The novelist who wrote X was
    of which nationality?"), or before it (it starts with a wh-word)."""
    wh = re.compile(r"^(which|in which|what|who|where|when|how)\b", re.IGNORECASE)
    out = set()
    for line in (ROOT / "data/tasks_v2" / set_name / "items.jsonl").read_text().splitlines():
        it = json.loads(line)
        if bool(wh.match(it["question"].strip())) == (order == "before"):
            out.add(it["id"])
    return out


def rows_of(run: str) -> list[dict]:
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    return rows if KEEP is None else [r for r in rows if r["id"] in KEEP]


def band_reading(runs: list[str]) -> dict:
    per_seed = {run: JS.score(rows_of(run)) for run in runs}
    pooled = JS.score([r for run in runs for r in rows_of(run)])
    out: dict = {"runs": runs, "pooled": pooled, "per_seed": per_seed, "reading": {}}
    for word in sorted({k.split("/")[0] for k in pooled}):
        for src in ("insert", "latent"):
            t = {c: pooled.get(f"{word}/{src}_{c}", {}).get("transfer") for c in ("k10", "k10_noans", "k10_noansctl", "ans", "ansctl", "k10_rand", "k10_rot")}
            if t["k10"] is None or t["k10_noans"] is None:
                continue
            k10 = t["k10"]
            if k10 < 10:
                verdict = "not read"
            elif t["k10_noans"] >= 2 / 3 * k10:
                verdict = "bridge"
            elif t["k10_noans"] <= 1 / 3 * k10 and (t["k10_noansctl"] or 0) >= 2 / 3 * k10:
                verdict = "answer"
            else:
                verdict = "mixed"
            suffices = k10 >= 10 and t["ans"] is not None and t["ans"] >= 2 / 3 * k10 and (t["ansctl"] or 0) < 10
            seeds = {run: per_seed[run].get(f"{word}/{src}_k10_noans", {}).get("transfer") for run in runs}
            out["reading"][f"{word}/{src}"] = {**t, "noans_share": round(t["k10_noans"] / k10, 2) if k10 else None,
                                               "verdict": verdict, "answer_alone_suffices": suffices, "noans_per_seed": seeds}  # fmt: skip
            for scrub in ("noansrel", "noansown"):  # note 11 addendum: the same rule at the narrower scrubs
                s, c = (pooled.get(f"{word}/{src}_k10_{x}", {}).get("transfer") for x in (scrub, scrub + "ctl"))
                if s is None or c is None:
                    continue
                v = ("not read" if k10 < 10 else "bridge" if s >= 2 / 3 * k10 else "answer" if s <= 1 / 3 * k10 and c >= 2 / 3 * k10 else "mixed")
                out["reading"][f"{word}/{src}/{scrub}"] = {"k10": k10, scrub: s, scrub + "ctl": c, "share": round(s / k10, 2) if k10 else None,
                                                          "ctl_share": round(c / k10, 2) if k10 else None, "verdict": v}  # fmt: skip
        kept = {c: pooled.get(f"{word}/{c}", {}).get("kept") for c in ("none", "remove_k10", "remove_k10_noans", "remove_k10_rot",
                                                                         "remove_k10_noansrel", "remove_k10_noansown")}  # fmt: skip
        if kept["remove_k10_noans"] is not None or kept["remove_k10_noansrel"] is not None:
            out["reading"][f"{word}/removal_kept"] = kept
    return out


def sweep_reading(run: str) -> dict:
    rows = rows_of(run)
    out: dict = {"run": run, "windows": {}, "onset": {}, "reading": {}}
    tags = sorted({r["band"] for r in rows}, key=lambda t: int(t[1:].split("-")[0]))
    for tag in tags:
        out["windows"][tag] = JS.score([r for r in rows if r["band"] == tag])
    keys = sorted({k for s in out["windows"].values() for k in s})
    for key in keys:
        series = [(tag, out["windows"][tag].get(key, {}).get("transfer")) for tag in tags]
        out["onset"][key] = next((tag for tag, v in series if v is not None and v >= 10), None)
    for word in sorted({k.split("/")[0] for k in keys}):
        for src in ("insert", "latent"):
            b, a = out["onset"].get(f"{word}/{src}_k10_noans"), out["onset"].get(f"{word}/{src}_ans")
            if b is None and a is None:
                continue
            idx = {t: i for i, t in enumerate(tags)}
            before = b is not None and (a is None or idx[b] < idx[a])
            out["reading"][f"{word}/{src}"] = {"noans_onset": b, "ans_onset": a, "bridge_before_answer": before}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--band", nargs="+", default=[])
    ap.add_argument("--sweep", default=None)
    ap.add_argument("--order", choices=["after", "before"], default=None, help="note 12: only items with the relation after / before")
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    a = ap.parse_args()
    global KEEP
    if a.order:
        KEEP = order_ids(a.set, a.order)
    out = {"order": a.order}
    if a.band:
        out["band"] = band_reading(a.band)
        for k, v in out["band"]["reading"].items():
            if k.endswith("removal_kept"):
                print(f"{k:22s} kept {v}")
            elif k.count("/") == 2:
                print(f"{k:22s} {v}")
            else:
                print(f"{k:12s} k10 {v['k10']:+5.1f}  noans {v['k10_noans']:+5.1f} ({v['noans_share']})  noansctl {v['k10_noansctl'] or 0:+5.1f}  "
                      f"ans {v['ans'] or 0:+5.1f}  ansctl {v['ansctl'] or 0:+5.1f}  rand {v['k10_rand'] or 0:+5.1f}  rot {v['k10_rot'] or 0:+5.1f}  "
                      f"-> {v['verdict']}; answer alone suffices: {v['answer_alone_suffices']}; noans per seed {v['noans_per_seed']}")  # fmt: skip
    if a.sweep:
        out["sweep"] = sweep_reading(a.sweep)
        for k, v in out["sweep"]["reading"].items():
            print(f"sweep {k:12s} {v}")
        for tag, s in out["sweep"]["windows"].items():
            print(tag, "  ".join(f"{k.split('/')[0]}/{k.split('/')[1]} {c['transfer']:+.0f}" for k, c in sorted(s.items()) if c.get("n") and k.split("/")[1] != "none"))
    d = RES / "nn_ans_read"
    d.mkdir(exist_ok=True)
    (d / f"{a.name}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
