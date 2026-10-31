"""cpuwins A3/A4 extract (post hoc, exploratory; 2026-10-30). CPU only, tokenizer only (no model weights loaded).
Reads results/ablate_v2/<P>jsuite_v4_test_chat_ko57_cand2_v1/{rows,n57_rows}.jsonl (note 57, draw 4001) and the v4 items,
and writes per MM item: clean/paper10 correctness, gold logp, paper10's pick2 token and its category (gold / X's passage
value / another entity's passage value / clean-top-10 rival / other relation answer / non-answer), E_A (= paper10 row's
retained.A, the share of the removal's energy in the answer span) and retained.R/R2/R4 (rank-matched random spans), edit_rel.
Also writes the same categories for other conditions (onlyA, top30, top30_keepRE, ansJ, ansRe, paper10_rot, onlyRperp)."""
import collections, json, os, sys, ast
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ.setdefault("HF_HOME", "/workspace/hf_cache")
sys.path.insert(0, "/workspace/bridge-jspace")
from transformers import AutoTokenizer
from scripts import suite_v1 as S

R = "/workspace/bridge-jspace/results/ablate_v2"
DATA = "/workspace/bridge-jspace/data/tasks_v2/jsuite_v4_test_chat/items.jsonl"
MODELS = {"9B": ("qwen35_9b_", "Qwen/Qwen3.5-9B", "c202236235762e1c871ad0ccb60c8ee5ba337b9a"),
          "27B": ("", "Qwen/Qwen3.6-27B", "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9"),
          "Lightning": ("nem35l_", "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16", "a9904d24bcc1d289a1950fa9d2b978c47cf903b9")}
CONDS = ["none", "paper10", "paper10_rot", "paper10_onlyA", "paper10_onlyRperp", "top30", "top30_keepRE", "top30_keepA", "ansJ", "ansRe"]

def lit(v):
    if isinstance(v, str):
        try:
            return ast.literal_eval(v)
        except Exception:
            return v
    return v

items = {}
for l in open(DATA):
    it = json.loads(l)
    if ":MM-" in it["id"] or ":MP-" in it["id"]:
        items[it["id"]] = it
out = open(sys.argv[1], "w")
for m, (p, repo, rev) in MODELS.items():
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    def forms(v, k="open"):
        return {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k), S.ids(tok, " " + v)[0], S.ids(tok, " " + v.lower())[0]}
    d = f"{R}/{p}jsuite_v4_test_chat_ko57_cand2_v1"
    riv = {json.loads(l)["id"]: json.loads(l) for l in open(f"{d}/n57_rows.jsonl")}
    raw = collections.defaultdict(dict)
    for l in open(f"{d}/rows.jsonl"):
        r = json.loads(l)
        if r.get("kind", "clean") == "clean" and r["condition"] in CONDS:
            raw[r["id"]][r["condition"]] = r
    n = 0
    for i, cs in raw.items():
        it = items[i]
        word = "MM" if ":MM-" in i else "MP"
        k = it["kind"]
        gold = it["answer"]
        pv = lit(it["passage_values"]); vocab = sorted(set(lit(it["answer_vocab"])))
        x_pv = pv.get(it["bridge"])
        other_pv = sorted({v for e, v in pv.items() if e != it["bridge"]})
        gold_f = forms(gold, k)
        xpv_f = forms(x_pv, k) if x_pv else set()
        opv_f = set().union(*[forms(v, k) for v in other_pv]) if other_pv else set()
        rv = riv.get(i, {})
        riv_tok = set(rv.get("riv_tok", [])) if isinstance(rv.get("riv_tok"), list) else set(lit(rv.get("riv_tok", "[]")))
        top10 = rv.get("top10"); top10 = lit(top10) if top10 is not None else []
        voc_f = {}
        for v in vocab:
            for t in forms(v, k):
                voc_f.setdefault(t, set()).add(v)
        # the real (remembered) attribute for MP items: X's real value
        real_f = forms(it["real"], k) if it.get("real") else set()
        rec = {"model": m, "id": i, "word": word, "bridge": it["bridge"], "rel": it["relation"], "gold": gold, "x_pv": x_pv,
               "real": it.get("real"), "n_vocab": len(vocab), "n_other_pv": len(other_pv), "conds": {}}
        for c, r in cs.items():
            t = r["pick2"]
            flags = {"gold": t in gold_f, "x_pv": t in xpv_f, "other_pv": t in opv_f, "rival": t in riv_tok,
                     "in_top10": t in set(top10), "answer": t in voc_f, "real": t in real_f}
            rec["conds"][c] = {"correct": bool(r["correct_cand2"]), "logp": r["logp"], "pick2": t, "dec": tok.decode([t]),
                               "flags": flags, "edit_rel": r.get("edit_rel"), "retained": r.get("retained")}
        out.write(json.dumps(rec) + "\n")
        n += 1
    print(m, n, flush=True)
