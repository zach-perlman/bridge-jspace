"""competence card data (agent 'competence', 2026-10-30; CPU, stored runs only; run from the box repo root).
Reads stored competence / competence_variants / knock-out runs and prints one JSON with every number + its source path."""
import collections, json, sys
from pathlib import Path
sys.path[:0] = [".", "scripts", "src"]
from scripts.nn_swap import v4_split
from scripts.score_greedy import right

R = Path("results"); D = Path("data/tasks_v2")
MODELS = [("qwen35_9b_", "Qwen3.5-9B"), ("", "Qwen3.6-27B"), ("nem35l_", "Nemotron-3.5-Lightning")]
SETS = {  # tag: (set, cv, ctl, ko-run suffix, words)
    "v4_4001": ("jsuite_v4_test_chat", "jsuite_v4_cv_v1", "jsuite_v4ctl_test_chat", "jsuite_v4_test_chat_ko_cand2_v1", ("MP", "MM")),
    "v4_4002": ("jsuite_v4p4002_test_chat", "jsuite_v4p4002_cv_v1", "jsuite_v4p4002ctl_test_chat", "jsuite_v4p4002_test_chat_ko37_cand2_v1", ("MP", "MM")),
    "v4_4003": ("jsuite_v4p4003_test_chat", "jsuite_v4p4003_cv_v1", "jsuite_v4p4003ctl_test_chat", "jsuite_v4p4003_test_chat_ko37_cand2_v1", ("MP", "MM")),
    "v5al": ("jsuite_v5al_test_chat", "jsuite_v5alctl_cv_v1", "jsuite_v5alctl_test_chat", "jsuite_v5al_test_chat_ko_cand2_v1", ("MP", "MM")),
    "v5kn2c": ("jsuite_v5kn2c_test_chat", "jsuite_v5kn2cctl_cv_v1", "jsuite_v5kn2cctl_test_chat", "jsuite_v5kn2c_test_chat_ko_cand2_v1", ("MC", "MC0")),
}
pct = lambda a, b: round(100 * a / b, 1) if b else None
out = {}
for P, name in MODELS:
    for tag, (S, CV, CTL, KO, words) in SETS.items():
        comp = f"{P}{S.replace('_test_chat', '')}_test_chat_competence_cand2_v1"
        cvr = f"{P}{CV}"; kor = f"{P}{KO}"
        items = {json.loads(l)["id"]: json.loads(l) for l in (D / S / "items.jsonl").open()}
        ctl = {json.loads(l)["id"]: json.loads(l) for l in (D / CTL / "items.jsonl").open()}
        parts = collections.defaultdict(dict); s1 = collections.defaultdict(dict)
        for l in (R / "tasks_v2" / comp / "items.jsonl").open():
            r = json.loads(l); parts[r["id"]][r["part"]] = bool(r["correct"])
            if r["part"] == "step1":
                s1[r["id"]] = {"gen": r.get("correct_gen"), "cand2": r.get("correct_cand2")}
        split = v4_split(comp, cvr, S)
        # knock-out rows: distinct gated ids per family (kind clean)
        ko_ids = collections.defaultdict(set)
        kop = R / "ablate_v2" / kor / "rows.jsonl"
        for l in kop.open():
            r = json.loads(l)
            if r.get("kind") == "clean": ko_ids[r["family"]].add(r["id"])
        kos = json.loads((R / "ablate_v2" / kor / "summary.json").read_text())
        cell = next(iter(kos["cells"].values()))
        res = {"sources": {"competence": f"results/tasks_v2/{comp}/items.jsonl", "cv": f"results/competence_variants/{cvr}/rows.jsonl",
                           "ko": f"results/ablate_v2/{kor}/{{summary.json,rows.jsonl}}", "data": f"data/tasks_v2/{S}/items.jsonl"}}
        for w in words:
            ids = [i for i in parts if f":{w}-" in i]
            acc = lambda k: (sum(parts[i][k] for i in ids if k in parts[i]), sum(1 for i in ids if k in parts[i]))
            c = {}
            for k in ("whole", "step1", "step2", "guess"):
                a, n = acc(k); c[k] = pct(a, n); c[k + "_n"] = n
            voc = [len(items[i].get("answer_vocab") or []) for i in ids]
            c["chance_vocab"] = round(100 * sum(1 / v for v in voc if v) / len(voc), 1)
            # majority-answer baseline per relation (domain), pooled
            byd = collections.defaultdict(collections.Counter)
            for i in ids: byd[items[i]["domain"]][items[i]["answer"]] += 1
            c["majority"] = pct(sum(cn.most_common(1)[0][1] for cn in byd.values()), len(ids))
            # composition given both hops right (hop 1 with passage, hop 2 alone)
            both = [i for i in ids if parts[i].get("step1") and parts[i].get("step2")]
            c["whole_given_both_hops"] = pct(sum(parts[i]["whole"] for i in both), len(both)); c["both_hops_n"] = len(both)
            # shortcut diagnostic: hop 1 (with passage) wrong, whole right
            h1x = [i for i in ids if "step1" in parts[i] and not parts[i]["step1"]]
            c["h1x_n"] = len(h1x); c["h1x_whole_right"] = pct(sum(parts[i]["whole"] for i in h1x), len(h1x))
            # hop 1 gen vs cand2 agreement
            g = [s1[i] for i in ids if i in s1 and s1[i]["gen"] is not None]
            c["hop1_gen_acc"] = pct(sum(bool(x["gen"]) for x in g), len(g)); c["hop1_cand2_acc"] = pct(sum(bool(x["cand2"]) for x in g), len(g))
            c["hop1_gen_cand2_agree"] = pct(sum(bool(x["gen"]) == bool(x["cand2"]) for x in g), len(g))
            # gate (scripts/nn_swap.v4_split: closed-book/ctl H1 right, hop 2 right, guess wrong; ok = whole right)
            ok = [i for i, s in split.items() if f":{w}-" in i and s == "ok"]; fail = [i for i, s in split.items() if f":{w}-" in i and s == "fail"]
            c["gate_ok"] = len(ok); c["gate_fail"] = len(fail); c["gate_whole_rate"] = pct(len(ok), len(ok) + len(fail))
            # knock-out gated n (summary) and the rows' distinct ids
            fam = cell.get(f"{w}/clean", {})
            c["ko_n_summary"] = fam.get("paper10", {}).get("n"); c["ko_n_rows"] = len(ko_ids.get(w, ()))
            c["ko_unedited_acc"] = round(100 * kos["unedited_accuracy"].get(f"{w}/clean", float("nan")), 1)
            c["ko_band"] = next(iter(kos["cells"]))
            c["ko_ids_subset_of_gate_ok"] = ko_ids.get(w, set()) <= set(ok)
            # name-reveal / eponymous flags
            c["name_reveals_all"] = sum(bool(items[i].get("name_reveals_answer")) for i in ids)
            c["name_reveals_in_ko"] = sum(bool(items[i].get("name_reveals_answer")) for i in ko_ids.get(w, ()))
            c["eponymous_in_ko"] = sum(bool(items[i].get("eponymous")) for i in ko_ids.get(w, ()))
            res[w] = c
        # controls (cv rows): cand2 acc, greedy alias-match acc, agreement
        cv = collections.defaultdict(list)
        for l in (R / "competence_variants" / cvr / "rows.jsonl").open():
            r = json.loads(l)
            if r.get("variant", "none") != "none": continue
            it = ctl[r["id"]]
            gr = any(right(r["text"], v) for v in {it["answer"], *(it.get("answer_aliases") or [])})
            cv[r["word"]].append((r["correct_cand2"] in (True, "True"), gr))
        res["controls"] = {w: {"n": len(v), "cand2": pct(sum(a for a, _ in v), len(v)), "greedy": pct(sum(b for _, b in v), len(v)),
                               "agree": pct(sum(a == b for a, b in v), len(v))} for w, v in sorted(cv.items())}
        out.setdefault(name, {})[tag] = res
        print(name, tag, "done", file=sys.stderr, flush=True)
# v2 greedy vs cand2 (Q0 greedy_all, amendment 58 note 1)
for P, name in MODELS:
    f = R / "greedy_all" / f"{P}greedy_all_v2test_v1" / "score_v1.json"
    d = json.loads(f.read_text())["cells"]
    out[name]["v2_greedy"] = {"source": str(f), **{w: d[w] for w in ("MP", "MM", "PM", "PP", "PK", "MK") if w in d}}
print(json.dumps(out, indent=1))
