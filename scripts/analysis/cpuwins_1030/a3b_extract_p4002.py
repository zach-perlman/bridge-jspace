"""cpuwins A3b (post hoc, exploratory): (1) for KO picks, which entity's passage value (by passage position) and the pick's
rank in the clean top-10; (2) natural MM failures (v4 gate, MM_fail, clean) categorised by the competence run's top token
(read_top string) against first-token decodes of gold / X's passage value / other passage values / other answers.
CPU only, tokenizer only."""
import collections, json, os, sys, ast
os.environ["CUDA_VISIBLE_DEVICES"] = ""; os.environ["HF_HUB_OFFLINE"] = "1"; os.environ.setdefault("HF_HOME", "/workspace/hf_cache")
sys.path.insert(0, "/workspace/bridge-jspace")
from transformers import AutoTokenizer
from scripts import suite_v1 as S
R = "/workspace/bridge-jspace/results/ablate_v2"
DATA = "/workspace/bridge-jspace/data/tasks_v2/jsuite_v4p4002_test_chat/items.jsonl"
MODELS = {"9B": ("qwen35_9b_", "Qwen/Qwen3.5-9B", "c202236235762e1c871ad0ccb60c8ee5ba337b9a"),
          "27B": ("", "Qwen/Qwen3.6-27B", "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9"),
          "Lightning": ("nem35l_", "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16", "a9904d24bcc1d289a1950fa9d2b978c47cf903b9")}
CONDS = ["none", "paper10", "paper10_rot", "paper10_onlyA", "top30_keepRE", "ansJ"]
lit = lambda v: ast.literal_eval(v) if isinstance(v, str) else v
items = {json.loads(l)["id"]: json.loads(l) for l in open(DATA)}
a1 = []
out = open(sys.argv[1], "w")
for m, (p, repo, rev) in MODELS.items():
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    forms = lambda v, k="open": {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k), S.ids(tok, " " + v)[0], S.ids(tok, " " + v.lower())[0]}
    d = f"{R}/{p}jsuite_v4p4002_test_chat_ko57_cand2_v1"
    riv = {json.loads(l)["id"]: json.loads(l) for l in open(f"{d}/n57_rows.jsonl")}
    raw = collections.defaultdict(dict)
    for l in open(f"{d}/rows.jsonl"):
        r = json.loads(l)
        if r.get("kind", "clean") == "clean" and r["condition"] in CONDS and r["family"] == "MM":
            raw[r["id"]][r["condition"]] = r
    for i, cs in raw.items():
        it = items[i]; pv = lit(it["passage_values"]); ents = lit(it["entities"])
        top10 = lit(riv[i]["top10"]) if i in riv else []
        rec = {"model": m, "src": "ko57", "id": i, "bridge": it["bridge"], "rel": it["relation"], "bpos": int(it["bridge_position"]),
               "n_ent": len(ents), "conds": {}}
        for c, r in cs.items():
            t = r["pick2"]
            hit = [j for j, e in enumerate(ents) if e in pv and t in forms(pv[e])]
            rec["conds"][c] = {"correct": bool(r["correct_cand2"]), "pv_pos": hit, "x_hit": any(ents[j] == it["bridge"] for j in hit),
                               "rank_in_clean_top10": (top10.index(t) + 1) if t in top10 else None}
        out.write(json.dumps(rec) + "\n")
    # natural failures and successes (clean, competence run's read_top string)
    for x in a1:
        if x["model"] != m or not x["family"].startswith("MM_"): continue
        it = items[x["id"]]; pv = lit(it["passage_values"]); ents = lit(it["entities"]); vocab = sorted(set(lit(it["answer_vocab"])))
        rt = (x["comp"].get("whole") or {}).get("read_top")
        if rt is None: continue
        dec = lambda v: {tok.decode([t]).strip() for t in forms(v)}
        cat = "non_answer"
        gold_d = dec(it["answer"]); xpv_d = dec(pv[it["bridge"]]); opv_d = set().union(*[dec(pv[e]) for e in ents if e != it["bridge"] and e in pv])
        voc_d = set().union(*[dec(v) for v in vocab])
        s = rt.strip()
        amb = sum([s in gold_d, s in xpv_d, s in opv_d])
        cat = "gold" if s in gold_d else "x_pv" if s in xpv_d else "other_pv" if s in opv_d else "answer" if s in voc_d else "non_answer"
        out.write(json.dumps({"model": m, "src": "natural", "id": x["id"], "family": x["family"], "bridge": it["bridge"], "bpos": int(it["bridge_position"]),
                              "read_top": rt, "cat": cat, "ambiguous": amb > 1}) + "\n")
    print(m, flush=True)
