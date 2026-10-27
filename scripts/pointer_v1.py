"""pointer_v1: scenes for a three-way dissociation patch (Dan's D3, 2026-10-20). What do the question tokens carry, in
transit, when a recalled bridge is used for an in-prompt lookup: the bridge's identity, a pointer to the statement that
binds it (its position), or the looked-up answer itself?

Background (UNVERIFIED, EXPERIMENTS.md rows 27, 32, 37, 52): on Qwen3.6-27B, copying C's question-token residual at
layers 44-52 flips RL (recalled cue -> in-prompt lookup) 98-100% of the time while the J-lens direction v_X - v_I flips
it 0%, although the lens reads the bridge there. Hypotheses for what the copy carries: H-pointer (an order/position
index of the matching statement, or a lexical key, as in binding-ID / lookback / "Mixing Mechanisms" work), H-word (the
bridge's identity in a subspace the lens cannot write), H-value (the answer digit, already fetched).

A scene: N entities of one domain (N = 3 or 5), each bound to a digit by one statement ("The cow's locker is 5.",
"The Mars card is in locker 5."), statements in a seeded order, optional filler sentences (dev only, same layout in
every prompt of the scene). Families on the same scenes (only the question differs, suite_v1 style):
  RL  recalled cue -> lookup:   "Which locker belongs to the animal known for mooing?"
  DL  entity named -> lookup:   "Which locker belongs to the cow?" (classic binding retrieval; the reference)
  RR  recalled cue -> recall:   "How many legs does the animal known for mooing have?" (a pointer is useless here)
  (BL, person -> entity -> lookup, is not built in v1: it needs ownership statements in every context.)

Sources (each a full prompt token-aligned with the base: same length, statements at the same token positions, cue
phrases of equal token length, so the question and the template sit at the same positions). In the base the queried
entity q_b sits at slot a; the source "dissoc" queries another entity q_s, which the base binds at slot c, and puts q_s
at slot k of its own statements, where the base has a third entity p. Patching the source's residual into the base
(question tokens and/or the template after them) predicts four distinct answers, all recorded in the item:
  none      d_b(q_b)    the base answer (the patch carries nothing the lookup uses)
  identity  d_b(q_s)    the base's digit for the source's entity (H-word, or a lexical key)
  position  d_b(p)      the base's digit at the source's queried slot k (H-pointer, positional)
  value     d_s(q_s)    the source's own answer, a digit absent from the base context (H-value)
For RR the predictions are recalled facts (rec(q_b), rec(q_s), rec(p)); value = identity there by construction.
Controls in the data: "same" (q_s = q_b at the same slot with the same digit; the other statements reshuffled and
redigited): every hypothesis predicts the base answer, so any change is damage from patching a residual computed on a
different context. "redigit" (the base context with q_b's digit replaced by the value digit, same question): only
H-value predicts a change. Run-time controls (scripts/pointer_swap.py): a matched-norm random direction and a random
other item's residual at matched norm.

Digits. Lookup digits are 1-9 (single tokens). Collision policy with the recalled digits: hard (every item): no digit
in the base context, and no value digit, equals the recalled digit of q_b, q_s or p, so for RL/DL a "recall" answer
and for RR a "lookup" answer stay distinguishable from the predictions; soft (where the pool allows): the scene's
lookup digits also avoid every scene entity's recalled digit (needs 9 - |recalled digits| >= N + 1 free digits; true
at N = 3, usually false at N = 5 in the one-to-one domains). Items record which policy applied and the remaining
collisions. Slots are balanced: (a, k) cycles through all ordered pairs of distinct slots in seeded blocks.

Sets (each (set, level, domain) has its own seed, so adding one never changes another's items):
  main  N = 5, no filler, 400 scenes per domain (every family on each scene), seed 701
  dev   pilot, never a headline: N = 3 and 5 without filler, N = 5 with 4 filler sentences; 60 scenes per cell, seed 702
  fit   RL only, N = 5, 200 scenes per domain, seed 703: pointer_swap's `fit` stage fits a slot direction here
Files: data/pointer_v1/<set>/<domain>_<family>_<level>.json, one item per line.

Stages:  make --set S (write-once; tokenizer only)   verify (regenerates every set, must equal its files)
         check --set S (tokenizer only: alignment, predictions, permutations, collisions, balance)
         manifest --set S [S ...] --name N --why W [--limit K]
         competence --name N (GPU: every item's base, each source and each step alone, unedited; greedy and the
         answer read, as suite_v1's competence)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import check_switches, switches
from scripts import suite_v1 as S

DATA = pins.DATA_DIR / "pointer_v1"
RESULTS = pins.RESULTS_DIR / "pointer_v1"
FAMILIES = ("RL", "DL", "RR")
SOURCES = ("dissoc", "same", "redigit")
HYPOTHESES = ("none", "identity", "position", "value")
DIGITS = tuple(range(1, 10))
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 701, "n": 400, "levels": {"e5f0": (5, 0)}, "families": FAMILIES},
    "dev": {"seed": 702, "n": 60, "levels": {"e3f0": (3, 0), "e5f0": (5, 0), "e5f4": (5, 4)}, "families": FAMILIES},
    "fit": {"seed": 703, "n": 200, "levels": {"e5f0": (5, 0)}, "families": ("RL",)},
}

# ---- domains --------------------------------------------------------------------------------------------------------
# Every entity is one token after a space in Qwen3.6-27B's tokenizer (checked by make/check), every cue in a domain has
# the same token count (so any two items of a domain line up), no cue contains a pool entity, a digit or a number word,
# and each cue names one entity of its pool. The recalled digit is a fact the model must bring from memory.
ANIMALS = {a: (legs, cue) for a, (legs, cue) in S.ANIMALS.items()}  # suite_v1's 16 animals and 2-token cues, legs
PLANETS = {  # order from the sun. Uranus is 2 tokens; Neptune's 3-token cues ("the last planet") give its order away
    "Mercury": (1, "the smallest planet"),
    "Venus": (2, "the hottest planet"),
    "Earth": (3, "our home planet"),
    "Mars": (4, "the red planet"),
    "Jupiter": (5, "the largest planet"),
    "Saturn": (6, "the ring planet"),
}
ELEMENTS = {  # atomic number. Beryllium, boron, fluorine are 2+ tokens; neon is 10 (two digits)
    "hydrogen": (1, "the lightest element"),
    "helium": (2, "the party balloon gas"),
    "lithium": (3, "the phone battery metal"),
    "carbon": (6, "the element in diamonds"),
    "nitrogen": (7, "the main atmospheric gas"),
    "oxygen": (8, "the gas fires need"),
}
MONTHS = {  # number in the calendar; cues "the month of <X> Day" with X one token. March dropped: its 2-token holiday is
    # Pi Day (3/14), which gives the 3 away; August: no well-known 2-token holiday; October-December are two digits
    "January": (1, "the month of Australia Day"),
    "February": (2, "the month of Leap Day"),
    "April": (4, "the month of Earth Day"),
    "May": (5, "the month of Memorial Day"),
    "June": (6, "the month of D-Day"),
    "July": (7, "the month of Independence Day"),
    "September": (9, "the month of Labor Day"),
}
# Templates. Animals keep suite_v1's wording A (the locker table, "the animal known for <cue>"), so RL here is the
# suite's RL without the ownership sentences; the other domains share a card-in-locker table.
CARD = {
    "statement": "The {e} card is in locker {d}.",
    "DL": "Which locker holds the {e} card?",
    "RL": "Which locker holds the card for {cue}?",
}
DOMAINS: dict[str, dict[str, Any]] = {
    "animals": {
        "entities": ANIMALS,
        "statement": "The {e}'s locker is {d}.",
        "DL": "Which locker belongs to the {e}?",
        "RL": "Which locker belongs to the animal known for {cue}?",
        "RR": "How many legs does the animal known for {cue} have?",
        "hop_cue": "Which animal is known for {cue}?",
        "hop_recall": "How many legs does a {e} have?",
        "fact": "legs",
    },
    "planets": {
        "entities": PLANETS,
        **CARD,
        "RR": "What number is {cue} in order from the sun?",
        "hop_cue": "Which planet is {cue}?",
        "hop_recall": "What number is {e} in order from the sun?",
        "fact": "order from the sun",
    },
    "elements": {
        "entities": ELEMENTS,
        **CARD,
        "RR": "What is the atomic number of {cue}?",
        "hop_cue": "Which element is {cue}?",
        "hop_recall": "What is the atomic number of {e}?",
        "fact": "atomic number",
    },
    "months": {
        "entities": MONTHS,
        **CARD,
        "RR": "What number is {cue} in the calendar?",
        "hop_cue": "Which month is {cue}?",
        "hop_recall": "What number is {e} in the calendar?",
        "fact": "number in the calendar",
    },
}
NUMBER_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
ORDINALS = ("zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth")


def rec(domain: str, e: str) -> int:
    return DOMAINS[domain]["entities"][e][0]


def cue(domain: str, e: str) -> str:
    return DOMAINS[domain]["entities"][e][1]


# ---- scenes ---------------------------------------------------------------------------------------------------------


def slot_plan(rng: random.Random, n: int, n_ent: int) -> list[tuple[int, int]]:
    """(a, k) per scene: the base query's slot and the source's query slot (the position prediction's slot), cycling
    through every ordered pair of distinct slots in seeded blocks, so both are balanced across slots."""
    pairs = [(a, k) for a in range(n_ent) for k in range(n_ent) if a != k]
    out: list[tuple[int, int]] = []
    while len(out) < n:
        block = list(pairs)
        rng.shuffle(block)
        out += block
    return out[:n]


def pick_entities(rng: random.Random, domain: str, n_ent: int) -> tuple[str, str, str, list[str]]:
    """q_b, q_s (recalled digits differ, so RR's none and identity differ), p (a recalled digit unlike both when the
    pool has one, so RR's position prediction is distinct too), and n_ent - 3 more."""
    pool = list(DOMAINS[domain]["entities"])
    while True:
        q_b, q_s = rng.sample(pool, 2)
        if rec(domain, q_b) != rec(domain, q_s):
            break
    rest = [e for e in pool if e not in (q_b, q_s)]
    distinct = [e for e in rest if rec(domain, e) not in (rec(domain, q_b), rec(domain, q_s))]
    p = rng.choice(distinct or rest)
    more = rng.sample([e for e in rest if e != p], n_ent - 3)
    return q_b, q_s, p, more


def digit_pool(domain: str, scene: list[str], critical: list[str], n_ent: int) -> tuple[list[int], str]:
    """The lookup digits a scene may use (see the docstring's collision policy) and which policy applied."""
    soft = [d for d in DIGITS if d not in {rec(domain, e) for e in scene}]
    if len(soft) >= n_ent + 1:
        return soft, "soft"
    hard = [d for d in DIGITS if d not in {rec(domain, e) for e in critical}]
    assert len(hard) >= n_ent + 1, f"{domain}: not enough lookup digits"
    return hard, "hard"


def context(domain: str, order: list[str], digits: list[int], lay: list[int | str]) -> str:
    facts = [DOMAINS[domain]["statement"].format(e=e, d=d) for e, d in zip(order, digits, strict=True)]
    return " ".join(S.weave(facts, lay))


def make_scene(rng: random.Random, domain: str, n_ent: int, n_fill: int, a: int, k: int) -> dict[str, Any]:
    """One scene: the base (order, digits), the dissoc / same / redigit sources, and the shared filler layout."""
    q_b, q_s, p, more = pick_entities(rng, domain, n_ent)
    c = rng.choice([s for s in range(n_ent) if s not in (a, k)])
    order: list[str] = [""] * n_ent
    order[a], order[k], order[c] = q_b, p, q_s
    free = [s for s in range(n_ent) if not order[s]]
    for s, e in zip(free, rng.sample(more, len(more)), strict=True):
        order[s] = e
    pool, policy = digit_pool(domain, order, [q_b, q_s, p], n_ent)
    digits = rng.sample(pool, n_ent)
    value = rng.choice([d for d in pool if d not in digits])
    # dissoc: q_s at slot k, the others in a seeded order; q_s's digit is the value, the others from the rest of the pool
    others = rng.sample([e for e in order if e != q_s], n_ent - 1)
    s_order = list(others)
    s_order.insert(k, q_s)
    s_digits = rng.sample([d for d in pool if d != value], n_ent - 1)
    s_digits.insert(k, value)
    # same: q_b at slot a with its digit; the others reshuffled (a different order) and redigited
    while True:
        rest = rng.sample([e for e in order if e != q_b], n_ent - 1)
        m_order = list(rest)
        m_order.insert(a, q_b)
        m_digits = rng.sample([d for d in pool if d != digits[a]], n_ent - 1)
        m_digits.insert(a, digits[a])
        if m_order != order:
            break
    r_digits = list(digits)
    r_digits[a] = value
    lay = S.layout(rng, n_ent, n_fill, S.FILLER)
    return {
        "q_b": q_b, "q_s": q_s, "p": p, "slots": {"query": a, "identity": c, "position": k},
        "order": order, "digits": digits, "value": value, "policy": policy, "layout": lay,
        "dissoc": (s_order, s_digits), "same": (m_order, m_digits), "redigit": (list(order), r_digits),
    }  # fmt: skip


def family_items(sc: dict[str, Any], domain: str, scene_id: str, level: str, n_fill: int) -> dict[str, dict]:
    """The three families' items on one scene: questions, answers, sources and their predictions, the steps alone."""
    d = DOMAINS[domain]
    q_b, q_s, p = sc["q_b"], sc["q_s"], sc["p"]
    order, digits, lay = sc["order"], sc["digits"], sc["layout"]
    look = dict(zip(order, digits, strict=True))
    base_ctx = context(domain, order, digits, lay)
    recalled = {e: rec(domain, e) for e in order}
    collisions = sorted({x for x in digits if x in recalled.values()})
    out = {}
    for fam in FAMILIES:
        if fam == "DL":
            question, src_question = d["DL"].format(e=q_b), d["DL"].format(e=q_s)
        else:
            question, src_question = d[fam].format(cue=cue(domain, q_b)), d[fam].format(cue=cue(domain, q_s))
        lookup = fam != "RR"
        answer = look[q_b] if lookup else rec(domain, q_b)
        sources = {}
        for src in SOURCES:
            s_order, s_digits = sc[src]
            s_look = dict(zip(s_order, s_digits, strict=True))
            if src == "dissoc":
                pred = (
                    {"none": look[q_b], "identity": look[q_s], "position": look[p], "value": s_look[q_s]}
                    if lookup
                    else {"none": rec(domain, q_b), "identity": rec(domain, q_s), "position": rec(domain, p),
                          "value": rec(domain, q_s)}
                )  # fmt: skip
                s_q, s_query = src_question, q_s
                s_answer = s_look[q_s] if lookup else rec(domain, q_s)
            else:
                s_q, s_query = question, q_b
                s_answer = s_look[q_b] if lookup else rec(domain, q_b)
                pred = {h: answer for h in HYPOTHESES}
                if src == "redigit" and lookup:
                    pred["value"] = s_look[q_b]
            sources[src] = {
                "context": context(domain, s_order, s_digits, lay), "question": s_q, "answer": str(s_answer),
                "entities": s_order, "digits": s_digits, "query": s_query, "query_slot": s_order.index(s_query),
                "predictions": {h: str(v) for h, v in pred.items()},
            }  # fmt: skip
        pd = sources["dissoc"]["predictions"]
        keys = HYPOTHESES if lookup else ("none", "identity", "position")
        item = {
            "id": f"{domain}-{fam}-{scene_id}", "family": fam, "domain": domain, "level": level,
            "scene": f"{domain}-{scene_id}", "n_entities": len(order), "n_filler": n_fill,
            "entities": order, "digits": digits, "recalled": recalled, "query": q_b,
            "cue": q_b if fam == "DL" else cue(domain, q_b), "slots": sc["slots"],
            "context": base_ctx, "question": question, "answer": str(answer), "answer_kind": "digit",
            "sources": sources, "distinct": len({pd[h] for h in keys}) == len(keys),
            "digit_policy": sc["policy"], "collisions": collisions,
        }  # fmt: skip
        if fam != "DL":
            item["hop1"] = {"question": d["hop_cue"].format(cue=cue(domain, q_b)), "answer": q_b, "kind": domain}
            hop2 = d["DL"].format(e=q_b) if lookup else d["hop_recall"].format(e=q_b)
            item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
        out[fam] = item
    return out


def generate_cell(seed: int, domain: str, level: str, n_ent: int, n_fill: int, n: int) -> dict[str, list[dict]]:
    """n scenes of one domain at one level, every family on each; contexts never repeat within the cell."""
    rng = random.Random(seed)
    plan = slot_plan(rng, n, n_ent)
    out: dict[str, list[dict]] = {f: [] for f in FAMILIES}
    seen: set[str] = set()
    i = 0
    while i < n:
        a, k = plan[i]
        sc = make_scene(rng, domain, n_ent, n_fill, a, k)
        key = context(domain, sc["order"], sc["digits"], sc["layout"])
        if key in seen:
            continue
        seen.add(key)
        for fam, item in family_items(sc, domain, f"{level}-{i:04d}", level, n_fill).items():
            out[fam].append(item)
        i += 1
    return out


def cell_seed(which: str, level: str, domain: str) -> int:
    spec = SETS[which]
    return spec["seed"] * 1000 + 10 * list(spec["levels"]).index(level) + list(DOMAINS).index(domain)


def generate(which: str, n: int | None = None) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note) for a set; tokenizer-free (make/check assert the token properties)."""
    spec = SETS[which]
    out = {}
    for level, (n_ent, n_fill) in spec["levels"].items():
        for domain in DOMAINS:
            seed = cell_seed(which, level, domain)
            fams = generate_cell(seed, domain, level, n_ent, n_fill, n or spec["n"])
            note = (
                f"scripts/pointer_v1.py make --set {which} (seed {seed}: {domain}, {n_ent} entities, {n_fill} filler)"
            )
            for fam in spec["families"]:
                items = fams[fam]
                label = f"{domain}_{fam}_{level}"
                out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    spec = SETS[which]
    return {
        f"{d}_{f}_{lv}": DATA / which / f"{d}_{f}_{lv}.json"
        for lv in spec["levels"]
        for d in DOMAINS
        for f in spec["families"]
    }


# ---- tokenizer checks -----------------------------------------------------------------------------------------------


def tokenizer():
    """The target's tokenizer from the local cache (a tokenizer-only snapshot is enough: the Mac has no weights)."""
    try:
        from bridge_jspace.tokens import load_tokenizer

        return load_tokenizer()
    except Exception:  # an incomplete snapshot (tokenizer files only): load just those
        from huggingface_hub import snapshot_download
        from transformers import AutoTokenizer

        files = ["tokenizer*", "vocab.json", "merges.txt", "chat_template.jinja", "config.json"]
        path = snapshot_download(
            pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True, allow_patterns=files
        )
        return AutoTokenizer.from_pretrained(path)


def check_pools(tok) -> dict[str, Any]:
    """Every entity one token after a space; one cue length per domain; cues name no pool entity, digit or number."""
    report = {}
    words = set(NUMBER_WORDS) | set(ORDINALS)
    for domain, d in DOMAINS.items():
        ents = d["entities"]
        bad = [e for e in ents if len(S.ids(tok, " " + e)) != 1]
        assert not bad, f"{domain}: not one token: {bad}"
        lengths = {e: len(S.ids(tok, " " + c)) for e, (_, c) in ents.items()}
        assert len(set(lengths.values())) == 1, f"{domain}: cue lengths differ: {lengths}"
        for _, c in ents.values():
            toks = set(re.findall(r"[a-z]+|\d", c.lower()))
            assert not toks & {x.lower() for x in ents}, f"{domain}: cue {c!r} names a pool entity"
            assert not toks & words, f"{domain}: cue {c!r} has a number word"
            assert not re.search(r"\d", c), f"{domain}: cue {c!r} has a digit"
        assert len({c for _, c in ents.values()}) == len(ents), f"{domain}: two entities share a cue"
        report[domain] = {"entities": len(ents), "cue_tokens": next(iter(lengths.values())),
                          "recalled": sorted({r for r, _ in ents.values()})}  # fmt: skip
    return report


def statement_spans(text: str, item_context: str, statements: list[str]) -> list[tuple[int, int]]:
    """Char spans of the context's statements and filler, in order, inside a rendered prompt."""
    start = text.index(item_context)
    spans, pos = [], start
    for s in statements:
        i = text.index(s, pos)
        spans.append((i, i + len(s)))
        pos = i + len(s)
    return spans


def token_index(offsets: list[tuple[int, int]], char: int) -> int:
    return next(i for i, (s, e) in enumerate(offsets) if s <= char < e)


def prompt_layout(tok, item: dict, ctx: str, question: str, order: list[str], digits: list[int]) -> dict[str, Any]:
    """ids, the first token of each statement, and the question's token span, of one rendered prompt."""
    from bridge_jspace.tokens import raw_encoding

    text = S.render(tok, ctx, question)
    enc = raw_encoding(tok, text, offsets=True)
    facts = [DOMAINS[item["domain"]]["statement"].format(e=e, d=d) for e, d in zip(order, digits, strict=True)]
    spans = statement_spans(text, ctx, facts)
    q0 = text.rindex("\n" + question) + 1
    offs = enc["offset_mapping"]
    return {
        "ids": list(enc["input_ids"]),
        "statement_starts": [token_index(offs, s) for s, _ in spans],
        "statement_ends": [token_index(offs, e - 1) for _, e in spans],
        "question": (token_index(offs, q0), token_index(offs, q0 + len(question) - 1)),
    }


def check_item(tok, item: dict) -> dict[str, Any]:
    """Token alignment of every source with the base, and the item's own bookkeeping (predictions, permutations,
    collision policy). Returns per-check booleans."""
    base = prompt_layout(tok, item, item["context"], item["question"], item["entities"], item["digits"])
    out: dict[str, Any] = {}
    for src, s in item["sources"].items():
        lay = prompt_layout(tok, item, s["context"], s["question"], s["entities"], s["digits"])
        same_len = len(lay["ids"]) == len(base["ids"])
        diff = S.changed(base["ids"], lay["ids"]) if same_len else None
        q0, q1 = base["question"]
        allowed = set()
        for st, en in zip(base["statement_starts"], base["statement_ends"], strict=True):
            allowed |= set(range(st, en + 1))
        allowed |= set(range(q0, q1 + 1))
        out[f"{src}_aligned"] = (
            same_len
            and lay["statement_starts"] == base["statement_starts"]
            and lay["statement_ends"] == base["statement_ends"]
            and lay["question"] == base["question"]
            and diff is not None
            and bool(diff)
            and set(diff) <= allowed  # only statements and the question's cue may differ; the template never
        )
    look = dict(zip(item["entities"], item["digits"], strict=True))
    sl = item["slots"]
    ents, dg = item["entities"], item["digits"]
    d = item["sources"]["dissoc"]
    lookup = item["family"] != "RR"
    pd = d["predictions"]
    q_s = d["query"]
    p = ents[sl["position"]]
    # permutations: the recorded slots hold what the predictions say
    perm = (
        ents[sl["query"]] == item["query"]
        and ents[sl["identity"]] == q_s
        and d["entities"][sl["position"]] == q_s
        and d["query_slot"] == sl["position"]
        and sorted(d["entities"]) == sorted(ents)
        and len(set(ents)) == len(ents)
    )
    if lookup:
        perm = perm and pd == {"none": str(look[item["query"]]), "identity": str(dg[sl["identity"]]),
                               "position": str(dg[sl["position"]]), "value": str(d["digits"][sl["position"]])}  # fmt: skip
        value_absent = int(pd["value"]) not in dg
        four_distinct = len(set(pd.values())) == 4
    else:
        perm = (
            perm
            and pd["none"] == str(item["recalled"][item["query"]])
            and pd["position"] == str(rec(item["domain"], p))
        )
        value_absent = True
        four_distinct = len({pd["none"], pd["identity"]}) == 2
    critical = {rec(item["domain"], e) for e in (item["query"], q_s, p)}
    hard_ok = not (set(dg) & critical) and int(d["digits"][sl["position"]]) not in critical
    soft_ok = not (set(dg) & set(item["recalled"].values()))
    same = item["sources"]["same"]
    redigit = item["sources"]["redigit"]
    out |= {
        "permutation": perm,
        "value_absent": value_absent,
        "predictions_distinct": four_distinct,
        "hard_collision_free": hard_ok,
        "soft_collision_free": soft_ok,
        "soft_promised": item["digit_policy"] == "soft",
        "same_noop": same["entities"][sl["query"]] == item["query"]
        and same["digits"][sl["query"]] == look[item["query"]]
        and same["context"] != item["context"]
        and len(set(same["predictions"].values())) == 1,
        "redigit_one_change": [x != y for x, y in zip(redigit["digits"], dg, strict=True)].count(True) == 1
        and redigit["entities"] == ents,
    }
    return out


def stage_make(which: str) -> None:
    tok = tokenizer()
    print(json.dumps(check_pools(tok)))
    for _label, (path, items, note) in generate(which).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"],
                "generator": note, "format": (__doc__ or "").split("\n\n")[2]}  # fmt: skip
        body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)  # one item per line: grep-able, compact
        path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    """Every set regenerated from this code equals its files."""
    for which in SETS:
        for label, (path, items, _) in generate(which).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = json.loads(path.read_text())["items"] == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def load_file(path: Path) -> list[dict]:
    return json.loads(path.read_text())["items"]


def stage_check(which: str) -> None:
    tok = tokenizer()
    report: dict[str, Any] = {"pools": check_pools(tok), "files": {}}
    for label, path in set_files(which).items():
        items = load_file(path)
        stats: collections.Counter = collections.Counter()
        slots = {k: collections.Counter() for k in ("query", "identity", "position")}
        answers, values, queries = collections.Counter(), collections.Counter(), collections.Counter()
        prompts, lengths = set(), []
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
            for k in slots:
                slots[k][it["slots"][k]] += 1
            answers[it["answer"]] += 1
            values[it["sources"]["dissoc"]["predictions"]["value"]] += 1
            queries[it["query"]] += 1
            prompts.add(S.render(tok, it["context"], it["question"]))
            lengths.append(len(S.ids(tok, S.render(tok, it["context"], it["question"]))))
        n = len(items)
        r = {"n": n, **stats, "unique_prompts": len(prompts), "prompt_tokens(min,median,max)": (min(lengths), statistics.median(lengths), max(lengths)),
             "slots": {k: dict(sorted(v.items())) for k, v in slots.items()}, "answers": dict(sorted(answers.items())),
             "values": dict(sorted(values.items())), "queries": dict(queries.most_common())}  # fmt: skip
        print(label, json.dumps(r))
        must = ("dissoc_aligned", "same_aligned", "redigit_aligned", "permutation", "value_absent", "hard_collision_free",
                "same_noop", "redigit_one_change")  # fmt: skip
        for k in must:
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert stats["predictions_distinct"] == n, f"{label}: predictions not distinct"
        assert stats["soft_collision_free"] >= stats["soft_promised"], f"{label}: soft policy broken"
        assert len(prompts) == n, f"{label}: repeated prompts"
        report["files"][label] = r
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


# ---- competence -----------------------------------------------------------------------------------------------------


def said(text: str, kind: str) -> str | None:
    """The first answer of the kind in the first non-empty line: a digit (digits, number words, ordinals) or an entity of
    the domain named by `kind`."""
    line = S.first_line(text)
    if kind == "digit":
        for t in re.findall(r"[a-z]+|\d+", line):
            if t.isdigit():
                return t
            if t in NUMBER_WORDS:
                return str(NUMBER_WORDS.index(t))
            if t in ORDINALS:
                return str(ORDINALS.index(t))
        return None
    lower = {w.lower(): w for w in DOMAINS[kind]["entities"]}
    return next((lower[t] for t in re.findall(r"[a-z]+", line) if t in lower), None)


def stage_manifest(name: str, why: str, sets: list[str], limit: int | None) -> None:
    pins.check_run_name(name)
    from bridge_jspace.data import sha256_of

    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"{s}/{label}": f for s in sets for label, f in set_files(s).items()}
    manifest = {
        "exp": "pointer_v1", "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
        "model": pins.model_pin(), "switches": switches(), "sets": sets,
        "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
        "limit": limit,
        "format": f"suite_v1's: {chat.format_note()}; the context, a newline, the question and '{S.INSTRUCTION}' as the "
        "user turn",
        "prompts": "base; each source (dissoc, same, redigit) with its own context and question; hop1 (cue -> entity, "
        "with the base context) and hop2 (the lookup with the entity named, or the recalled fact) for RL and RR",
        "judge_mode": judge_mode(),
        "judge": judge_rule(),
        "answer_read": "suite_v1's: one forward with a digit answer's space token appended; p and margin of the answer's "
        "first token; whether the read's top token is the greedy answer",
        "eligibility": "pointer_swap uses items with every prompt right (base, the three sources, the steps alone)",
    }  # fmt: skip
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


PROMPT_KINDS = ("clean", *(f"src_{s}" for s in SOURCES), "hop1", "hop2")
JUDGE_GREEDY = ("the first answer of the item's kind in the first non-empty line of 8 greedy tokens (digits, number words "
                "and ordinals for digits; the domain's entities otherwise)")  # fmt: skip
# Amendment 2026-10-21 (before any raw-format patching result was opened): in raw format Qwen3.6-27B opens its greedy
# reply with a think block ("\n\n<think>..."), so the 8-token greedy judge never reaches the answer (d3v4_competence_raw_27b:
# 0% in every cell with the read's top token right). In raw format a prompt is therefore judged by the one-forward read
# the patching itself uses; greedy agreement is still recorded (correct_greedy) and reported, not used.
JUDGE_READ = ("raw format: a digit prompt is right iff the top token of one forward with the digit's space token appended "
              "(pointer_swap's read) is the expected digit; a word prompt (the cue -> entity step, never read by the "
              "patching) iff the greedy judge finds the entity in 4 greedy tokens after the model's own empty think block "
              "(RAW_WORD_PREFIX, the start of its greedy reply where it does not think); the plain greedy judge is "
              "recorded as correct_greedy, not used (amendment 2026-10-21)")  # fmt: skip
RAW_WORD_PREFIX = "\n\n<think>\n\n</think>\n\n"


JUDGE_READ_CHAT = ("read judge (BJ_JUDGE=read): a prompt is right iff the top token of one forward (a digit answer's "
                   "space token appended: pointer_swap's read) is the expected answer's first token; the greedy judge is "
                   "recorded as correct_greedy, not used")  # fmt: skip


def judge_mode(fmt: str | None = None) -> str:
    """'read' or 'greedy': BJ_JUDGE if set (a target whose greedy reply is not the read's answer, e.g. OLMo-3-7B-Instruct
    naming the bridge instead of the looked-up digit), else read in raw format (the 2026-10-21 amendment), greedy in
    chat."""
    mode = os.environ.get("BJ_JUDGE") or ("read" if (fmt or chat.FORMAT) == "raw" else "greedy")
    assert mode in ("read", "greedy"), f"BJ_JUDGE={mode!r}: read or greedy"
    return mode


def judge_rule(fmt: str | None = None) -> str:
    """The competence judge of a run in this prompt format and judge mode (manifests record it)."""
    if judge_mode(fmt) == "greedy":
        return JUDGE_GREEDY
    return JUDGE_READ if (fmt or chat.FORMAT) == "raw" else JUDGE_READ_CHAT


def read_right(tok, p: dict) -> bool:
    """The read's top token is the expected answer's first token (as S.read_answers reads it)."""
    first = tok.decode([S.answer_token(tok, p["expected"], p["answer_kind"])]).strip().lower()
    return bool(p.get("read_top")) and p["read_top"].lower() == first


def raw_word_reads(model, tok, prompts: list[dict]) -> None:
    """4 greedy tokens per word prompt after RAW_WORD_PREFIX (continuation_think)."""
    import torch

    prefix = S.ids(tok, RAW_WORD_PREFIX)
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"]) + len(prefix)].append(p)
    for group in by_len.values():
        for i in range(0, len(group), 64):
            chunk = group[i : i + 64]
            x = torch.tensor([p["ids"] + prefix for p in chunk], device="cuda")
            for p, text in zip(chunk, model.generate_batch(x, 4, [{}] * len(chunk)), strict=True):
                p["continuation_think"] = text


def raw_right(tok, p: dict) -> bool:
    """JUDGE_READ: digit prompts by the read, word prompts by the greedy judge after the empty think block."""
    if p["answer_kind"] == "digit":
        return read_right(tok, p)
    return (said(p.get("continuation_think", ""), p["judge"]) or "").lower() == p["expected"].lower()


def item_prompts(it: dict) -> dict[str, tuple[str, str, str, str]]:
    """kind -> (context, question, expected answer, answer kind) for one item."""
    kind = it.get("answer_kind", "digit")  # pointer_v5's word answers: "colour"
    spec = {"clean": (it["context"], it["question"], it["answer"], kind)}
    for s in SOURCES:
        src = it["sources"][s]
        spec[f"src_{s}"] = (src["context"], src["question"], src["answer"], kind)
    for h in ("hop1", "hop2"):
        if h in it:
            spec[h] = (it["context"], it[h]["question"], it[h]["answer"], it[h]["kind"])
    return spec


def stage_competence(name: str) -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.stats import wilson
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    check_switches(manifest)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    chat.check_format(manifest)  # prompts rendered in the manifest's format (BJ_FORMAT)
    for f, pin in manifest["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []
    labels = list(manifest["items"])
    for label in labels:
        for it in load_file(pins.REPO_ROOT / manifest["items"][label]["file"])[: manifest.get("limit")]:
            for kind, (ctx, q, ans, akind) in item_prompts(it).items():
                prompts.append({"label": label, "family": it["family"], "domain": it["domain"], "id": it["id"],
                                "kind": kind, "expected": ans, "answer_kind": "digit" if akind == "digit" else "word",
                                "judge": akind, "ids": S.ids(tok, S.render(tok, ctx, q))})  # fmt: skip
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    step = int(os.environ.get("BJ_GEN_BATCH", "64"))  # long prompts (pointer_v4 long, ~2100 tokens): smaller on a 27B
    chunks = [g[i : i + step] for g in by_len.values() for i in range(0, len(g), step)]
    for chunk in progress(chunks, "generate"):
        texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
        for p, text in zip(chunk, texts, strict=True):
            p["continuation"] = text
            p["said"] = said(text, p["judge"])
            p["correct"] = (p["said"] or "").lower() == p["expected"].lower()
    t_gen = time.time() - t0
    S.read_answers(model, tok, prompts)
    t_read = time.time() - t0 - t_gen
    fmt = chat.manifest_format(manifest)
    mode = manifest.get("judge_mode", judge_mode(fmt))
    assert mode == judge_mode(fmt), f"the manifest's judge is {mode}; set BJ_JUDGE={mode}"
    if mode == "read":  # JUDGE_READ (raw, the 2026-10-21 amendment) / JUDGE_READ_CHAT: the reads decide
        if fmt == "raw":
            raw_word_reads(model, tok, [p for p in prompts if p["answer_kind"] == "word"])
        for p in prompts:
            p["correct_greedy"] = p["correct"]
            p["correct"] = raw_right(tok, p) if fmt == "raw" else read_right(tok, p)
    rows = [{k: v for k, v in p.items() if k not in ("ids", "forced")} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary: dict[str, Any] = {"labels": {}, "seconds_generate": round(t_gen), "seconds_read": round(t_read),
                               "prompt_format": fmt, "judge_mode": mode, "judge": judge_rule(fmt)}  # fmt: skip
    for label in labels:
        fr = [r for r in rows if r["label"] == label]
        per_item: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in fr:
            per_item[r["id"]][r["kind"]] = r["correct"]
        cells = {}
        for kind in PROMPT_KINDS:
            got = [v[kind] for v in per_item.values() if kind in v]
            if got:
                cells[kind] = dict(zip(("rate", "lo", "hi"), wilson(sum(got), len(got)), strict=True)) | {"k": sum(got)}
        clean = [r for r in fr if r["kind"] == "clean"]
        summary["labels"][label] = {
            "n": len(per_item), "cells": cells, "eligible": sum(all(v.values()) for v in per_item.values()),
            "reliable": cells["clean"]["lo"] >= 0.85,
            "clean_median_p_answer": statistics.median(r["p_answer"] for r in clean),
            "read_agrees_with_greedy": statistics.mean((r["said"] or "").lower().startswith(r["read_top"].lower())
                                                       if r["read_top"] else False for r in fr),
            **({"clean_greedy_right": statistics.mean(r["correct_greedy"] for r in clean)} if mode == "read" else {}),
        }  # fmt: skip
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = ["| label | n | " + " | ".join(PROMPT_KINDS) + " | eligible | median p | read = greedy |",
             "|---" * (len(PROMPT_KINDS) + 5) + "|"]  # fmt: skip
    for label, s in summary["labels"].items():
        c = s["cells"]
        cols = [
            f"{100 * c[k]['rate']:.0f}% [{100 * c[k]['lo']:.0f},{100 * c[k]['hi']:.0f}]" if k in c else "-"
            for k in PROMPT_KINDS
        ]
        lines.append(f"| {label} | {s['n']} | " + " | ".join(cols) + f" | {s['eligible']} | "
                     f"{s['clean_median_p_answer']:.3f} | {100 * s['read_agrees_with_greedy']:.1f}% |")  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument("--set", dest="sets", nargs="+", choices=list(SETS), default=["main"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items per file (a smoke run)")
    args = ap.parse_args()
    if args.stage == "make":
        for s in args.sets:
            stage_make(s)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        for s in args.sets:
            stage_check(s)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.sets, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
