"""Note 61b's registered AT reading (amendment 85 addendum): mean over the with-attention windows (L13-15, L17-19) of
(MP dark - mid) minus the same mean over the without windows (L12-14, L16-18), paired bridge bootstrap over MP items (note 58's
K.boot, bridges as units). Reads the stored run only."""
import collections, json, sys
from pathlib import Path
ROOT = Path("/workspace/bridge-jspace"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K
from scripts.nn_ko49_read import rows_at
items = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data/tasks_v2/jsuite_v4_test_chat/items.jsonl").open()}
d = ROOT / "results/ablate_v2/qwen35_9b_jsuite_v4_test_chat_ko61b_cand2_v1"
acc = rows_at(d)
W_ATT, W_NO = ("L13-15", "L17-19"), ("L12-14", "L16-18")
def dm(i, w):  # MP item i: loss(dark) - loss(mid) in {-1, 0, 1}
    return int(acc[("MP", f"midperm_{w}")][i][0]) - int(acc[("MP", f"darkperm_{w}")][i][0])
by = collections.defaultdict(list)
for i, (ok, _) in acc[("MP", "none")].items():
    if all(i in acc[("MP", f"{k}perm_{w}")] for w in W_ATT + W_NO for k in ("dark", "mid")):
        by[items[i]["bridge"]].append(sum(dm(i, w) for w in W_ATT) / 2 - sum(dm(i, w) for w in W_NO) / 2)
m100 = lambda xs: 100 * sum(xs) / len(xs)
u = [x for v in by.values() for x in v]
s, ci = m100(u), K.boot(by, m100)
lab = "the 9B's dark-space lookup route runs through the full-attention layer's window" if s >= 15 and ci and ci[0] > 0 else "not met"
print(f"reading note61b AT qwen35_9b_: {lab!r} | with-attention minus without, mean MP (dark - mid) {round(s, 1)} {ci} (n MP {len(u)}, {len(by)} bridges)")
