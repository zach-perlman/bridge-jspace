"""M - P difference between two module 1 runs (paper10, all starts), 95% bootstrap over bridges resampled jointly."""
import collections, json, random, sys
a_run, b_run, set_name = sys.argv[1], sys.argv[2], sys.argv[3]
items = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/tasks_v2/{set_name}/items.jsonl")}
def load(run):
    rows = [json.loads(l) for l in open(f"results/ablate_v2/{run}/rows.jsonl")]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"] and r["kind"] == "clean"}
    sel = collections.defaultdict(list)
    for r in rows:
        if r["condition"] == "paper10" and r["kind"] == "clean" and (r["family"], r["id"]) in ok:
            sel[r["family"][1]].append((items[r["id"]]["bridge"], r["correct"]))
    return sel
A, B = load(a_run), load(b_run)
def mp(sel, pick=None):
    v = {}
    for f in "PM":
        tot = [(c, (pick[b] if pick else 1)) for b, c in sel[f] if (pick is None or pick[b])]
        n = sum(m for _, m in tot)
        v[f] = 100 * (1 - sum(c * m for c, m in tot) / n)
    return v["M"] - v["P"]
bridges = sorted({b for s in (A, B) for f in "PM" for b, _ in s[f]})
rng = random.Random(0); ds = []
for _ in range(2000):
    pick = collections.Counter(rng.choice(bridges) for _ in bridges)
    ds.append(mp(B, pick) - mp(A, pick))
ds.sort()
print(f"M-P {a_run}: {mp(A):+.1f}; {b_run}: {mp(B):+.1f}; difference (second - first) {mp(B) - mp(A):+.1f} [{ds[50]:+.1f}, {ds[1949]:+.1f}] over {len(bridges)} bridges")
