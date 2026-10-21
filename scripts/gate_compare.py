"""gate_compare: does this box reproduce another box's results item by item? (Zach, 2026-10-21: the 2x H200 NVL box
after the B200 went down; the B200 gate's rule: >= 97% item agreement.) Compares a tasks_v2 competence run's
correct flags (whole question, each step, C, O, guess) or an ablate_v2 run's rows (shared keys only).

python scripts/gate_compare.py competence NEW OLD | ablate NEW OLD
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins


def load(kind: str, run: str) -> dict:
    if kind == "competence":
        path = pins.RESULTS_DIR / "tasks_v2" / run / "items.jsonl"
        return {(r["id"], r["part"]): r["correct"] for r in map(json.loads, path.read_text().splitlines())}
    path = pins.RESULTS_DIR / "ablate_v2" / run / "rows.jsonl"
    return {(r["family"], r["id"], r["kind"], r["band"], r["condition"]): r["correct"]
            for r in map(json.loads, path.read_text().splitlines())}  # fmt: skip


def main(kind: str, new: str, old: str) -> int:
    a, b = load(kind, new), load(kind, old)
    keys = sorted(set(a) & set(b))
    assert keys, "no shared keys"
    agree = sum(a[k] == b[k] for k in keys) / len(keys)
    acc_new, acc_old = sum(a[k] for k in keys) / len(keys), sum(b[k] for k in keys) / len(keys)
    ok = agree >= 0.97
    out = {"kind": kind, "new": new, "old": old, "shared": len(keys), "agreement": round(agree, 4),
           "accuracy_new": round(acc_new, 4), "accuracy_old": round(acc_old, 4), "passes_97": ok}  # fmt: skip
    print(json.dumps(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
