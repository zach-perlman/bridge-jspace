"""tasks_v2/full_v8_two has no builder script: it is full_v8's two-step lines, unchanged and in order (its manifest's
rule). This test is what checks it (data/SOURCES.md)."""

import hashlib
import json

from bridge_jspace import pins

SETS = pins.DATA_DIR / "tasks_v2"


def test_full_v8_two_is_the_two_step_lines_of_full_v8():
    src = SETS / "full_v8" / "items.jsonl"
    man = json.loads((SETS / "full_v8_two" / "manifest.json").read_text())
    assert man["derived_from"]["set"] == "full_v8"
    assert hashlib.sha256(src.read_bytes()).hexdigest() == man["derived_from"]["sha256"]
    two = [line for line in src.read_text().splitlines() if len(json.loads(line)["word"]) == 2]
    assert two and (SETS / "full_v8_two" / "items.jsonl").read_text() == "".join(line + "\n" for line in two)
    assert man["n_items"] == len(two)
