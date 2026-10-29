"""Hand labels for Muse's sheet (results/x52_atoms/hand-20261028T235654Z), written by the agent reading sheet.md only;
Muse's atoms and the classifier's labels for them had not been seen (blind); every rank not listed is 'other'."""

import json
import sys
from pathlib import Path

HAND = {
    "muse-glimmer-30b|P2-L0-0016": {1: "new_bridge", 2: "bridge", 3: "bridge", 5: "function", 6: "function",
                                    11: "new_bridge", 13: "function"},
    "muse-glimmer-30b|P2-L0-0073": {1: "bridge", 2: "new_bridge", 3: "same_class", 4: "new_bridge", 18: "function"},
    "muse-glimmer-30b|P2-L0-0133": {1: "bridge", 2: "new_bridge", 8: "same_class"},
    "muse-glimmer-30b|P2-L0-0150": {1: "new_bridge", 2: "bridge", 3: "bridge"},
    "muse-glimmer-30b|P2-L0-0287": {2: "new_bridge", 3: "bridge", 21: "bridge", 23: "function"},
}  # fmt: skip

d = Path(sys.argv[1])
sheet = json.loads((d / "sheet.json").read_text())
assert set(HAND) == set(sheet), sorted(set(HAND) ^ set(sheet))
out = {k: {str(a[0]): HAND[k].get(a[0], "other") for a in sheet[k]["atoms"]} for k in sheet}
path = d / "labels.json"
assert not path.exists(), f"{path} exists: labels are written once"
path.write_text(json.dumps(out, indent=1) + "\n")
print("wrote", path)
