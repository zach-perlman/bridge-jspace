"""build_v3 (Zach, 2026-10-28): rebuild every jsuite v3 set exactly, from the committed generator, bridge table and seed.

The items are not in the public repo (amendment 58 note 4). This runs scripts/jsuite_v3.py (seed 3001, 2 renderings)
into a temporary set, splits it as the runs use it, and derives the note 9 sets:
  jsuite_v3_test_chat          rendering 0 (every run so far)
  jsuite_v3r1_test_chat        rendering 1 (held for replication)
  jsuite_v3probes_test_chat    the clue-only questions, wording A
  jsuite_v3probesB_test_chat   wording B (scripts/v3_probes_b.py)
  jsuite_v3fc_test_chat        final clause only (scripts/v3_finalclause.py)
  jsuite_v3ra_test_chat        rendering A: RM MM PM with the relation after the bridge (scripts/v3_relafter.py; note 12)
and prints each file's sha256 (compare with docs/v3_sha256.txt).

python scripts/build_v3.py
"""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data" / "tasks_v2"


def main() -> None:
    tmp = "jsuite_v3build"
    subprocess.run([sys.executable, str(ROOT / "scripts/jsuite_v3.py"), "--name", tmp, "--seed", "3001", "--reps", "2"], check=True, cwd=ROOT)
    src = D / f"{tmp}_test_chat" / "items.jsonl"
    lines = src.read_text().splitlines(keepends=True)
    parts = {"jsuite_v3_test_chat": [], "jsuite_v3r1_test_chat": [], "jsuite_v3probes_test_chat": []}
    for line in lines:
        it = json.loads(line)
        name = "jsuite_v3probes_test_chat" if it.get("module") == "probes" else ("jsuite_v3_test_chat" if it.get("rep") == 0 else "jsuite_v3r1_test_chat")
        parts[name].append(line)
    for name, ls in parts.items():
        (D / name).mkdir(parents=True, exist_ok=True)
        (D / name / "items.jsonl").write_text("".join(ls))
    shutil.rmtree(D / f"{tmp}_test_chat")
    for script in ("v3_probes_b.py", "v3_finalclause.py", "v3_relafter.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=True, cwd=ROOT)
    for name in ("jsuite_v3_test_chat", "jsuite_v3r1_test_chat", "jsuite_v3probes_test_chat", "jsuite_v3probesB_test_chat", "jsuite_v3fc_test_chat", "jsuite_v3ra_test_chat"):
        f = D / name / "items.jsonl"
        print(hashlib.sha256(f.read_bytes()).hexdigest(), f"data/tasks_v2/{name}/items.jsonl", sum(1 for _ in f.open()))


if __name__ == "__main__":
    main()
