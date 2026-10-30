"""cpuwins A2 peek (post hoc, descriptive): note 56 clean rows (cond none), J++ ranks at the answer position (full vocab).
For each conv, median rank of peer_answer (e3') and peer_bridge (e2') at the knock-out band L12-16 and at L26-30,
among items whose clean output class is 'peer' (said e3')."""
import json, sys, collections, statistics as st
LAY = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 27, 28, 29, 30]
for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path)]
    clean = [r for r in rows if r["cond"] == "none" and r.get("ranks")]
    print("==", path.split("/")[-2], len(clean))
    for conv in ["instr_vis", "hyp_vis", "prem_vis", "press_vis", "prem_hid"]:
        xs = [r for r in clean if r["conv"] == conv and r["cls"] == "peer"]
        if not xs: continue
        out = {}
        for what in ["peer_answer", "peer_bridge", "orig_answer", "orig_bridge"]:
            for nm, ls in [("L12-16", [12, 14, 16]), ("L26-30", [26, 28, 30])]:
                idx = [LAY.index(l) for l in ls]
                v = [st.median([r["ranks"]["jpp"][what][i] for i in idx]) for r in xs]
                out[f"{what}@{nm}"] = st.median(v)
        print(conv, "n", len(xs), {k: round(v, 1) for k, v in out.items()})
