"""nn_ko43_read (Zach, 2026-10-30, prereg amendment 68 note 43): note 37 on a held-out v4 data draw (jsuite_v4p4002), read
against seed 4001 (CPU). Inputs (results/ablate_v2/nn_ko_read/), per model prefix P:
  seed 4001: {P}note37.json (scripts/nn_ko37_read.py), {P}note41.json (scripts/nn_ko41_read.py, if note 41 ran)
  seed 4002: {P}jsuite_v4p4002_test_chat_note37.json and, if note 41's conditions were in the run,
             {P}jsuite_v4p4002_test_chat_note41.json (nn_ko37_read / nn_ko41_read --set jsuite_v4p4002_test_chat)
"Replicates" = the same note 37 reading per model (and, if run on both draws, the same note 41 keep and removal readings;
note 41's output-side run is not part of note 43). The headline gap (MM - MP under paper10, with its bridge bootstrap) of
each draw is reported beside. Writes results/ablate_v2/nn_ko_read/{P}note43.json and prints a line per reading.

python scripts/nn_ko43_read.py PREFIX      (PREFIX "" for the 27B, qwen35_9b_ for the 9B, nem35l_ for Lightning)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "results" / "ablate_v2" / "nn_ko_read"
SET2 = "jsuite_v4p4002_test_chat"


def load(name: str) -> dict | None:
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main(P: str) -> dict:
    a37, b37 = load(f"{P}note37.json"), load(f"{P}{SET2}_note37.json")
    a41, b41 = load(f"{P}note41.json"), load(f"{P}{SET2}_note41.json")
    out: dict = {"prefix": P, "readings": {}, "headline_gap": {}}
    for draw, d in (("4001", a37), ("4002", b37)):
        c = ((d or {}).get("v4", {}).get("all", {}).get("conditions", {}) or {}).get("paper10")
        out["headline_gap"][draw] = {"gap": c["gap"], "gap_ci": c["gap_ci"], "loss_MM": c["loss_MM"], "loss_MP": c["loss_MP"],
                                     "n_MM": c["n_MM"], "n_MP": c["n_MP"]} if c else None  # fmt: skip
    pairs = {"note37": ((a37 or {}).get("v4", {}).get("all", {}).get("reading"), (b37 or {}).get("v4", {}).get("all", {}).get("reading")),
             "note41_keep": ((a41 or {}).get("keep", {}).get("reading"), (b41 or {}).get("keep", {}).get("reading")),
             "note41_removal": ((a41 or {}).get("removal", {}).get("reading"), (b41 or {}).get("removal", {}).get("reading"))}  # fmt: skip
    for k, (x, y) in pairs.items():
        out["readings"][k] = {"4001": x, "4002": y, "replicates": (x == y) if x is not None and y is not None else None}
    print(f"note 43 {P or '27b_'}: " + "; ".join(f"{k}: 4001 {v['4001']!r} / 4002 {v['4002']!r} -> replicates {v['replicates']}"
                                              for k, v in out["readings"].items()))  # fmt: skip
    print(f"  headline gap (paper10, MM - MP): {json.dumps(out['headline_gap'])}")
    D.mkdir(parents=True, exist_ok=True)
    (D / f"{P}note43.json").write_text(json.dumps(out, indent=1) + "\n")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    main(ap.parse_args().prefix)
