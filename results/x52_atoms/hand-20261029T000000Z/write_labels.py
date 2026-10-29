"""Hand labels for the Z2 sheet (results/x52_atoms/hand-20261029T000000Z), the lookup's own passage (reader K),
written by the agent from the sheet. NOT blind: the labeller had already seen the classifier's labels on the printed
Z2 examples of an earlier report (two of the items here, Istanbul and Sony, among them for the 9B). The classifier was
not changed after this sheet was written. Every rank not listed is 'other'."""

import json
import sys
from pathlib import Path

HAND = {
    "qwen3.5-9b|jsuite_v2_test_chat|j2:cities:M-L1-Istanbul-0": {1: "answer_own", 3: "answer_own"},
    "qwen3.5-9b|jsuite_v2_test_chat|j2:people:M-L1-Liszt-0": {1: "new_bridge", 16: "function", 22: "function"},
    "qwen3.5-9b|jsuite_v2nb_test_chat|j2:companies:M-L0-Sony-0": {20: "function", 23: "function"},
    "qwen3.5-9b|jsuite_v2nb_test_chat|j2:countries:M-L0-Colombia-0": {5: "function"},
    "qwen3.5-9b|jsuite_v2nb_test_chat|j2:people:M-L1-Sibelius-0": {6: "answer_own"},
    "qwen3.6-27b|jsuite_v2_test_chat|j2:cities:M-L1-Kyoto-0": {},
    "qwen3.6-27b|jsuite_v2_test_chat|j2:people:M-L0-Hokusai-0": {},
    "qwen3.6-27b|jsuite_v2nb_test_chat|j2:cities:M-L1-Geneva-0": {},
    "qwen3.6-27b|jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0": {1: "new_bridge", 15: "same_class"},
    "qwen3.6-27b|jsuite_v2nb_test_chat|j2:people:M-L1-Liszt-0": {13: "function"},
    "muse-glimmer-30b|jsuite_v2_test_chat|j2:cities:M-L1-Istanbul-0": {14: "function"},
    "muse-glimmer-30b|jsuite_v2_test_chat|j2:people:M-L1-Dante-0": {2: "bridge", 4: "answer_own"},
    "muse-glimmer-30b|jsuite_v2nb_test_chat|j2:companies:M-L0-Sony-0": {18: "function"},
    "muse-glimmer-30b|jsuite_v2nb_test_chat|j2:companies:M-L1-BlackBerry-0": {},
    "muse-glimmer-30b|jsuite_v2nb_test_chat|j2:people:M-L1-Pushkin-0": {4: "answer_own"},
}

d = Path(sys.argv[1])
sheet = json.loads((d / "sheet.json").read_text())
assert set(HAND) == set(sheet), sorted(set(HAND) ^ set(sheet))
out = {k: {str(a[0]): HAND[k].get(a[0], "other") for a in sheet[k]["atoms"]} for k in sheet}
path = d / "labels.json"
assert not path.exists(), f"{path} exists: labels are written once"
path.write_text(json.dumps(out, indent=1) + "\n")
print("wrote", path)
