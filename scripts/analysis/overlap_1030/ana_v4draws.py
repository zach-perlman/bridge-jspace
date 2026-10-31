"""overlap agent (post hoc): note 37 (gap, keepA rescue) on v4 draws p4002 / p4003, split by the draw-4001 overlap cut
(per bridge: concept-token excess share in A at the band's middle layer; bridges without a concept token excluded), and by relation."""
import collections, json, statistics as st, sys
ROOT = "/workspace/bridge-jspace"
sys.path[:0] = [ROOT, ROOT + "/scripts"]
from scripts import nn_ko37_read as K
from scripts.nn_ko49_read import rows_at
from pathlib import Path
RES = Path(ROOT) / "results" / "ablate_v2"
MODELS = {"qwen35_9b_": "qwen3.5-9b", "": "qwen3.6-27b", "nem35l_": "nemotron-3.5-lightning"}
ana = json.load(open("/tmp/ana_v4.json"))
out = {}
def sub(acc, ids):
    return collections.defaultdict(dict, {k: {i: v for i, v in d.items() if i in ids} for k, d in acc.items()})
def met(acc, items, ids):
    m = K.measures(sub(acc, ids), items, lambda it: True)
    cs = m.get("conditions", {}); r = m.get("ratio", {})
    p = cs.get("paper10", {})
    return {"n_MM": m["n"].get("MM"), "n_br": len({items[i]["bridge"] for i in ids if i in acc[("MM", "none")]}), "gap": p.get("gap"), "gap_ci": p.get("gap_ci"),
            "lossMP": p.get("loss_MP"), "rescue": None if r.get("ratio") is None else round(1 - r["ratio"], 3),
            "rescue_ci": None if not r.get("ratio_ci") else [round(1 - r["ratio_ci"][1], 3), round(1 - r["ratio_ci"][0], 3)],
            "gap_keepA": cs.get("paper10_keepA", {}).get("gap")}
for P, target in MODELS.items():
    ov = json.load(open(f"/tmp/ov_v4_{target}.json"))
    mid = str(ov["mid"]); res = ov["sets"]["jsuite_v4_test_chat"]
    exc = {k: v["per_layer"][mid]["A"] - st.mean(v["per_layer"][mid]["rand"]) for k, v in res.items() if "skipped" not in v}
    cut = ana[P or "27b_"]["excess_A"]["cut"]
    for d in ("p4002", "p4003"):
        SET = f"jsuite_v4{d}_test_chat"
        run = RES / f"{P}{SET}_ko37_cand2_v1"
        if not (run / "rows.jsonl").exists():
            continue
        items = {json.loads(l)["id"]: json.loads(l) for l in open(f"{ROOT}/data/tasks_v2/{SET}/items.jsonl")}
        acc = rows_at(run)
        gated = set(acc[("MM", "none")]) | set(acc[("MP", "none")])
        key = lambda i: f"{items[i]['relation']}|{items[i]['bridge']}"
        miss = {key(i) for i in gated} - set(exc) - {k for k, v in res.items()}
        rec = {"bridges_not_in_4001": len(miss), "all": met(acc, items, gated),
               "low": met(acc, items, {i for i in gated if key(i) in exc and exc[key(i)] <= cut}),
               "high": met(acc, items, {i for i in gated if key(i) in exc and exc[key(i)] > cut}),
               "no_concept": met(acc, items, {i for i in gated if key(i) not in exc})}
        for rel in ("people", "cities", "companies", "landmarks"):
            rec[rel] = met(acc, items, {i for i in gated if items[i]["relation"] == rel})
        out[f"{P or '27b_'}{d}"] = rec
        print("==", P or "27b_", d, "bridges not in 4001's table:", len(miss))
        for k, v in rec.items():
            if isinstance(v, dict):
                print(f"  {k:10s} {v}")
json.dump(out, open("/tmp/ana_v4draws.json", "w"), indent=1)
