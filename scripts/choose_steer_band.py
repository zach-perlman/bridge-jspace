"""choose_steer_band: the aligned steering band (Zach, 2026-10-22; the rule fixed before any Qwen3-32B or Muse copy-sweep
data, applying the Day 3 plan's pre-stated "if the corrected ceiling clears 0.5 only later, rerun steering at an aligned
band"). From a copy_sweep run in band mode: the earliest start layer L such that pasting C's state from L through
L + window flips >= 50% of P->P, P->M, M->P and M->M alike, at one position set (question or final; final first on a tie).
Prints "LO-HI POSSET": the steering band (L to L + window, capped at the last lens layer) and the position set. Exit 1 if
no band qualifies. Writes results/write_max/steer_band/RUN.json.

python scripts/choose_steer_band.py COPY_SWEEP_RUN
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

WORDS = ("PP", "PM", "MP", "MM")


def main(run: str) -> int:
    d = pins.RESULTS_DIR / "copy_sweep" / run
    flips = json.loads((d / "summary.json").read_text())["flips"]
    window = json.loads((d / "manifest.json").read_text()).get("window", 12)
    starts = sorted({int(k.split("/")[2][1:]) for k in flips})
    found = None
    for lo in starts:
        for pos in ("final", "question"):
            vals = [flips.get(f"{w}/{pos}/L{lo}", {}).get("band") for w in WORDS]
            if all(v is not None and v >= 0.5 for v in vals):
                found = (lo, pos, vals)
                break
        if found:
            break
    out = {"run": run, "window": window, "rule": (__doc__ or "").split("\n\n")[0], "band": None}
    if found:
        lo, pos, vals = found
        hi = min(lo + window, pins.N_LAYERS - 2)
        out |= {"band": f"{lo}-{hi}", "possets": pos, "flips_at_band": dict(zip(WORDS, vals, strict=True))}
    (pins.RESULTS_DIR / "write_max" / "steer_band").mkdir(parents=True, exist_ok=True)
    (pins.RESULTS_DIR / "write_max" / "steer_band" / f"{run}.json").write_text(json.dumps(out, indent=2) + "\n")
    if not found:
        print(f"no band reaches 50% for all of {WORDS}", file=sys.stderr)
        return 1
    print(f"{out['band']} {out['possets']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
