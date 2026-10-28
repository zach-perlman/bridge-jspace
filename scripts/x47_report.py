"""x47_report (batch 47, amendment 4, test 47.10; jobs/c3/batch47.yaml "47.10", design and rule fixed in advance; Q47.10
in predictions/2026-10-28_dan.md): report the address, on-demand surfacing into the J-space.

Gurnee et al.: information not normally in the J-space can be surfaced to it on demand. The address (the pointer U) is
not verbalizable (47.0). Does it become lens-readable, and lens-dependent, when the task is to report it?

Scenes: the routes generator's C0 scenes (x6_routes.scenes, seed 2510: three one-token animals, their three locker
sentences first, then three pick sentences; O: <asked> picked A; S: <asked> picked B, same lockers, same digits),
locker-first by construction, so the asked item's locker sits in slot 1, 2 or 3 at random (the control of dumbest way 1:
the report must track the slot, not say "first"; its read accuracy per true slot is in gate.json). Four readers, each a
separate prompt over the same context (dumbest way 3; asserted: in the question-last order the four prompts share every
token through the bridge word, and each reader's gate is computed on its own prompt):
  lookup        "Which locker belongs to <p>'s pick?"                           digit   O: A's digit        S: B's digit
  recall        "How many legs does <p>'s pick have?"                           digit   O: legs(A)          S: legs(B)
  report        "Was the locker of <p>'s pick listed first, second or third?"   word    O: A's slot's word  S: B's
  report_digit  "Was the locker of <p>'s pick listed 1, 2 or 3?"                digit   O: A's slot         S: B's (beside)
Reads: X0's chat read (tasks_v2's prompt, thinking off, 'Answer:' prefilled): a digit reader with the space token
appended, the top token over the vocabulary; the word reader right after 'Answer:', its answer token ' first' /
' second' / ' third' with the leading space (suite_v1.answer_token's word rule; the ordinal words are one token with and
without the space on the 9B, the 27B and Muse: the plan checks). Switch = the top token is S's answer (the report: S's
slot's ordinal). The digit report is read beside the report: it neither gates nor selects items.

Two question orders, each with its own gate, items, change and reads:
  last   the question after the context, as every routes test (tasks_v2's prompt)
  first  the question with its instruction before the context, one user turn (47.7(a)'s order)
Why both: in the question-last order the bridge word precedes the question, so its state at L is the same under the
four prompts (causal attention; asserted on the ids), and the rule's lens clause "under the report prompt vs the lookup
prompt" cannot differ there. In the question-first order the model knows the task at the bridge word: that is where
surfacing on demand can show. Both orders run; the rule is applied per order; which order is the headline is Dan's
call (the spec's as-computed paragraph records the agent's recommendation).

Reads at the bridge word (per order and reader, on O's state at L): the J++ lens readout (JLens.readout, the full
vocabulary's lens logits), the rank (1 = top; special tokens out) of the correct (O's) slot's ordinal, the best of its
four spellings, and of the slot digit; top-5 = rank <= 5; the rank among the three ordinals and among the ten digits
and the top-20 tokens beside (the view). The slot probe (x0_probe (b): ridge on the bridge-word states for the locker
sentence's index, entities held out, 5 folds) is the control: the address is there under every prompt.
Arms (the change h_S - h_O at the bridge word at L, added on O; each reader patched with the change of its own prompt,
one shared change in the question-last order): whole; without J++ (signed OMP, K = 25, over the J++ lens's letter-token
atoms PLUS the ten digit tokens: the main test's letter-only restriction is lifted here, so ordinal and digit atoms can be
picked; which ordinal atoms the dictionary holds is recorded in the manifest, which are picked per item in norms.jsonl);
without a random part of J++'s share (X0's random subspace, seed 888 + L); without U (the 4 pointer directions,
x0_massmean's layout-free class means on the model's x0_probe_v4 states, never refit); without a random part of U's
share; only U; only a random part of U's share.

Rule (jobs/c3/batch47.yaml 47.10, verbatim): "Surfaced on demand": under the report prompt the lens ranks the correct
ordinal in its top-5 in >= 0.4 of items (under the lookup prompt <= 0.1), and the report loses >= 0.3 of its switches
without J++ beyond random, while the lookup on the same scenes loses <= 0.10 (as before). "Reported late, not
surfaced": the lens stays <= 0.1 at the bridge word under the report prompt and the report loses <= 0.1 without J++ but
>= 0.3 without U; the address is converted to a word at the question, not at the token. As computed: "loses x of its
switches without P beyond random" is X0's extra loss, Jdep - Rdep = (1 - S_noP / S_whole) - (1 - S_noP_rand /
S_whole) over the order's items; the "without U" clause the same way against U's random part; "the lens ranks ... in
>= 0.4 of items" is the share of the order's items with top-5 rank; points from counts, cluster-bootstrap CIs over the
bridge items (10,000 resamples, seed 0) beside them; point estimates decide, EPS 1e-9 at the bars. Gate 0.80 per reader
and order on the unedited O prompts (read accuracy); an order whose report (or lookup, or recall) misses the gate is
"not tested"; a reader whose whole change switches fewer than 30 items (X0's VALID_N) has no interpretable loss, and the
order is "not tested" for that reader's clause. Neither label: "neither".

SEALED (as batch 45): the run writes per-item files only; verdict, view and figures refuse until
predictions/2026-10-28_dan.md holds Dan's committed Q47.10 answer at HEAD.

uv run python scripts/x47_report.py plan                                              # CPU: scenes, ordinals, 5 prompts
BJ_TARGET=qwen3.6-27b uv run python scripts/x47_report.py run --name x47_report_27b   # GPU (sealed; the gate first)
uv run python scripts/x47_report.py verdict --runs qwen35_9b_x47_report x47_report_27b muse30_x47_report   # CPU
uv run python scripts/x47_report.py view --name x47_report_27b                        # CPU: the verify-pack view
uv run python scripts/x47_report.py figures --verdict results/x47_report/x47_10-<UTC> # CPU
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import statistics
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

EXP = "x47_report"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION, TEST = "Q47.10", "47.10"
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_report", "qwen3.6-27b": "x47_report_27b", "muse-glimmer-30b": "muse30_x47_report"}
ORDERS = ("last", "first")
ORDER_TEXT = {"last": "question-last: the question after the context (tasks_v2's prompt, as every routes test)",
              "first": "question-first: the question and its instruction before the context, one user turn"}  # fmt: skip
READERS = ("lookup", "recall", "report", "report_digit")
GATED = ("lookup", "recall", "report")  # the digit report is read beside: it neither gates nor selects items
QUESTIONS = {"lookup": R.LOOKUP_Q, "recall": R.RECALL_Q,
             "report": "Was the locker of {p}'s pick listed first, second or third?",
             "report_digit": "Was the locker of {p}'s pick listed 1, 2 or 3?"}  # fmt: skip
KIND = {"lookup": "digit", "recall": "digit", "report": "word", "report_digit": "digit"}
ORDINALS = ("first", "second", "third")
ARMS = ("none", "whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand")
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change h_S - h_O at the bridge word at L",
    "no_jpp": "without its J++ part (signed OMP, K = 25, letter and digit atoms)",
    "no_jpp_rand": "without a random part of J++'s share",
    "no_alf": "without U (the 4 pointer directions)",
    "no_alf_rand": "without a random part of U's share",
    "keep_alf": "only U's part",
    "keep_alf_rand": "only a random part of U's share",
}
PARTS = (("jpp", "no_jpp", "no_jpp_rand"), ("alf", "no_alf", "no_alf_rand"))
N_GEN, N_ITEMS = 500, 200  # C0 scenes generated (the gate's denominator); the first eligible kept per order
TOP = 5  # "in its top-5"
SURF_LENS, SURF_LENS_OTHER, SURF_REPORT, SURF_LOOKUP = 0.4, 0.1, 0.3, 0.10
LATE_LENS, LATE_JPP, LATE_U = 0.1, 0.1, 0.3
MIN_SWITCHES = X.VALID_N
EPS = 1e-9  # a value exactly at a bar counts as at the bar
LOCKER_RE = re.compile(r"The locker of the (\w+) is (\d)\.")
RULE = ('"Surfaced on demand": under the report prompt the lens ranks the correct ordinal in its top-5 in >= 0.4 of '
        "items (under the lookup prompt <= 0.1), and the report loses >= 0.3 of its switches without J++ beyond random, "
        'while the lookup on the same scenes loses <= 0.10 (as before). "Reported late, not surfaced": the lens stays '
        "<= 0.1 at the bridge word under the report prompt and the report loses <= 0.1 without J++ but >= 0.3 without "
        "U; the address is converted to a word at the question, not at the token.")  # fmt: skip
LABELS = {"surfaced": "surfaced on demand", "late": "reported late, not surfaced", "neither": "neither",
          "not tested": "not tested"}  # fmt: skip


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def spellings(word: str) -> tuple[str, ...]:
    """The four spellings of an ordinal word a token may carry: bare, with a leading space, capitalised, both."""
    return (word, " " + word, word.capitalize(), " " + word.capitalize())


def ordinal_tokens(tok) -> dict[str, dict[str, int | None]]:
    """Per ordinal word, each spelling's token id where it is one token (else None): the single-token check."""
    from scripts import suite_v1 as S

    out: dict[str, dict[str, int | None]] = {}
    for w in ORDINALS:
        out[w] = {}
        for sp in spellings(w):
            ids = S.ids(tok, sp)
            out[w][sp] = ids[0] if len(ids) == 1 else None
    return out


def answer_ids(tok) -> dict[str, list[int]]:
    """Per ordinal word, the ids of its single-token spellings (the read token ' <word>' first)."""
    out = {}
    for w, sp in ordinal_tokens(tok).items():
        ids = [sp[" " + w], *(v for k, v in sp.items() if k != " " + w and v is not None)]
        assert ids[0] is not None, f"{w!r}: ' {w}' is not one token on this tokenizer"
        out[w] = [int(v) for v in ids]
    return out


def suffix(tok, kind: str) -> list[int]:
    """What X0's chat read appends before reading: the space token for a digit answer, nothing for a word."""
    from scripts import suite_v1 as S

    return S.ids(tok, " ") if kind == "digit" else []


def prompt(tok, context: str, question: str, kind: str, order: str) -> str:
    """The reader's prompt: question-last = tasks_v2's prompt (X.render, chat); question-first = the question and its
    instruction, a newline, the context, in the same user turn (chat.chat_text: the template, 'Answer:' prefilled)."""
    from bridge_jspace import chat
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    item = {"format": "prose", "kind": kind, "context": context, "question": question}
    if order == "last":
        return X.render(tok, item, "chat", context)
    assert order == "first", order
    instr = T.DIGIT_INSTRUCTION if kind == "digit" else S.INSTRUCTION
    return chat.chat_text(tok, f"{question} {instr}\n{context}")


def encode_reader(tok, contexts: dict[str, str], asked: str, bridges: dict[str, str], question: str, kind: str,
                  order: str) -> tuple[dict | None, str]:  # fmt: skip
    """One reader's O and S prompts (ids, texts) and the bridge word's position: one token at the same index in both
    (else None and why)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    ids, at, texts = {}, {}, {}
    for v in ("org", "alt"):
        ctx, x = contexts[v], bridges[v]
        text = prompt(tok, ctx, question, kind, order)
        if text.count(ctx) != 1:
            return None, "the context is not once in the prompt"
        enc = raw_encoding(tok, text, offsets=True)
        sent = f"{asked} picked the {x}."
        w0 = text.index(ctx) + ctx.index(sent) + sent.index(x)
        ids[v], texts[v] = list(enc["input_ids"]), text
        at[v] = SP.tokens_in(enc["offset_mapping"], w0, w0 + len(x))
    if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
        return None, "the bridge is not one token at the same index in O and S"
    return {"question": question, "kind": kind, "ids": ids, "pos": at["org"][0], "text": texts}, ""


def locker_slots(context: str) -> dict[str, int]:
    """Each locker item's slot: its locker sentence's index among the context's locker sentences, in order."""
    return {m.group(1): i for i, m in enumerate(LOCKER_RE.finditer(context))}


def pick_index(context: str, asked: str) -> int:
    """The asked person's pick sentence's index among the context's sentences (x0_probe's pick_index)."""
    sents = context.split(". ")
    return next(i for i, s in enumerate(sents) if s.startswith(f"{asked} picked"))


def build_item(tok, c: dict, orders: tuple[str, ...] = ORDERS) -> tuple[dict | None, str]:
    """A 47.10 item from one routes C0 case: the four readers' prompts per order, the answers (the report's: the
    slot's ordinal), the bridge position; None and why where a prompt cannot be used. In the question-last order the
    lookup's and the recall's ids must be x6_routes's (asserted) and every reader must share the lookup's prefix
    through the bridge word."""
    from scripts import suite_v1 as S

    assert c["condition"] == "C0", f"{c['scene']}: 47.10 runs on C0 scenes, not {c['condition']}"
    asked, a_item, bridge = R.asked_of(c), c["bridge"], c["cf_bridge"]
    slots = locker_slots(c["context"])
    assert slots == locker_slots(c["cf_context"]), f"{c['scene']}: O and S do not share the lockers"
    assert len(slots) == 3, f"{c['scene']}: {len(slots)} lockers, not three"
    s_a, s_b = slots[a_item], slots[bridge]
    assert s_a != s_b, f"{c['scene']}: A and B share a slot"
    answers = {"lookup": (c["readers"][X.LOOKUP]["answer"], c["readers"][X.LOOKUP]["cf_answer"]),
               "recall": (c["readers"][X.RECALL]["answer"], c["readers"][X.RECALL]["cf_answer"]),
               "report": (ORDINALS[s_a], ORDINALS[s_b]), "report_digit": (str(s_a + 1), str(s_b + 1))}  # fmt: skip
    contexts, bridges = {"org": c["context"], "alt": c["cf_context"]}, {"org": a_item, "alt": bridge}
    by_order = {}
    for order in orders:
        readers = {}
        for w in READERS:
            rd, why = encode_reader(tok, contexts, asked, bridges, QUESTIONS[w].format(p=asked), KIND[w], order)
            if rd is None:
                return None, f"{order}: {w}: {why}"
            org, alt = answers[w]
            rd.update({"answer": org, "cf_answer": alt, "tok_A": S.answer_token(tok, org, KIND[w]),
                       "tok_b": S.answer_token(tok, alt, KIND[w])})  # fmt: skip
            readers[w] = rd
        if order == "last":
            for w, key in (("lookup", X.LOOKUP), ("recall", X.RECALL)):
                assert readers[w]["ids"] == c["readers"][key]["ids"], f"{c['scene']}: {w}'s ids are not x6_routes's"
            pos, lk = readers["lookup"]["pos"], readers["lookup"]["ids"]
            for w in READERS:
                if readers[w]["pos"] != pos or any(readers[w]["ids"][v][: pos + 1] != lk[v][: pos + 1] for v in lk):
                    return None, f"{order}: {w}'s prompt differs from the lookup's before the bridge word"
        by_order[order] = {"shared_prefix": order == "last", "readers": readers}
    return {"scene": c["scene"], "entity": a_item, "cf_bridge": bridge, "domain": c["domain"], "asked": asked,
            "context": c["context"], "cf_context": c["cf_context"], "slot": {"org": s_a, "alt": s_b},
            "pick_index": pick_index(c["context"], asked), "orders": by_order}, ""  # fmt: skip


def build_items(tok, n_gen: int = N_GEN, orders: tuple[str, ...] = ORDERS) -> tuple[list[dict], dict]:
    """The routes generator's C0 scenes (seed 2510) as 47.10 items, and the counts (drops by reason, slots)."""
    cases, dropped = R.scenes(tok, n_gen)
    out = []
    for c in cases:
        if c["condition"] != "C0":
            continue
        it, why = build_item(tok, c, orders)
        if it is None:
            dropped[why] += 1
        else:
            out.append(it)
    counts = {"generated_C0": sum(c["condition"] == "C0" for c in cases), "items": len(out),
              "entities": len({it["entity"] for it in out}), "dropped": dict(dropped),
              "slot_of_O_bridge": dict(collections.Counter(it["slot"]["org"] for it in out)),
              "slot_of_S_bridge": dict(collections.Counter(it["slot"]["alt"] for it in out))}  # fmt: skip
    return out, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    """The example items: k random indices of n (seed 0), as X0 picks its examples."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def marked_prompt(decode, rd: dict, v: str, tok=None) -> str:
    """The reader's prompt (O or S) as the model reads it, the bridge word in ⟦...⟧, the read suffix appended."""
    text = R.marked(decode, rd["ids"][v], rd["pos"])
    return text + (decode(suffix(tok, rd["kind"])) if tok is not None else "")


def stage_plan(n_gen: int = N_GEN, k: int = 5) -> dict:
    """Tokenizer only: the items and drops, the ordinal words' tokens (single-token check; in the letter dictionary
    iff they carry a letter), and k example items' report prompts (seed 0), both readers, both orders, the bridge
    marked."""
    from bridge_jspace.model import _HAS_LETTER
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    items, counts = build_items(tok, n_gen)
    ords = ordinal_tokens(tok)
    counts["target"] = pins.TARGET
    counts["ordinal_tokens"] = {w: {sp: None if v is None else {"id": v, "letter_atom": bool(_HAS_LETTER.search(tok.decode([v])))}
                                    for sp, v in sp_.items()} for w, sp_ in ords.items()}  # fmt: skip
    counts["slot_digit_tokens"] = {
        str(i + 1): int(tok(str(i + 1), add_special_tokens=False).input_ids[0]) for i in range(3)
    }
    counts["read"] = {w: {"kind": KIND[w], "suffix": suffix(tok, KIND[w]), "question": QUESTIONS[w]} for w in READERS}
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    for i in example_indices(len(items), k):
        it = items[i]
        print(f"\n### {it['scene']}: bridge {it['entity']} (slot {it['slot']['org'] + 1}) -> {it['cf_bridge']} "
              f"(slot {it['slot']['alt'] + 1})")  # fmt: skip
        for order in it["orders"]:
            for w in ("report", "report_digit"):
                rd = it["orders"][order]["readers"][w]
                print(f"\n[{order}] {w}: O answers {rd['answer']!r} (token {rd['tok_A']}), S answers "
                      f"{rd['cf_answer']!r} (token {rd['tok_b']}); bridge token {rd['pos']}\n")  # fmt: skip
                print(marked_prompt(decode, rd, "org", tok))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def said_ordinal(text: str) -> str | None:
    """What the greedy text says, as an ordinal word: the first ordinal word of the first line, or '1' / '2' / '3' as
    its ordinal (lenient, as X0's digit read takes number words as digits); None if neither."""
    from scripts import suite_v1 as S

    for t in re.findall(r"[a-z]+|\d+", S.first_line(text)):
        if t in ORDINALS:
            return t
        if t in ("1", "2", "3"):
            return ORDINALS[int(t) - 1]
    return None


def said(text: str, kind: str) -> str | None:
    from scripts import suite_v1 as S

    return said_ordinal(text) if kind == "word" else S.said(text, "digit")


def dictionary_ids(letters, digits):
    """The no_jpp arm's atoms: the J++ lens's letter tokens plus the ten digit tokens (the letter-only restriction of
    the main test lifted), as one tensor without duplicates."""
    import torch

    ids = torch.cat([letters.to(digits.device), digits])
    assert ids.unique().numel() == ids.numel(), "the digit tokens overlap the letter tokens"
    return ids


def atom_report(tok, atom_ids: list[int], digit_ids: list[int]) -> dict:
    """Which ordinal atoms (the four spellings of first / second / third) and which digit atoms the dictionary holds."""
    index = {int(t): i for i, t in enumerate(atom_ids)}
    ords = {w: {sp: None if v is None else {"id": v, "atom": index.get(v)} for sp, v in sp_.items()}
            for w, sp_ in ordinal_tokens(tok).items()}  # fmt: skip
    return {"atoms": len(atom_ids), "ordinal_atoms": ords,
            "ordinal_atoms_present": sorted(sp for w in ords for sp, v in ords[w].items() if v and v["atom"] is not None),
            "ordinal_spellings_absent": sorted(sp for w in ords for sp, v in ords[w].items() if not v or v["atom"] is None),
            "digit_atoms": {tok.decode([d]): index.get(int(d)) for d in digit_ids}}  # fmt: skip


def lens_ranks(logits, slot: dict[str, int], ords: dict[str, list[int]], slot_digits: dict[str, int],
               value_digit: int, special: list[int], decode, top: int = TOP, n_top: int = 20) -> dict:  # fmt: skip
    """From the lens readout at the bridge word (logits [vocab]): the rank (1 = top, special tokens out) of O's slot's
    ordinal (its best spelling) and S's, of O's slot digit and of the lookup's answer digit (the value); the ranks
    among the three ordinals and the ten digits; top-k flags; the top-n_top tokens."""
    lg = logits.float().clone()
    if special:
        lg[special] = float("-inf")

    def best(ids: list[int]) -> float:
        return max(float(lg[t]) for t in ids)

    def rank_of(ids: list[int]) -> int:
        return int((lg > best(ids)).sum()) + 1

    o_word, s_word = ORDINALS[slot["org"]], ORDINALS[slot["alt"]]
    o_digit = slot_digits[str(slot["org"] + 1)]
    among3 = 1 + sum(best(ords[w]) > best(ords[o_word]) for w in ORDINALS if w != o_word)
    digits = list(slot_digits.values())
    among_digits = 1 + sum(float(lg[d]) > float(lg[o_digit]) for d in digits if d != o_digit)
    r_ord, r_dig = rank_of(ords[o_word]), rank_of([o_digit])
    return {"rank_ordinal": r_ord, "top5_ordinal": int(r_ord <= top), "rank_ordinal_alt": rank_of(ords[s_word]),
            "rank_ordinal_among3": among3, "rank_digit": r_dig, "top5_digit": int(r_dig <= top),
            "rank_digit_among_digits": among_digits, "rank_value_digit": rank_of([value_digit]),
            "top20": [decode([int(t)]) for t in lg.topk(n_top).indices]}  # fmt: skip


def competence(model, items: list[dict], orders: tuple[str, ...], ws, cand: dict) -> list[dict]:
    """Unedited O and S prompts of every reader and order: 8 greedy tokens (what the model says), the decisive read
    (the top token is the answer token) and the cand read (first among the reader's candidate tokens)."""
    import torch

    from bridge_jspace.utils import progress

    tok = model.tokenizer
    rows = []
    with torch.no_grad():
        for it in progress(items, "competence (item)"):
            for order in orders:
                for w, rd in it["orders"][order]["readers"].items():
                    ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                    texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                    for i, (v, gold, tok_gold) in enumerate((("org", rd["answer"], rd["tok_A"]),
                                                             ("alt", rd["cf_answer"], rd["tok_b"]))):  # fmt: skip
                        logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", suffix(tok, KIND[w]), ws)
                        s = said(texts[i], KIND[w])
                        rows.append({"scene": it["scene"], "order": order, "reader": w, "variant": v,
                                     "slot": it["slot"][v], "greedy": texts[i], "said": s, "right": s == gold,
                                     "read_right": int(logits[0].argmax()) == tok_gold,
                                     "cand_right": X.first_among(logits[0], tok_gold, cand[w])})  # fmt: skip
    return rows


def gate_of(items: list[dict], comp: list[dict], orders: tuple[str, ...], gate_min: float = X.GATE,
            n_items: int = N_ITEMS) -> tuple[dict, dict[str, list[dict]]]:  # fmt: skip
    """Per order: each reader's gate on its own unedited O prompts (read accuracy >= gate_min, every reader in GATED
    must pass), the report readers' read accuracy per true slot (dumbest way 1), and the chosen items: the first
    n_items whose gated readers say and read O's and S's answers right."""
    right = {(r["scene"], r["order"], r["reader"], r["variant"]): r for r in comp}
    gate, chosen = {}, {}
    for order in orders:
        org = {w: [right[(it["scene"], order, w, "org")] for it in items] for w in READERS}
        acc = {w: float(np.mean([r["read_right"] for r in rows])) for w, rows in org.items()}
        by_slot = {}
        for w in ("report", "report_digit"):
            by_slot[w] = {}
            for s in range(3):
                mine = [r["read_right"] for r in org[w] if r["slot"] == s]
                by_slot[w][str(s + 1)] = [float(np.mean(mine)) if mine else None, len(mine)]
        ok = [it for it in items
              if all(right[(it["scene"], order, w, v)]["right"] and right[(it["scene"], order, w, v)]["read_right"]
                     for w in GATED for v in ("org", "alt"))]  # fmt: skip
        failed = [w for w in GATED if acc[w] < gate_min - EPS]
        gate[order] = {"items": len(items), "org_read_accuracy": acc,
                       "org_said_accuracy": {w: float(np.mean([r["right"] for r in rows])) for w, rows in org.items()},
                       "report_read_accuracy_by_true_slot": by_slot, "gate": gate_min, "failed": failed,
                       "pass": not failed, "eligible": len(ok), "chosen": min(n_items, len(ok)) if not failed else 0}  # fmt: skip
        chosen[order] = ok[:n_items] if not failed else []
    return gate, chosen


def stage_run(name: str, why: str, orders: tuple[str, ...] = ORDERS, n_gen: int = N_GEN, n_items: int = N_ITEMS,
              gate_min: float = X.GATE) -> Path:  # fmt: skip
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S
    from scripts import x0_massmean as MM
    from scripts import x0_parts as XP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.10 reads chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"47.10 runs on {sorted(RUNS)}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": TEST,
         "spec": f"jobs/c3/batch47.yaml ({TEST})", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)}, "layer": layer,
         "scenes": f"x6_routes.scenes C0 (seed {R.SEED}), {n_gen} generated; the first {n_items} eligible per order",
         "orders": {o: ORDER_TEXT[o] for o in orders}, "readers": {w: {"question": QUESTIONS[w], "kind": KIND[w]} for w in READERS},
         "gated_readers": list(GATED), "gate": gate_min, "arms": ARM_TEXT, "k": X.K_MAIN, "omp": "signed",
         "dictionary": "the J++ lens's letter-token atoms plus the ten digit tokens (the letter-only restriction lifted)",
         "pointer": {"states_run": R.STATES[target], "basis": "x0_massmean.subspaces Alf (layout-free class means of the locker slot), not refit"},
         "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at the part's share of ||change||^2",
         "change": "h_S - h_O at the bridge word at L on each reader's own prompt; in the question-last order the four prompts share the prefix through the bridge word (asserted), so the lookup's change serves all four",
         "read": "X0's chat read: a digit reader with the space token appended, the word reader right after 'Answer:'; switch = the top token is S's answer (the report: S's slot's ordinal); right = O's",
         "lens_read": "JLens.readout of O's bridge-word state at L (full vocabulary, special tokens out): the rank of O's slot's ordinal (best of four spellings) and of its digit; top-5 = rank <= 5",
         "probe": "x0_probe (b), the locker sentence's index, entities held out (the verdict stage, from states.npz)",
         "rule": RULE, "seeds": {"scenes": R.SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED,
                                 "random_subspace": f"{X.SUBSPACE_SEED} + layer"}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    m["ordinal_tokens"] = ordinal_tokens(tok)
    items, counts = build_items(tok, n_gen, orders)
    counts["target"] = target
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    ords = answer_ids(tok)
    ord_read = torch.tensor([ords[w][0] for w in ORDINALS], device=model.device)
    cand = {w: ord_read if KIND[w] == "word" else digits for w in READERS}
    comp = competence(model, items, orders, ws, cand)
    X.write_jsonl(out / "competence.jsonl", comp)
    gate, chosen = gate_of(items, comp, orders, gate_min, n_items)
    (out / "gate.json").write_text(json.dumps({"dropped": counts["dropped"], "gate": gate}, indent=2) + "\n")
    print(json.dumps({"gate": gate}), flush=True)
    tested = [o for o in orders if chosen[o]]
    m["orders_tested"] = tested
    if not tested:
        m["not_tested"] = {o: gate[o]["failed"] or "no eligible item" for o in orders}
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print(f"not tested: the gate failed in every order ({m['not_tested']}); see gate.json", flush=True)
        return out

    letters = model.letter_token_ids()
    atom_ids = dictionary_ids(letters, digits.to(letters.device))
    lens = JLens(model, "jpp")
    jdic = lens.vectors(layer, atom_ids)
    atom_list = [int(t) for t in atom_ids.tolist()]
    m["dictionary_atoms"] = atom_report(tok, atom_list, [int(d) for d in digits.tolist()])
    ord_atoms = {v["atom"] for w in m["dictionary_atoms"]["ordinal_atoms"].values() for v in w.values()
                 if v and v["atom"] is not None}  # fmt: skip
    dig_atoms = {a for a in m["dictionary_atoms"]["digit_atoms"].values() if a is not None}
    slot_digits = {str(i + 1): S.answer_token(tok, str(i + 1), "digit") for i in range(3)}
    special = sorted(model.special_ids)
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device=jdic.device)
    m["pointer"]["rank"] = int(alf.shape[1])
    basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(jdic.device)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    decode = lambda ids: tok.decode([int(t) for t in ids])  # noqa: E731
    rows, lens_rows, norms, greedy = [], [], [], []
    states: dict[str, list] = collections.defaultdict(list)
    with torch.no_grad():
        for order in tested:
            mine = chosen[order]
            examples = set(example_indices(len(mine)))
            for i, it in enumerate(progress(mine, f"{TEST} {order} at L{layer} (item)")):
                rds = it["orders"][order]["readers"]
                shared = it["orders"][order]["shared_prefix"]
                source = {w: ("lookup" if shared else w) for w in READERS}
                h: dict[str, dict] = {}
                for w in dict.fromkeys(source.values()):
                    rd = rds[w]
                    h[w] = {v: model.run(torch.tensor([rd["ids"][v]], device=model.device), record=(layer,))[1][layer][rd["pos"]]
                            .float().to(jdic.device) for v in ("org", "alt")}  # fmt: skip
                x = torch.stack([h[source[w]]["alt"] - h[source[w]]["org"] for w in READERS])  # [readers, d]
                h_org = torch.stack([h[source[w]]["org"] for w in READERS])
                jpp = X.fit(jdic, x, X.K_MAIN, "signed")
                atoms = XP.omp_atoms(jdic, x, X.K_MAIN)
                ptr = (x @ alf) @ alf.T
                sh = {
                    k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                    for k, v in (("jpp", jpp), ("alf", ptr))
                }
                arms = {"whole": x, "no_jpp": x - jpp, "no_jpp_rand": x - SP.random_subspace_part(x, sh["jpp"], basis),
                        "no_alf": x - ptr, "no_alf_rand": x - SP.random_subspace_part(x, sh["alf"], basis),
                        "keep_alf": ptr, "keep_alf_rand": SP.random_subspace_part(x, sh["alf"], basis)}  # fmt: skip
                assert ("none", *arms) == ARMS
                lens_logits = lens.readout(h_org, layer)  # [readers, vocab]
                for k, w in enumerate(READERS):
                    rd = rds[w]
                    picked = [int(a) for a in atoms[k].tolist()]
                    base = {
                        "scene": it["scene"],
                        "entity": it["entity"],
                        "order": order,
                        "reader": w,
                        "source": source[w],
                    }
                    norms.append({**base, "norm": round(float(x[k].norm()), 4),
                                  **{f"share_{p}": round(float(v[k]), 5) for p, v in sh.items()},
                                  "ordinal_atoms_picked": [decode([atom_list[a]]) for a in picked if a in ord_atoms],
                                  "digit_atoms_picked": [decode([atom_list[a]]) for a in picked if a in dig_atoms]})  # fmt: skip
                    lens_rows.append({**base, **lens_ranks(lens_logits[k], it["slot"], ords, slot_digits,
                                                           rds["lookup"]["tok_A"], special, decode)})  # fmt: skip
                    states[f"{order}__{w}"].append(h_org[k].cpu().numpy())
                    edits = [{}, *({layer: AddRows(arms[a][k : k + 1], [rd["pos"]])} for a in ARMS[1:])]
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", suffix(tok, KIND[w]), ws)
                    for a, lg in zip(ARMS, logits, strict=True):
                        top = int(lg.argmax())
                        rows.append({**base, "domain": it["domain"], "arm": a, "slot_org": it["slot"]["org"],
                                     "slot_alt": it["slot"]["alt"], **X.read_row(lg, rd, cand[w]),
                                     "right": int(top == rd["tok_A"]), "top_text": decode([top])})  # fmt: skip
                    if i in examples:
                        o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                        texts = model.generate_batch(o_ids, X.GEN_TOKENS, edits)
                        greedy += [{**base, "arm": a, "greedy": t} for a, t in zip(ARMS, texts, strict=True)]
            states[f"{order}__scenes"] = [it["scene"] for it in mine]
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "lens.jsonl", lens_rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    blob = {}
    for key, v in states.items():
        if key.endswith("__scenes"):
            blob[key] = np.array(v)
        else:
            hh = np.stack(v)
            blob[key] = hh.astype(np.float16) if np.abs(hh).max() < 6e4 else hh
    np.savez_compressed(out / "states.npz", **blob)
    try:
        ref = R.c0_reference(target)
    except OSError as e:  # the reference run's outcomes are not on this machine: the check is descriptive
        print(f"no C0 reference here ({e})", flush=True)
        ref = None
    c0 = [r["switched"] for r in rows if r["order"] == "last" and r["reader"] == "lookup" and r["arm"] == "whole"]
    rate = float(np.mean(c0)) if c0 else None
    (out / "c0_check.json").write_text(json.dumps({
        "c0_lookup_switch_question_last": rate, "reference": ref, "tolerance": R.C0_TOL,
        "within": None if rate is None or ref is None else bool(abs(rate - ref) <= R.C0_TOL),
        "note": "descriptive here (the routes test's C0 sanity, on the question-last lookup); Muse has no reference"}) + "\n")  # fmt: skip
    m["items"] = {o: len(chosen[o]) for o in orders}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.10 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    mt = re.search(r"^Dan:(.*)$", block, re.M)
    return mt.group(1).strip() if mt else ""


def reader_cells(rows: list[dict], order: str, reader: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One order's and reader's items: each arm's switch rate, X0's cell (Jdep, Rdep, extra loss) for J++ and for U
    against their random parts, only-U minus its random part (paired), and the unedited read's accuracy."""
    by = {
        a: {r["scene"]: r for r in rows if r["order"] == order and r["reader"] == reader and r["arm"] == a}
        for a in ARMS
    }
    scenes = list(by["whole"])
    missing = [(s, a) for s in scenes for a in ARMS if s not in by[a]]
    assert not missing, f"{order} {reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    ents = [by["whole"][s]["entity"] for s in scenes]
    sw = {a: [int(by[a][s]["switched"]) for s in scenes] for a in ARMS}
    rr = X.resampled_rates(sw, ents, n_boot)
    out: dict[str, Any] = {"n": len(scenes), "entities": len(set(ents)), "switches_whole": int(sum(sw["whole"])),
                           "rate": {a: [float(np.mean(sw[a])), *X.interval(rr[a])] for a in ARMS},
                           "right_unedited": float(np.mean([by["none"][s]["right"] for s in scenes]))}  # fmt: skip
    for part, no, rand in PARTS:
        c = X.cell({"whole": sw["whole"], "no_part": sw[no], "no_rand": sw[rand]}, ents, n_boot)
        out[part] = {k: c[k] for k in ("Jdep", "Rdep", "excess", "valid")}
    out["keep_alf_minus_rand"] = [float(np.mean(sw["keep_alf"]) - np.mean(sw["keep_alf_rand"])),
                                  *X.interval(rr["keep_alf"] - rr["keep_alf_rand"])]  # fmt: skip
    return out


def lens_shares(lens_rows: list[dict], order: str, reader: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One order's and reader's items: the share with the correct ordinal (digit) in the lens's top-5, the share with
    it first among the three ordinals (ten digits), with cluster-bootstrap CIs, and median ranks."""
    mine = [r for r in lens_rows if r["order"] == order and r["reader"] == reader]
    assert mine, f"{order} {reader}: no lens rows"
    ents = [r["entity"] for r in mine]
    flags = {"top5_ordinal": [int(r["top5_ordinal"]) for r in mine], "top5_digit": [int(r["top5_digit"]) for r in mine],
             "first_among_ordinals": [int(r["rank_ordinal_among3"] == 1) for r in mine],
             "first_among_digits": [int(r["rank_digit_among_digits"] == 1) for r in mine],
             "top5_ordinal_of_S": [int(r["rank_ordinal_alt"] <= TOP) for r in mine],
             "top5_value_digit": [int(r["rank_value_digit"] <= TOP) for r in mine]}  # fmt: skip
    rr = X.resampled_rates(flags, ents, n_boot)
    return {"n": len(mine), **{k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in flags.items()},
            "median_rank_ordinal": statistics.median(r["rank_ordinal"] for r in mine),
            "median_rank_digit": statistics.median(r["rank_digit"] for r in mine),
            "source": mine[0]["source"]}  # fmt: skip


def probe_control(src: Path, order: str, reader: str, items: dict[str, dict], n_boot: int = X.N_BOOT) -> dict | None:
    """The slot probe (x0_probe (b), the locker sentence's index, entities held out) on the order's and reader's
    bridge-word states; None without them."""
    from scripts import x0_probe as PR

    z = np.load(src / "states.npz")
    key = f"{order}__{reader}"
    if key not in z:
        return None
    scenes = [str(s) for s in z[f"{order}__scenes"]]
    h = z[key].astype(np.float64)
    assert len(scenes) == h.shape[0], f"{key}: {h.shape[0]} states for {len(scenes)} scenes"
    probe_items = [{"scene": s, "entity": items[s]["entity"], "locker_index": items[s]["slot"]["org"],
                    "pick_index": items[s]["pick_index"], "layout": PR.layout(items[s]["context"], items[s]["pick_index"])}
                   for s in scenes]  # fmt: skip
    r = PR.score(h, probe_items, "locker sentence", n_boot)
    return {k: r[k] for k in ("n", "entities", "classes", "chance", "probe", "majority", "structure", "layout",
                              "best_baseline", "probe_minus_best") if k in r}  # fmt: skip


def rule(lens_report: float, lens_lookup: float, report_jpp: float, lookup_jpp: float, report_alf: float,
         gate_ok: bool, n_switches: dict[str, int] | None = None) -> dict[str, Any]:  # fmt: skip
    """47.10's two labels on one order's point estimates (lens_*: the share of items with the correct ordinal in the
    lens's top-5 under that reader's prompt; *_jpp / *_alf: the reader's extra loss without the part beyond random).
    Not tested if the gate failed or (n_switches given) the report's or the lookup's whole change switches fewer than
    MIN_SWITCHES items."""
    if not gate_ok:
        return {"label": "not tested", "why": "the gate failed"}
    few = {w: n for w, n in (n_switches or {}).items() if n < MIN_SWITCHES}
    if few:
        return {"label": "not tested", "why": f"the whole change switches fewer than {MIN_SWITCHES}: {few}"}
    surfaced = {"lens_report": lens_report >= SURF_LENS - EPS, "lens_lookup": lens_lookup <= SURF_LENS_OTHER + EPS,
                "report_jpp": report_jpp >= SURF_REPORT - EPS, "lookup_jpp": lookup_jpp <= SURF_LOOKUP + EPS}  # fmt: skip
    late = {"lens_report": lens_report <= LATE_LENS + EPS, "report_jpp": report_jpp <= LATE_JPP + EPS,
            "report_alf": report_alf >= LATE_U - EPS}  # fmt: skip
    label = "surfaced" if all(surfaced.values()) else "late" if all(late.values()) else "neither"
    return {"label": label, "surfaced": surfaced, "late": late,
            "why": f"lens top-5: report {lens_report:.2f}, lookup {lens_lookup:.2f}; extra loss without J++: report "
                   f"{report_jpp:.2f}, lookup {lookup_jpp:.2f}; report without U {report_alf:.2f}"}  # fmt: skip


def order_result(src: Path, order: str, rows: list[dict], lens_rows: list[dict], gate: dict, items: dict[str, dict],
                 n_boot: int = X.N_BOOT) -> dict[str, Any]:  # fmt: skip
    """One run's order: the gate, each reader's cells and lens shares, the probe, the rule."""
    g = gate[order]
    if not g["pass"] or not any(r["order"] == order for r in rows):
        return {"order": order, "gate": g, "rule": {"label": "not tested", "why": f"gate failed for {g['failed']}"
                                                    if g["failed"] else "no items run"}}  # fmt: skip
    readers = {w: reader_cells(rows, order, w, n_boot) for w in READERS}
    lens = {w: lens_shares(lens_rows, order, w, n_boot) for w in READERS}
    probes = {w: probe_control(src, order, w, items, n_boot) for w in ("lookup", "report")}
    r = rule(lens["report"]["top5_ordinal"][0], lens["lookup"]["top5_ordinal"][0], readers["report"]["jpp"]["excess"][0],
             readers["lookup"]["jpp"]["excess"][0], readers["report"]["alf"]["excess"][0], True,
             {w: readers[w]["switches_whole"] for w in ("report", "lookup")})  # fmt: skip
    return {"order": order, "gate": g, "readers": readers, "lens": lens, "probe": probes, "rule": r}


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending (not here), not tested (the gate), or its orders' results."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "gate.json").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.10 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or gate here"}
    m = json.loads((src / "manifest.json").read_text())
    gate = json.loads((src / "gate.json").read_text())["gate"]
    items = {it["scene"]: it for it in X.read_jsonl(src / "cases.jsonl")}
    rows = X.read_jsonl(src / "outcomes.jsonl") if (src / "outcomes.jsonl").exists() else []
    lens_rows = X.read_jsonl(src / "lens.jsonl") if (src / "lens.jsonl").exists() else []
    norms = X.read_jsonl(src / "norms.jsonl") if (src / "norms.jsonl").exists() else []
    orders = {o: order_result(src, o, rows, lens_rows, gate, items, n_boot) for o in m["orders"]}
    picked = {o: {w: {"ordinal": float(np.mean([bool(n["ordinal_atoms_picked"]) for n in norms if n["order"] == o and n["reader"] == w] or [0])),
                      "digit": float(np.mean([bool(n["digit_atoms_picked"]) for n in norms if n["order"] == o and n["reader"] == w] or [0]))}
                  for w in READERS} for o in m["orders"]}  # fmt: skip
    c0 = json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else None
    status = "tested" if any(o["rule"]["label"] not in ("not tested",) for o in orders.values()) else "not tested"
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "status": status, "orders": orders,
            "dictionary_atoms": {k: m.get("dictionary_atoms", {}).get(k) for k in ("atoms", "ordinal_atoms_present", "ordinal_spellings_absent", "digit_atoms")},
            "atoms_picked_share": picked, "c0_check": c0, "plan": json.loads((src / "plan.json").read_text()),
            "ordinal_tokens": m.get("ordinal_tokens")}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [mm["target"] for mm in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"} for t in RUNS
               if t not in targets]  # fmt: skip
    out = RESULTS / f"x47_10-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.10: report the address (on-demand surfacing into the J-space)", "",
             f"Batch 47, amendment 4, test {TEST} (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). Routes C0 scenes, "
             "four readers as separate prompts over the same context, two question orders; the change at the bridge "
             "word at the layer fixed in advance. Extra loss = Jdep − Rdep over the order's items; cluster bootstrap "
             f"over bridge items ({n_boot}, seed {X.BOOT_SEED}). Point estimates decide. UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}", "",
             "| model | order | status | n | lens top-5 ordinal: report | lookup | report: extra loss without J++ | "
             "without U | lookup: without J++ | recall: without J++ | label |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] == "pending":
            lines.append(f"| {mm['target']} | - | pending ({mm['why']}) | | | | | | | | |")
            continue
        for o, res in mm["orders"].items():
            r = res["rule"]
            if "readers" not in res:
                lines.append(f"| {mm['target']} | {o} | not tested ({r['why']}) | | | | | | | | {LABELS[r['label']]} |")
                continue
            rd, ln = res["readers"], res["lens"]
            lines.append(f"| {mm['target']} | {o} | {r['label'] if r['label'] == 'not tested' else 'tested'} | "
                         f"{rd['report']['n']} | {fmt(ln['report']['top5_ordinal'])} | {fmt(ln['lookup']['top5_ordinal'])} | "
                         f"{fmt(rd['report']['jpp']['excess'])} | {fmt(rd['report']['alf']['excess'])} | "
                         f"{fmt(rd['lookup']['jpp']['excess'])} | {fmt(rd['recall']['jpp']['excess'])} | "
                         f"**{LABELS[r['label']]}**" + ("" if r["label"] != "not tested" else f" ({r['why']})") + " |")  # fmt: skip
    lines += ["", "Per order and reader: switch rate per arm, and X0's cells (Jdep = switches lost without the part, "
              "Rdep = without its random part, extra loss = Jdep − Rdep); only U minus its random part (paired).", "",
              "| model | order | reader | n (switches, whole) | " + " | ".join(ARMS[1:]) + " | J++: Jdep | Rdep | extra "
              "| U: Jdep | Rdep | extra | only U − random |", "|---|---|---|---|" + "---|" * (len(ARMS) - 1 + 7)]  # fmt: skip
    for mm in models:
        if mm["status"] == "pending":
            continue
        for o, res in mm["orders"].items():
            for w, c in res.get("readers", {}).items():
                lines.append(f"| {mm['target']} | {o} | {w} | {c['n']} ({c['switches_whole']}) | "
                             + " | ".join(fmt(c["rate"][a]) for a in ARMS[1:]) + " | "
                             + " | ".join(fmt(c[p][k]) for p in ("jpp", "alf") for k in ("Jdep", "Rdep", "excess"))
                             + f" | {fmt(c['keep_alf_minus_rand'])} |")  # fmt: skip
    lines += ["", "The lens at the bridge word (O's state at L, under each reader's own prompt; in the question-last "
              "order the four prompts share the state): the share of items with the correct ordinal / slot digit in the "
              "lens's top-5, first among the three ordinals / ten digits, median ranks; the slot probe (x0_probe (b), "
              "entities held out) beside.", "",
              "| model | order | reader | n | top-5 ordinal | top-5 digit | first of 3 ordinals | first of 10 digits | "
              "median rank ordinal / digit | top-5 value digit | slot probe (best baseline) |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] == "pending":
            continue
        for o, res in mm["orders"].items():
            for w, ln in res.get("lens", {}).items():
                p = res["probe"].get(w)
                probe = (
                    f"{fmt(p['probe'])} ({p['best_baseline']} {fmt(p[p['best_baseline']]) if p['best_baseline'] != 'chance' else p['chance']})"
                    if p
                    else "-"
                )
                lines.append(f"| {mm['target']} | {o} | {w} | {ln['n']} | {fmt(ln['top5_ordinal'])} | {fmt(ln['top5_digit'])} | "
                             f"{fmt(ln['first_among_ordinals'])} | {fmt(ln['first_among_digits'])} | "
                             f"{ln['median_rank_ordinal']} / {ln['median_rank_digit']} | {fmt(ln['top5_value_digit'])} | {probe} |")  # fmt: skip
    lines += ["", "Gates (read accuracy on the unedited O prompts, per reader on its own prompt; the report readers also "
              "by the true slot of the asked item's locker: dumbest way 1), items, the dictionary's ordinal atoms "
              "(dumbest way 2), the share of items whose 25 atoms include an ordinal / digit atom, the C0 check:", ""]  # fmt: skip
    for mm in models:
        if mm["status"] == "pending":
            continue
        for o, res in mm["orders"].items():
            g = res["gate"]
            by_slot = {
                w: {s: ("-" if v[0] is None else f"{v[0]:.2f}") + f" (n={v[1]})" for s, v in d.items()}
                for w, d in g["report_read_accuracy_by_true_slot"].items()
            }
            lines.append(f"- {mm['target']} ({mm['run']}, L{mm['layer']}), {o}: gate {g['org_read_accuracy']} "
                         f"(pass {g['pass']}; failed {g['failed'] or 'none'}); report by slot {by_slot}; eligible "
                         f"{g['eligible']} of {g['items']}, chosen {g['chosen']}; atoms picked {mm['atoms_picked_share'].get(o)}")  # fmt: skip
        d = mm["dictionary_atoms"]
        lines.append(f"- {mm['target']}: dictionary {d['atoms']} atoms; ordinal atoms present {d['ordinal_atoms_present']}; "
                     f"absent {d['ordinal_spellings_absent'] or 'none'}; digit atoms {d['digit_atoms']}; C0 check {mm['c0_check']}; "
                     f"plan {mm['plan'].get('dropped')}")  # fmt: skip
    lines += ["", "The rule is applied per order. In the question-last order the lens clause cannot separate the "
              "readers (one state); the question-first order is where surfacing on demand can show. Which order "
              "answers Q47.10 is Dan's call (the spec's as-computed paragraph)."]  # fmt: skip
    (out / "x47_10.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "x47_10.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- view and figures (CPU) ---------------------------------------------------------------------------------------


def stage_view(name: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> Path:
    """The verify-pack view: k random items of each tested order (seed 0): every reader's O prompt as the model reads
    it (the bridge word in ⟦...⟧, the read suffix appended), S's prompt, each arm's answer and switch, the greedy
    text where recorded, and the lens's top-20 at the bridge word with the ranks."""
    assert dan_answer(), f"sealed: {PREDICTIONS} has no committed answer to {QUESTION}"
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    items = X.read_jsonl(src / "cases.jsonl")
    by_scene = {it["scene"]: it for it in items}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    reads = {(r["scene"], r["order"], r["reader"], r["arm"]): r for r in rows}
    lens = {(r["scene"], r["order"], r["reader"]): r for r in X.read_jsonl(src / "lens.jsonl")}
    greedy = {
        (g["scene"], g["order"], g["reader"], g["arm"]): g["greedy"]
        for g in X.read_jsonl(src / "examples_greedy.jsonl")
    }
    out = src / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# 47.10 view: {name}", "", f"Model {m['model']['target']}, layer {m['layer']}. Prompts exactly as the "
             "model reads them (ids decoded, the template included); ⟦...⟧ the bridge word where the change is added; "
             "the read suffix appended (a space token for a digit reader, nothing for the word reader). UNVERIFIED.", ""]  # fmt: skip
    for order in m.get("orders_tested", []):
        scenes = list(dict.fromkeys(r["scene"] for r in rows if r["order"] == order))
        picked = [scenes[i] for i in example_indices(len(scenes), k, seed)]
        lines += [f"## {ORDER_TEXT[order]}: {len(picked)} random items of {len(scenes)} (seed {seed})", ""]
        for s in picked:
            it = by_scene[s]
            lines += [f"### {s}: bridge {it['entity']} (slot {it['slot']['org'] + 1}) → {it['cf_bridge']} "
                      f"(slot {it['slot']['alt'] + 1})", ""]  # fmt: skip
            for w in READERS:
                rd = it["orders"][order]["readers"][w]
                suf = " " if KIND[w] == "digit" else ""
                ln = lens[(s, order, w)]
                lines += [f"**{w}** ({KIND[w]}): O answers {rd['answer']!r}, S answers {rd['cf_answer']!r}; lens at the "
                          f"bridge word: ordinal rank {ln['rank_ordinal']} (among 3: {ln['rank_ordinal_among3']}), "
                          f"digit rank {ln['rank_digit']}; top-20 {ln['top20']}", "", "O, as read:", "", "```",
                          R.marked(decode, rd["ids"]["org"], rd["pos"]) + suf, "```", "", "S (the source):", "", "```",
                          R.marked(decode, rd["ids"]["alt"], rd["pos"]) + suf, "```", "",
                          "| arm | what | top token | switched | right | greedy |", "|---|---|---|---|---|---|"]  # fmt: skip
                for a in ARMS:
                    r = reads[(s, order, w, a)]
                    lines.append(f"| {a} | {ARM_TEXT[a]} | {r['top_text']!r} | {r['switched']} | {r['right']} | "
                                 f"{greedy.get((s, order, w, a))!r} |")  # fmt: skip
                lines.append("")
    (out / "examples.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def stage_figures(verdict_dir: Path) -> list[Path]:
    """One figure per model from a verdict folder: per order, each reader's extra loss without J++ and without U
    (bars with 95% intervals), and the share of items with the correct ordinal in the lens's top-5 under each
    reader's prompt: the same address, two consumers."""
    assert dan_answer(), f"sealed: {PREDICTIONS} has no committed answer to {QUESTION}"
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    blob = json.loads((verdict_dir / "x47_10.json").read_text())
    paths = []
    for mm in blob["models"]:
        orders = [o for o, r in mm.get("orders", {}).items() if "readers" in r]
        if not orders:
            continue
        fig, axes = plt.subplots(2, len(orders), figsize=(5 * len(orders), 7), squeeze=False)
        for j, o in enumerate(orders):
            res = mm["orders"][o]
            xs = np.arange(len(READERS))
            for d, (part, label) in enumerate((("jpp", "without J++"), ("alf", "without U"))):
                v = [res["readers"][w][part]["excess"] for w in READERS]
                pts = [x[0] if x[0] == x[0] else 0.0 for x in v]
                err = [
                    [max(0.0, x[0] - x[1]) if x[0] == x[0] else 0 for x in v],
                    [max(0.0, x[2] - x[0]) if x[0] == x[0] else 0 for x in v],
                ]
                axes[0, j].bar(xs + (d - 0.5) * 0.38, pts, 0.38, yerr=err, capsize=3, label=label)
            axes[0, j].axhline(0, color="black", lw=0.8)
            axes[0, j].set_xticks(xs, READERS)
            axes[0, j].set_title(f"{mm['target']} L{mm['layer']}, {o}: {LABELS[res['rule']['label']]}")
            axes[0, j].set_ylabel("extra loss of the switch")
            axes[0, j].legend(fontsize=8)
            v = [res["lens"][w]["top5_ordinal"] for w in READERS]
            axes[1, j].bar(
                xs,
                [x[0] for x in v],
                0.5,
                yerr=[[x[0] - x[1] for x in v], [x[2] - x[0] for x in v]],
                capsize=3,
                color="tab:gray",
            )
            axes[1, j].axhline(SURF_LENS, color="tab:red", lw=0.8, ls="--")
            axes[1, j].axhline(SURF_LENS_OTHER, color="tab:blue", lw=0.8, ls=":")
            axes[1, j].set_xticks(xs, READERS)
            axes[1, j].set_ylim(0, 1)
            axes[1, j].set_ylabel("lens: correct ordinal in top-5 (share)")
        fig.tight_layout()
        p = verdict_dir / f"x47_10_{mm['run'].strip('()')}.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)
    print("wrote", *paths)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view", "figures"])
    ap.add_argument("--name", help="run / view: the run name (results/x47_report/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 47.10 runs (9B, 27B, Muse)")
    ap.add_argument("--why", default=f"batch 47, test {TEST} (jobs/c3/batch47.yaml; {QUESTION})")
    ap.add_argument("--orders", default=",".join(ORDERS), help="run: the question orders, comma-separated (last,first)")
    ap.add_argument("--n-gen", type=int, default=N_GEN, help="run / plan: C0 scenes generated")
    ap.add_argument("--n-items", type=int, default=N_ITEMS, help="run: the first eligible items kept per order")
    ap.add_argument("--verdict", type=Path, help="figures: the verdict folder")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.n_gen)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        orders = tuple(o for o in a.orders.split(",") if o)
        assert set(orders) <= set(ORDERS), f"--orders {orders}: of {ORDERS}"
        assert len(set(orders)) == len(orders), f"--orders {orders}: an order twice"
        stage_run(a.name, a.why, orders, a.n_gen, a.n_items)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    elif a.stage == "view":
        assert a.name, "view needs --name"
        stage_view(a.name)
    else:
        assert a.verdict, "figures needs --verdict"
        stage_figures(a.verdict)


if __name__ == "__main__":
    main()
