"""Hand labels for results/x52_atoms/hand-20261028T235223Z (written by the agent reading sheet.md only, without the
classifier's output; every rank not listed is 'other')."""

import json
import sys
from pathlib import Path

HAND = {
    "qwen3.5-9b|P2-L0-0016": {1: "bridge", 2: "new_bridge", 3: "bridge", 5: "new_bridge", 7: "bridge"},
    "qwen3.5-9b|P2-L0-0064": {5: "new_bridge", 9: "bridge"},
    "qwen3.5-9b|P2-L0-0115": {1: "new_bridge", 2: "bridge", 3: "new_bridge"},
    "qwen3.5-9b|P2-L0-0135": {1: "new_bridge", 2: "bridge", 6: "function"},
    "qwen3.5-9b|P2-L0-0288": {1: "function", 2: "new_bridge", 5: "function", 11: "function"},
    "qwen3.6-27b|P2-L0-0008": {1: "new_bridge", 2: "bridge"},
    "qwen3.6-27b|P2-L0-0051": {1: "new_bridge", 2: "new_bridge", 3: "bridge"},
    "qwen3.6-27b|P2-L0-0084": {1: "bridge", 2: "function", 6: "new_bridge"},
    "qwen3.6-27b|P2-L0-0097": {21: "function"},
    "qwen3.6-27b|P2-L0-0206": {1: "new_bridge", 5: "bridge", 8: "answer_other", 10: "function", 13: "function"},
}

d = Path(sys.argv[1])
sheet = json.loads((d / "sheet.json").read_text())
assert set(HAND) == set(sheet), sorted(set(HAND) ^ set(sheet))
out = {k: {str(a[0]): HAND[k].get(a[0], "other") for a in sheet[k]["atoms"]} for k in sheet}
path = d / "labels.json"
assert not path.exists(), f"{path} exists: labels are written once"
path.write_text(json.dumps(out, indent=1) + "\n")
print("wrote", path)
