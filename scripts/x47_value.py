"""x47_value (batch 47, amendment 1, test 47.7; jobs/c3/batch47.yaml, rules fixed in advance; Q47.7 in
predictions/2026-10-28_dan.md): the value, address by default, prefetched on demand?

The model keeps an address at the bridge word, not the number, when the question comes last (the routes test: value 0
of 300 on four models). Three parts, each a sealed GPU run per model and a CPU verdict:

(a) question-first (`--part a`; 9B L12, 27B L32, Muse L26). The routes scenes (x6_routes.scenes, seed 2510, the same
    scene ids as the x6_routes runs: C2 another item moved with a new number, C0 the sanity swap), each reader's
    question BEFORE the context in the same user turn: user content "Question: <q> <the digit instruction>\\n\\n<context>",
    the chat template, the assistant turn prefilled "Answer:" (the template's prefill is the "\\n\\nAnswer:" of the design;
    question-last is x6_routes' prompt, "<context>\\n<q> <instruction>"). Same read (the top token after a digit's space).
    Dumbest way 1: the bridge is the same token (asserted: the same token id, the same offset from the context's first
    token, one token at one index in O and S); its absolute index moves by the question block's token count (recorded).
    With the question first the two readers' prompts differ before the bridge, so the change h_S - h_O is computed per
    reader from its own prompts (question-last: one change from the lookup's prompt, the readers' prefixes equal).
    Dumbest way 2: the digits are drawn independently of the slots (x6_routes' generator); asserted on the generated set
    by a permutation chi-square test (slot of the bridge's locker sentence vs its digit, p >= 0.01).
    Gate 0.80 per reader and condition on the question-first prompts (reported; below it: "not tested"). Eligible: both
    readers say and read O's and S's answers right in both renderings; the first 300 per condition.
    Reads: routes shares (identity / position / value) under every arm, question-first; the whole change question-last
    in the same run (the paired position difference); the value probe (x0_probe's (a): ridge, entities held out) on the
    lookup's O state at the bridge word, question-first vs question-last; the lens readout's rank of the answer digit
    among the 10 digit tokens at that state (X0's digit check), question-first vs question-last.
    Arms: whole; without J++ (signed OMP, k = 25, over the lens atoms of the letter tokens AND the digit tokens: the main
    test's letter-only restriction is lifted here); without a random part of its share; without U (x0_massmean's Alf of
    the x0_probe_v4 states, not refit); without a random part of its share.
    C0: the question-first lookup's switch rate against x6_routes' reference (within 0.10; Muse --c0-min 0.5), written to
    c0_check.json; the run does not stop (sealed), the verdict labels a failed model "C0 failed".
(c) other formats (`--part c`; question-last; 9B, 27B, Muse). The varied scenes (tasks_v2 x0b_v2, x0b_generalize's
    aligned cases; prose / JSON / table), locker-first (the bridge's locker statement before the pick), with "another
    item moved" counterfactuals: the asked pick x -> t (x0b's alt candidate: another person's pick with a different
    locker and memory number), t's locker statement trades places with a third locker item u's (both before the pick;
    seeded choice), t's number replaced by e, a number not in the scene; identity -> locker(t), position -> locker(u),
    value -> e, original -> locker(x), the four distinct. Both number styles (digits and words; the answers are read as
    digits as in x0b). 9B and Muse: the held-out half of 45d's split only (x7_pcf/<model>_x45d_fit/split.json), with
    the per-format refit pointer (pcf_<format>.npz, rank 4) removed vs a random part of its share; the 27B has no refit
    basis (none fit on it in 45d) and runs whole / J++ / U only. Gate 0.80 per reader and format; at most 300 per format.
(b) word-valued lockers (`--part b`; 9B, Muse; cut first if late). The routes scenes with single-token colours as the
    locker values (red, blue, green, pink, gold, grey, teal, navy; checked single-token with a leading space on the
    model's tokenizer, a failing colour dropped and reported), the lookup read as a word (right after "Answer:", no
    space token), the recall as a digit; question-last and question-first, arms as (a) on both; the probe and the lens
    rank (among the colour tokens) as (a).

Verdict (CPU, `verdict --part a|c|b`): refuses until predictions/2026-10-28_dan.md holds Dan's Q47.7 answer at HEAD.
Cluster bootstrap over bridge items, 10,000 resamples, seed 0; a value at a bar counts as at the bar (EPS 1e-9).
(a) per model: "prefetch on demand" if the question-first C2 value share >= 0.15 and the value probe >= 0.6 (the rule's
    premise, question-last value <= 0.05 and probe <= 0.4, is checked and reported); "the prefetched value is in the
    J-space" (read only where prefetch holds) if the value share falls >= 0.3 beyond the random part without J++ and
    the lens ranks the digit first in >= 0.4 of items question-first; "address regardless" if the value share <= 0.05
    and the probe within 0.1 of question-last. Over the models: a label holds on >= 2 of 3 (the J-space label only
    where prefetch holds). Beside it: position share question-first minus question-last (paired, with its interval).
(c) "never the value generalizes" if value <= 0.05 in every format on every model (every cell tested); "a position route
    in JSON / table" per cell if the position share >= 0.2 and the refit pointer's removal cuts it >= 0.3 beyond random.
(b) as (a) on the colour value, per rendering; a value route "appears" question-last if its share >= 0.15 (then: does
    the J++ part carry it, without-J++ cutting value answers >= 0.3 beyond random); "never the value holds for a word
    value too" if the question-last value share <= 0.05 on every tested model.

uv run python scripts/x47_value.py plan --part a                                  # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_value.py run --part a --name qwen35_9b_x47_7a   # GPU (sealed)
uv run python scripts/x47_value.py verdict --part a --runs qwen35_9b_x47_7a x47_7a_27b muse30_x47_7a   # CPU
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
from scripts import x6_routes as R

EXP = "x47_value"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS, QUESTION = "predictions/2026-10-28_dan.md", "Q47.7"
PARTS = ("a", "c", "b")
RENDERINGS = ("ql", "qf")  # question-last (x6_routes' prompt), question-first
CONDS = ("C0", "C2")
COLOURS = ("red", "blue", "green", "pink", "gold", "grey", "teal", "navy")
DIGITS = tuple(str(d) for d in range(1, 10))
ROUTES = R.ROUTES
ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand")
ARMS_PCF = ("no_pcf", "no_pcf_rand")
REMOVED = {"jpp": ("no_jpp", "no_jpp_rand"), "alf": ("no_alf", "no_alf_rand"), "pcf": ("no_pcf", "no_pcf_rand")}
# which renderings carry which arms per part (the others carry the whole change only, for the paired comparison)
ARM_RENDERINGS = {"a": {"qf": ARMS, "ql": ("whole",)}, "b": {"qf": ARMS, "ql": ARMS}, "c": {"ql": (*ARMS, *ARMS_PCF)}}
# (c): the refit-pointer arms run only where a 45d basis exists (PCF_FIT); a model without one reads ARMS alone
GATE_RENDERINGS = {"a": ("qf",), "b": ("ql", "qf"), "c": ("ql",)}
N_GEN, N_ITEMS, CAP_FORMAT = R.N_GEN, R.N_ITEMS, 300
SET_C, FORMATS = "x0b_v2", ("prose", "json", "table")
INDEP_SEED, INDEP_PERMS, INDEP_P = 4707, 2000, 0.01  # dumbest way 2: slot vs digit, permutation chi-square
MOVE_SEED = 4708  # (c): the third item u and the new number e per scene
PCF_FIT = {"qwen3.5-9b": "x7_pcf/qwen35_9b_x45d_fit", "muse-glimmer-30b": "x7_pcf/muse30b_x45d_fit"}
RUNS = {"a": {"qwen3.5-9b": "qwen35_9b_x47_7a", "qwen3.6-27b": "x47_7a_27b", "muse-glimmer-30b": "muse30_x47_7a"},
        "c": {"qwen3.5-9b": "qwen35_9b_x47_7c", "qwen3.6-27b": "x47_7c_27b", "muse-glimmer-30b": "muse30_x47_7c"},
        "b": {"qwen3.5-9b": "qwen35_9b_x47_7b", "muse-glimmer-30b": "muse30_x47_7b"}}  # fmt: skip
# the bars (jobs/c3/batch47.yaml, 47.7, fixed in advance)
PREFETCH_VALUE, PREFETCH_PROBE, QL_VALUE, QL_PROBE = 0.15, 0.6, 0.05, 0.4
JSPACE_FALL, JSPACE_LENS = 0.3, 0.4
ADDRESS_VALUE, ADDRESS_NEAR = 0.05, 0.1
MODELS_MIN = 2
C_VALUE, C_POSITION, C_CUT = 0.05, 0.2, 0.3
B_APPEARS, B_NEVER, B_CUT = 0.15, 0.05, 0.3
EPS = 1e-9
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
RULE = {
    "a": "prefetch on demand: question-first value share >= 0.15 and the value probe >= 0.6 (question-last <= 0.05 / "
         "<= 0.4), on >= 2 of 3 models; the prefetched value is in the J-space (read only if prefetch holds): without J++ "
         "(digits allowed) value answers fall >= 0.3 beyond random and the lens ranks the digit first in >= 0.4 of items; "
         "address regardless: value share <= 0.05 and the probe within 0.1 of question-last",
    "c": "never the value generalizes if value <= 0.05 in every format on every model; a position route in JSON / table "
         "if the position share >= 0.2 and the refit pointer's removal cuts it >= 0.3 beyond random",
    "b": "as (a); if a value route appears, does the J++ part carry it (without-J++ cuts value answers >= 0.3 beyond "
         "random)? if no value appears question-last, never the value holds for a word value too",
}  # fmt: skip


# ---- prompts (tokenizer only) -------------------------------------------------------------------------------------


def instruction(kind: str) -> str:
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    return T.DIGIT_INSTRUCTION if kind == "digit" else S.INSTRUCTION


def user_content(question: str, context: str, kind: str, rendering: str) -> str:
    """The user turn: question-last as tasks_v2 renders the routes items; question-first with the question block (the
    question and its instruction) before the context."""
    assert rendering in RENDERINGS, rendering
    instr = instruction(kind)
    return f"{context}\n{question} {instr}" if rendering == "ql" else f"Question: {question} {instr}\n\n{context}"


def render(tok, question: str, context: str, kind: str, rendering: str) -> str:
    from bridge_jspace import chat

    return chat.chat_text(tok, user_content(question, context, kind, rendering), "chat")


def space_of(tok, kind: str) -> list[int]:
    """The read's appended token: a digit's space (X0's chat read); nothing for a word answer (read right after
    'Answer:', the answer's token carrying its own space, as suite_v1)."""
    from scripts import suite_v1 as S

    return S.ids(tok, " ") if kind == "digit" else []


def encode_prompt(tok, text: str, context: str, w0: int, word: str) -> tuple[list[int], list[int], int]:
    """The prompt's ids, the token positions overlapping `word` at character offset w0 of the context, and the position
    of the context's first token."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    assert text.count(context) == 1, "the context is not once in the prompt"
    enc = raw_encoding(tok, text, offsets=True)
    start = text.index(context)
    at = SP.tokens_in(enc["offset_mapping"], start + w0, start + w0 + len(word))
    first = SP.tokens_in(enc["offset_mapping"], start, start + 1)
    return list(enc["input_ids"]), at, first[0]


def encode_reader(tok, question: str, kind: str, o: str, s: str, w0: tuple[int, int], words: tuple[str, str],
                  renderings: tuple[str, ...]) -> dict | str:  # fmt: skip
    """One reader's O and S prompts in each rendering: ids, the bridge's position (one token at one index shared by O
    and S) and the context's first token; the reason (str) when a rendering fails. Across renderings (dumbest way 1):
    the same token at the same offset from the context's first token, every context token up to the bridge equal."""
    out: dict[str, Any] = {"ids": {}, "pos": {}, "ctx0": {}}
    for r in renderings:
        ids_o, at_o, c_o = encode_prompt(tok, render(tok, question, o, kind, r), o, w0[0], words[0])
        ids_s, at_s, c_s = encode_prompt(tok, render(tok, question, s, kind, r), s, w0[1], words[1])
        if len(at_o) != 1 or at_o != at_s or c_o != c_s:
            return f"{r}: the bridge is not one token at the same index in O and S"
        out["ids"][r], out["pos"][r], out["ctx0"][r] = {"org": ids_o, "alt": ids_s}, at_o[0], c_o
    if set(renderings) >= set(RENDERINGS):
        pq, pl, cq, cl = out["pos"]["qf"], out["pos"]["ql"], out["ctx0"]["qf"], out["ctx0"]["ql"]
        # from the context's second token on (its first may carry the preceding newline in byte-level BPE)
        if pq - cq != pl - cl or out["ids"]["qf"]["org"][cq + 1 : pq + 1] != out["ids"]["ql"]["org"][cl + 1 : pl + 1]:
            return "the bridge token moves within the context between the renderings"
        out["shift"] = pq - pl
    return out


def said_of(text: str, kind: str) -> str | None:
    """What the greedy reply says: suite_v1's digit judge, or the first colour word of the first non-empty line."""
    from scripts import suite_v1 as S

    if kind == "digit":
        return S.said(text, "digit")
    return next((w for w in re.findall(r"[a-z]+", S.first_line(text)) if w in COLOURS), None)


# ---- routes scenes with digit or colour values ((a), (b)) ---------------------------------------------------------


def scenes(tok, n: int, kind: str = "digit", seed: int = R.SEED, renderings: tuple[str, ...] = RENDERINGS,
           conds: tuple[str, ...] = CONDS, pool: tuple[str, ...] | None = None) -> tuple[list[dict], collections.Counter]:  # fmt: skip
    """x6_routes.scenes' draws exactly (seed, the same scene ids, so the items pair with the x6_routes runs), the
    values digits (as there) or colours from `pool` (default COLOURS), C0 and C2 only, each reader encoded in every
    rendering (encode_reader); drops counted by reason."""
    from scripts import suite_v1 as S

    legs, animals, people = R.pools(tok)
    pool = pool or (DIGITS if kind == "digit" else COLOURS)
    rng = random.Random(seed)
    out, dropped = [], collections.Counter()
    i = 0
    while len(out) < n * len(conds):
        i += 1
        assert i < 100 * n, f"the generator cannot fill {n} scenes per condition: {dropped}"
        A, B, C = rng.sample(animals, 3)
        if legs[A] == legs[B]:
            dropped["A and B have the same number of legs"] += 1
            continue
        # five values as x6_routes draws them (its fourth, C1's new digit, is drawn and unused here, keeping the stream)
        a, b, c, _, e = (str(v) for v in rng.sample(range(1, 10), 5)) if kind == "digit" else rng.sample(pool, 5)
        asked, p1, p2 = rng.sample(people, 3)
        order = rng.sample([A, B, C], 3)
        val = {A: a, B: b, C: c}
        picks = rng.sample([(asked, A), (p1, B), (p2, C)], 3)
        o = R.context([(x, val[x]) for x in order], picks)  # pyright: ignore[reportArgumentType]  (values as str)
        for cond in R.CONDITIONS:  # x6_routes' order; C1 is not built here
            if cond not in conds:
                continue
            if cond == "C0":
                s_lock = [(x, val[x]) for x in order]
                s_pick, bridge = [(q, B if q == asked else x) for q, x in picks], B
                expect = {"switch": b, "original": a}
            else:
                sw = {B: C, C: B}
                s_lock = [(sw.get(x, x), e if sw.get(x, x) == B else val[sw.get(x, x)]) for x in order]
                s_pick, bridge = [(q, B if q == asked else x) for q, x in picks], B
                expect = {"identity": b, "position": c, "value": e, "original": a}
            s = R.context(s_lock, s_pick)  # pyright: ignore[reportArgumentType]
            s_answer = expect["switch"] if cond == "C0" else expect["value"]
            readers, why = {}, ""
            for w, q, ans, k in ((X.LOOKUP, R.LOOKUP_Q, (a, s_answer), kind),
                                 (X.RECALL, R.RECALL_Q, (str(legs[A]), str(legs[bridge])), "digit")):  # fmt: skip
                sent_o, sent_s = f"{asked} picked the {A}.", f"{asked} picked the {bridge}."
                enc = encode_reader(tok, q.format(p=asked), k, o, s, (o.index(sent_o) + sent_o.index(A),
                                    s.index(sent_s) + sent_s.index(bridge)), (A, bridge), renderings)  # fmt: skip
                if isinstance(enc, str):
                    why = enc
                    break
                readers[w] = {"question": q.format(p=asked), "kind": k, "answer": ans[0], "cf_answer": ans[1],
                              "tok_A": S.answer_token(tok, ans[0], k), "tok_b": S.answer_token(tok, ans[1], k),
                              "space": space_of(tok, k), **enc}  # fmt: skip
            if not why and "ql" in renderings:
                lk, rc = readers[X.LOOKUP], readers[X.RECALL]
                pos = lk["pos"]["ql"]
                if rc["pos"]["ql"] != pos or any(lk["ids"]["ql"][v][: pos + 1] != rc["ids"]["ql"][v][: pos + 1]
                                                 for v in ("org", "alt")):  # fmt: skip
                    why = "the readers' question-last prompts differ before the bridge"
            if why:
                dropped[f"{cond}: {why}"] += 1
            elif sum(c_["condition"] == cond for c_ in out) < n:
                out.append({"scene": f"{cond}-{i:04d}", "condition": cond, "kind": kind, "format": "prose",
                            "bridge": A, "cf_bridge": bridge, "context": o, "cf_context": s,
                            "slot": order.index(A), "cf_slot": [x for x, _ in s_lock].index(bridge),
                            "expect": {k_: v for k_, v in expect.items() if k_ != "switch"},
                            "route_tokens": {k_: S.answer_token(tok, v, kind) for k_, v in expect.items() if k_ != "switch"},
                            "renderings": list(renderings), "readers": readers})  # fmt: skip
    return out, dropped


def classify(top: int, case: dict) -> str:
    hit = [rt for rt in ("identity", "position", "value", "original") if case["route_tokens"].get(rt) == top]
    return hit[0] if hit else "other"


def independence(pairs: list[tuple[Any, Any]], n_perm: int = INDEP_PERMS, seed: int = INDEP_SEED) -> dict:
    """Dumbest way 2: a permutation chi-square test of independence between the two labels of each pair (the bridge's
    locker slot and its value), p = (1 + #permuted chi2 >= observed) / (1 + n_perm); Cramer's V beside it."""
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    ka, kb = sorted(set(a), key=str), sorted(set(b), key=str)
    ia, ib = np.array([ka.index(v) for v in a]), np.array([kb.index(v) for v in b])

    def chi2(y: np.ndarray) -> float:
        t = np.zeros((len(ka), len(kb)))
        np.add.at(t, (ia, y), 1)
        exp = np.outer(t.sum(1), t.sum(0)) / t.sum()
        return float(((t - exp) ** 2 / np.where(exp > 0, exp, 1)).sum())

    obs = chi2(ib)
    rng = np.random.default_rng(seed)
    null = np.array([chi2(rng.permutation(ib)) for _ in range(n_perm)])
    p = float((1 + (null >= obs - 1e-12).sum()) / (1 + n_perm))
    table = np.zeros((len(ka), len(kb)), dtype=int)
    np.add.at(table, (ia, ib), 1)
    v = math.sqrt(obs / (len(a) * max(1, min(len(ka), len(kb)) - 1))) if len(a) else float("nan")
    return {"n": len(a), "chi2": round(obs, 3), "df": (len(ka) - 1) * (len(kb) - 1), "p": p, "cramers_v": round(v, 4),
            "rows": [str(x) for x in ka], "cols": [str(x) for x in kb], "table": table.tolist(),
            "independent": p >= INDEP_P}  # fmt: skip


def colour_pool(tok) -> tuple[list[str], list[str]]:
    """The colours that are one token with a leading space on this tokenizer, and those that are not (dropped)."""
    ok = [c for c in COLOURS if R.one_token(tok, c)]
    return ok, [c for c in COLOURS if c not in ok]


# ---- (c): the varied scenes with another item moved ---------------------------------------------------------------


def moved_context(item: dict, t: str, u: str, e: int) -> str:
    """The varied scene's S: t's and u's locker statements trade places (x7_pcf.swap_lockers), t's number becomes e,
    and the asked pick x becomes t (x0b_generalize.alt_context); nothing else changes."""
    from scripts import x0b_generalize as B
    from scripts import x7_pcf as PC

    ctx = PC.swap_lockers(item, t, u)
    old = PC.locker_statement(item, t)
    new = PC.locker_statement({**item, "facts": {**item["facts"], "locker": {**item["facts"]["locker"], t: e}}}, t)
    assert ctx.count(old) == 1, f"{item.get('id')}: {old!r} is not once after the swap"
    return B.alt_context({**item, "context": ctx.replace(old, new)}, t)


def moved_case(tok, pp: dict, pm: dict, rng: random.Random) -> tuple[dict | None, str]:
    """One varied scene's case (both readers, question-last) with another item moved, or the reason it is dropped:
    locker-first; t = the first alt candidate (x0b) whose locker statement is before the pick and for which a third
    locker item u before the pick with a number different from x's and t's exists (u and the new number e seeded from
    rng); the bridge one token at one index in O and S, O and S equal from the bridge on."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T
    from scripts import x0b_generalize as B
    from scripts import x7_pcf as PC

    f = pp["facts"]
    x, locker = f["x"], f["locker"]
    if B.order_of(pp) != "before":
        return None, "the bridge's locker statement comes after the pick"
    cands = [t for t in B.alt_candidates(pp, pm) if PC.before_pick(pp, t)]
    if not cands:
        return None, "no other pick with a different locker and memory number before the pick"
    free = [n for n in range(1, 10) if n not in set(locker.values())]
    if not free:
        return None, "no new number left"
    values = T.DOMAINS[pp["domain"]].values
    why = "no alt aligns"
    for t in cands:
        others = sorted(u for u in locker if u not in (x, t) and PC.before_pick(pp, u)
                        and locker[u] not in (locker[x], locker[t]))  # fmt: skip
        if not others:
            why = "no third locker item before the pick with a distinct number"
            continue
        u, e = rng.choice(others), rng.choice(free)
        s_ctx = moved_context(pp, t, u, e)
        expect = {"identity": str(locker[t]), "position": str(locker[u]), "value": str(e), "original": str(locker[x])}
        assert len(set(expect.values())) == 4, expect
        readers, pos = {}, None
        for w, it, ans in (
            (X.LOOKUP, pp, (pp["answer"], str(locker[t]))),
            (X.RECALL, pm, (pm["answer"], str(values[t]))),
        ):
            ids_o, at_o = B.encode(tok, it, it["context"], x)
            ids_s, at_s = B.encode(tok, it, s_ctx, t)
            if len(at_o) != 1 or at_s != at_o:
                why = "the bridge is not one token at the same index in O and S (a number word's token count changes)"
                break
            if ids_s[at_o[0] + 1 :] != ids_o[at_o[0] + 1 :]:
                why = "S differs from O after the bridge"
                break
            tok_a, tok_b = (S.answer_token(tok, v, "digit") for v in ans)
            if tok_a == tok_b:
                why = "the org and alt answers share their first token"
                break
            pos = at_o[0]
            readers[w] = {"id": it["id"], "question": it["question"], "kind": "digit", "answer": ans[0],
                          "cf_answer": ans[1], "tok_A": tok_a, "tok_b": tok_b, "space": space_of(tok, "digit"),
                          "ids": {"ql": {"org": ids_o, "alt": ids_s}}, "pos": {"ql": pos}}  # fmt: skip
        if len(readers) < 2 or pos is None:
            continue
        if any(readers[X.LOOKUP]["ids"]["ql"][v][: pos + 1] != readers[X.RECALL]["ids"]["ql"][v][: pos + 1]
               for v in ("org", "alt")):  # fmt: skip
            why = "the readers' prompts differ before the bridge"
            continue
        o = B.ordinals(pp)
        return {"scene": pp["scene"], "condition": "C2", "kind": "digit", "format": pp["format"], "level": pp.get("level"),
                "domain": pp["domain"], "numbers": pp["numbers"], "bridge": x, "cf_bridge": t, "third": u,
                "context": pp["context"], "cf_context": s_ctx, "slot": o["locker_index"], "expect": expect,
                "route_tokens": {k: S.answer_token(tok, v, "digit") for k, v in expect.items()},
                "renderings": ["ql"], "readers": readers}, ""  # fmt: skip
    return None, why


def varied_cases(
    tok, set_name: str = SET_C, pcf_from: str | None = None, seed: int = MOVE_SEED
) -> tuple[list[dict], dict]:
    """(c)'s cases over the set's scenes (both readers present, the same context); with pcf_from (45d's fit run), the
    held-out half per format only (x0b_generalize.held_out)."""
    from scripts import tasks_v2 as T
    from scripts import x0b_generalize as B

    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in X.READERS:
            by_scene[it["scene"]][it["word"]] = it
    cases, dropped = [], collections.Counter()
    for scene in sorted(by_scene):
        pair = by_scene[scene]
        if set(pair) != set(X.READERS) or pair[X.LOOKUP]["context"] != pair[X.RECALL]["context"]:
            dropped["the readers' scenes differ or a reader is missing"] += 1
            continue
        c, why = moved_case(tok, pair[X.LOOKUP], pair[X.RECALL], random.Random(f"{seed}|{scene}"))
        if c is None:
            dropped[f"{pair[X.LOOKUP]['format']}: {why}"] += 1
        else:
            cases.append(c)
    counts: dict[str, Any] = {"set": set_name, "scenes": len(by_scene), "cases": len(cases),
                              "dropped": dict(sorted(dropped.items())), "pcf_from": pcf_from}  # fmt: skip
    if pcf_from:
        split = json.loads((pins.RESULTS_DIR / pcf_from / "split.json").read_text())
        assert split["set"] == set_name, f"{pcf_from}: fit on set {split['set']}, not {set_name}"
        cases = B.held_out(cases, split)
        counts["held_out_cases"] = len(cases)
    counts["per_format"] = dict(collections.Counter(c["format"] for c in cases))
    counts["per_numbers"] = dict(collections.Counter(c["numbers"] for c in cases))
    return cases, counts


# ---- the plan (tokenizer only) ------------------------------------------------------------------------------------


def build(part: str, tok, target: str | None = None) -> tuple[list[dict], dict]:
    """The part's cases on this tokenizer and the plan's counts (drops, dumbest ways 1 and 2, the colour pool)."""
    target = target or pins.TARGET
    if part == "c":
        return varied_cases(tok, SET_C, PCF_FIT.get(target))
    pool = None
    counts: dict[str, Any] = {}
    if part == "b":
        ok, bad = colour_pool(tok)
        counts["colours"] = {"single_token": ok, "dropped": bad}
        assert len(ok) >= 5, f"fewer than 5 single-token colours on this tokenizer: {ok}"
        pool = tuple(ok)
    cases, dropped = scenes(tok, N_GEN, "digit" if part == "a" else "colour", pool=pool)
    base = {c["context"]: c for c in cases}  # one O per base scene (C0 and C2 share it)
    counts.update({"cases": dict(collections.Counter(c["condition"] for c in cases)), "dropped": dict(dropped),
                   "slot_value_independence_O": independence([(c["slot"], c["readers"][X.LOOKUP]["answer"])
                                                              for c in base.values()]),
                   "slot_value_independence_S_C2": independence([(c["cf_slot"], c["expect"]["value"])
                                                                 for c in cases if c["condition"] == "C2"]),
                   "bridge_shift_qf_minus_ql": {READER_NAME[w]: dict(collections.Counter(c["readers"][w]["shift"]
                                                                                        for c in cases))
                                                for w in X.READERS}})  # fmt: skip
    for key in ("slot_value_independence_O", "slot_value_independence_S_C2"):
        assert counts[key]["independent"], f"{key}: p = {counts[key]['p']} < {INDEP_P}"
    return cases, counts


def marked_prompt(decode, ids: list[int], pos: int, space: list[int]) -> str:
    """The prompt as the model reads it (the read's appended token included), the bridge token in ⟦...⟧."""
    return R.marked(decode, ids + space, pos)


def sample_prompts(cases: list[dict], decode, k: int = 5, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random C2 cases (seed): the lookup's prompt in every rendering and the recall's question-first, marked."""
    c2 = [c for c in cases if c["condition"] == "C2"] or cases
    lines = []
    for c in random.Random(seed).sample(c2, min(k, len(c2))):
        lines += [f"## {c['scene']} ({c.get('format', 'prose')}): bridge {c['bridge']} -> {c['cf_bridge']}; expected "
                  f"{c['expect']}"]  # fmt: skip
        for w, rd in c["readers"].items():
            for r in rd["ids"]:
                if w == X.RECALL and r == "ql":
                    continue
                lines += [f"**{READER_NAME[w]}, {r}** (O answers {rd['answer']}, S answers {rd['cf_answer']}; bridge token "
                          f"{rd['pos'][r]}" + (f", shift {rd['shift']}" if "shift" in rd else "") + "):", "```",
                          marked_prompt(decode, rd["ids"][r]["org"], rd["pos"][r], rd["space"]), "```"]  # fmt: skip
        lines.append("")
    return lines


def stage_plan(part: str) -> dict:
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    cases, counts = build(part, tok)
    counts["target"] = pins.TARGET
    print(json.dumps(counts, indent=1, ensure_ascii=False))
    print("\n".join(sample_prompts(cases, lambda ids: tok.decode([int(t) for t in ids]))))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def competence(model, cases: list[dict], ws) -> list[dict]:
    """Unedited O and S prompts of both readers in every rendering: 8 greedy tokens (what the model says, judged by
    said_of), the decisive read (the top token at the read step)."""
    import torch

    from bridge_jspace.utils import progress

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (case)"):
            for w, rd in c["readers"].items():
                for r in rd["ids"]:
                    ids = torch.tensor([rd["ids"][r]["org"], rd["ids"][r]["alt"]], device="cuda")
                    texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                    for i, (v, gold, tok_gold) in enumerate(
                        (("org", rd["answer"], rd["tok_A"]), ("alt", rd["cf_answer"], rd["tok_b"]))
                    ):
                        logits, _ = X.read_logits(model, rd["ids"][r][v], [{}], "chat", rd["space"], ws)
                        said = said_of(texts[i], rd["kind"])
                        rows.append({"scene": c["scene"], "reader": w, "rendering": r, "variant": v, "greedy": texts[i],
                                     "said": said, "right": said == gold, "read_right": int(logits[0].argmax()) == tok_gold})  # fmt: skip
    return rows


def stored_ql_competence(cases: list[dict], run: str) -> list[dict] | None:
    """(a): the x6_routes run's competence rows for the question-last prompts, which are this run's exactly (the same
    generator, seed and tokenizer; every case's ids and bridge position asserted equal to the stored case's); None
    when the run is not here, then the prompts are read afresh."""
    src = R.RESULTS / run
    if not (src / "competence.jsonl").exists() or not (src / "cases.jsonl").exists():
        return None
    stored = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    for c in cases:
        s = stored.get(c["scene"])
        assert s is not None, f"{run}: no stored case {c['scene']}"
        for w in X.READERS:
            assert c["readers"][w]["ids"]["ql"] == s["readers"][w]["ids"], (
                f"{run} {c['scene']} {w}: the stored ids differ"
            )
            assert c["readers"][w]["pos"]["ql"] == s["pos"], f"{run} {c['scene']}: the stored bridge position differs"
    want = {c["scene"] for c in cases}
    rows = [{**r, "rendering": "ql"} for r in X.read_jsonl(src / "competence.jsonl")
            if r["scene"] in want and r["rendering"] == "chat"]  # fmt: skip
    assert len(rows) == 4 * len(cases), f"{run}: {len(rows)} stored competence rows for {len(cases)} cases"
    return rows


ROUTES_RUN = {
    "qwen3.5-9b": "qwen35_9b_x6_routes",
    "qwen3.6-27b": "x6_routes_27b",
    "muse-glimmer-30b": "muse30b_x6_routes",
}


def group_of(part: str, c: dict) -> str:
    return c["format"] if part == "c" else c["condition"]


def gate_cases(part: str, cases: list[dict], comp: list[dict], gate_min: float = X.GATE) -> tuple[dict, list[dict]]:
    """Per group (condition, or format for (c)) and rendering: O's read accuracy per reader; the gate (>= gate_min for
    both readers in the part's gate renderings); eligible: both readers say and read O and S right in every rendering;
    chosen: the first N per group (scene order) of the groups that pass."""
    right = {(r["scene"], r["reader"], r["rendering"], r["variant"]): r for r in comp}
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for c in cases:
        groups[group_of(part, c)].append(c)
    n_max = CAP_FORMAT if part == "c" else N_ITEMS
    gate, chosen = {}, []
    for g, mine in sorted(groups.items()):
        rends = mine[0]["renderings"]
        acc = {r: {w: float(np.mean([right[(c["scene"], w, r, "org")]["read_right"] for c in mine])) for w in X.READERS}
               for r in rends}  # fmt: skip
        ok = [c for c in mine if all(right[(c["scene"], w, r, v)]["right"] and right[(c["scene"], w, r, v)]["read_right"]
                                     for w in X.READERS for r in rends for v in ("org", "alt"))]  # fmt: skip
        passed = all(acc[r][w] >= gate_min for r in GATE_RENDERINGS[part] for w in X.READERS)
        gate[g] = {"cases": len(mine), "org_read_accuracy": acc, "gate_renderings": list(GATE_RENDERINGS[part]),
                   "pass": passed, "eligible": len(ok), "used": min(len(ok), n_max) if passed else 0}  # fmt: skip
        chosen += ok[:n_max] if passed else []
    return gate, chosen


def value_tokens(tok, kind: str, pool: tuple[str, ...]) -> list[int]:
    from scripts import suite_v1 as S

    return [S.answer_token(tok, v, kind) for v in pool]


def stage_run(part: str, name: str, why: str, c0_min: float | None = None) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    assert part in PARTS, part
    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.7 renders chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS[part], f"47.7({part}) runs on {sorted(RUNS[part])}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    pcf_from = PCF_FIT.get(target) if part == "c" else None
    arm_rends = ARM_RENDERINGS[part]
    m = {"exp": EXP, "run": name, "part": part, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": f"47.7({part})",
         "spec": "jobs/c3/batch47.yaml (47.7, amendment 1)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)}, "layer": layer, "k": X.K_MAIN, "omp": "signed",
         "dictionary": "J++ lens atoms of the letter tokens and the digit tokens (the main test's letter-only restriction lifted)",
         "arms": {r: list(a) for r, a in arm_rends.items()}, "gate": X.GATE, "gate_renderings": list(GATE_RENDERINGS[part]),
         "n_per_group": CAP_FORMAT if part == "c" else N_ITEMS, "alf_from": R.STATES[target], "pcf_from": pcf_from,
         "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at each part's share of ||change||^2",
         "change": "h_S - h_O at the bridge word at L; question-first: per reader from its own prompts; question-last: from "
                   "the lookup's prompt (the readers' prefixes equal), read by both",
         "read": "the top token at the read step (a digit's space token appended; a word answer read right after 'Answer:')",
         "probe_states": "the lookup's O state at the bridge word per rendering (states.npz; x0_probe's (a) at the verdict)",
         "readout": "the lens vectors (unit=False) of the value pool's tokens at that state: the rank of O's answer",
         "c0": {"reference": R.c0_reference(target), "tolerance": R.C0_TOL, "c0_min": c0_min,
                "stop": "recorded in c0_check.json, the run does not stop (sealed); the verdict labels a failed model"},
         "rule": RULE[part], "seeds": {"scenes": R.SEED, "independence": INDEP_SEED, "move": MOVE_SEED,
                                       "random_subspace": f"{X.SUBSPACE_SEED} + layer", "bootstrap": X.BOOT_SEED,
                                       "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    cases, counts = build(part, tok, target)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in counts.items() if "independence" not in k}, ensure_ascii=False), flush=True)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    stored = stored_ql_competence(cases, ROUTES_RUN[target]) if part == "a" else None
    if stored is None:
        comp = competence(model, cases, ws)
    else:  # (a): the question-last prompts are x6_routes' own; only the question-first prompts are read afresh
        m["ql_competence_from"] = ROUTES_RUN[target]
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        comp = stored + competence(
            model,
            [
                {**c, "readers": {w: {**rd, "ids": {"qf": rd["ids"]["qf"]}} for w, rd in c["readers"].items()}}
                for c in cases
            ],
            ws,
        )
    gate, chosen = gate_cases(part, cases, comp)
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    (out / "gate.json").write_text(json.dumps({"gate": gate, "chosen": len(chosen)}, indent=2) + "\n")
    print(json.dumps(gate), flush=True)
    if not chosen:
        raise SystemExit("no group passed the gate fixed in advance (or none had eligible items); see gate.json")
    kind = chosen[0]["kind"]
    pool = DIGITS if kind == "digit" else tuple(counts["colours"]["single_token"])
    vt = torch.tensor(value_tokens(tok, kind, pool), device="cuda")
    lens = JLens(model, "jpp")
    allowed = torch.unique(torch.cat([model.letter_token_ids(), digits]))
    jdic = lens.vectors(layer, allowed)
    vvec = lens.vectors(
        layer, vt, unit=False
    )  # [pool, d]: the lens's logits of the value tokens, up to the norm's gain
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device="cuda")
    pcf = {f: torch.tensor(np.load(pins.RESULTS_DIR / pcf_from / f"pcf_{f}.npz")["P"], dtype=torch.float32, device="cuda")
           for f in FORMATS} if pcf_from else {}  # fmt: skip
    basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
    examples = set(sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(chosen)), min(X.K_EXAMPLES, len(chosen)))))
    keys: list[tuple[int, str, str]] = []  # (item index, rendering, reader) of each change
    deltas, states, readout = [], [], []
    with torch.no_grad():
        for i, c in enumerate(progress(chosen, f"changes at layer {layer} (case)")):
            for r in c["renderings"]:
                h: dict[str, dict] = {}
                for w in X.READERS:
                    rd = c["readers"][w]
                    if r == "ql" and w == X.RECALL:
                        h[w] = h[X.LOOKUP]  # the same prefix: the same change
                    else:
                        h[w] = {v: model.run(torch.tensor([rd["ids"][r][v]], device="cuda"), record=(layer,))[1][layer][rd["pos"][r]].float()
                                for v in ("org", "alt")}  # fmt: skip
                    if r in arm_rends:
                        keys.append((i, r, w))
                        deltas.append((h[w]["alt"] - h[w]["org"]).to("cuda"))
                ho = h[X.LOOKUP]["org"].to("cuda")
                states.append((i, r, ho.cpu().numpy()))
                score = vvec @ ho
                order = [pool[j] for j in score.argsort(descending=True).tolist()]
                ans = c["readers"][X.LOOKUP]["answer"]
                readout.append({"scene": c["scene"], "condition": c["condition"], "rendering": r, "entity": c["bridge"],
                                "answer": ans, "rank": order.index(ans) + 1, "top": order[0], "n_candidates": len(pool),
                                "rank_cf_value": order.index(c["expect"].get("value", c["expect"].get("identity"))) + 1})  # fmt: skip
        x = torch.stack(deltas)
        jpp = X.fit(jdic, x, X.K_MAIN, "signed")
        ptr = (x @ alf) @ alf.T
        parts = {"jpp": jpp, "alf": ptr}
        if pcf:
            parts["pcf"] = torch.stack([(x[j] @ pcf[chosen[i]["format"]]) @ pcf[chosen[i]["format"]].T
                                        for j, (i, _, _) in enumerate(keys)])  # fmt: skip
        sh = {k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30) for k, v in parts.items()}
        arms = {"whole": x}
        for k, (no, rand) in REMOVED.items():
            if k in parts:
                arms[no], arms[rand] = x - parts[k], x - SP.random_subspace_part(x, sh[k], basis)
        norms = [{"scene": chosen[i]["scene"], "condition": chosen[i]["condition"], "rendering": r, "reader": w,
                  "norm": round(float(x[j].norm()), 4), **{f"share_{k}": round(float(v[j]), 5) for k, v in sh.items()}}
                 for j, (i, r, w) in enumerate(keys)]  # fmt: skip
        rows, greedy = [], []
        for j, (i, r, w) in enumerate(progress(keys, f"reads at layer {layer} (change)")):
            c, rd = chosen[i], chosen[i]["readers"][w]
            names = [a for a in arm_rends[r] if a in arms]
            edits = [{}] + [{layer: AddRows(arms[a][j : j + 1], [rd["pos"][r]])} for a in names]
            logits, _ = X.read_logits(model, rd["ids"][r]["org"], edits, "chat", rd["space"], ws)
            for a, lg in zip(("none", *names), logits, strict=True):
                top = int(lg.argmax())
                rows.append({"scene": c["scene"], "condition": c["condition"], "format": c.get("format", "prose"),
                             "entity": c["bridge"], "reader": w, "rendering": r, "arm": a, "top_text": tok.decode([top]),
                             "route": classify(top, c) if w == X.LOOKUP else None, "right": int(top == rd["tok_A"]),
                             **X.read_row(lg, rd, digits)})  # fmt: skip
            if i in examples:
                texts = model.generate_batch(torch.tensor([rd["ids"][r]["org"]], device="cuda"), X.GEN_TOKENS, edits)
                greedy += [{"scene": c["scene"], "reader": w, "rendering": r, "arm": a, "greedy": t}
                           for a, t in zip(("none", *names), texts, strict=True)]  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "readout.jsonl", readout)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    hs = np.stack([s for _, _, s in states])
    hs = hs.astype(np.float16) if np.abs(hs).max() < 6e4 else hs  # fp16 when it fits (as x0_probe), else fp32
    np.savez_compressed(out / "states.npz", h=hs, scene=np.array([chosen[i]["scene"] for i, _, _ in states]),
                        rendering=np.array([r for _, r, _ in states]))  # fmt: skip
    X.write_jsonl(out / "items.jsonl", [{"scene": chosen[i]["scene"], "condition": chosen[i]["condition"], "rendering": r,
                                         "entity": chosen[i]["bridge"], "answer": chosen[i]["readers"][X.LOOKUP]["answer"],
                                         "slot": chosen[i]["slot"], "context": chosen[i]["context"],
                                         "format": chosen[i].get("format", "prose")} for i, r, _ in states])  # fmt: skip
    if part != "c":
        c0 = {}
        for r in arm_rends:
            sw = [row["switched"] for row in rows if row["condition"] == "C0" and row["reader"] == X.LOOKUP
                  and row["rendering"] == r and row["arm"] == "whole"]  # fmt: skip
            rate = float(np.mean(sw)) if sw else float("nan")
            ref = m["c0"]["reference"]
            ok = (rate >= c0_min) if c0_min is not None else (ref is not None and abs(rate - ref) <= R.C0_TOL)
            c0[r] = {"c0_lookup_switch": rate, "n": len(sw), "reference": ref, "c0_min": c0_min, "ok": bool(ok)}
        (out / "c0_check.json").write_text(json.dumps(c0, indent=1) + "\n")
        print("C0:", json.dumps(c0), flush=True)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.7 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan:(.*)$", block, re.M)
    return found.group(1).strip() if found else ""


def ci3(p: float, r: np.ndarray) -> list[float]:
    return [float(p), *X.interval(r)]


def route_shares(rows: list[dict], where, arms: tuple[str, ...], n_boot: int = X.N_BOOT) -> dict | None:
    """The lookup's route shares per arm on the rows `where` selects (paired over the scenes every arm has; cluster
    bootstrap over bridge items), with each removed part's fall beyond its random part (share(rand) - share(no)) for
    value and position, and the resamples kept for further paired differences."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP and where(r)]
    by = {a: {r["scene"]: r for r in lk if r["arm"] == a} for a in arms}
    by = {a: v for a, v in by.items() if v}
    if "whole" not in by:
        return None
    scenes_ = sorted(set.intersection(*(set(v) for v in by.values())))
    if not scenes_:
        return None
    ents = [by["whole"][s]["entity"] for s in scenes_]
    sw = {f"{rt}|{a}": [int(by[a][s]["route"] == rt) for s in scenes_] for a in by for rt in ROUTES}
    rr = X.resampled_rates(sw, ents, n_boot)
    pt = {k: float(np.mean(v)) for k, v in sw.items()}
    out: dict[str, Any] = {"n": len(scenes_), "entities": len(set(ents)), "scenes": scenes_,
                           "arms": {a: {rt: ci3(pt[f"{rt}|{a}"], rr[f"{rt}|{a}"]) for rt in ROUTES} for a in by},
                           "fall_beyond_random": {}, "_rr": rr, "_pt": pt}  # fmt: skip
    for k, (no, rand) in REMOVED.items():
        if no in by and rand in by:
            out["fall_beyond_random"][k] = {rt: ci3(pt[f"{rt}|{rand}"] - pt[f"{rt}|{no}"], rr[f"{rt}|{rand}"] - rr[f"{rt}|{no}"])
                                            for rt in ("value", "position", "identity")}  # fmt: skip
    return out


def paired_rendering_diff(rows: list[dict], cond: str, rt: str, n_boot: int = X.N_BOOT) -> list[float] | None:
    """The lookup's share of route rt under the whole change, question-first minus question-last, on the scenes read in
    both renderings (paired resamples)."""
    by = {r_: {r["scene"]: r for r in rows if r["reader"] == X.LOOKUP and r["condition"] == cond and r["arm"] == "whole"
               and r["rendering"] == r_} for r_ in RENDERINGS}  # fmt: skip
    scenes_ = sorted(set(by["qf"]) & set(by["ql"]))
    if not scenes_:
        return None
    sw = {r_: [int(by[r_][s]["route"] == rt) for s in scenes_] for r_ in RENDERINGS}
    rr = X.resampled_rates(sw, [by["qf"][s]["entity"] for s in scenes_], n_boot)
    return ci3(float(np.mean(sw["qf"]) - np.mean(sw["ql"])), rr["qf"] - rr["ql"])


def probe_numbers(src: Path, n_boot: int = X.N_BOOT) -> dict[str, dict]:
    """x0_probe's (a) (ridge, entities held out) on the lookup's O state per rendering, one state per O context."""
    from scripts import x0_probe as P

    z = np.load(src / "states.npz")
    h, rends = z["h"].astype(np.float64), [str(r) for r in z["rendering"]]
    items = X.read_jsonl(src / "items.jsonl")
    assert len(items) == len(rends)
    out = {}
    for r in sorted(set(rends)):
        seen: set[str] = set()
        idx = []
        for i, it in enumerate(items):
            if rends[i] == r and it["context"] not in seen:
                seen.add(it["context"])
                idx.append(i)
        sub = [items[i] for i in idx]
        if (
            len(idx) < 2 * P.K_OUTER
            or len({it["entity"] for it in sub}) < P.K_OUTER
            or len({it["answer"] for it in sub}) < 2
        ):
            out[r] = {"n": len(idx), "probe": [float("nan")] * 3, "why": "too few items, entities or classes"}
            continue
        out[r] = P.score(h[idx], sub, "answer digit", n_boot)
    return out


def lens_numbers(readout: list[dict], n_boot: int = X.N_BOOT) -> dict[str, dict]:
    """Per rendering: the share of items (one per O context, as the probe) whose answer the lens ranks first among the
    value pool's tokens, with its interval; the median rank beside it."""
    out = {}
    for r in sorted({x["rendering"] for x in readout}):
        seen: set[tuple] = set()
        mine = []
        for x in readout:
            key = (x["scene"].split("-", 1)[-1], x["entity"], x["answer"])  # the base scene: C0 and C2 share O
            if x["rendering"] == r and key not in seen:
                seen.add(key)
                mine.append(x)
        first = [int(x["rank"] == 1) for x in mine]
        rr = X.resampled_rates({"first": first}, [x["entity"] for x in mine], n_boot)
        out[r] = {"n": len(mine), "first": ci3(float(np.mean(first)) if mine else float("nan"), rr["first"]),
                  "median_rank": float(np.median([x["rank"] for x in mine])) if mine else float("nan"),
                  "chance": 1 / mine[0]["n_candidates"] if mine else float("nan")}  # fmt: skip
    return out


def ge(v: float, bar: float) -> bool:
    return bool(v == v and v >= bar - EPS)


def le(v: float, bar: float) -> bool:
    return bool(v == v and v <= bar + EPS)


def rule_a(m: dict) -> dict:
    """47.7(a) on one model's numbers (point estimates): the three labels and the rule's question-last premise."""
    if m["status"] != "tested":
        return {"prefetch": False, "jspace": False, "address": False, "premise_ql": None, "why": m["why"]}
    v_qf = m["shares"]["qf"]["arms"]["whole"]["value"][0]
    v_ql = m["shares"]["ql"]["arms"]["whole"]["value"][0] if m["shares"].get("ql") else float("nan")
    p_qf, p_ql = m["probe"]["qf"]["probe"][0], m["probe"]["ql"]["probe"][0]
    fall = m["shares"]["qf"]["fall_beyond_random"].get("jpp", {}).get("value", [float("nan")])[0]
    lens_qf = m["lens"]["qf"]["first"][0]
    prefetch = ge(v_qf, PREFETCH_VALUE) and ge(p_qf, PREFETCH_PROBE)
    out = {"prefetch": prefetch, "jspace": prefetch and ge(fall, JSPACE_FALL) and ge(lens_qf, JSPACE_LENS),
           "address": le(v_qf, ADDRESS_VALUE) and le(abs(p_qf - p_ql), ADDRESS_NEAR),
           "premise_ql": le(v_ql, QL_VALUE) and le(p_ql, QL_PROBE),
           "why": f"value qf {v_qf:.3f} (ql {v_ql:.3f}); probe qf {p_qf:.3f}, ql {p_ql:.3f}; value fall beyond random "
                  f"without J++ {fall:.3f}; lens first qf {lens_qf:.3f} (ql {m['lens']['ql']['first'][0]:.3f})"}  # fmt: skip
    return out


def batch_a(models: list[dict]) -> dict:
    """The labels over the models: each holds on at least MODELS_MIN; the J-space label is read only where prefetch
    holds (and needs prefetch on the batch)."""
    tested = [m for m in models if m["status"] == "tested"]
    n = {k: sum(m["rule"][k] for m in tested) for k in ("prefetch", "jspace", "address")}
    prefetch = n["prefetch"] >= MODELS_MIN
    label = ("prefetch on demand" + (", the prefetched value is in the J-space" if n["jspace"] >= MODELS_MIN else
                                     ", not shown in the J-space") if prefetch else
             "address regardless" if n["address"] >= MODELS_MIN else "neither label on 2 of 3 models")  # fmt: skip
    return {"label": label, "counts": n, "tested": [m["run"] for m in tested],
            "not_tested": [m["run"] for m in models if m["status"] != "tested"], "models": len(models)}  # fmt: skip


def rule_c(cell: dict | None) -> dict:
    """47.7(c) on one (model, format) cell."""
    if cell is None:
        return {"tested": False, "value_ok": None, "position_route": None}
    v, p = cell["arms"]["whole"]["value"][0], cell["arms"]["whole"]["position"][0]
    cut = cell["fall_beyond_random"].get("pcf", {}).get("position")
    return {"tested": True, "value_ok": le(v, C_VALUE), "n": cell["n"],
            "position_route": None if cut is None else (ge(p, C_POSITION) and ge(cut[0], C_CUT)),
            "value": v, "position": p, "pcf_cut": None if cut is None else cut[0]}  # fmt: skip


def batch_c(models: list[dict]) -> dict:
    cells = [(m["run"], f, m["rule"][f]) for m in models for f in FORMATS]
    tested = [c for c in cells if c[2]["tested"]]
    bad = [f"{run}/{f}" for run, f, r in tested if not r["value_ok"]]
    complete = len(tested) == len(cells)
    label = "does not generalize" if bad else "never the value generalizes" if complete else "incomplete"
    return {"label": label, "value_above": bad, "position_route": [f"{run}/{f}" for run, f, r in tested if r["position_route"]],
            "untested": [f"{run}/{f}" for run, f, r in cells if not r["tested"]]}  # fmt: skip


def rule_b(m: dict) -> dict:
    """47.7(b) on one model: per rendering, whether a value route appears (>= 0.15), the J++ part carries it (fall
    beyond random >= 0.3) and whether no value appears (<= 0.05)."""
    out = {}
    for r in RENDERINGS:
        s = m["shares"].get(r) if m["status"] == "tested" else None
        if not s:
            out[r] = {"tested": False}
            continue
        v = s["arms"]["whole"]["value"][0]
        fall = s["fall_beyond_random"].get("jpp", {}).get("value", [float("nan")])[0]
        out[r] = {"tested": True, "value": v, "appears": ge(v, B_APPEARS), "never": le(v, B_NEVER),
                  "jpp_carries": ge(fall, B_CUT), "fall_jpp": fall}  # fmt: skip
    return out


def batch_b(models: list[dict]) -> dict:
    ql = [(m["run"], m["rule"]["ql"]) for m in models if m["rule"]["ql"]["tested"]]
    return {"appears_ql": [run for run, r in ql if r["appears"]], "jpp_carries_ql": [run for run, r in ql if r["appears"] and r["jpp_carries"]],
            "never_the_value_word": bool(ql) and all(r["never"] for _, r in ql), "tested": [run for run, _ in ql],
            "qf_appears": [m["run"] for m in models if m["rule"]["qf"].get("appears")]}  # fmt: skip


def model_result(part: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), not tested (the gate or C0), or its numbers and the part's rule."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS[part].items()}.get(run)
        assert target, (
            f"no 47.7({part}) run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS[part].values())}"
        )
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    gate = json.loads((src / "gate.json").read_text())["gate"]
    out: dict[str, Any] = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "gate": gate, "status": "tested",
                           "why": "", "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip
    if part == "c":
        cells = {}
        for f in FORMATS:
            arms = (*ARMS, *ARMS_PCF)
            cells[f] = (
                route_shares(rows, lambda r, f=f: r["format"] == f and r["rendering"] == "ql", arms, n_boot)
                if gate.get(f, {}).get("pass")
                else None
            )
        out["cells"] = {
            f: ({k: v for k, v in c.items() if not k.startswith("_")} if c else None) for f, c in cells.items()
        }
        out["rule"] = {f: rule_c(cells[f]) for f in FORMATS}
        out["tested_formats"] = [f for f in FORMATS if cells[f]]
        return out
    c0 = json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else {}
    out["c0"] = c0
    if not gate.get("C2", {}).get("pass"):
        out.update({"status": "not tested", "why": "C2 failed the 0.80 gate on the question-first prompts" if part == "a"
                    else "C2 failed the 0.80 gate"})  # fmt: skip
    elif any(not v["ok"] for v in c0.values()):
        out.update({"status": "not tested", "why": "C0 failed: " + json.dumps(c0)})
    shares = {}
    for r in RENDERINGS:
        s = route_shares(rows, lambda x, r=r: x["condition"] == "C2" and x["rendering"] == r, ARMS, n_boot)
        if s:
            shares[r] = {k: v for k, v in s.items() if not k.startswith("_")}
    out["shares"] = shares
    out["position_qf_minus_ql"] = paired_rendering_diff(rows, "C2", "position", n_boot)
    out["value_qf_minus_ql"] = paired_rendering_diff(rows, "C2", "value", n_boot)
    out["probe"] = probe_numbers(src, n_boot)
    out["lens"] = lens_numbers(X.read_jsonl(src / "readout.jsonl"), n_boot)
    if part == "b":
        out["colours"] = out["plan"].get("colours")
    for r in RENDERINGS:
        if out["status"] == "tested" and (r not in shares or r not in out["probe"] or r not in out["lens"]):
            out.update({"status": "not tested", "why": f"no {r} rows, states or readout"})
    out["rule"] = rule_a(out) if part == "a" else rule_b(out)
    return out


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def yn(b: bool | None) -> str:
    return "-" if b is None else "yes" if b else "no"


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view: k random items of the run (seed 0; the run's own example draw), each reader's O prompt per
    rendering exactly as the model reads it with the bridge in ⟦...⟧, S's prompt, and every arm's answer, route and
    greedy text."""
    from bridge_jspace.review import checks as RC

    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    tk = RC.tokenizer(m["model"]["target"])
    decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    reads = collections.defaultdict(list)
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        reads[(r["scene"], r["reader"], r["rendering"])].append(r)
    greedy = {
        (g["scene"], g["reader"], g["rendering"], g["arm"]): g["greedy"]
        for g in X.read_jsonl(src / "examples_greedy.jsonl")
    }
    chosen = list(dict.fromkeys(r["scene"] for r in X.read_jsonl(src / "outcomes.jsonl")))
    picked = [chosen[i] for i in sorted(random.Random(seed).sample(range(len(chosen)), min(k, len(chosen))))]
    lines = [f"## {run}: {len(picked)} random items of {len(chosen)} (seed {seed})", ""]
    for s in picked:
        c = cases[s]
        lines += [f"### {s} ({c['condition']}, {c.get('format', 'prose')}): bridge {c['bridge']} → {c['cf_bridge']}; expected "
                  f"{c['expect']}", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            for r in rd["ids"]:
                if not reads.get((s, w, r)):
                    continue
                lines += [f"**{READER_NAME[w]}, {r}**: O's answer {rd['answer']}, S's answer {rd['cf_answer']}; bridge token "
                          f"{rd['pos'][r]}", "", "O, as read:", "```",
                          marked_prompt(decode, rd["ids"][r]["org"], rd["pos"][r], rd["space"]), "```", "S (the source):",
                          "```", marked_prompt(decode, rd["ids"][r]["alt"], rd["pos"][r], rd["space"]), "```", "",
                          "| arm | answer | route | switched | right | greedy |", "|---|---|---|---|---|---|"]  # fmt: skip
                for x in reads[(s, w, r)]:
                    lines.append(f"| {x['arm']} | {x['top_text']!r} | {x['route'] or ''} | {x['switched']} | {x['right']} | "
                                 f"{greedy.get((s, w, r, x['arm']))!r} |")  # fmt: skip
                lines.append("")
    return lines


def report_a(part: str, models: list[dict], v: dict, answer: str, n_boot: int) -> list[str]:
    what = "digit" if part == "a" else "colour"
    lines = [f"# 47.7({part}): {'question-first: prefetch on demand?' if part == 'a' else 'word-valued lockers'}", "",
             f"Batch 47, test 47.7 (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). C2 routes scenes (another item moved, "
             f"a new {what}); shares of the lookup's answers by route under each arm; the value probe (x0_probe (a), "
             f"entities held out) and the lens's rank of the answer among the {what} tokens at the lookup's O state at the "
             f"bridge word. Cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE[part]}.", ""]  # fmt: skip
    if part == "a":
        lines += [f"**Verdict: {v['label']}** (prefetch on {v['counts']['prefetch']}, J-space on {v['counts']['jspace']}, "
                  f"address on {v['counts']['address']} of {len(v['tested'])} tested models; at least {MODELS_MIN} needed)"
                  + (f"; not tested: {', '.join(v['not_tested'])}" if v["not_tested"] else "") + ".", ""]  # fmt: skip
    else:
        lines += [f"**A value route appears question-last on: {', '.join(v['appears_ql']) or 'none'}** (the J++ part carries it "
                  f"on: {', '.join(v['jpp_carries_ql']) or 'none'}); never the value holds for a word value too: "
                  f"{yn(v['never_the_value_word'])} (tested: {', '.join(v['tested']) or 'none'}; question-first appears on: "
                  f"{', '.join(v['qf_appears']) or 'none'}).", ""]  # fmt: skip
    lines += ["| model | run | status | rendering | n | identity | position | value | original | other |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | | | | |")
            continue
        for r, s in m["shares"].items():
            w = s["arms"]["whole"]
            lines.append(f"| {m['target']} | {m['run']} | {m['status']}{(' (' + m['why'] + ')') if m['why'] else ''} | {r} | "
                         f"{s['n']} | " + " | ".join(fmt(w[rt]) for rt in ROUTES) + " |")  # fmt: skip
    lines += ["", "Per arm (question-first, and question-last where its arms ran): value and position shares; the fall "
              "beyond the random part (share without the random part minus share without the part):", "",
              "| model | rendering | arm | value | position | identity |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for r, s in m["shares"].items():
            for a, sh in s["arms"].items():
                lines.append(
                    f"| {m['target']} | {r} | {a} | {fmt(sh['value'])} | {fmt(sh['position'])} | {fmt(sh['identity'])} |"
                )
            for k, d in s["fall_beyond_random"].items():
                lines.append(f"| {m['target']} | {r} | fall beyond random: {k} | {fmt(d['value'])} | {fmt(d['position'])} | "
                             f"{fmt(d['identity'])} |")  # fmt: skip
    lines += ["", "The probe and the lens at the lookup's O state (one per O context):", "",
              "| model | rendering | n | probe | majority | chance | lens ranks the answer first | median rank |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for r in RENDERINGS:
            p, ln = m["probe"].get(r), m["lens"].get(r)
            if p and ln:
                lines.append(f"| {m['target']} | {r} | {p['n']} | {fmt(p['probe'])} | {fmt(p.get('majority'))} | "
                             f"{p.get('chance', float('nan')):.2f} | {fmt(ln['first'])} | {ln['median_rank']} |")  # fmt: skip
    lines += ["", "Position and value share question-first minus question-last (the whole change, paired):", ""]
    for m in models:
        if m["status"] != "pending":
            lines.append(f"- {m['target']}: position {fmt(m['position_qf_minus_ql'])}, value {fmt(m['value_qf_minus_ql'])}; "
                         f"rule: {json.dumps(m['rule'])}; C0 {json.dumps(m.get('c0'))}; gate "
                         f"{json.dumps({g: x['org_read_accuracy'] for g, x in m['gate'].items()})}"
                         + (f"; colours {m['colours']}" if m.get("colours") else ""))  # fmt: skip
    return lines


def report_c(models: list[dict], v: dict, answer: str, n_boot: int) -> list[str]:
    lines = ["# 47.7(c): never the value, in prose / JSON / table?", "",
             f"Batch 47, test 47.7 (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). The varied scenes, locker-first, "
             "another item moved with a new number; question-last; the lookup's route shares per format under the whole "
             "change, and without the per-format refit pointer (45d) vs a random part (9B, Muse). Cluster bootstrap over "
             f"bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "", f"Rule (fixed in advance): {RULE['c']}.", "",
             f"**Verdict: {v['label']}** (value above {C_VALUE}: {', '.join(v['value_above']) or 'none'}; a position route: "
             f"{', '.join(v['position_route']) or 'none'}; untested cells: {', '.join(v['untested']) or 'none'}).", "",
             "| model | format | n | identity | position | value | original | other | position cut by the refit pointer "
             "beyond random | value cut | rule |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | pending ({m['why']}) | | | | | | | | | |")
            continue
        for f in FORMATS:
            c = m["cells"][f]
            if c is None:
                g = m["gate"].get(f, {})
                lines.append(
                    f"| {m['target']} | {f} | not tested (gate {json.dumps(g.get('org_read_accuracy'))}) | | | | | | | | |"
                )
                continue
            w, cut = c["arms"]["whole"], c["fall_beyond_random"].get("pcf")
            lines.append(f"| {m['target']} | {f} | {c['n']} | " + " | ".join(fmt(w[rt]) for rt in ROUTES)
                         + f" | {fmt(cut['position']) if cut else '-'} | {fmt(cut['value']) if cut else '-'} | "
                         f"{json.dumps(m['rule'][f])} |")  # fmt: skip
    lines += [
        "",
        "Every arm per format:",
        "",
        "| model | format | arm | identity | position | value |",
        "|---|---|---|---|---|---|",
    ]
    for m in models:
        if m["status"] == "pending":
            continue
        for f in FORMATS:
            c = m["cells"][f]
            for a, sh in c["arms"].items() if c else []:
                lines.append(
                    f"| {m['target']} | {f} | {a} | {fmt(sh['identity'])} | {fmt(sh['position'])} | {fmt(sh['value'])} |"
                )
    return lines


def stage_verdict(part: str, runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    assert part in PARTS, part
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(part, r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    assert set(targets) <= set(RUNS[part]), f"47.7({part}) runs on {sorted(RUNS[part])}"
    for t in RUNS[part]:
        if t not in targets:
            models.append({"run": f"({RUNS[part][t]})", "target": t, "status": "pending", "why": "no run given",
                           "rule": {r: {"tested": False} for r in RENDERINGS} if part == "b" else
                           {f: rule_c(None) for f in FORMATS} if part == "c" else {}})  # fmt: skip
    v = batch_a(models) if part == "a" else batch_c(models) if part == "c" else batch_b(models)
    out = RESULTS / f"x47_7{part}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = report_c(models, v, answer, n_boot) if part == "c" else report_a(part, models, v, answer, n_boot)
    (out / f"x47_7{part}.json").write_text(json.dumps({"part": part, "runs": runs, "dan": answer, "verdict": v, "models": models},
                                                      indent=1, ensure_ascii=False) + "\n")  # fmt: skip
    (out / f"x47_7{part}.md").write_text("\n".join(lines) + "\n")
    ex = [f"# 47.7({part}) examples (verify pack): prompts exactly as the model reads them; ⟦...⟧ the bridge word where "
          "the change is added. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--part", required=True, choices=PARTS)
    ap.add_argument("--name", help="run: the run name (results/x47_value/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the part's runs (default: the job specs' names)")
    ap.add_argument("--why", default="batch 47, test 47.7 (jobs/c3/batch47.yaml; Q47.7)")
    ap.add_argument(
        "--c0-min", type=float, default=None, help="run: a descriptive C0 gate (Muse: 0.5), else the reference"
    )
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.part)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.part, a.name, a.why, a.c0_min)
    else:
        stage_verdict(a.part, a.runs or list(RUNS[a.part].values()), a.n_boot)


if __name__ == "__main__":
    main()
