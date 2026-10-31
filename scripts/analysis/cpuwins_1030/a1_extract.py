"""cpuwins A1 (post hoc, exploratory; 2026-10-30): per-item features for 'is the recalled answer readable upstream?'
Reads results/nn_readout/<P>nn_readout_v4prime_v1/rows.jsonl (note 25 readout: J++ and logit lens, every 2nd layer,
targets bridge/attr/other/third/ctx, ranks among the relation's candidates) and the model's v4 competence run
(results/tasks_v2/<P>jsuite_v4_test_chat_competence_cand2_v1/items.jsonl). Writes one JSON line per item to stdout-file.
Read-only on results. Windows = note 25's pre-registered windows (not chosen here)."""
import collections, json, sys
R = "/workspace/bridge-jspace/results"
MODELS = {  # prefix, desc_end window, final window (note 25)
    "9B": ("qwen35_9b_", (4, 16), (21, 30)),
    "27B": ("", (16, 40), (49, 62)),
    "Lightning": ("nem35l_", (6, 26), (34, 50)),
}
out = open(sys.argv[1], "w")
for m, (p, wd, wf) in MODELS.items():
    rows = collections.defaultdict(lambda: collections.defaultdict(list))
    meta = {}
    for line in open(f"{R}/nn_readout/{p}nn_readout_v4prime_v1/rows.jsonl"):
        r = json.loads(line)
        lo, hi = wd if r["site"] == "desc_end" else wf
        meta[r["id"]] = (r["family"], r["rel"], r["bridge"])
        key = (r["site"], r["lens"], r["what"])
        rows[r["id"]][key].append((r["layer"], r["rank"], r["k"]))
    comp = collections.defaultdict(dict)
    for line in open(f"{R}/tasks_v2/{p}jsuite_v4_test_chat_competence_cand2_v1/items.jsonl"):
        r = json.loads(line)
        comp[r["id"]][r["part"]] = {k: r.get(k) for k in ("margin", "p_answer", "read_top", "expected", "correct", "gen")}
    n = 0
    for i, d in rows.items():
        fam, rel, br = meta[i]
        rec = {"model": m, "id": i, "family": fam, "rel": rel, "bridge": br, "comp": comp.get(i, {})}
        feats = {}
        for (site, lens, what), xs in d.items():
            lo, hi = wd if site == "desc_end" else wf
            xs = sorted(xs)
            win = [(la, rk, k) for la, rk, k in xs if lo <= la <= hi]
            feats[f"{site}|{lens}|{what}"] = {
                "top1": sum(rk == 1 for _, rk, _ in win) / len(win),
                "mrr": sum(1 / rk for _, rk, _ in win) / len(win),
                "k": win[0][2],
                "ranks_all": [rk for _, rk, _ in xs], "layers_all": [la for la, _, _ in xs],
            }
        rec["f"] = feats
        out.write(json.dumps(rec) + "\n")
        n += 1
    print(m, n, "items", flush=True)
