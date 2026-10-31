"""nn_decomp_read (Zach, 2026-10-28, prereg amendment 58 note 10): note 10's fixed readings of the decomposition runs (CPU).

Per run, band, word and donor (insert, latent): the transfer (points moved to the donor's answer, jswap.score, with its
95% bootstrap interval over bridges) under full, lens, rem, remfix and lensrand; lens, rem and remfix as shares of full;
and note 10's reading: not read if full < 10; "through" if lens >= 2/3 full and remfix <= 1/3 full with lensrand < 10;
else "around" if rem >= 2/3 full; else "mixed". Writes results/nn_swap/RUN/readings.json.

python scripts/nn_decomp_read.py RUN [RUN ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("full", "lens", "rem", "remfix", "lensrand")


def reading(t: dict[str, float]) -> str:
    full = t["full"]
    if full < 10:
        return "not read"
    if t["lens"] >= 2 / 3 * full and t["remfix"] <= 1 / 3 * full and t["lensrand"] < 10:
        return "through"
    return "around" if t["rem"] >= 2 / 3 * full else "mixed"


def main(runs: list[str]) -> None:
    for run in runs:
        s = json.loads((ROOT / "results/nn_swap" / run / "summary.json").read_text())
        s = s.get("scores", s)
        out = {}
        for band, word in sorted({tuple(k.split("/")[:2]) for k in s}):
            for donor in ("insert", "latent"):
                got = {c: s.get(f"{band}/{word}/{c}_{donor}") for c in CELLS}
                if not all(got.values()):
                    continue
                t = {c: v["transfer"] for c, v in got.items()}
                rec = {"n": got["full"]["n"], **{c: round(t[c], 1) for c in CELLS}, "ci": {c: got[c]["ci"] for c in CELLS}}
                if t["full"] > 0:
                    rec.update({f"{c}_share": round(t[c] / t["full"], 2) for c in ("lens", "rem", "remfix")})
                rec["reading"] = reading(t)
                out[f"{band}/{word}/{donor}"] = rec
                shares = "  ".join(f"{c} {rec.get(c + '_share', 0):4.0%}" for c in ("lens", "rem", "remfix"))
                print(f"{run:38s} {band:7s} {word} {donor:6s} n {rec['n']:4d}  full {t['full']:+5.1f} {got['full']['ci']}  "
                      f"lens {t['lens']:+5.1f}  rem {t['rem']:+5.1f}  remfix {t['remfix']:+5.1f}  lensrand {t['lensrand']:+5.1f}  "
                      f"{shares}  -> {rec['reading']}")  # fmt: skip
        (ROOT / "results/nn_swap" / run / "readings.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
