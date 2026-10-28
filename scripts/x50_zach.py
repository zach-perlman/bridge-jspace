"""x50_zach (batch 50, Z1 and Z2; jobs/c3/batch50.yaml, design and rules fixed in advance; Q50.1 / Q50.2 in
predictions/2026-10-28_dan.md): our change-removal on Zach's jsuite passages.

Items. Zach's v3 is not on the box: his v2 facts module (scripts/jsuite_v2.py), the main set jsuite_v2_test_chat (seed
2601; the set behind his headline and late-band numbers), and jsuite_v2nb_test_chat (his second seed) only if fewer than
N_ITEMS passages are eligible on the main set. A passage is a scene of his: one start (P or M), one level, one bridge;
its K item (the true facts of every entity stated: our lookup) and its M item (the bridge's fact not stated, the other
entities carry fictional values: our recall) ask the same question with the same answer; the passages share their
pointer / filler sentences and their order and differ only in the final-hop sentences. Leak filter (v2's descriptions
can leak): a description is dropped if it holds an answer word or one of its derived words (jsuite_v2_tables.DERIV, e.g.
French / France), for O's answer and S's.

Z1 (P start, named bridge). The pointer sentence names the bridge ("Tess Garland was raised in Bolivia."). S: the same
sentence names another entity of the passage, of the same relation, whose true fact the K passage states and whose
answer is not the bridge's; nothing else changes. The other entity is the first of the passage's candidates (a seeded
order per scene) whose name ends at the same token index (only the name's tokens change). Order strata (from the K
passage): fact-first if the bridge's fact sentence comes before the pointer sentence, else fact-after (the original
bridge's, as x0_split_by_order; the other entity's order is recorded beside). v2 has no hard-read flag.

Z2 (M start, never-named bridge). The question describes the bridge ("Which continent is the country that is home to
Machu Picchu in?"). S: the question describes another entity of the passage (same relation, its true fact stated in the
K passage, another answer) by one of its descriptions; the description ends at the same token index. Competence step
(47.3's): per description 10 prompts (5 wordings x 2 instructions, no passage) asking which entity it is; a description
is kept if the model names its entity (or one of its other names) in >= 0.90 of them; O's description and S's must be
kept.

The operation, both parts: Delta = h_S - h_O at the patch token (Z1: the last token of the pointer sentence's name; Z2:
the description's last token) at L (9B L12, 27B L32, Muse L26 and L36, both reported), per reader (the K and M
passages differ before the patch token, so each reader gets its own Delta), added on O. Arms: whole; without the J++
part (signed OMP, k = 25, the letter-token J++ atoms at L, X0's dictionary and pinned lens); without a random part of
its share (X0's random subspace, seed 888 + L). The read: the top token after the prompt (his chat framing: one user
turn, thinking off, no prefill) against the answer's first token (his "open" read, ablate_v2's correct_top). K switch:
the other entity's stated fact; M switch: the other entity's memory fact (the same word: K states true facts). The M
reader's lure (the other entity's fictional value stated in the M passage) is a route beside.

Gate (batch 47's): O's read accuracy >= 0.80 per reader over every candidate passage whose competence was run; eligible:
both readers say and read O's and S's answers right; the first N_ITEMS in passage order. The reads run on the eligible
passages whatever the gate says (gate.json records it; the verdict calls a failed gate "not tested" and shows the
numbers as descriptive only; the same gate over Zach's own competence-kept passages is recorded beside).

SEALED: the run writes per-item outputs only; `verdict` refuses until predictions/2026-10-28_dan.md holds Dan's Q50.1 (Z1)
or Q50.2 (Z2) at HEAD; it applies the rules and writes the verify-pack view (10 random passages, seed 0) and the figure
beside Zach's stored per-item knock-out rows (no rerun).

uv run python scripts/x50_zach.py plan                                              # CPU, three tokenizers
BJ_TARGET=qwen3.5-9b uv run python scripts/x50_zach.py run --part z1 --name qwen35_9b_x50_z1   # GPU, sealed
uv run python scripts/x50_zach.py verdict --part z1                                 # CPU, after Q50.1
uv run python scripts/x50_zach.py view --part z1                                    # CPU, the view alone (sealed too)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import subprocess
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

EXP = "x50_zach"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch50.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
PARTS = ("z1", "z2")
QUESTION = {"z1": "Q50.1", "z2": "Q50.2"}
WORDS = {"z1": ("PK", "PM"), "z2": ("MK", "MM")}  # (K final: lookup, M final: recall)
SETS = ("jsuite_v2_test_chat", "jsuite_v2nb_test_chat")  # the main set; the second seed only if items run short
TARGETS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
LAYERS = {"qwen3.5-9b": (12,), "qwen3.6-27b": (32,), "muse-glimmer-30b": (26, 36)}
RUNS = {p: {"qwen3.5-9b": f"qwen35_9b_x50_{p}", "qwen3.6-27b": f"x50_{p}_27b", "muse-glimmer-30b": f"muse30_x50_{p}"}
        for p in PARTS}  # fmt: skip
READERS = ("K", "M")
LOOKUP, RECALL = READERS
ARMS = ("whole", "no_jpp", "no_jpp_rand")
N_ITEMS, GATE, CF_SEED, EPS = 200, 0.80, 5001, 1e-9
GEN_TOKENS, DESC_GEN_TOKENS = 8, 12
DESC_BAR = 0.90
N_VIEW, VIEW_SEED = 10, 0
GAP_MIN, LOOKUP_MAX, THROUGH_MIN, ORDER_RATIO = 0.3, 0.10, 0.20, 2.0
INSTRUCTION = "Answer with just the answer, nothing else."  # tasks_v2.NATURAL_CHAT_INSTRUCTION (his chat framing)
DESC_INSTRUCTIONS = (INSTRUCTION, "Reply with the name only.")
DESC_TEMPLATES = ("{q1}", "Which {noun} is {d}?", "Name {d}.", "What is the name of {d}?",
                  "I am thinking of {d}. Which {noun} is it?")  # fmt: skip
RULE = {
    "z1": ("Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> \"the split holds on his passages\"; lookup >= 0.20 -> "
           "\"the lookup follows the lens here\"; else in between. Order split (after the gate, before the data): items "
           "where the bridge's fact sentence comes before the pointer sentence vs after. \"The order pattern replicates\" "
           "if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our "
           "65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items "
           "-> \"not a lookup-difficulty effect\"."),
    "z2": ("Per model, the 47.3 rule: (a) the split holds: gap >= 0.3, lookup <= 0.10; (a') the computed bridge is handed "
           "through the lens: lookup >= 0.20; (d) in between."),
}  # fmt: skip
AS_COMPUTED = (
    "Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages "
    "(J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M "
    "reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, "
    "10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under "
    "the whole change) holds no clause (\"can't tell\"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader "
    "beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change "
    "switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer "
    "sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether "
    "they separate). Hard-read: no flag in v2, so not tested."
)  # fmt: skip
# Zach's stored per-item knock-out rows on jsuite_v2_test_chat (scripts/ablate_v2.py; J++ top-10 at his band; 'none',
# 'paper10' and 'paper10_rot' rows per item id): the band starting at our L ("full"), and his question-only knock-out
# ("question"; Z2 beside, the nearest stored erase at the description). No M-start swap rows exist (jswap is P/T only).
BESIDE = {
    "qwen3.5-9b": {"full": "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1",
                   "question": "qwen35_9b_jsuite_v2_test_chat_ko_cand2_posquestion_v1"},
    "qwen3.6-27b": {"full": "jsuite_v2_test_chat_ko_cand2_v1", "question": "jsuite_v2_test_chat_ko_cand2_posquestion_v1"},
    "muse-glimmer-30b": {"full": "muse30_jsuite_v2_test_chat_ko_cand2_v1",
                         "question": "muse30_jsuite_v2_test_chat_ko_cand2_L36-42_posquestion_v1"},
}  # fmt: skip
BESIDE_BAND = {"qwen3.5-9b": "L12-16", "qwen3.6-27b": "L32-40", "muse-glimmer-30b": "L36-42"}


# ---- passages (CPU) -----------------------------------------------------------------------------------------------


def tables():
    from scripts import jsuite_v2_tables as TB

    return TB


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def fact(rel: str, e: str) -> str:
    return tables().REL2[rel]["facts"][e][0]


def kfact(rel: str, w: int, e: str) -> str:
    """The K passage's true-fact sentence for e (jsuite_v2.facts_items' kf)."""
    a = fact(rel, e)
    return (
        tables()
        .REL2[rel]["kfact"][w]
        .format(x=e, X=cap(e), a=a, al=a.lower(), an="an" if a[0].upper() in "AEIOU" else "a")
    )


def lure(rel: str, w: int, e: str, context: str) -> str | None:
    """The value e's fictional final-hop sentence (pfact) states in an M passage, or None."""
    t = tables().REL2[rel]["pfact"][w]
    pat = re.escape(t)
    for key, rep in (("{x}", re.escape(e)), ("{X}", re.escape(cap(e))), ("{an}", "(?:a|an)")):
        pat = pat.replace(re.escape(key), rep)
    for key in ("{a}", "{al}"):
        pat = pat.replace(re.escape(key), r"(?P<a>[A-Za-z][A-Za-z ]*?)", 1)
    m = re.search(pat, context)
    if not m:
        return None
    vocab = {v.lower(): v for v in tables().vocab(rel)}
    return vocab.get(m.group("a").lower())


def giveaways(answer: str) -> list[str]:
    return [answer, *tables().DERIV.get(answer, [])]


def leaks(desc: str, answers: list[str]) -> list[str]:
    """The answer words (or derived words) the description holds, case-insensitive whole words."""
    return [w for a in answers for w in giveaways(a) if re.search(r"(?i)\b" + re.escape(w) + r"\b", desc)]


def person(item: dict) -> str:
    """The asked person of a P-start item, read off its description (the pdesc wording)."""
    t = tables().REL2[item["relation"]]["pdesc"][item["wording"]]
    m = re.fullmatch(re.escape(t).replace(re.escape("{p}"), "(?P<p>.+)"), item["start_desc"])
    assert m, f"{item['id']}: the description does not match its wording"
    return m.group("p")


def pointer(item: dict, x: str) -> str:
    """The pointer sentence naming x for the item's asked person (bind templates use {x}, never {X})."""
    return tables().REL2[item["relation"]]["bind"][item["wording"]].format(p=person(item), x=x, X=cap(x))


def descriptions(rel: str, e: str) -> list[tuple[str, str]]:
    """e's (description, hop-1 question) pairs as jsuite_facts.m_desc writes them."""
    from scripts import jsuite_facts as JF

    return [JF.m_desc(noun, r, rel == "people") for noun, r in tables().REL2[rel]["facts"][e][1]]


def question(item: dict, d: str) -> str:
    return tables().REL2[item["relation"]]["q2M"][item["wording"]].format(d=d, D=cap(d))


def alts(rel: str, e: str) -> list[str]:
    """e's names that count (jsuite_v2's hop-1 alts: the name, its other names, a person's first name)."""
    from scripts import natural_v1 as N

    TB = tables()
    names = {e, *TB.ALT.get(rel, {}).get(e, []), TB.FIRST_NAMES.get(e, N.FIRST_NAMES.get(e, e))}
    return sorted({n[4:] if n.startswith("the ") else n for n in names} | names)


def says(text: str, names: list[str]) -> bool:
    """The reply's first line holds one of the names (case-insensitive, whole words)."""
    from scripts import suite_v1 as S

    line = S.first_line(text)
    return any(re.search(r"(?i)\b" + re.escape(n) + r"\b", line) for n in names)


def pairs(items: list[dict], part: str) -> tuple[list[dict], collections.Counter]:
    """Each scene's K and M items of the part's start (same passage layout, same question and answer), in scene order."""
    kw, mw = WORDS[part]
    by: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in items:
        if it.get("module") == "facts" and it["word"] in (kw, mw):
            by[it["scene"]][LOOKUP if it["word"] == kw else RECALL] = it
    out, why = [], collections.Counter()
    for scene in sorted(by):
        p = by[scene]
        if set(p) != set(READERS):
            why["a reader is missing"] += 1
            continue
        k, m = p[LOOKUP], p[RECALL]
        if any(k[f] != m[f] for f in ("question", "answer", "bridge", "entities", "wording", "relation", "start_desc")):
            why["the K and M items differ in question, answer, bridge or entities"] += 1
            continue
        out.append(p)
    return out, why


def span_tokens(
    tok, text: str, ctx: str, sent: str, word: str, item_q: str | None = None
) -> tuple[list[int], list[int]]:
    """The rendered prompt's ids and the token positions of `word` in `sent` (in the context, or in the question when
    item_q is given)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    enc = raw_encoding(tok, text, offsets=True)
    if item_q is None:
        assert text.count(ctx) == 1, "the context is not once in the prompt"
        assert ctx.count(sent) == 1, "the pointer sentence is not once in the context"
        w0 = text.index(ctx) + ctx.index(sent) + sent.rindex(word)
    else:
        at = text.rindex(item_q)
        w0 = at + item_q.index(word)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(word))


def render(tok, item: dict, context: str, q: str) -> str:
    from scripts import tasks_v2 as T

    return T.render(tok, {**item, "context": context, "question": q})


def answer_tok(tok, a: str) -> int:
    from scripts import suite_v1 as S

    return S.answer_token(tok, a, "open")


def encode(tok, part: str, p: dict, e: str, d_e: str | None = None) -> tuple[dict | None, str]:
    """Both readers' O and S prompts with e as S's bridge (Z1: named in the pointer sentence; Z2: described by d_e in the
    question), or the reason it does not align: the patch token (the name's / description's last token) at one index in
    O and S, only the name's / description's tokens differ, distinct first answer tokens."""
    k = p[LOOKUP]
    rel, x, real, w = k["relation"], k["bridge"], k["answer"], k["wording"]
    cf_ans = fact(rel, e)
    readers = {}
    for r in READERS:
        it = p[r]
        ctx, q = it["context"], it["question"]
        if part == "z1":
            sent, cf_sent = pointer(it, x), pointer(it, e)
            cf_ctx, cf_q = ctx.replace(sent, cf_sent), q
            ids_o, at_o = span_tokens(tok, render(tok, it, ctx, q), ctx, sent, x)
            ids_s, at_s = span_tokens(tok, render(tok, it, cf_ctx, q), cf_ctx, cf_sent, e)
        else:
            assert d_e is not None
            cf_ctx, cf_q = ctx, question(it, d_e)
            d_o = it["start_desc"]
            ids_o, at_o = span_tokens(tok, render(tok, it, ctx, q), ctx, "", d_o if d_o in q else cap(d_o), q)
            ids_s, at_s = span_tokens(tok, render(tok, it, ctx, cf_q), ctx, "", d_e if d_e in cf_q else cap(d_e), cf_q)
        if len(ids_o) != len(ids_s) or not at_o or not at_s or at_o[-1] != at_s[-1]:
            return None, "the patch token is not at one index in O and S"
        changed = [i for i, (a, b) in enumerate(zip(ids_o, ids_s, strict=True)) if a != b]
        if not changed or not all(min(at_o[0], at_s[0]) <= i <= at_o[-1] for i in changed):
            return None, "tokens outside the name / description change"
        tok_a, tok_b = answer_tok(tok, real), answer_tok(tok, cf_ans)
        if tok_a == tok_b:
            return None, "O's and S's answers share their first token"
        lu = lure(rel, w, e, ctx) if r == RECALL else None
        readers[r] = {"id": it["id"], "question": q, "cf_question": cf_q, "context": ctx, "cf_context": cf_ctx,
                      "answer": real, "cf_answer": cf_ans, "ids": {"org": ids_o, "alt": ids_s}, "pos": at_o[-1],
                      "span": [at_o[0], at_o[-1]], "tok_A": tok_a, "tok_b": tok_b, "lure": lu,
                      "tok_lure": answer_tok(tok, lu) if lu else None}  # fmt: skip
    case = {"part": part, "scene": k["scene"], "set": k.get("_set"), "relation": rel, "bridge": x, "cf_bridge": e,
            "level": k["level"], "popularity": k["popularity"], "half": k.get("half"), "wording": w,
            "answer": real, "cf_answer": cf_ans, "readers": readers}  # fmt: skip
    if part == "z1":
        ctx = k["context"]
        ptr = ctx.index(pointer(k, x))
        case["order"] = {"bridge_fact_first": ctx.index(kfact(rel, w, x)) < ptr,
                         "cf_fact_first": ctx.index(kfact(rel, w, e)) < ptr}  # fmt: skip
        case["stratum"] = "fact-first" if case["order"]["bridge_fact_first"] else "fact-after"
    else:
        case["desc"], case["cf_desc"] = k["start_desc"], d_e
    return case, ""


def others(p: dict) -> list[str]:
    """The passage's other entities whose answer differs from the bridge's, in a seeded order per scene (their facts
    are stated in the K passage: asserted)."""
    k = p[LOOKUP]
    rel, x = k["relation"], k["bridge"]
    cands = sorted(e for e in k["entities"] if e != x and fact(rel, e) != fact(rel, x))
    for e in cands:
        assert kfact(rel, k["wording"], e) in k["context"], f"{k['id']}: {e}'s fact is not stated in the K passage"
    random.Random(f"{CF_SEED}|{k['scene']}").shuffle(cands)
    return cands


def z1_cases(tok, ps: list[dict]) -> tuple[list[dict], collections.Counter]:
    """Z1: per passage the first aligning other entity (seeded order); drops counted by reason."""
    out, why = [], collections.Counter()
    for p in ps:
        if leaks(p[LOOKUP]["start_desc"], [p[LOOKUP]["answer"]]):
            why["leak: the description holds the answer"] += 1
            continue
        cands = others(p)
        if not cands:
            why["no other entity with another answer"] += 1
            continue
        reasons = []
        for e in cands:
            c, r = encode(tok, "z1", p, e)
            if c is not None:
                c["cf_candidates"] = len(cands)
                out.append(c)
                break
            reasons.append(r)
        else:
            why[f"no candidate aligns ({reasons[0]})"] += 1
    return out, why


def z2_options(tok, ps: list[dict]) -> tuple[list[tuple[dict, list[dict]]], collections.Counter]:
    """Z2: per passage every aligning, non-leaking (other entity, description) option in the seeded entity order (the
    competence step picks among them); drops counted by reason."""
    out, why = [], collections.Counter()
    for p in ps:
        k = p[LOOKUP]
        rel = k["relation"]
        if leaks(k["start_desc"], [k["answer"]]):
            why["leak: O's description holds the answer"] += 1
            continue
        cands = others(p)
        if not cands:
            why["no other entity with another answer"] += 1
            continue
        opts, leaked, reasons = [], 0, []
        for e in cands:
            for d, _ in descriptions(rel, e):
                if leaks(d, [k["answer"], fact(rel, e)]):
                    leaked += 1
                    continue
                c, r = encode(tok, "z2", p, e, d)
                if c is None:
                    reasons.append(r)
                else:
                    c["cf_candidates"] = len(cands)
                    opts.append(c)
        why["(options dropped for a leak)"] += leaked
        if not opts:
            why[f"no option aligns ({reasons[0] if reasons else 'every option leaks'})"] += 1
            continue
        out.append((p, opts))
    return out, why


def desc_prompts(tok, descs: dict[tuple[str, str, str], str]) -> list[dict]:
    """The competence prompts: per (relation, entity, description), DESC_TEMPLATES x DESC_INSTRUCTIONS, no passage."""
    from bridge_jspace.tokens import raw_encoding

    out = []
    for (rel, e, d), q1 in sorted(descs.items()):
        noun = "person" if rel == "people" else tables().REL2[rel]["noun"]
        for t, tmpl in enumerate(DESC_TEMPLATES):
            for i, instr in enumerate(DESC_INSTRUCTIONS):
                msg = f"{tmpl.format(q1=q1, noun=noun, d=d)} {instr}"
                text = tok.apply_chat_template([{"role": "user", "content": msg}], tokenize=False,
                                               add_generation_prompt=True, enable_thinking=False)  # fmt: skip
                out.append({"relation": rel, "entity": e, "desc": d, "template": t, "instruction": i, "text": text,
                            "ids": raw_encoding(tok, text)["input_ids"]})  # fmt: skip
    return out


def desc_table(rows: list[dict]) -> dict[str, dict]:
    """Per description: prompts, right, share, kept (share >= DESC_BAR)."""
    by: dict[tuple, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by[(r["relation"], r["entity"], r["desc"])].append(r)
    out = {}
    for (rel, e, d), rs in sorted(by.items()):
        right = sum(r["right"] for r in rs)
        out[f"{rel}|{e}|{d}"] = {"relation": rel, "entity": e, "desc": d, "prompts": len(rs), "right": right,
                                 "share": round(right / len(rs), 4), "kept": right / len(rs) >= DESC_BAR - EPS}  # fmt: skip
    return out


def z2_choose(options: list[tuple[dict, list[dict]]], kept: dict[str, dict]) -> tuple[list[dict], collections.Counter]:
    """Per passage: O's description kept, then the first option whose description is kept."""
    ok = lambda rel, e, d: kept.get(f"{rel}|{e}|{d}", {}).get("kept", False)  # noqa: E731
    out, why = [], collections.Counter()
    for p, opts in options:
        k = p[LOOKUP]
        if not ok(k["relation"], k["bridge"], k["start_desc"]):
            why["competence: O's description not named >= 0.90"] += 1
            continue
        good = [c for c in opts if ok(c["relation"], c["cf_bridge"], c["cf_desc"])]
        if not good:
            why["competence: no S description named >= 0.90"] += 1
            continue
        out.append(good[0])
    return out, why


def z2_descs(options: list[tuple[dict, list[dict]]]) -> dict[tuple[str, str, str], str]:
    """Every description the options use (O's and S's), with its hop-1 question."""
    out = {}
    for p, opts in options:
        k = p[LOOKUP]
        rel = k["relation"]
        for e in {k["bridge"], *(c["cf_bridge"] for c in opts)}:
            for d, q1 in descriptions(rel, e):
                out[(rel, e, d)] = q1
    return out


def load_pairs(set_name: str, part: str) -> tuple[list[dict], collections.Counter]:
    from scripts import tasks_v2 as T

    items = [{**it, "_set": set_name} for it in T.load(set_name)]
    return pairs(items, part)


# ---- plan (CPU) ---------------------------------------------------------------------------------------------------


def mark(decode, ids: list[int], pos: int) -> str:
    return decode(ids[:pos]) + "⟦" + decode(ids[pos : pos + 1]) + "⟧" + decode(ids[pos + 1 :])


def plan_one(tok, part: str) -> dict:
    out: dict[str, Any] = {}
    for s in SETS:
        ps, why = load_pairs(s, part)
        if part == "z1":
            cases, drop = z1_cases(tok, ps)
            out[s] = {"passages": len(ps), "pair_drops": dict(why), "cases": len(cases), "drops": dict(drop),
                      "strata": dict(collections.Counter(c["stratum"] for c in cases)),
                      "cf_order": dict(collections.Counter(str(c["order"]["cf_fact_first"]) for c in cases)),
                      "relations": dict(collections.Counter(c["relation"] for c in cases)),
                      "lure_found": sum(c["readers"][RECALL]["lure"] is not None for c in cases)}  # fmt: skip
        else:
            opts, drop = z2_options(tok, ps)
            cases = [o[0] for _, o in opts]  # before the competence step: each passage's first option
            out[s] = {"passages": len(ps), "pair_drops": dict(why), "with_options": len(opts), "drops": dict(drop),
                      "options": sum(len(o) for _, o in opts), "descriptions": len(z2_descs(opts)),
                      "competence_prompts": len(z2_descs(opts)) * len(DESC_TEMPLATES) * len(DESC_INSTRUCTIONS),
                      "relations": dict(collections.Counter(c["relation"] for c in cases))}  # fmt: skip
        out[s]["examples"] = [example(tok.decode, c) for c in cases[:5]] if s == SETS[0] else []
    return out


def example(decode, c: dict) -> dict:
    ex = {"scene": c["scene"], "bridge": c["bridge"], "cf_bridge": c["cf_bridge"], "answer": c["answer"],
          "cf_answer": c["cf_answer"], **({"stratum": c["stratum"]} if "stratum" in c else {}),
          **({"desc": c["desc"], "cf_desc": c["cf_desc"]} if "desc" in c else {})}  # fmt: skip
    for r, rd in c["readers"].items():
        ex[r] = {"id": rd["id"], "O": mark(decode, rd["ids"]["org"], rd["pos"]), "S": mark(decode, rd["ids"]["alt"], rd["pos"]),
                 "lure": rd["lure"]}  # fmt: skip
    return ex


def stage_plan(plan_dir: str | None = None) -> Path:
    """On BJ_TARGET's tokenizer, per part: passages, drops by reason, strata, and 5 rendered prompt pairs (both readers,
    the patch token in ⟦…⟧), written as plan-<target>.{json,md} to plan_dir (default results/x50_zach/plan-<UTC>/; run
    once per model into one folder). Z2 is counted before its competence step (the GPU's)."""
    from bridge_jspace.utils import git_state
    from scripts import x45m

    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    t = pins.TARGET
    tok = x45m.tokenizer()
    blob: dict[str, Any] = {"target": t, "code": git_state(), "sets": list(SETS), "words": WORDS, "n_items": N_ITEMS,
                            "cf_seed": CF_SEED}  # fmt: skip
    lines = [f"# x50_zach plan on {t}'s tokenizer (UNVERIFIED)", ""]
    for part in PARTS:
        res = plan_one(tok, part)
        blob[part] = res
        main = res[SETS[0]]
        lines += [f"## {t} {part}", "", "main set: " + json.dumps({k: v for k, v in main.items() if k != "examples"}), "",
                  f"second seed: {json.dumps({k: v for k, v in res[SETS[1]].items() if k != 'examples'})}", ""]  # fmt: skip
        for ex in main["examples"]:
            lines += [f"### {ex['scene']}: {ex['bridge']} -> {ex['cf_bridge']} ({ex['answer']} -> {ex['cf_answer']})"
                      + (f", {ex['stratum']}" if "stratum" in ex else "")
                      + (f"; {ex['desc']!r} -> {ex['cf_desc']!r}" if "desc" in ex else ""), ""]  # fmt: skip
            for r in READERS:
                lines += [f"**{r}** ({ex[r]['id']}; lure {ex[r]['lure']}) O:", "", "```", ex[r]["O"], "```", "", "S:", "",
                          "```", ex[r]["S"], "```", ""]  # fmt: skip
    (out / f"plan-{t}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / f"plan-{t}.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


# ---- GPU ----------------------------------------------------------------------------------------------------------


def generate(model, prompts: list[dict], n_tokens: int, desc: str) -> list[str]:
    """n_tokens greedy tokens per prompt, prompts of one length batched together."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_split as P

    texts: list[str | None] = [None] * len(prompts)
    by_len: dict[int, list[int]] = collections.defaultdict(list)
    for i, p in enumerate(prompts):
        by_len[len(p["ids"])].append(i)
    chunks = [idx[s : s + P.BATCH] for idx in by_len.values() for s in range(0, len(idx), P.BATCH)]
    with torch.no_grad():
        for chunk in progress(chunks, desc):
            ids = torch.tensor([prompts[i]["ids"] for i in chunk], device=model.device)
            for i, t in zip(chunk, model.generate_batch(ids, n_tokens, [{} for _ in chunk]), strict=True):
                texts[i] = t
    return [t or "" for t in texts]


def desc_competence(model, prompts: list[dict]) -> list[dict]:
    texts = generate(model, prompts, DESC_GEN_TOKENS, "description competence (prompt batch)")
    return [{**{k: p[k] for k in ("relation", "entity", "desc", "template", "instruction")}, "greedy": t,
             "right": says(t, alts(p["relation"], p["entity"]))} for p, t in zip(prompts, texts, strict=True)]  # fmt: skip


def competence(model, cases: list[dict], ws) -> list[dict]:
    """Unedited O and S of both readers: GEN_TOKENS greedy tokens (said right: the reply's first line holds the answer)
    and the decisive read (the top token is the answer's first token)."""
    import torch

    from bridge_jspace.utils import progress

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (passage)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                texts = model.generate_batch(ids, GEN_TOKENS, [{}, {}])
                for i, (v, gold, tok_gold) in enumerate((("org", rd["answer"], rd["tok_A"]),
                                                         ("alt", rd["cf_answer"], rd["tok_b"]))):  # fmt: skip
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", [], ws)
                    top = int(logits[0].argmax())
                    rows.append({"scene": c["scene"], "set": c["set"], "reader": w, "variant": v, "greedy": texts[i],
                                 "right": says(texts[i], [gold]), "read_right": top == tok_gold, "top": top})  # fmt: skip
    return rows


def gate_of(cases: list[dict], comp: list[dict], kept_ids: set[str] | None = None) -> tuple[dict, list[dict]]:
    """The gate (O's read accuracy >= GATE per reader over the cases) and the eligible cases (both readers say and read
    O's and S's answers right), in case order; with kept_ids, the same gate over Zach's competence-kept passages."""
    right = {(r["set"], r["scene"], r["reader"], r["variant"]): r for r in comp}
    key = lambda c, w, v: (c["set"], c["scene"], w, v)  # noqa: E731
    acc = {w: float(np.mean([right[key(c, w, "org")]["read_right"] for c in cases])) if cases else 0.0 for w in READERS}
    ok = [c for c in cases if all(right[key(c, w, v)]["right"] and right[key(c, w, v)]["read_right"]
                                  for w in READERS for v in ("org", "alt"))]  # fmt: skip
    gate: dict[str, Any] = {"cases": len(cases), "org_read_accuracy": acc, "gate": GATE,
                            "pass": bool(cases) and all(a >= GATE - EPS for a in acc.values()), "eligible": len(ok)}  # fmt: skip
    if kept_ids is not None:
        mine = [c for c in cases if c["set"] == SETS[0] and c["readers"][LOOKUP]["id"] in kept_ids]
        g2, ok2 = gate_of(mine, comp)
        gate["over_zach_kept"] = {k: g2[k] for k in ("cases", "org_read_accuracy", "pass")} | {"eligible": len(ok2)}
    return gate, ok


def zach_kept(target: str) -> set[str] | None:
    """The item ids Zach's knock-out rows hold for the target (his competence-kept items), None without the run."""
    path = pins.RESULTS_DIR / "ablate_v2" / BESIDE[target]["full"] / "rows.jsonl"
    if not path.exists():
        return None
    return {json.loads(line)["id"] for line in path.read_text().splitlines() if '"condition": "none"' in line}


def manifest(name: str, part: str, target: str, layers: tuple[int, ...]) -> dict:
    from bridge_jspace.data import sha256_of
    from bridge_jspace.utils import git_state

    inputs = {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p)
              for p in [SPEC, *(pins.DATA_DIR / "tasks_v2" / s / "items.jsonl" for s in SETS)] if p.exists()}  # fmt: skip
    return {"exp": EXP, "run": name, "part": part, "test": part.upper(), "spec": "jobs/c3/batch50.yaml",
            "question": f"{QUESTION[part]} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "inputs": inputs,
            "sets": list(SETS), "words": list(WORDS[part]), "layers": list(layers), "n_items": N_ITEMS, "gate": GATE,
            "arms": list(ARMS), "k": X.K_MAIN, "omp": "signed", "cf_seed": CF_SEED,
            "patch": "the last token of the pointer sentence's name" if part == "z1" else "the description's last token",
            "read": "the top token after the prompt (his chat framing, no prefill) against the answer's first token",
            "desc_competence": {"templates": list(DESC_TEMPLATES), "instructions": list(DESC_INSTRUCTIONS),
                                "bar": DESC_BAR, "tokens": DESC_GEN_TOKENS} if part == "z2" else None,
            "rule": RULE[part], "as_computed": AS_COMPUTED, "beside": BESIDE.get(target),
            "seeds": {"cf_order": CF_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer", "bootstrap": X.BOOT_SEED,
                      "view": VIEW_SEED},
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION[part]} answer"}  # fmt: skip


def build(tok, model, part: str, set_name: str, out: Path) -> tuple[list[dict], dict]:
    """The set's cases for the part (Z2: after its description competence step, rows appended to out/)."""
    ps, why = load_pairs(set_name, part)
    if part == "z1":
        cases, drop = z1_cases(tok, ps)
        return cases, {"passages": len(ps), "pair_drops": dict(why), "drops": dict(drop), "cases": len(cases)}
    opts, drop = z2_options(tok, ps)
    prompts = desc_prompts(tok, z2_descs(opts))
    rows = desc_competence(model, prompts)
    with (out / "desc_competence.jsonl").open("a") as f:
        f.writelines(json.dumps({**r, "set": set_name}) + "\n" for r in rows)
    table = desc_table(rows)
    cases, drop2 = z2_choose(opts, table)
    counts = {"passages": len(ps), "pair_drops": dict(why), "drops": dict(drop), "with_options": len(opts),
              "descriptions": len(table), "descriptions_kept": sum(t["kept"] for t in table.values()),
              "competence_drops": dict(drop2), "cases": len(cases)}  # fmt: skip
    return cases, counts


def stage_run(name: str, part: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in LAYERS, f"batch 50 runs on {sorted(LAYERS)}, not {target}"
    layers = LAYERS[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, part, target, layers)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    ws = X.whitespace_mask(model)

    # the cases, set by set until N_ITEMS are eligible; the gate over every case whose competence ran
    cases, comp, counts, ok = [], [], {}, []
    for s in SETS:
        got, counts[s] = build(tok, model, part, s, out)
        cases += got
        comp += competence(model, got, ws)
        _, ok = gate_of(cases, comp)
        if len(ok) >= N_ITEMS:
            break
    gate, ok = gate_of(cases, comp, zach_kept(target))
    chosen = ok[:N_ITEMS]
    gate.update({"chosen": len(chosen), "counts": counts, "sets_used": sorted({c["set"] for c in cases}),
                 "chosen_sets": dict(collections.Counter(c["set"] for c in chosen)),
                 "order": [[c["set"], c["scene"]] for c in chosen]})  # fmt: skip
    if part == "z1":
        gate["chosen_strata"] = dict(collections.Counter(c["stratum"] for c in chosen))
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    (out / "gate.json").write_text(json.dumps(gate, indent=1) + "\n")
    print(json.dumps({k: v for k, v in gate.items() if k != "order"}, indent=1), flush=True)
    if not chosen:
        print("not tested: no eligible passage", flush=True)
        return out

    with torch.no_grad():
        # the change per reader at the patch token, every layer in one forward per prompt
        deltas: dict[str, list] = {r: [] for r in READERS}
        for c in progress(chosen, f"the change at the patch token, L{list(layers)} (passage)"):
            for r, rd in c["readers"].items():
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=layers)[1] for v in ("org", "alt")}
                deltas[r].append(
                    torch.stack([(h["alt"][la][rd["pos"]] - h["org"][la][rd["pos"]]).float() for la in layers])
                )
        rows, norms = [], []
        for li, la in enumerate(layers):
            jdic = JLens(model, "jpp").vectors(la, model.letter_token_ids()).to(dev)
            basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            arms: dict[str, dict[str, Any]] = {}
            for r in READERS:
                x = torch.stack([d[li] for d in deltas[r]]).to(dev)
                more, sh = R.removal_arms(x, {"jpp": X.fit(jdic, x, X.K_MAIN, "signed").to(dev)}, basis)
                arms[r] = {"whole": x, **more}
                assert tuple(arms[r]) == ARMS, tuple(arms[r])
                norms += [{"scene": c["scene"], "set": c["set"], "layer": la, "reader": r, "norm": round(float(x[i].norm()), 4),
                           "share_jpp": round(float(sh["jpp"][i]), 5)} for i, c in enumerate(chosen)]  # fmt: skip
            del jdic
            for i, c in enumerate(progress(chosen, f"reads at L{la} (passage)")):
                for r, rd in c["readers"].items():
                    cands = torch.tensor(sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}),
                                         device=dev)  # fmt: skip
                    edits = [{}] + [{la: AddRows(arms[r][a][i : i + 1], [rd["pos"]])} for a in ARMS]
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", [], ws)
                    for a, lg in zip(("none", *ARMS), logits, strict=True):
                        row = X.read_row(lg, rd, cands)
                        rows.append({"scene": c["scene"], "set": c["set"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                                     "relation": c["relation"], "stratum": c.get("stratum"), "layer": la, "reader": r,
                                     "arm": a, "route": route(row["top"], rd), **row})  # fmt: skip
            X.write_jsonl(out / "outcomes.jsonl", rows)  # rewritten after each layer (a partial run keeps its rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    m["items"] = len(chosen)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


def route(top: int, rd: dict) -> str:
    """switch (the other entity's answer), original, lure (the M passage's stated value for the other entity), other."""
    if top == rd["tok_b"]:
        return "switch"
    if top == rd["tok_A"]:
        return "original"
    return "lure" if rd.get("tok_lure") is not None and top == rd["tok_lure"] else "other"


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(question: str, rev: str = "HEAD") -> str:
    """Dan's committed answer to the question (the 'Dan:' line of its block in the predictions file at `rev`), '' if
    none (x47_chain.dan_answer's reading)."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{question}**" not in text:
        return ""
    block = text.split(f"**{question}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def require_answer(part: str) -> str:
    answer = dan_answer(QUESTION[part])
    assert answer, (
        f"sealed: {PREDICTIONS} has no committed answer to {QUESTION[part]} (its 'Dan:' line is empty at HEAD)"
    )
    return answer


def ok(z: float | None) -> bool:
    return not (z is None or math.isnan(z))


def main_rule(part: str, lookup: float, gap: float) -> str:
    """Z1: split holds / follows the lens / in between; Z2: (a) / (a') / (d); can't tell when undefined."""
    if not ok(lookup):
        return "can't tell (no lookup switch under the whole change)"
    names = {"z1": ("the split holds on his passages", "the lookup follows the lens here", "in between"),
             "z2": ("(a) the split holds", "(a') the computed bridge is handed through the lens", "(d) in between")}[part]  # fmt: skip
    if ok(gap) and gap >= GAP_MIN - EPS and lookup <= LOOKUP_MAX + EPS:
        return names[0]
    if lookup >= THROUGH_MIN - EPS:
        return names[1]
    return names[2]


def order_rule(first: list[float], after: list[float]) -> dict:
    """Replicates iff the fact-first whole-change switch share >= 2 x the fact-after one (point estimates); the
    intervals beside and whether they separate."""
    f, a = first[0], after[0]
    holds = ok(f) and ok(a) and f > 0 and f >= ORDER_RATIO * a - EPS
    return {"replicates": bool(holds), "ratio": (f / a if a > 0 else math.inf if f > 0 else math.nan) if ok(f) and ok(a) else math.nan,
            "separate": bool(ok(first[1]) and ok(after[2]) and first[1] > after[2])}  # fmt: skip


def share_ci(values: list[int], ents: list[str], n_boot: int) -> list[float]:
    if not values:
        return [math.nan, math.nan, math.nan]
    rr = X.resampled_rates({"s": values}, ents, n_boot)["s"]
    return [float(np.mean(values)), *X.interval(rr)]


def layer_result(part: str, rows: list[dict], n_boot: int) -> dict:
    """At one layer: per reader X0's cell (whole / no J++ / no random), the gap on paired draws, the rule; Z1 the order
    strata (the K reader's whole-change switch share per stratum)."""
    by = {(r["set"], r["scene"], r["reader"], r["arm"]): r for r in rows}
    keys = list(dict.fromkeys((r["set"], r["scene"]) for r in rows if r["arm"] == "whole" and r["reader"] == LOOKUP))
    ent = {(r["set"], r["scene"]): r["entity"] for r in rows}
    ents = [ent[k] for k in keys]
    cells, draws, routes = {}, {}, {}
    for w in READERS:
        sw = {a: [int(by[(*k, w, a)]["switched"]) for k in keys] for a in ARMS}
        cells[w] = X.cell({"whole": sw["whole"], "no_part": sw["no_jpp"], "no_rand": sw["no_jpp_rand"]}, ents, n_boot)
        rr = X.resampled_rates(sw, ents, n_boot)
        draws[w] = X.dependence(rr["whole"], rr["no_jpp"]) - X.dependence(rr["whole"], rr["no_jpp_rand"])
        routes[w] = {a: dict(collections.Counter(by[(*k, w, a)]["route"] for k in keys)) for a in ("none", *ARMS)}
    gap = [cells[RECALL]["excess"][0] - cells[LOOKUP]["excess"][0], *X.interval(draws[RECALL] - draws[LOOKUP])]
    out = {"n": len(keys), "entities": len(set(ents)), "lookup": cells[LOOKUP], "recall": cells[RECALL], "gap": gap,
           "verdict": main_rule(part, cells[LOOKUP]["excess"][0], gap[0]), "routes": routes}  # fmt: skip
    if part == "z1":
        strata = {}
        for s in ("fact-first", "fact-after"):
            ks = [k for k in keys if by[(*k, LOOKUP, "whole")]["stratum"] == s]
            strata[s] = {"n": len(ks), "whole_switch": share_ci([int(by[(*k, LOOKUP, "whole")]["switched"]) for k in ks],
                                                                [ent[k] for k in ks], n_boot)}  # fmt: skip
        out["order"] = {
            "strata": strata,
            **order_rule(strata["fact-first"]["whole_switch"], strata["fact-after"]["whole_switch"]),
        }
        out["hard_read"] = "no hard-read flag in v2 (not tested)"
    return out


def beside(target: str, part: str, cases: list[dict], n_boot: int) -> dict:
    """Zach's stored per-item knock-out on our chosen passages of the main set (joined by item id): per passage his
    accuracy lost (none minus paper10, and minus paper10_rot) on the M item minus on the K item, mean with a cluster
    bootstrap over the bridge entity; per stored run (full band; Z2 also question-only)."""
    out: dict[str, Any] = {"band": BESIDE_BAND.get(target), "swap": "no M-start swap or erase rows in his results "
                           "(jswap covers P and T starts only)" if part == "z2" else None}  # fmt: skip
    mine = [c for c in cases if c["set"] == SETS[0]]
    for kind, run in BESIDE.get(target, {}).items():
        if part == "z1" and kind != "full":
            continue
        path = pins.RESULTS_DIR / "ablate_v2" / run / "rows.jsonl"
        if not path.exists():
            out[kind] = {"run": run, "status": "no rows here"}
            continue
        want = {c["readers"][w]["id"] for c in mine for w in READERS}
        acc: dict[tuple[str, str], int] = {}
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if r["id"] in want and r.get("kind") == "clean" and r["condition"] in ("none", "paper10", "paper10_rot"):
                acc[(r["id"], r["condition"])] = int(bool(r["correct"]))
        res: dict[str, Any] = {"run": run}
        for ctrl in ("paper10", "paper10_rot"):
            vals, ents = [], []
            for c in mine:
                ids = [c["readers"][w]["id"] for w in (RECALL, LOOKUP)]
                if all((i, cond) in acc for i in ids for cond in ("none", ctrl)):
                    lost = [acc[(i, "none")] - acc[(i, ctrl)] for i in ids]
                    vals.append(lost[0] - lost[1])
                    ents.append(c["bridge"])
            res[ctrl] = {"joined": len(vals), "m_minus_k": share_ci(vals, ents, n_boot) if vals else [math.nan] * 3}
        out[kind] = res
    return out


def model_result(part: str, run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {
            "run": run,
            "target": {r: t for t, r in RUNS[part].items()}.get(run),
            "status": "pending",
            "why": "no run here",
        }
    m = json.loads((src / "manifest.json").read_text())
    base: dict[str, Any] = {"run": run, "target": m["model"]["target"], "layers": m["layers"]}
    if not (src / "gate.json").exists():
        return {**base, "status": "pending", "why": "no gate.json yet"}
    gate = json.loads((src / "gate.json").read_text())
    base["gate"] = {k: v for k, v in gate.items() if k != "order"}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    if not rows:
        return {**base, "status": "pending" if gate.get("chosen") else "not tested", "why": "no outcome rows"}
    layers = {la: layer_result(part, [r for r in rows if r["layer"] == la], n_boot) for la in m["layers"]
              if any(r["layer"] == la for r in rows)}  # fmt: skip
    cases = X.read_jsonl(src / "cases.jsonl")
    chosen = {(s, sc) for s, sc in gate["order"]}
    status = "tested" if gate["pass"] else "not tested (gate; numbers descriptive only)"
    return {
        **base,
        "status": status,
        "layer_results": layers,
        "beside": beside(m["model"]["target"], part, [c for c in cases if (c["set"], c["scene"]) in chosen], n_boot),
    }


def fmt(v: list | None) -> str:
    if v is None or not ok(v[0]):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def view(part: str, run: str, decode=None, k: int = N_VIEW, seed: int = VIEW_SEED) -> list[str]:
    """The verify-pack view: k random chosen passages (seed, over the sorted chosen ones), each reader's O prompt as the
    model reads it with the patch token in ⟦…⟧, S's prompt with the same token marked, every arm's top token per layer."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    keys = sorted({(r["set"], r["scene"]) for r in rows})
    lines = [f"## {run} ({m['model']['target']}, L{m['layers']}): {min(k, len(keys))} random passages of {len(keys)} "
             f"(random.Random({seed}) over the sorted (set, scene) keys)", ""]  # fmt: skip
    for key in sorted(random.Random(seed).sample(keys, min(k, len(keys)))):
        c = cases[key]
        extra = f", {c['stratum']}" if part == "z1" else f"; {c['desc']!r} -> {c['cf_desc']!r}"
        lines += [
            f"### {key[1]} ({key[0]}): {c['bridge']} -> {c['cf_bridge']} ({c['answer']} -> {c['cf_answer']}){extra}",
            "",
        ]
        for w, rd in c["readers"].items():
            lines += [f"**{w}** ({rd['id']}): O's answer {rd['answer']}, S's {rd['cf_answer']}, lure {rd['lure']}", "",
                      "O, as read:", "", "```", mark(decode, rd["ids"]["org"], rd["pos"]), "```", "", "S (the source):",
                      "", "```", mark(decode, rd["ids"]["alt"], rd["pos"]), "```", "",
                      "| layer | arm | top token | route |", "|---|---|---|---|"]  # fmt: skip
            for r in rows:
                if (r["set"], r["scene"]) == key and r["reader"] == w:
                    lines.append(f"| {r['layer']} | {r['arm']} | {decode([r['top']])!r} | {r['route']} |")
            lines.append("")
    return lines


def figure(part: str, models: list[dict], path: Path) -> None:
    """Our gap (M minus K extra loss) and Zach's M - K knock-out on the same passages, per model (and layer)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels, ours, his = [], [], []
    for mm in models:
        for la, lr in mm.get("layer_results", {}).items():
            labels.append(f"{mm['target']}\nL{la}")
            ours.append(lr["gap"])
            his.append(mm["beside"].get("full", {}).get("paper10", {}).get("m_minus_k", [math.nan] * 3))
    fig, ax = plt.subplots(figsize=(max(4, 1.6 * len(labels)), 3.2))
    xs = np.arange(len(labels))
    for off, vals, name in (
        (-0.18, ours, "our gap (M - K extra loss)"),
        (0.18, his, "his M - K knock-out (J++ top-10)"),
    ):
        v = np.array([x[0] for x in vals], dtype=float)
        err = np.array([[x[0] - x[1], x[2] - x[0]] for x in vals], dtype=float).T if vals else None
        ax.bar(xs + off, v, 0.36, yerr=err, label=name, capsize=3)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(xs, labels, fontsize=8)
    ax.set_ylabel("share")
    ax.set_title(f"batch 50 {part.upper()}: our removal vs his knock-out, same passages (UNVERIFIED)", fontsize=9)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def stage_verdict(part: str, runs: list[str], n_boot: int = X.N_BOOT, decode=None) -> Path:
    answer = require_answer(part)
    models = [model_result(part, r, n_boot) for r in runs]
    out = RESULTS / f"{part}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = [f"# Batch 50 {part.upper()}: our change-removal on Zach's passages (UNVERIFIED)", "",
             f"{QUESTION[part]} (Dan: {answer}). Items: {SETS[0]} (and {SETS[1]} only if short), words {WORDS[part]}, "
             f"leak filter. Cluster bootstrap over the bridge entity ({n_boot}, seed {X.BOOT_SEED}).", "",
             f"Rule (fixed in advance): {RULE[part]}", "", f"As computed: {AS_COMPUTED}", "",
             "| model | run | status | layer | n (entities) | K extra loss | M extra loss | gap | verdict | K S_whole | "
             "M S_whole |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if "layer_results" not in mm:
            lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} ({mm.get('why', '')}) | | | | | | | | |")
            continue
        for la, lr in mm["layer_results"].items():
            lk, rc = lr["lookup"], lr["recall"]
            lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} | {la} | {lr['n']} ({lr['entities']}) | "
                         f"{fmt(lk['excess'])} | {fmt(rc['excess'])} | {fmt(lr['gap'])} | {lr['verdict']} | "
                         f"{fmt(lk['S_whole'])} | {fmt(rc['S_whole'])} |")  # fmt: skip
    for mm in models:
        if "layer_results" not in mm:
            continue
        g = mm["gate"]
        lines += ["", f"## {mm['target']} ({mm['run']})", "",
                  f"Gate: O's read accuracy {g['org_read_accuracy']} over {g['cases']} passages, pass {g['pass']}; over "
                  f"Zach's kept passages {g.get('over_zach_kept')}; eligible {g['eligible']}, chosen {g['chosen']} "
                  f"(sets {g.get('chosen_sets')}); counts {json.dumps(g.get('counts'))}.", ""]  # fmt: skip
        for la, lr in mm["layer_results"].items():
            lines.append(f"L{la}: routes {json.dumps(lr['routes'])}")
            if part == "z1":
                o = lr["order"]
                lines.append(f"L{la} order: fact-first {fmt(o['strata']['fact-first']['whole_switch'])} (n "
                             f"{o['strata']['fact-first']['n']}), fact-after {fmt(o['strata']['fact-after']['whole_switch'])} "
                             f"(n {o['strata']['fact-after']['n']}); ratio {o['ratio']:.2f}; replicates {o['replicates']}; "
                             f"intervals separate {o['separate']}. Hard-read: {lr['hard_read']}.")  # fmt: skip
        b = mm["beside"]
        lines += ["", f"Beside (Zach's stored rows, band {b['band']}): " + "; ".join(
            f"{kind} {v['run']}: " + ", ".join(f"{ctrl} M-K {fmt(v[ctrl]['m_minus_k'])} (joined {v[ctrl]['joined']})"
                                               for ctrl in ("paper10", "paper10_rot") if ctrl in v)
            for kind, v in b.items() if isinstance(v, dict)) + (f". {b['swap']}" if b.get("swap") else ""), ""]  # fmt: skip
    (out / f"{part}.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str) + "\n"
    )
    (out / f"{part}.md").write_text("\n".join(lines) + "\n")
    figure(part, models, out / f"{part}_beside.png")
    ex = [f"# Batch 50 {part.upper()} view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the patch token. "
          "UNVERIFIED.", ""]  # fmt: skip
    for mm in models:
        if "layer_results" in mm:
            ex += view(part, mm["run"], decode)
    (out / "view.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(part: str, runs: list[str], decode=None) -> Path:
    require_answer(part)
    out = RESULTS / f"{part}-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = [f"# Batch 50 {part.upper()} view (verify pack). UNVERIFIED.", ""]
    for run in runs:
        if (RESULTS / run / "outcomes.jsonl").exists():
            lines += view(part, run, decode)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--part", choices=PARTS)
    ap.add_argument("--name", help="run: the run name (results/x50_zach/<name>/)")
    ap.add_argument("--runs", nargs="+", help="verdict / view: the runs (default: the part's three)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--plan-dir", help="plan: the folder to write into (one per model, the same folder)")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.plan_dir)
        return
    assert a.part, f"{a.stage} needs --part"
    runs = a.runs or list(RUNS[a.part].values())
    if a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.part)
    elif a.stage == "view":
        stage_view(a.part, runs)
    else:
        stage_verdict(a.part, runs, a.n_boot)


if __name__ == "__main__":
    main()
