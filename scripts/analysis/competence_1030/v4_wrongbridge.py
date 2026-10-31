"""[C] post hoc (agent 'competence', 2026-10-30, CPU, stored rows only): (1) a v4 analogue of note 9's wrong-bridge test from
the v4 competence runs (hop 1's greedy name; the whole question's top-token read 'read_top'); (2) the v4 knock-out gap on
the 'no revealing name' subset alone (scripts/ko_subsets_v4.run with one extra subset). Not pre-registered."""
import collections, json, random, re, sys
from pathlib import Path
sys.path[:0] = [".", "scripts"]
import ko_subsets_v4 as KS

ROOT = Path(".")
B = {(b["relation"], b["bridge"]): b for b in json.load(open("data/v3_bridges.json"))}
MODELS = [("qwen35_9b_", "Qwen3.5-9B"), ("", "Qwen3.6-27B"), ("nem35l_", "Nemotron-3.5-Lightning")]
items = {json.loads(l)["id"]: json.loads(l) for l in open("data/tasks_v2/jsuite_v4_test_chat/items.jsonl")}
fold = lambda s: re.sub(r"[^a-z]", "", s.lower())

def names(rel, e):
    b = B.get((rel, e)); alts = []
    if b:
        a = b.get("bridge_alts"); alts = a if isinstance(a, list) else eval(a) if a else []
    return [e] + list(alts)

def real(rel, e):
    b = B.get((rel, e)); return b["answer"] if b else None

def pick(read_top, values):
    """the one value whose folded form starts with the folded first token, else None (ambiguous / none)."""
    t = fold(read_top or "")
    if not t: return None
    hits = {v for v in values if v and fold(v).startswith(t)}
    return hits.pop() if len(hits) == 1 else ("AMBIG" if hits else None)

out = {}
for P, name in MODELS:
    rows = collections.defaultdict(dict)
    for l in open(f"results/tasks_v2/{P}jsuite_v4_test_chat_competence_cand2_v1/items.jsonl"):
        r = json.loads(l); rows[r["id"]][r["part"]] = r
    res = {}
    for w in ("MP", "MM"):
        cnt = collections.Counter(); per = collections.defaultdict(list)
        for i, pr in rows.items():
            if f":{w}-" not in i or "step1" not in pr or "whole" not in pr: continue
            it = items[i]; X, rel, ents = it["bridge"], it["relation"], it["entities"]
            gen = pr["step1"].get("gen") or ""
            hit = lambda e: any(re.search(r"\b" + re.escape(n.lower()) + r"\b", gen.lower()) for n in names(rel, e))
            if hit(X): cnt["hop1_right"] += 1; continue
            others = [e for e in ents if e != X and hit(e)]
            if len(others) != 1: cnt["hop1_unknown_or_multi"] += 1; continue
            Bp = others[0]
            val = (lambda e: it["passage_values"][e]) if w == "MP" else (lambda e: real(rel, e))
            if val(Bp) is None or val(X) is None or fold(val(Bp)) == fold(val(X)): cnt["wrong_same_or_unknown_value"] += 1; continue
            dist = [e for e in ents if e not in (X, Bp)]
            vals = {e: val(e) for e in ents}
            p = pick(pr["whole"].get("read_top"), [v for v in vals.values()])
            if p == "AMBIG": cnt["read_ambiguous"] += 1; continue
            cnt["wrong_known"] += 1
            own = p is not None and fold(p) == fold(vals[Bp]); tru = p is not None and fold(p) == fold(vals[X])
            dv = [vals[e] for e in dist if vals[e] and fold(vals[e]) not in (fold(vals[Bp]), fold(vals[X]))]
            base = sum(p is not None and fold(p) == fold(v) for v in dv) / len(dv) if dv else 0.0
            per[X].append((own, tru, base))
        us = [u for k in per for u in per[k]]
        n = len(us)
        f = lambda us: 100 * (sum(o for o, _, _ in us) - sum(b for _, _, b in us)) / len(us)
        keys, rng, bs = sorted(per), random.Random(0), []
        for _ in range(2000):
            s = [u for k in (rng.choice(keys) for _ in keys) for u in per[k]]
            if s: bs.append(f(s))
        bs.sort()
        res[w] = {"counts": dict(cnt), "n": n, "own_bridge": round(100 * sum(o for o, _, _ in us) / n, 1) if n else None,
                  "true_despite_wrong": round(100 * sum(t for _, t, _ in us) / n, 1) if n else None,
                  "baseline_per_distractor": round(100 * sum(b for _, _, b in us) / n, 1) if n else None,
                  "own_minus_baseline": round(f(us), 1) if n else None,
                  "ci": [round(bs[int(0.025 * len(bs))], 1), round(bs[int(0.975 * len(bs)) - 1], 1)] if bs else None,
                  "n_bridges": len(keys)}
    out[name] = {"wrongbridge_v4_4001": res}
# (2) knock-out gap without revealing names only
KS.SUBSETS = {"all": KS.SUBSETS["all"], "no revealing name": lambda it: not it.get("name_reveals_answer"),
              "revealing name only": lambda it: bool(it.get("name_reveals_answer"))}
for P, name in MODELS:
    r = KS.run(P)
    out[name]["ko_subsets"] = {s: {c: r[s][c] for c in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize") if c in r[s]} for s in r}
print(json.dumps(out, indent=1))
