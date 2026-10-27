"""x0_first_mention (Dan's cross-tab, 24 Oct evening; descriptive, added after data): does the lookup's switch depend on
where the alt item's first earlier mention sits?

On the single-change items whose org and alt locker sentences both come before the asked pick, the alt item is
mentioned earlier by its locker sentence and, when its original picker's sentence comes before the asked pick, by that
pick sentence too. The first of these earlier mentions is where the probe's first-mention pointer points (x0_probe_patched,
the duplicate-pick check). Per reader: the share switched by the whole edit and without the J++ part (k = 25), split by
the first earlier mention (the locker sentence / the other person's pick sentence); 95% CIs from a cluster bootstrap over
bridge entities (10,000 resamples, seed 0). Writes results/x0_necessity/<single run>/first-mention-<UTC>/.

uv run python scripts/x0_first_mention.py --single x0_single_27b_r2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X
from scripts import x0_probe_patched as PP
from scripts import x0_strata as ST

NOTE = "Descriptive, added after data (Dan's cross-tab, 24 Oct evening); not part of X0's rule."
ARMS = {"whole": ("-", 0, "-", "whole"), "without the J++ part": ("jpp", X.K_MAIN, "signed", "no_part")}


def first_mention(case: dict) -> str:
    """'locker' or 'other pick': which earlier mention of the alt item comes first in the context."""
    side, other = PP.other_pick(case)
    locker = PP.locker_index(case["context"], case["cf_bridge"])
    return "other pick" if side == "before" and other < locker else "locker"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--single", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    src = X.RESULTS / a.single
    pred = json.loads((src / "manifest.json").read_text())["predicted"]
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == pred]
    keep = {}
    for s in {r["scene"] for r in rows}:
        f = ST.features(cases[s])
        if f["org locker vs asked pick"] == "before" and f["alt locker vs asked pick"] == "before":
            keep[s] = first_mention(cases[s])
    got = {
        (r["scene"], r["reader"], (r["dict"], r["k"], r["omp"], r["arm"])): r["switched"]
        for r in rows
        if r["scene"] in keep
    }
    ent = {r["scene"]: r["entity"] for r in rows}
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# The lookup's switch by the alt item's first earlier mention: {a.single}, layer {pred}", "",
             f"{NOTE} Single-change items with both locker sentences before the asked pick. Bootstrap over bridge "
             f"entities ({a.n_boot} resamples). UNVERIFIED.", "",
             "| reader | first earlier mention | n | switched, whole edit | switched, without the J++ part |",
             "|---|---|---|---|---|"]  # fmt: skip
    blob: dict = {"run": a.single, "layer": pred, "note": NOTE, "rows": []}
    for w in X.READERS:
        for first in ("locker", "other pick"):
            scenes = sorted(s for s, f in keep.items() if f == first)
            sw = {name: [got[(s, w, arm)] for s in scenes] for name, arm in ARMS.items()}
            r = X.resampled_rates(sw, [ent[s] for s in scenes], a.n_boot)
            res = {name: [float(np.mean(v)), *X.interval(r[name])] for name, v in sw.items()}
            blob["rows"].append({"reader": w, "first": first, "n": len(scenes), **res})
            lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {first} sentence | {len(scenes)} | "
                         f"{ci(res['whole'])} | {ci(res['without the J++ part'])} |")  # fmt: skip
    out = src / f"first-mention-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "first_mention.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "first_mention.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
