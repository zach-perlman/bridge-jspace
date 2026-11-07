"""Convert data/figures/status.csv (grammar v2: status, tag) to the styles-plot registry schema in
data/figures/status_sp.csv (figure, cell, timing, claim, claim_reason, reason, source), the file plotstyle.toml names.

timing = post_hoc where the old status is post_hoc, else fixed_in_advance; claim = not_claimed (claim_reason = the
text after "not claimed: ") where the old tag says so, descriptive where the old status is descriptive, else claimed.
scripts/status_registry.py still writes the old schema; run this after it.

uv run python scripts/convert_status_registry.py
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "data" / "figures" / "status.csv"
OUT = REPO / "data" / "figures" / "status_sp.csv"
COLUMNS = ("figure", "cell", "timing", "claim", "claim_reason", "reason", "source")
NOT_CLAIMED = "not claimed: "


def convert(row: dict) -> dict:
    status, tag = row["status"], row["tag"]
    if tag and not tag.startswith(NOT_CLAIMED):
        raise ValueError(f"{row['figure']} {row['cell']}: unknown tag {tag!r}")
    if status not in ("fixed_in_advance", "post_hoc", "descriptive", "not_claimed"):
        raise ValueError(f"{row['figure']} {row['cell']}: unknown status {status!r}")
    claim = "not_claimed" if tag else "descriptive" if status == "descriptive" else "claimed"
    return {"figure": row["figure"], "cell": row["cell"],
            "timing": "post_hoc" if status == "post_hoc" else "fixed_in_advance", "claim": claim,
            "claim_reason": tag.removeprefix(NOT_CLAIMED), "reason": row["reason"], "source": row["source"]}  # fmt: skip


def main() -> None:
    with SRC.open(newline="") as f:
        rows = [convert(r) for r in csv.DictReader(f)]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(REPO)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
