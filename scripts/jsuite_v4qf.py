"""jsuite_v4qf (Zach, 2026-10-29, prereg amendment 59 note 27): v4 with the question first. Copies data/tasks_v2/jsuite_v4_test_chat
and jsuite_v4ctl_test_chat to jsuite_v4qf_test_chat and jsuite_v4ctlqf_test_chat, every item unchanged except "qfirst": true
(scripts/tasks_v2.render then puts the question and its instruction before the passage, in the same user turn). Same ids.

python scripts/jsuite_v4qf.py
"""

import hashlib
import json
import shutil
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
for src, dst in (("jsuite_v4_test_chat", "jsuite_v4qf_test_chat"), ("jsuite_v4ctl_test_chat", "jsuite_v4ctlqf_test_chat")):
    assert not (DATA / dst).exists(), f"{dst} exists; sets are written once"
    shutil.copytree(DATA / src, DATA / dst)
    rows = [json.loads(line) for line in (DATA / src / "items.jsonl").read_text().splitlines()]
    text = "".join(json.dumps({**r, "qfirst": True}) + "\n" for r in rows)
    (DATA / dst / "items.jsonl").write_text(text)
    print(dst, len(rows), "items, sha256", hashlib.sha256(text.encode()).hexdigest()[:16])
