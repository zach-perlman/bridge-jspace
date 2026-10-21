"""pad_check: does ablate_v2 --pad (length-sorted, right-padded batches) give the same knock-out rows as exact-length
batches? (Zach, 2026-10-21: padded batching as a speed-up, validated item by item before use.) Rule, fixed before the
check ran: padding is accepted if >= 98% of rows (family x item x kind x band x condition) agree on correct, and no
condition's accuracy differs by more than 1 point. Exit code 0 = accepted.

python scripts/pad_check.py EXACT_RUN PADDED_RUN
"""

from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

RES = pins.RESULTS_DIR / "ablate_v2"


def rows(run: str) -> dict:
    out = {}
    for r in map(json.loads, (RES / run / "rows.jsonl").read_text().splitlines()):
        out[(r["family"], r["id"], r["kind"], r["band"], r["condition"])] = r
    return out


def main(exact: str, padded: str) -> int:
    a, b = rows(exact), rows(padded)
    keys = sorted(set(a) & set(b))
    assert keys, "no shared rows"
    assert len(keys) == len(a) == len(b), f"row sets differ: {len(a)} exact, {len(b)} padded, {len(keys)} shared"
    agree = statistics.mean(a[k]["correct"] == b[k]["correct"] for k in keys)
    dlogp = [abs(a[k]["logp"] - b[k]["logp"]) for k in keys]
    by: dict = collections.defaultdict(lambda: ([], []))
    for k in keys:
        by[(k[3], k[4])][0].append(a[k]["correct"])
        by[(k[3], k[4])][1].append(b[k]["correct"])
    shifts = {f"{band}/{cond}": statistics.mean(y) - statistics.mean(x) for (band, cond), (x, y) in by.items()}
    ok = agree >= 0.98 and all(abs(v) <= 0.01 for v in shifts.values())
    summary = {"exact": exact, "padded": padded, "rows": len(keys), "agreement": agree,
               "median_abs_dlogp": statistics.median(dlogp), "max_abs_dlogp": max(dlogp),
               "accuracy_shift_padded_minus_exact": shifts, "accepted": ok}  # fmt: skip
    (RES / padded / "pad_check.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
