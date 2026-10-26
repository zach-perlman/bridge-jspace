"""jswap_pool (Zach, 2026-10-26): a jswap run scored on its memory finals pooled (PM PA PN TM TA TN), as jswap.score. python scripts/jswap_pool.py RUN"""
import json, sys
sys.path.insert(0, "/workspace/bridge-jspace"); sys.path.insert(0, "/workspace/bridge-jspace/src")
from scripts import jswap as JS
rows = [json.loads(l) for l in open(f"/workspace/bridge-jspace/results/jswap/{sys.argv[1]}/rows.jsonl")]
MEM = ("PM", "PA", "PN", "TM", "TA", "TN")
s = JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEM])
for c in ("swap", "remove", "swap_rot", "swap_u", "swap_comp", "paste"):
    v = s.get(f"memory/{c}")
    if v:
        print(f"memory {c:10s} n {v['n']:4d} kept {v['kept']:5.1f} donor {v['donor']:5.1f} other {v['other']:5.1f} transfer {v['transfer']:+5.1f} {v['ci']}")
