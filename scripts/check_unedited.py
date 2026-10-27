"""Smoke gate for an early_push_where run in a new prompt format (Dan, 23 Oct ~00:45, OLMo's raw-format D4): every
scene was drawn from the competence run's items that are right on every prompt, so the run's own unedited answers
(outcome rows with kind "none") must all be right (role "A"). Exits 0 if they are; exits 3 (stop the job's chain, as
d1_precheck does) if any is not, i.e. the run renders or reads prompts differently from the competence run.

  uv run python scripts/check_unedited.py --run NAME
"""

import argparse
import json
import sys

from bridge_jspace import pins


def check(rows: list[dict]) -> tuple[int, int]:
    """(n unedited rows, n right) over the run's outcome rows."""
    none = [r for r in rows if r.get("kind") == "none"]
    return len(none), sum(r.get("role") == "A" for r in none)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="an early_push_where run name")
    a = ap.parse_args()
    path = pins.RESULTS_DIR / "early_push_where" / a.run / "outcomes.jsonl"
    rows = [json.loads(x) for x in path.read_text().splitlines()]
    n, right = check(rows)
    ok = n > 0 and right == n
    print(f"check_unedited {a.run}: {right} of {n} unedited answers right; {'RUN' if ok else 'STOP (format mismatch)'}")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
