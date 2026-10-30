import collections, json
R = "/workspace/bridge-jspace/results"; D = "/workspace/bridge-jspace/data/tasks_v2"
main = {json.loads(l)["id"]: json.loads(l) for l in open(f"{D}/jsuite_v4_test_chat/items.jsonl")}
for m, P in (("9b", "qwen35_9b_"), ("27b", ""), ("lightning", "nem35l_")):
    acc = collections.defaultdict(dict)
    for l in open(f"{R}/ablate_v2/{P}jsuite_v4_test_chat_ko_cand2_v1/rows.jsonl"):
        r = json.loads(l)
        if r.get("kind", "clean") == "clean" and r["condition"] in ("none", "paper10", "paper10_rot"):
            acc[(r["family"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
    out = {}
    for rel in ("people", "other"):
        keep = (lambda i: main[i]["relation"] == "people") if rel == "people" else (lambda i: main[i]["relation"] != "people")
        res = {}
        for c in ("paper10", "paper10_rot"):
            l = {}
            for f in ("MM", "MP"):
                ids = [i for i in acc[(f, "none")] if keep(i)]
                l[f] = (100 * sum(acc[(f, "none")][i] - acc[(f, c)][i] for i in ids) / len(ids), len(ids))
            res[c] = (round(l["MM"][0] - l["MP"][0], 1), l["MM"][1], l["MP"][1])
        out[rel] = res
    print(m, out)
