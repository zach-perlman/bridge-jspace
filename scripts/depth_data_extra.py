"""Add to data/figures/depth/data.csv the card numbers the depth README quotes whose rows its old builders never wrote:
the answer-arm check's shift beyond K random directions (one run per model) and the made-up-fact passages' F4 / F4b
splits. Each row is read by key from its run file; a row already present is checked, not rewritten (a different value
stops the script), so a second run changes nothing.

uv run python scripts/depth_data_extra.py
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "figures" / "depth" / "data.csv"
FIELDS = ["figure", "model", "quantity", "value", "lo", "hi", "n", "source"]
KRAND = "answer arms: recall, the all-language shift beyond the same count of random directions (b_beyond_K_random)"
# the run each model's README value comes from (the 27B's is the rerun with batch 8)
KRAND_RUNS = {"qwen3.5-9b": "runs/answer_arms_krand/qwen3.5-9b/krand/summary.json",
              "qwen3.6-27b": "runs/answer_arms_krand/qwen3.6-27b/krand_b8/summary.json",
              "muse-glimmer-30b": "runs/answer_arms_krand/muse-glimmer-30b/krand/summary.json"}  # fmt: skip
Z1P = "results/z1p_checks/20261030T222158Z/tables.json"
# (table key, path inside it, the row's quantity); n is read from the path's parent
Z1P_ROWS = (
    ("F4", ("without", "lookup_excess"), "made-up facts F4, without the 23 passages: lookup, switches lost beyond a random part"),
    ("F4", ("without", "recall_excess"), "made-up facts F4, without the 23 passages: recall, switches lost beyond a random part"),
    ("F4", ("without", "gap"), "made-up facts F4, without the 23 passages: the gap"),
    ("F4b", ("without_those_items", "lookup_excess"), "made-up facts F4b, without the 54 items: lookup, switches lost beyond a random part"),
    ("F4b", ("without_those_items", "recall_excess"), "made-up facts F4b, without the 54 items: recall, switches lost beyond a random part"),
    ("F4b", ("without_those_items", "gap"), "made-up facts F4b, without the 54 items: the gap"),
)  # fmt: skip


def rows() -> list[dict]:
    out = []
    for model, path in KRAND_RUNS.items():
        rec = json.loads((REPO / path).read_text())["readers"]["recall"]
        v, lo, hi = rec["b_beyond_K_random"]
        out.append({"figure": "cards", "model": model, "quantity": KRAND, "value": v, "lo": lo, "hi": hi,
                    "n": rec["n"], "source": path})  # fmt: skip
    tables = json.loads((REPO / Z1P).read_text())
    model = json.loads((REPO / Z1P).with_name("manifest.json").read_text())["model"]
    for key, (part, field), quantity in Z1P_ROWS:
        block = tables[key][part]
        v, lo, hi = block[field]
        out.append({"figure": "cards", "model": model, "quantity": quantity, "value": v, "lo": lo, "hi": hi,
                    "n": block["n"], "source": f"{Z1P} | {key}"})  # fmt: skip
    return out


def main() -> int:
    text = DATA.read_text()
    have = {(r["figure"], r["model"], r["quantity"]): r for r in csv.DictReader(io.StringIO(text))}
    new = []
    for r in rows():
        old = have.get((r["figure"], r["model"], r["quantity"]))
        if old is None:
            new.append(r)
        elif any(str(old[k]) != str(r[k]) for k in ("value", "lo", "hi", "n", "source")):
            print(f"data.csv row differs from its source: {old} vs {r}", file=sys.stderr)
            return 1
    if new:
        buf = io.StringIO()
        csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n").writerows(new)
        DATA.write_text(text + buf.getvalue())
    print(f"data/figures/depth/data.csv: {len(new)} rows added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
