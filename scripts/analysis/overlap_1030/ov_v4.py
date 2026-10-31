"""overlap agent (post hoc, exploratory; CPU, lens files only): bridge-answer overlap for v4 items.

For each v4 bridge X (the described entity; items' "bridge" = steps[0].answer) and each layer of the model's v4 band:
  share_A   = mean over the bridge's unit J++ vectors (first tokens of "X" and " X", letter tokens) of |P_A b|^2,
              A = span of the unit J++ vectors of the item's keepA "forms" rows (ablate_v2.tasks_prompts lines 333-343,
              --keepA-forms every), letter tokens only; same construction as paper_swap_6b.shares.
  rand_A    = the same share for 20 random letter-token spans of |A| rows (random.Random(f"ovv4:{target}:{rel}:{k}"),
              never A's rows or any bridge token of the relation); excess_A = share_A - mean(rand_A).
  share_own = share inside span(the item's own memory answer's forms: as written / lower, with / without a leading space,
              first tokens; letter rows), with 20 random spans of the same size (random.Random(f"ovv4own:{target}:{X}:{k}")).
Writes /tmp/ov_v4_<target>.json.
BJ_TARGET=<target> python /tmp/ov_v4.py SET [SET ...]
"""

import json
import os
import random
import statistics
import sys
import time

ROOT = "/workspace/bridge-jspace"
sys.path[:0] = [ROOT + "/src", ROOT, ROOT + "/scripts"]
import torch  # noqa: E402

torch.set_num_threads(12)
from bridge_jspace import pins  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.tokens import concept_token, load_tokenizer  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts.paper_swap_6b import LensOnly, letter_ids, shares  # noqa: E402

BANDS = {"qwen3.5-9b": (12, 16), "qwen3.6-27b": (32, 40), "nemotron-3.5-lightning": (27, 33)}
N_RAND = 20
target = pins.TARGET
assert pins.FROZEN_LENS == "jpp", pins.FROZEN_LENS
lo, hi = BANDS[target]
layers = list(range(lo, hi + 1))
mid = (lo + hi) // 2
t0 = time.time()
lm = LensOnly("cpu")
lens = JLens(lm, "jpp")
tok = load_tokenizer()
W = lm.hf.lm_head.weight
gain = lm.norm_gain()
letters = letter_ids(tok, W.shape[0])
LET = set(letters)
print(f"{target}: loaded, {len(letters)} letters, {time.time() - t0:.0f}s", flush=True)
Jc = {}


def J(la):
    if la not in Jc:
        Jc[la] = lens._J_cpu[la].float()
    return Jc[la]


def vec(la, ids):
    rows = (W[torch.tensor(ids, dtype=torch.long)].float() * gain) @ J(la)
    return torch.nn.functional.normalize(rows, dim=-1)


def first(text):
    x = S.ids(tok, text)
    return x[0] if x else None


def item_forms(it):
    """ablate_v2.tasks_prompts' 'forms' for the clean question (kind open)."""
    k, a = it["kind"], it["answer"]
    vocab = it["answer_vocab"]
    both = lambda v: {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k)}  # noqa: E731
    ok2 = both(a)
    cands2 = {t for v in vocab for t in both(v)} | ok2
    sp = lambda v: {S.ids(tok, " " + v)[0], S.ids(tok, " " + v.lower())[0]}  # noqa: E731
    src = set(vocab) | {a}
    return sorted(cands2 | {t for v in src for t in sp(v)})


def own_forms(a):
    return sorted({t for t in (first(a), first(a.lower()), first(" " + a), first(" " + a.lower())) if t is not None})


out = {"target": target, "band": [lo, hi], "mid": mid, "layers": layers, "sets": {}}
rand_cache = {}
for SET in sys.argv[1:]:
    items = [json.loads(l) for l in open(f"{ROOT}/data/tasks_v2/{SET}/items.jsonl")]
    items = [it for it in items if it["word"] in ("MM", "MP")]
    rel_bridges = {}
    for it in items:
        rel_bridges.setdefault(it["relation"], set()).add(it["steps"][0]["answer"])
    res = {}
    A_by_rel = {}
    for it in items:
        if it["word"] != "MM":
            continue
        A = tuple(sorted(set(item_forms(it)) & LET))
        A_by_rel.setdefault(it["relation"], set()).add(A)
    for rel, As in A_by_rel.items():
        assert len(As) == 1, (rel, len(As))  # MM forms are relation-level (the memory answer is in the vocab)
    for it in items:
        X = it["steps"][0]["answer"]
        rel = it["relation"]
        key = f"{rel}|{X}"
        if key in res:
            continue
        mm = next(j for j in items if j["word"] == "MM" and j["steps"][0]["answer"] == X and j["relation"] == rel)
        A = list(next(iter(A_by_rel[rel])))
        B = sorted({t for t in (first(X), first(" " + X)) if t is not None and t in LET})
        try:
            ct = concept_token(tok, X)
            single = True
        except ValueError:
            ct, single = None, False
        own = sorted(set(own_forms(mm["answer"])) & LET)
        bar = set(A) | {t for x in rel_bridges[rel] for t in (first(x), first(" " + x)) if t is not None}
        if (rel, len(A)) not in rand_cache:
            pool = sorted(LET - bar)
            rand_cache[(rel, len(A))] = [sorted(random.Random(f"ovv4:{target}:{rel}:{k}").sample(pool, len(A))) for k in range(N_RAND)]
        rands = rand_cache[(rel, len(A))]
        per = {}
        if ct is None or ct not in LET:
            res[key] = {"relation": rel, "bridge": X, "answer": mm["answer"], "skipped": "no single-token concept surface", "B_first": B}
            continue
        pool_own = sorted(LET - set(own) - {ct})
        rands_own = [sorted(random.Random(f"ovv4own:{target}:{X}:{k}").sample(pool_own, len(own))) for k in range(N_RAND)] if own else []
        for la in layers:
            Bv = vec(la, [ct])
            r = {"A": shares(vec(la, A), Bv), "rand": [shares(vec(la, s), Bv) for s in rands]}
            if own:
                r["own"] = shares(vec(la, own), Bv)
                r["rand_own"] = [shares(vec(la, s), Bv) for s in rands_own]
            per[la] = r
        res[key] = {"relation": rel, "bridge": X, "answer": mm["answer"], "n_A": len(A), "concept": ct, "concept_in_A": ct in set(A), "B_first": B,
                    "single_token": single, "name_reveals_answer": mm.get("name_reveals_answer", False),
                    "concept_decoded": tok.decode([ct]), "per_layer": per}
    out["sets"][SET] = res
    print(f"{target} {SET}: {len(res)} bridges, {time.time() - t0:.0f}s", flush=True)
json.dump(out, open(f"/tmp/ov_v4_{target}.json", "w"))
print("done", time.time() - t0)
