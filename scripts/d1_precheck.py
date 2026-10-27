"""d1_precheck (22 Oct night; the brief's T2 condition, fixed before any run): may the D1 chain run on this model?

Runs iff the model's lens gate v1 passed (results/lens_gate/<gate>/summary.json "gate") AND at least --min-topics
topics have >= --min-items scenes eligible for PP and PM in the tasks_v2 competence run (tasks_v2.eligible, level 0).
Prints the reason either way; exits 3 when the chain must stop (the job is then logged as stopped by the precheck).

uv run python scripts/d1_precheck.py --gate G --competence C [--tasks-set d1_topics_v2 --min-topics 2 --min-items 30]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins


def topics_ok(scenes_by_topic: dict[str, int], min_topics: int, min_items: int) -> bool:
    return sum(n >= min_items for n in scenes_by_topic.values()) >= min_topics


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--tasks-set", default="d1_topics_v2")
    ap.add_argument("--min-topics", type=int, default=2)
    ap.add_argument("--min-items", type=int, default=30)
    a = ap.parse_args()
    from scripts import tasks_v2 as T

    gate = json.loads((pins.RESULTS_DIR / "lens_gate" / a.gate / "summary.json").read_text())["gate"]["pass"]
    items = T.eligible(a.tasks_set, a.competence, ["PP", "PM"], 10**6, level="0")
    by_topic: dict[str, set] = collections.defaultdict(set)
    for it in items:
        by_topic[it["domain"]].add(it["scene"])
    counts = {t: len(s) for t, s in sorted(by_topic.items())}
    ok = bool(gate) and topics_ok(counts, a.min_topics, a.min_items)
    print(f"d1_precheck: gate v1 {'passed' if gate else 'failed'}; eligible scenes per topic {counts}; "
          f"{'RUN' if ok else 'STOP'} (needs the gate and >= {a.min_topics} topics with >= {a.min_items} scenes)")  # fmt: skip
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
