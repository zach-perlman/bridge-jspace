"""fullname_gate_v4 (post hoc, NOT pre-registered; 2026-10-30, Zach's MC: "Full-name gate check (CPU)").
The v4 gate's closed-book hop-1 check (nn_swap.v4_split) passes an item if cand2 is right or the greedy reply STARTS with
the bridge's name or an alias (score_greedy.right). Replies that give the full name ("Chinua Achebe" for "Achebe") fail.
Here: per model, how many scenes fail H1 only because of that (the reply contains a name/alias as a whole word, not at the
start), how many of them would pass the rest of the gate (step2 right, guess wrong), how they differ from gated items, and
how far they could move the knock-out gap (bounds; their knock-out rows do not exist)."""
import collections, json, re, sys
sys.path.insert(0, "/workspace/bridge-jspace")
from scripts.score_greedy import right, clean, fold, ALIASES  # noqa: E402

R = "/workspace/bridge-jspace/results"
D = "/workspace/bridge-jspace/data/tasks_v2"
ctl = {json.loads(l)["id"]: json.loads(l) for l in open(f"{D}/jsuite_v4ctl_test_chat/items.jsonl")}
main = {json.loads(l)["id"]: json.loads(l) for l in open(f"{D}/jsuite_v4_test_chat/items.jsonl")}

def contains(text, ans):
    t = clean(text)
    for a in ALIASES.get(ans, set()) | {ans}:
        fa = fold(a)
        if fa and re.search(r"(?<![a-z])" + re.escape(fa) + r"(?![a-z])", t):
            return True
    return False

def ko_gap(P):
    acc = collections.defaultdict(dict)
    for l in open(f"{R}/ablate_v2/{P}jsuite_v4_test_chat_ko_cand2_v1/rows.jsonl"):
        r = json.loads(l)
        if r.get("kind", "clean") == "clean" and r["condition"] in ("none", "paper10"):
            acc[(r["family"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
    loss = {f: 100 * sum(acc[(f, "none")][i] - acc[(f, "paper10")][i] for i in acc[(f, "none")]) / len(acc[(f, "none")]) for f in ("MM", "MP")}
    n = {f: len(acc[(f, "none")]) for f in ("MM", "MP")}
    return loss, n

out = {}
for m, P in (("9b", "qwen35_9b_"), ("27b", ""), ("lightning", "nem35l_")):
    h1_strict, h1_lenient = {}, {}
    for l in open(f"{R}/competence_variants/{P}jsuite_v4_cv_v1/rows.jsonl"):
        r = json.loads(l)
        if r.get("variant", "none") == "none" and ":H1-" in r["id"]:
            it = ctl[r["id"]]
            names = {it["answer"], *it["answer_aliases"]}
            k = r["id"].replace(":H1-", ":XX-")
            h1_strict[k] = bool(r["correct_cand2"]) or any(right(r["text"], v) for v in names)
            h1_lenient[k] = h1_strict[k] or any(contains(r["text"], v) for v in names)
    parts = collections.defaultdict(dict)
    for l in open(f"{R}/tasks_v2/{P}jsuite_v4_test_chat_competence_cand2_v1/items.jsonl"):
        r = json.loads(l)
        parts[r["id"]][r["part"]] = bool(r["correct"])
    rec = collections.Counter(); rel = collections.Counter(); relg = collections.Counter(); pop = collections.Counter(); popg = collections.Counter()
    whole = {"new": collections.Counter(), "gated": collections.Counter()}
    for i, d in parts.items():
        if not (":MP-" in i or ":MM-" in i):
            continue
        fam = "MM" if ":MM-" in i else "MP"
        key = i.replace(":MP-", ":XX-").replace(":MM-", ":XX-")
        rest = d.get("step2") and d.get("guess") is False
        if h1_strict.get(key) and rest:
            rec[f"gated_{fam}"] += 1; relg[main[i]["relation"]] += 1; popg[main[i].get("popularity")] += 1
            whole["gated"][fam] += bool(d.get("whole")); whole["gated"][fam + "_n"] += 1
        elif h1_lenient.get(key) and rest:
            rec[f"new_{fam}"] += 1; rel[main[i]["relation"]] += 1; pop[main[i].get("popularity")] += 1
            whole["new"][fam] += bool(d.get("whole")); whole["new"][fam + "_n"] += 1
    loss, n_ko = ko_gap(P)
    gap = loss["MM"] - loss["MP"]
    # the knock-out counts only items right unedited (whole ok); new items that would enter: whole-right ones
    m_new = {f: whole["new"][f] for f in ("MM", "MP")}
    def bound(mm_loss_new, mp_loss_new):
        mm = (loss["MM"] * n_ko["MM"] + mm_loss_new * m_new["MM"]) / (n_ko["MM"] + m_new["MM"])
        mp = (loss["MP"] * n_ko["MP"] + mp_loss_new * m_new["MP"]) / (n_ko["MP"] + m_new["MP"])
        return round(mm - mp, 1)
    out[m] = {"gap_now": round(gap, 1), "n_ko": n_ko, "new_gated_items": dict(rec),
              "new_whole_right": m_new,
              "gap_if_new_items_behave_like_gated": round(gap, 1),
              "gap_bounds": {"worst_low (new MM lose 0, new MP lose 100)": bound(0, 100), "worst_high (new MM lose 100, new MP lose 0)": bound(100, 0),
                             "new items show no gap (both lose the gated MP rate)": bound(loss["MP"], loss["MP"])},
              "relations_new": dict(rel), "relations_gated": dict(relg), "popularity_new": dict(pop), "popularity_gated": dict(popg),
              "whole_right_rate": {k: {f: round(100 * v[f] / max(1, v[f + "_n"]), 1) for f in ("MM", "MP")} for k, v in whole.items()}}
    print(m, json.dumps(out[m], indent=None)[:1500])
json.dump(out, open("/workspace/bridge-jspace/results/ablate_v2/nn_ko_read/v4_fullname_gate.json", "w"), indent=1)
