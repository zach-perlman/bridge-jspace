"""x47_agnostic (batch 47, test 47.11; jobs/c3/batch47.yaml amendment 4, rule fixed in advance; Q47.11 in
predictions/2026-10-28_dan.md): is the pointer item-agnostic?

Routes scenes (x6_routes' layout: three locker sentences first, then three pick sentences; C2, "another item moved":
Iris picked B in S, B's and C's locker sentences swapped, B's number new) with three item types in one job:
  animals  the routes test's items (the reference the new types are read against; U was fit on animal scenes)
  fruits   objects: single-token fruits; the recall asks the fruit's colour ("What color is Iris's pick?", a word read)
  names    people's names as the items ("The locker of Alice is 5." / "Iris picked Alice."), distinct from the three
           pickers' names; no attribute fact exists for a name, so the recall is skipped (the rule is about the
           lookup's position answers)
Same layout, slots and digits across the types: per scene index the five digits, the three people, the slot order and
the pick order come from one shared stream (SEED); only the items come from the type's own stream, so the ith scene of
each type differs in its items alone (a type whose ith scene fails a check loses it; counted).

Arms at the bridge word at L (the change Δ = h_S - h_O added on O; X0's chat read: the digit's space token appended
for a digit reader, nothing for a word reader; switch = the top token is S's answer's first token):
  whole; no_alf (without U: Δ - U U^T Δ) vs no_alf_rand (a random part of U's share of ||Δ||^2); keep_alf (only U:
  U U^T Δ) vs keep_alf_rand. U = x47_atoms.pointer_basis: x0_massmean's layout-free mass-mean directions of the locker
  slot, fit on the probe's fresh animal scenes, never refit.
  The fallback, always computed, read only if the rule fails: U' refit per item type inside the job on half the chosen
  scenes (seeded split; U' = x0_massmean.mass_mean of O's bridge-word states by the O bridge's locker slot, rank 2),
  arms no_refit / no_refit_rand / keep_refit / keep_refit_rand read on the other half only.
Readers: lookup "Which locker belongs to Iris's pick?" (every type); recall (animals: legs; fruits: colour). Gate 0.80
per reader per type on O unedited (read accuracy over the type's generated scenes); the items are the first N scenes
in generator order on which the lookup says and reads O's and S's answers right; the recall is read on those of them it
gets right too, where its gate passed (reported, not in the rule; a failed recall gate leaves the lookup test in place).

Rule (verbatim, jobs/c3/batch47.yaml 47.11): "An address, not an animal code" if without U cuts position answers >= 0.3
beyond random on both new item types (within 0.1 of the animal result), and only-U gives position >= 0.15. If it fails,
refit U per item type and report both: the code is slot x type.
As computed: per model and type, position share = the share of the type's lookup items whose top token is the position
route's digit (x6_routes.classify); fall = position share without the random part minus position share without U
(paired cluster bootstrap over the O bridge item, 10,000, seed 0, CI beside; point estimates decide, EPS 1e-9); the
animal result = the same job's animal type (the stored routes run's number reported beside). A new type holds if fall >=
0.3, |fall - fall_animals| <= 0.1 and the only-U position share >= 0.15. Q47.11 per model: yes if both new types hold;
no otherwise; "not tested" if the animal type or a new type failed its lookup gate. When a type fails: its refit on the
held-out half, same bars (fall' >= 0.3, keep' >= 0.15): "slot x type" if the refit passes where the fixed U did not.

SEALED: the run writes per-item files only; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's
committed Q47.11 answer at HEAD.

uv run python scripts/x47_agnostic.py plan --targets qwen3.5-9b muse-glimmer-30b   # CPU: pools, single-token checks,
                                                                                    #   5 rendered prompts per type
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_agnostic.py run --name qwen35_9b_x47_agnostic   # GPU (sealed)
uv run python scripts/x47_agnostic.py verdict     # CPU, after Dan's Q47.11
uv run python scripts/x47_agnostic.py view        # CPU, after Dan's Q47.11: 10 random items per type, seed 0
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_atoms as A

EXP = "x47_agnostic"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = A.PREDICTIONS
QUESTION = "Q47.11"
TYPES = ("animals", "fruits", "names")
REFERENCE, NEW_TYPES = "animals", ("fruits", "names")
SEED, SPLIT_SEED, N_GEN, N_ITEMS = 4711, 4712, R.N_GEN, R.N_ITEMS
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_agnostic", "muse-glimmer-30b": "muse30_x47_agnostic"}
STORED_ANIMALS = {
    "qwen3.5-9b": "qwen35_9b_x6_routes_keeponly",
    "muse-glimmer-30b": "muse30b_x6_routes",
}  # the stored routes runs
ARMS = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand")
REFIT_ARMS = ("no_refit", "no_refit_rand", "keep_refit", "keep_refit_rand")
ARM_TEXT = {"whole": "the whole change", "no_alf": "without U (fit on animals, not refit)",
            "no_alf_rand": "without a random part of U's share", "keep_alf": "only U", "keep_alf_rand": "only a random part of U's share",
            "no_refit": "without U' (refit on this type's fit half)", "no_refit_rand": "without a random part of U''s share",
            "keep_refit": "only U'", "keep_refit_rand": "only a random part of U''s share"}  # fmt: skip
FALL, NEAR, KEEP = 0.3, 0.1, 0.15
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULE = ('"An address, not an animal code" if without U cuts position answers >= 0.3 beyond random on both new item types '
        "(within 0.1 of the animal result), and only-U gives position >= 0.15. If it fails, refit U per item type and "
        "report both: the code is slot x type")  # fmt: skip
LOOKUP_Q = R.LOOKUP_Q
RECALL = {"animals": ("How many legs does {p}'s pick have?", "digit"), "fruits": ("What color is {p}'s pick?", "word"),
          "names": None}  # fmt: skip
# fruits with one common colour (the recall's one-word answer); "orange" the fruit is left out (its name is its colour)
FRUITS = {"banana": "yellow", "lemon": "yellow", "lime": "green", "cherry": "red", "plum": "purple", "strawberry": "red",
          "raspberry": "red", "blueberry": "blue", "blackberry": "black", "tomato": "red", "avocado": "green",
          "pumpkin": "orange", "apricot": "orange", "kiwi": "green", "pear": "green", "apple": "red", "melon": "green",
          "coconut": "brown", "cranberry": "red", "papaya": "orange", "fig": "purple", "olive": "green",
          "pomegranate": "red", "mango": "orange", "peach": "orange", "grape": "purple", "tangerine": "orange",
          "grapefruit": "pink", "watermelon": "green", "pineapple": "yellow"}  # fmt: skip
COLOURS = ("red", "yellow", "green", "orange", "purple", "blue", "black", "brown", "pink")
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


# ---- scenes (tokenizer only) ---------------------------------------------------------------------------------------


def ref(kind: str, x: str) -> str:
    """How an item is named in a sentence: 'the frog', 'the plum', 'Alice'."""
    return x if kind == "names" else f"the {x}"


def context(kind: str, lockers: list[tuple[str, int]], picks: list[tuple[str, str]]) -> str:
    return " ".join(
        [f"The locker of {ref(kind, x)} is {d}." for x, d in lockers]
        + [f"{p} picked {ref(kind, x)}." for p, x in picks]
    )


def item_pools(tok) -> tuple[dict[str, list[str]], dict[str, dict[str, Any]], dict[str, list[str]]]:
    """Per type its one-token items (on this tokenizer) and their facts (animals: legs; fruits: colour; names: none),
    and the words of each type's list that are not one token here (dropped, reported)."""
    from scripts import suite_v1 as S

    legs, animals, _ = R.pools(tok)
    lists = {"animals": animals, "fruits": sorted(FRUITS), "names": sorted(S.PEOPLE)}
    pools = {t: [w for w in words if R.one_token(tok, w)] for t, words in lists.items()}
    dropped = {t: [w for w in words if w not in pools[t]] for t, words in lists.items()}
    facts = {"animals": {a: legs[a] for a in pools["animals"]}, "fruits": {f: FRUITS[f] for f in pools["fruits"]},
             "names": {}}  # fmt: skip
    return pools, facts, dropped


def said_of(text: str, kind: str) -> str | None:
    """What the greedy text says: a digit (suite_v1.said) or the first colour word of its first line."""
    from scripts import suite_v1 as S

    if kind == "digit":
        return S.said(text, "digit")
    return next((w for w in re.findall(r"[a-z]+", S.first_line(text)) if w in COLOURS), None)


def encode(tok, kind: str, o: str, s: str, asked: str, a_item: str, bridge: str, facts: dict, expect: dict,
           scene: str, rendering: str = "chat") -> tuple[dict | None, str]:  # fmt: skip
    """Both readers' O and S prompts (the recall only for a type with a fact); the bridge one token at the same index
    in O and S (else dropped with the reason); each reader's read suffix (the digit's space token, or nothing for a
    word answer) and answer tokens (distinct, else dropped)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    specs = [(X.LOOKUP, LOOKUP_Q, "digit", (expect["original"], expect["value"]))]
    if RECALL[kind] is not None:
        q, rk = RECALL[kind]
        specs.append((X.RECALL, q, rk, (facts[a_item], facts[bridge])))
    readers, pos = {}, None
    for w, q, rk, ans in specs:
        ids, at = {}, {}
        for v, ctx, x in (("org", o, a_item), ("alt", s, bridge)):
            item = {"format": "prose", "kind": rk, "context": ctx, "question": q.format(p=asked)}
            text = X.render(tok, item, rendering, ctx)
            enc = raw_encoding(tok, text, offsets=True)
            sent = f"{asked} picked {ref(kind, x)}."
            assert ctx.count(sent) == 1, f"{scene}: the asked pick sentence is not once in the context"
            w0 = text.index(ctx) + ctx.index(sent) + sent.rindex(x)
            ids[v], at[v] = list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(x))
        if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
            return None, "the bridge is not one token at the same index in O and S"
        if pos is not None and at["org"][0] != pos:
            return None, "the readers' bridge positions differ"
        pos = at["org"][0]
        org_ans, alt_ans = (str(v) for v in ans)
        tok_a, tok_b = (S.answer_token(tok, x, rk) for x in (org_ans, alt_ans))
        if tok_a == tok_b:
            return None, f"{READER_NAME[w]}: O's and S's answers share their first token"
        readers[w] = {"question": q.format(p=asked), "kind": rk, "answer": org_ans, "cf_answer": alt_ans, "ids": ids,
                      "tok_A": tok_a, "tok_b": tok_b, "suffix": S.ids(tok, " ") if rk == "digit" else []}  # fmt: skip
    assert pos is not None
    if X.RECALL in readers:
        for v in ("org", "alt"):
            if readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1]:
                return None, "the readers' prompts differ before the bridge"
    routes = {k: S.answer_token(tok, str(v), "digit") for k, v in expect.items()}
    return {"scene": scene, "type": kind, "condition": "C2", "rendering": rendering, "domain": kind, "bridge": a_item,
            "cf_bridge": bridge, "context": o, "cf_context": s, "pos": pos, "expect": dict(expect),
            "route_tokens": routes, "readers": readers}, ""  # fmt: skip


def scenes(tok, n: int, types: tuple[str, ...] = TYPES, seed: int = SEED, rendering: str = "chat",
           pools_facts: tuple | None = None) -> tuple[list[dict], collections.Counter]:  # fmt: skip
    """n C2 scenes per type, matched across the types (the shared draws per scene index: digits a-e, the three people,
    the slot order of A / B / C and the pick order); the items from each type's own stream. Dropped scenes counted by
    type and reason."""
    pools, facts, _ = pools_facts or item_pools(tok)
    _, _, people = R.pools(tok)
    shared = random.Random(seed)
    streams = {t: random.Random(f"{EXP}|{seed}|{t}") for t in types}
    out: dict[str, list[dict]] = {t: [] for t in types}
    dropped: collections.Counter = collections.Counter()
    i = 0
    while any(len(out[t]) < n for t in types):
        i += 1
        assert i < 100 * n, f"the generator cannot fill {n} scenes per type: {dropped}"
        a, b, c, d, e = shared.sample(range(1, 10), 5)
        asked, p1, p2 = shared.sample(people, 3)
        order = shared.sample([0, 1, 2], 3)  # slot k holds the locker sentence of item order[k] (0 = A, 1 = B, 2 = C)
        pick_order = shared.sample([0, 1, 2], 3)
        for t in types:
            if len(out[t]) >= n:
                continue
            pool = [x for x in pools[t] if x not in (asked, p1, p2)] if t == "names" else pools[t]
            if len(pool) < 3:
                dropped[f"{t}: fewer than three items"] += 1
                continue
            items = streams[t].sample(pool, 3)
            A_, B_, C_ = items
            if t != "names" and facts[t][A_] == facts[t][B_]:
                dropped[f"{t}: A and B share their fact"] += 1
                continue
            val = {A_: a, B_: b, C_: c}
            lockers = [(items[j], val[items[j]]) for j in order]
            picks = [[(asked, A_), (p1, B_), (p2, C_)][j] for j in pick_order]
            o = context(t, lockers, picks)
            sw = {B_: C_, C_: B_}
            s_lock = [(sw.get(x, x), e if sw.get(x, x) == B_ else val[sw.get(x, x)]) for x, _ in lockers]
            s_pick = [(q, B_ if q == asked else x) for q, x in picks]
            s = context(t, s_lock, s_pick)
            expect = {"identity": b, "position": c, "value": e, "original": a}
            case, why = encode(tok, t, o, s, asked, A_, B_, facts[t], expect, f"{t}-{i:04d}", rendering)
            if case is None:
                dropped[f"{t}: {why}"] += 1
                continue
            case.update({"index": i, "slot_org": order.index(0), "slot_alt": order.index(1), "people": [asked, p1, p2],
                         "digits": [a, b, c, d, e], "items": items})  # fmt: skip
            out[t].append(case)
    return [c for t in types for c in out[t]], dropped


def single_token_report(targets: list[str]) -> dict:
    """Per type and target, which words of the fixed lists are one token (with a leading space) on the target's pinned
    tokenizer (the review's tokenizer.json), and the words kept on every target."""
    from bridge_jspace.review import checks as RC
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    legs = T.DOMAINS["animals"].values
    lists = {"animals": sorted(a for a in legs if 0 <= legs[a] <= 9), "fruits": sorted(FRUITS), "names": sorted(S.PEOPLE),
             "colours": list(COLOURS)}  # fmt: skip
    out: dict[str, Any] = {}
    for t, words in lists.items():
        per = {}
        for target in targets:
            tk = RC.tokenizer(target)
            per[target] = {w: len(tk.encode(" " + w, add_special_tokens=False).ids) == 1 for w in words}
        kept = [w for w in words if all(per[m][w] for m in targets)]
        out[t] = {"n": len(words), "kept_on_every_target": kept, "n_kept": len(kept),
                  "not_one_token": {m: [w for w in words if not per[m][w]] for m in targets}}  # fmt: skip
    return out


def stage_plan(targets: list[str], k: int = 5) -> dict:
    """Tokenizer only (the target's): the pools and single-token checks per target, the generated scenes per type and
    the drops, and k rendered prompts per type (seed 0) as the model will read them. The models' competence (read
    accuracy per reader and type) needs the GPU: the job measures it first and writes gate.json."""
    from scripts import x45m

    tok = x45m.tokenizer()
    pools, facts, dropped_words = item_pools(tok)
    cases, dropped = scenes(tok, N_GEN, pools_facts=(pools, facts, dropped_words))
    out: dict[str, Any] = {"target": pins.TARGET, "layer": X.PREDICTED[pins.TARGET], "seed": SEED,
                           "pools": {t: {"n": len(p), "items": p, "not_one_token_here": dropped_words[t]} for t, p in pools.items()},
                           "facts": {"fruits": facts["fruits"]}, "single_token": single_token_report(targets),
                           "cases": dict(collections.Counter(c["type"] for c in cases)), "dropped": dict(dropped),
                           "recall": {t: (RECALL[t][0] if RECALL[t] else "none: no clean one-token fact for a name; the recall is skipped")
                                      for t in TYPES},
                           "competence": "measured in the job (gate.json, printed first): O's read accuracy per reader and type, gate 0.80",
                           "examples": {}}  # fmt: skip
    for t in TYPES:
        mine = [c for c in cases if c["type"] == t]
        picks = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(mine)), min(k, len(mine))))
        out["examples"][t] = [{"scene": mine[i]["scene"], "O": mine[i]["context"], "S": mine[i]["cf_context"],
                               "expect": mine[i]["expect"], "pos": mine[i]["pos"],
                               "readers": {READER_NAME[w]: {"question": rd["question"], "answers": [rd["answer"], rd["cf_answer"]],
                                                            "prompt_O": R.marked(lambda ids: tok.decode(ids), rd["ids"]["org"], mine[i]["pos"])}
                                           for w, rd in mine[i]["readers"].items()}} for i in picks]  # fmt: skip
    folder = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{pins.RUN_PREFIX.rstrip('_')}"
    folder.mkdir(parents=True)
    (folder / "plan.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# 47.11 plan on {pins.TARGET} (L{out['layer']}): {k} rendered prompts per type (seed {X.EXAMPLES_SEED}), "
             "as the model reads them; ⟦...⟧ the bridge word. Counts in plan.json.", ""]  # fmt: skip
    for t, exs in out["examples"].items():
        lines += [
            f"## {t}: {out['cases'][t]} scenes generated; pool {out['pools'][t]['n']} items; recall: {out['recall'][t]}",
            "",
        ]
        for e in exs:
            lines += [f"### {e['scene']} (bridge token {e['pos']}; expected digits {e['expect']})", "", f"O: {e['O']}", "",
                      f"S: {e['S']}", ""]  # fmt: skip
            for w, rd in e["readers"].items():
                lines += [f"**{w}** ({rd['question']}; O answers {rd['answers'][0]}, S answers {rd['answers'][1]}):", "", "```",
                          rd["prompt_O"], "```", ""]  # fmt: skip
    (folder / "prompts.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k_: v for k_, v in out.items() if k_ != "examples"}, indent=1, ensure_ascii=False))
    print("wrote", folder)
    return out


# ---- GPU ------------------------------------------------------------------------------------------------------------


def competence(model, cases: list[dict], ws) -> list[dict]:
    """Unedited O and S prompts of each reader: 8 greedy tokens (what the model says), and the decisive read."""
    import torch

    from bridge_jspace.utils import progress

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (case)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                for i, (v, gold, tok_gold) in enumerate(
                    (("org", rd["answer"], rd["tok_A"]), ("alt", rd["cf_answer"], rd["tok_b"]))
                ):
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", rd["suffix"], ws)
                    said = said_of(texts[i], rd["kind"])
                    rows.append({"scene": c["scene"], "type": c["type"], "reader": w, "variant": v, "greedy": texts[i],
                                 "said": said, "right": said == gold, "read_right": int(logits[0].argmax()) == tok_gold})  # fmt: skip
    return rows


def gate_and_items(cases: list[dict], comp: list[dict], n: int = N_ITEMS, gate_min: float = X.GATE
                   ) -> tuple[dict, dict[str, list[dict]], dict[str, set[str]]]:  # fmt: skip
    """Per type: each reader's gate (O's read accuracy over the type's scenes >= gate_min) and eligible count; the
    chosen items (the first n lookup-eligible scenes in generator order, if the lookup's gate passed); the chosen scenes
    the recall is read on (those it gets right unedited on O and S, if its gate passed)."""
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate: dict[str, Any] = {}
    chosen: dict[str, list[dict]] = {}
    recall_on: dict[str, set[str]] = {}
    for t in dict.fromkeys(c["type"] for c in cases):
        mine = [c for c in cases if c["type"] == t]
        readers = list(mine[0]["readers"])
        g: dict[str, Any] = {"cases": len(mine), "readers": {}}
        ok: dict[str, list[dict]] = {}
        for w in readers:
            acc = float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in mine]))
            said = float(np.mean([right[(c["scene"], w, "org")]["right"] for c in mine]))
            ok[w] = [c for c in mine if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                            for v in ("org", "alt"))]  # fmt: skip
            g["readers"][READER_NAME[w]] = {"org_read_accuracy": acc, "org_said_accuracy": said,
                                            "pass": acc >= gate_min - EPS, "eligible": len(ok[w])}  # fmt: skip
        lk = g["readers"]["lookup"]
        chosen[t] = ok[X.LOOKUP][:n] if lk["pass"] else []
        rc = g["readers"].get("recall")
        recall_on[t] = (
            ({c["scene"] for c in ok[X.RECALL]} & {c["scene"] for c in chosen[t]}) if rc and rc["pass"] else set()
        )
        g.update({"chosen": len(chosen[t]), "recall_read_on": len(recall_on[t]), "gate": gate_min})
        gate[t] = g
    return gate, chosen, recall_on


def refit_basis(h_fit: np.ndarray, slots: list[int]) -> np.ndarray:
    """U' for one item type: x0_massmean's mass-mean directions of the locker slot (class means minus the grand mean,
    orthonormalised; rank = slots - 1) on the fit half's O bridge-word states [n, d]. The routes layout is one layout
    group, so subtracting the grand mean is the layout-free step."""
    from scripts import x0_massmean as MM

    assert len(set(slots)) >= 2, f"the fit half has {len(set(slots))} slot(s): no basis"
    u = MM.mass_mean(h_fit.astype(np.float64), slots)
    assert u.shape[1] >= 1, "the slot class means coincide: no refit basis"
    return u


def split_halves(scenes_: list[str], kind: str, seed: int = SPLIT_SEED) -> tuple[list[int], list[int]]:
    """The fit half and the test half of a type's chosen items (indices), one seeded shuffle per type."""
    idx = list(range(len(scenes_)))
    random.Random(f"{EXP}|{seed}|{kind}").shuffle(idx)
    half = len(idx) // 2
    return sorted(idx[:half]), sorted(idx[half:])


def pointer_basis(target: str) -> np.ndarray:
    """U: the pointer directions fit on fresh animal scenes (x47_atoms.pointer_basis; never refit), [d, r]."""
    return A.pointer_basis(target)


def stage_run(name: str, why: str, types: tuple[str, ...] = TYPES, n: int = N_ITEMS, gate_min: float = X.GATE) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.11 renders chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"47.11 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "47.11",
         "spec": "jobs/c3/batch47.yaml (47.11, amendment 4)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)}, "layer": layer, "types": list(types),
         "condition": "C2 (another item moved: Iris picks B; B's and C's locker sentences swapped, B's number new)",
         "n_per_type": n, "n_generated_per_type": N_GEN, "gate": gate_min, "arms": ARM_TEXT,
         "pointer": {"U": f"x47_atoms.pointer_basis ({R.STATES[target]}): layout-free mass-mean slot directions on fresh animal scenes, not refit",
                     "refit": "U' per type: x0_massmean.mass_mean of O's bridge-word states by the O bridge's locker slot on the "
                              "fit half (seeded split), read on the test half only (the fallback)"},
         "random_part": f"X0's random subspace at each part's share of ||Δ||^2, seed {X.SUBSPACE_SEED} + layer",
         "read": "X0's chat read: the digit's space token appended for a digit reader, nothing for a word reader; switch = "
                 "the top token is S's answer's first token; the lookup's top token classified identity / position / value / "
                 "original / other (x6_routes.classify)",
         "items_rule": "per type the first n scenes in generator order on which the lookup says and reads O's and S's "
                       "answers right, if its gate (O read accuracy >= gate) passed; the recall read on those it gets right "
                       "too, if its gate passed (reported, not in the rule)",
         "recall": {t: (RECALL[t][0] if RECALL[t] else "skipped: no clean fact for a name") for t in types},
         "rule": RULE, "bars": {"fall": FALL, "near_animals": NEAR, "keep": KEEP},
         "seeds": {"scenes": SEED, "split": SPLIT_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    pools, facts, dropped_words = item_pools(tok)
    cases, dropped = scenes(tok, N_GEN, types, pools_facts=(pools, facts, dropped_words))
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    comp = competence(model, cases, ws)
    gate, chosen, recall_on = gate_and_items(cases, comp, n, gate_min)
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    plan = {"pools": {t: {"n": len(p), "items": p, "not_one_token": dropped_words[t]} for t, p in pools.items()},
            "generated": dict(collections.Counter(c["type"] for c in cases)), "dropped": dict(dropped), "gate": gate}  # fmt: skip
    (out / "gate.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print("competence report:", json.dumps(gate, ensure_ascii=False), flush=True)
    assert any(chosen.values()), "no type passed the lookup's gate; see gate.json"
    alf = torch.tensor(pointer_basis(target), dtype=torch.float32, device=model.device)
    basis = None
    rows, norms, refit_info = [], [], {}
    with torch.no_grad():
        for t in types:
            mine = chosen[t]
            if not mine:
                continue
            h_org, deltas = [], []
            for c in progress(mine, f"{t}: Δ at the bridge word (case)"):
                ids = c["readers"][X.LOOKUP]["ids"]
                h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][c["pos"]]
                     for v in ("org", "alt")}  # fmt: skip
                h_org.append(h["org"].float())
                deltas.append((h["alt"] - h["org"]).float())
            x, h0 = torch.stack(deltas), torch.stack(h_org)
            if basis is None:
                basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(x.device)
            fit, test = split_halves([c["scene"] for c in mine], t)
            u2 = torch.tensor(refit_basis(h0[fit].cpu().numpy(), [mine[i]["slot_org"] for i in fit]),
                              dtype=torch.float32, device=x.device)  # fmt: skip
            parts = {"alf": (x @ alf) @ alf.T, "refit": (x @ u2) @ u2.T}
            arms, sh = {"whole": x}, {}
            for key, part in parts.items():
                sh[key] = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                rand = SP.random_subspace_part(x, sh[key], basis)
                arms.update(
                    {f"no_{key}": x - part, f"no_{key}_rand": x - rand, f"keep_{key}": part, f"keep_{key}_rand": rand}
                )
            assert set(arms) == {*ARMS, *REFIT_ARMS}
            q_u, q_u2 = R.orthonormal(alf), R.orthonormal(u2)
            near = ((h0[test] - h0[fit].mean(0)) @ u2).cpu().numpy()  # the held-out slot read-out of U' (descriptive)
            means = {s: ((h0[[i for i in fit if mine[i]["slot_org"] == s]] - h0[fit].mean(0)).mean(0) @ u2).cpu().numpy()
                     for s in sorted({mine[i]["slot_org"] for i in fit})}  # fmt: skip
            guess = [min(means, key=lambda s: float(np.linalg.norm(near[j] - means[s]))) for j in range(len(test))]
            refit_info[t] = {"n_fit": len(fit), "n_test": len(test), "rank": int(u2.shape[1]), "fit_scenes": [mine[i]["scene"] for i in fit],
                             "cos2_U_refit": R._cos2(q_u, q_u2), "held_out_slot_accuracy": float(np.mean([g == mine[i]["slot_org"] for g, i in zip(guess, test, strict=True)])),
                             "median_share_alf": float(sh["alf"].median()), "median_share_refit": float(sh["refit"].median())}  # fmt: skip
            test_set = set(test)
            for i, c in enumerate(progress(mine, f"{t}: reads at layer {layer} (case)")):
                norms.append({"scene": c["scene"], "type": t, "half": "test" if i in test_set else "fit", "norm": round(float(x[i].norm()), 4),
                              "share_alf": round(float(sh["alf"][i]), 5), "share_refit": round(float(sh["refit"][i]), 5),
                              "slot_org": c["slot_org"], "slot_alt": c["slot_alt"]})  # fmt: skip
                names = list(ARMS) + (list(REFIT_ARMS) if i in test_set else [])
                for w, rd in c["readers"].items():
                    if w == X.RECALL and c["scene"] not in recall_on[t]:
                        continue
                    edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in names]
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
                    for a, lg in zip(("none", *names), logits, strict=True):
                        top = int(lg.argmax())
                        rows.append({"scene": c["scene"], "type": t, "entity": c["bridge"], "half": "test" if i in test_set else "fit",
                                     "reader": w, "arm": a, "top": top, "top_text": tok.decode([top]),
                                     "route": R.classify(top, c) if w == X.LOOKUP else None, **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    (out / "refit.json").write_text(json.dumps(refit_info, indent=2) + "\n")
    m["items"] = {t: len(chosen[t]) for t in types}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(rows)} reads (sealed: no verdict)", flush=True)
    return out


# ---- verdict and view (CPU, sealed) ---------------------------------------------------------------------------------


def unsealed() -> str:
    answer = A.dan_answer(QUESTION)
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def _ci(pt: float, boot) -> list[float]:
    return [pt, *X.interval(boot)]


def type_numbers(rows: list[dict], kind: str, n_boot: int = X.N_BOOT) -> dict | None:
    """One type's lookup numbers: per arm the route shares (cluster bootstrap over the O bridge item, paired across
    arms), the position fall beyond random (no_alf_rand - no_alf) and only-U's position share; the same for the refit
    on the test half; the recall's S-answer share per arm beside. None without lookup rows."""
    lk = [r for r in rows if r["type"] == kind and r["reader"] == X.LOOKUP]
    if not lk:
        return None

    def block(mine: list[dict], part: str) -> dict:
        no, rand, keep, keep_rand = f"no_{part}", f"no_{part}_rand", f"keep_{part}", f"keep_{part}_rand"
        arms = ("whole", no, rand, keep, keep_rand)
        by = {a: {r["scene"]: r for r in mine if r["arm"] == a} for a in arms}
        scenes_ = sorted(set.intersection(*(set(v) for v in by.values())))
        if not scenes_:
            return {"n": 0}
        ents = [by["whole"][s]["entity"] for s in scenes_]
        sw = {f"{rt}|{a}": [int(by[a][s]["route"] == rt) for s in scenes_] for a in arms for rt in R.ROUTES}
        rr = X.resampled_rates(sw, ents, n_boot)
        pt = {k: float(np.mean(v)) for k, v in sw.items()}
        shares = {a: {rt: _ci(pt[f"{rt}|{a}"], rr[f"{rt}|{a}"]) for rt in R.ROUTES} for a in arms}

        def fall(rt: str) -> list[float]:  # the route's share without the random part minus without the part (paired)
            return _ci(pt[f"{rt}|{rand}"] - pt[f"{rt}|{no}"], rr[f"{rt}|{rand}"] - rr[f"{rt}|{no}"])

        return {"n": len(scenes_), "entities": len(set(ents)), "shares": shares, "position_fall": fall("position"),
                "identity_fall": fall("identity"), "keep_position": shares[keep]["position"],
                "keep_rand_position": shares[keep_rand]["position"]}  # fmt: skip

    fixed = block(lk, "alf")
    refit = block([r for r in lk if r["half"] == "test"], "refit")
    rc = [r for r in rows if r["type"] == kind and r["reader"] == X.RECALL]
    recall = None
    if rc:
        by = {a: {r["scene"]: int(r["switched"]) for r in rc if r["arm"] == a} for a in ("whole", *ARMS[1:])}
        scenes_ = sorted(set.intersection(*(set(v) for v in by.values())))
        ent = {r["scene"]: r["entity"] for r in rc}
        sw = {a: [by[a][s] for s in scenes_] for a in by}
        rr = X.resampled_rates(sw, [ent[s] for s in scenes_], n_boot)
        recall = {"n": len(scenes_), "S_answer": {a: _ci(float(np.mean(v)), rr[a]) for a, v in sw.items()}}
    return {"fixed": fixed, "refit": refit, "recall": recall}


def type_label(num: dict | None, animals: dict | None, tested: bool) -> dict:
    """The rule on one new type (point estimates, EPS at the bars): not tested (its lookup gate, or the animal
    reference's, failed); else holds if fall >= FALL, |fall - fall_animals| <= NEAR and only-U position >= KEEP; when it
    fails, the refit's reading on the test half ("slot x type" if fall' >= FALL and keep' >= KEEP)."""
    if not tested or num is None or not num["fixed"]["n"] or animals is None or not animals["fixed"]["n"]:
        return {"status": "not tested", "holds": False, "label": "not tested"}
    f, fa = num["fixed"], animals["fixed"]
    fall, keep = f["position_fall"][0], f["keep_position"][0]
    clauses = {
        "fall": fall >= FALL - EPS,
        "near_animals": abs(fall - fa["position_fall"][0]) <= NEAR + EPS,
        "keep": keep >= KEEP - EPS,
    }
    holds = all(clauses.values())
    out = {"status": "tested", "holds": holds, "clauses": clauses, "fall": f["position_fall"], "keep": f["keep_position"],
           "fall_animals": fa["position_fall"], "label": "an address (U transfers)" if holds else "U does not transfer"}  # fmt: skip
    r = num["refit"]
    if r["n"]:
        rf, rk = r["position_fall"][0], r["keep_position"][0]
        out["refit"] = {"n": r["n"], "fall": r["position_fall"], "keep": r["keep_position"],
                        "passes": rf >= FALL - EPS and rk >= KEEP - EPS}  # fmt: skip
        if not holds:
            out["label"] = (
                "slot x type (the refit passes)" if out["refit"]["passes"] else "neither U nor the refit (U' fails too)"
            )
    return out


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), or per type the numbers and the rule."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.11 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {
            "run": run,
            "target": target,
            "status": "pending",
            "answer": "pending",
            "why": "the run has no manifest or outcomes here",
        }
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    gate = json.loads((src / "gate.json").read_text())["gate"]
    refit = json.loads((src / "refit.json").read_text()) if (src / "refit.json").exists() else {}
    nums = {t: type_numbers(rows, t, n_boot) for t in m["types"]}
    tested = {t: bool(gate.get(t, {}).get("readers", {}).get("lookup", {}).get("pass")) for t in m["types"]}
    animals = nums.get(REFERENCE) if tested.get(REFERENCE) else None
    labels = {t: type_label(nums[t], animals, tested[t]) for t in NEW_TYPES if t in nums}
    if not tested.get(REFERENCE) or any(lab["status"] == "not tested" for lab in labels.values()):
        answer = "not tested"
    else:
        answer = "yes" if all(lab["holds"] for lab in labels.values()) else "no"
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "status": "tested", "answer": answer,
            "numbers": nums, "labels": labels, "gate": gate, "refit": refit, "tested": tested,
            "stored_animals": stored_animals(m["model"]["target"], n_boot)}  # fmt: skip


def stored_animals(target: str, n_boot: int = X.N_BOOT) -> dict | None:
    """The stored animal routes run's C2 position fall beyond random and only-U share (descriptive, beside the same
    job's animal type); None where the run is not here."""
    run = STORED_ANIMALS.get(target)
    src = pins.RESULTS_DIR / R.EXP / run if run else None
    if src is None or not (src / "outcomes.jsonl").exists():
        return None
    rows = [
        {**r, "type": REFERENCE, "half": "test"} for r in X.read_jsonl(src / "outcomes.jsonl") if r["condition"] == "C2"
    ]
    num = type_numbers(rows, REFERENCE, n_boot)
    f = num["fixed"] if num else {}
    return {
        "run": run,
        "n": f.get("n"),
        "position_fall": f.get("position_fall"),
        "keep_position": f.get("keep_position"),
    }


def fmt(v) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    lines = ["# 47.11: is the pointer item-agnostic?", "",
             f"Batch 47, test 47.11 (jobs/c3/batch47.yaml, amendment 4; {QUESTION}, Dan: {answer}). Routes scenes (C2, another "
             "item moved) with animals (the reference), fruits and names as the items, matched digits / people / slots; U "
             "fit on animal scenes, not refit; the change at the bridge word at L; cluster bootstrap over the O bridge item "
             f"({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             "| model | type | n | position fall beyond random (no_alf_rand − no_alf) | fall, animals (same job) | only-U position | only-random position | label |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | | pending ({m['why']}) | | | | | |")
            continue
        for t, num in m["numbers"].items():
            if num is None or not num["fixed"]["n"]:
                lines.append(f"| {m['target']} | {t} | 0 | not tested (gate) | | | | not tested |")
                continue
            f = num["fixed"]
            lab = m["labels"].get(t, {}).get("label", "reference")
            fa = m["numbers"].get(REFERENCE)
            lines.append(f"| {m['target']} | {t} | {f['n']} | {fmt(f['position_fall'])} | "
                         f"{fmt(fa['fixed']['position_fall']) if fa and fa['fixed']['n'] else '-'} | {fmt(f['keep_position'])} | "
                         f"{fmt(f['keep_rand_position'])} | **{lab}** |")  # fmt: skip
    lines += ["", "**Q47.11 per model:** " + "; ".join(f"{m['target']}: **{m['answer']}**" for m in models) + ".", "",
              "The refit U' (per type, on the fit half; read on the test half only; the fallback, reported always):", "",
              "| model | type | test n | fall' beyond random | only-U' position | passes the bars | cos² U·U' | held-out slot read-out of U' |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for t, num in m["numbers"].items():
            if num is None or not num["refit"]["n"]:
                continue
            r, info = num["refit"], m["refit"].get(t, {})
            passes = r["position_fall"][0] >= FALL - EPS and r["keep_position"][0] >= KEEP - EPS
            c2 = info.get("cos2_U_refit")
            lines.append(f"| {m['target']} | {t} | {r['n']} | {fmt(r['position_fall'])} | {fmt(r['keep_position'])} | {yn(passes)} | "
                         f"{'-' if c2 is None else f'{c2:.3f}'} | {info.get('held_out_slot_accuracy', '-')} |")  # fmt: skip
    lines += ["", "Lookup route shares per arm (identity / position / value / original / other), and the recall's S-answer share "
              "where it was read:", "", "| model | type | arm | n | " + " | ".join(R.ROUTES) + " | recall S (n) |",
              "|---|---|---|---|" + "---|" * (len(R.ROUTES) + 1)]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for t, num in m["numbers"].items():
            if num is None:
                continue
            for blk in ("fixed", "refit"):
                b = num[blk]
                if not b["n"]:
                    continue
                for a, s in b["shares"].items():
                    if blk == "refit" and a == "whole":
                        continue
                    rc = num["recall"]
                    rs = fmt(rc["S_answer"][a]) + f" ({rc['n']})" if rc and a in rc["S_answer"] else "-"
                    lines.append(
                        f"| {m['target']} | {t} | {a} | {b['n']} | "
                        + " | ".join(fmt(s[rt]) for rt in R.ROUTES)
                        + f" | {rs} |"
                    )
    lines += [
        "",
        "Gates (O's read accuracy per reader and type; the lookup's decides the items, the recall's whether it is read):",
        "",
    ]
    for m in models:
        if m["status"] == "pending":
            continue
        for t, g in m["gate"].items():
            lines.append(f"- {m['target']}, {t}: " + "; ".join(f"{w} {v['org_read_accuracy']:.3f} (said {v['org_said_accuracy']:.3f}, pass {yn(v['pass'])}, eligible {v['eligible']})"
                                                              for w, v in g["readers"].items()) + f"; chosen {g['chosen']}, recall read on {g['recall_read_on']}")  # fmt: skip
        sa = m["stored_animals"]
        if sa:
            lines.append(f"- {m['target']}, the stored animal routes run {sa['run']} (descriptive, beside the same job's animals): "
                         f"position fall {fmt(sa['position_fall'])}, only-U position {fmt(sa['keep_position'])} (n = {sa['n']})")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "answer": "pending", "why": "no run given"}
               for t in RUNS if t not in targets]  # fmt: skip
    out = RESULTS / f"x47_11-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    (out / "x47_11.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "x47_11.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(run: str, decode, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """Per type, k random items of the run (seed 0): each reader's O prompt as the model reads it (the read suffix
    appended) with the bridge word in ⟦...⟧, S's prompt, and every arm's answer (top token, route, switched)."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    lines = [f"## {run} ({m['model']['target']}, L{m['layer']})", ""]
    for t in m["types"]:
        items = list(dict.fromkeys(r["scene"] for r in rows if r["type"] == t))
        lines += [f"### {t}: {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
        for i in sorted(random.Random(seed).sample(range(len(items)), min(k, len(items)))):
            c = cases[items[i]]
            lines += [f"#### {c['scene']}: bridge {c['bridge']} → {c['cf_bridge']}, token {c['pos']}; expected digits {c['expect']}; "
                      f"O bridge's slot {c['slot_org']}, S bridge's O-slot {c['slot_alt']}", ""]  # fmt: skip
            for w, rd in c["readers"].items():
                mine = [r for r in rows if r["scene"] == c["scene"] and r["reader"] == w]
                if not mine:
                    lines += [f"**{READER_NAME[w]}**: not read (its gate, or the item not right unedited)", ""]
                    continue
                lines += [f"**{READER_NAME[w]}** ({rd['kind']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "", "O, as read:", "",
                          "```", R.marked(decode, rd["ids"]["org"] + rd["suffix"], c["pos"]), "```", "", "S (the source):", "",
                          "```", R.marked(decode, rd["ids"]["alt"] + rd["suffix"], c["pos"]), "```", "",
                          "| arm | what | answer (top token) | route | switched |", "|---|---|---|---|---|"]  # fmt: skip
                lines += [f"| {r['arm']} | {ARM_TEXT.get(r['arm'], 'O unedited')} | {r['top_text']!r} | {r.get('route') or ''} | {r['switched']} |"
                          for r in mine]  # fmt: skip
                lines.append("")
    return lines


def stage_view(runs: list[str], decode_for=None) -> Path:
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.11 verify-pack view: prompts exactly as the model reads them (a digit reader's read appends the space "
             "token; a word reader's appends nothing); ⟦...⟧ the bridge word, where the change (or the arm's part of it) is "
             "added at L. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        if (RESULTS / run / "outcomes.jsonl").exists():
            target = json.loads((RESULTS / run / "manifest.json").read_text())["model"]["target"]
            lines += view_lines(run, (decode_for or A.default_decode)(target))
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out / "view.md")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x47_agnostic/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.11 (jobs/c3/batch47.yaml amendment 4; Q47.11, sealed)")
    ap.add_argument("--types", nargs="+", default=list(TYPES), choices=list(TYPES))
    ap.add_argument(
        "--targets", nargs="+", default=list(RUNS), help="plan: the targets whose tokenizers check the pools"
    )
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the 47.11 runs")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.targets)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, tuple(a.types))
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    else:
        stage_view(a.runs)


if __name__ == "__main__":
    main()
