"""code_pointer_v1: pointer_v1's three-way dissociation patch in Python code, where pointers are literal (Dan's D3,
2026-10-21; the animal/locker scenes read as too toy). When a lookup's key must first be found, what do the question
tokens carry in transit: the key's identity, a pointer to the dict entry that binds it (its position), or the value?

Background (UNVERIFIED; scripts/pointer_v1.py's docstring, EXPERIMENTS.md rows 27, 32, 37, 52): on Qwen3.6-27B, copying
the counterfactual's question-token residual at layers 44-52 flips RL 98-100% while the J-lens direction flips it 0%.
pointer_v1 asks what that copy carries (H-word / H-pointer / H-value). Code makes the pointer concrete (a list index, a
variable naming another variable, a dict entry) and suite_v1's CODE family (a two-dict lookup, "What does this Python
code print?") is answered 100% by the 27B in chat format.

A scene: N keys of one domain (N = 5 main; 3 and 8 dev), each bound to a digit 0-9 by one entry of one dict line,
`lockers = {"cow": 5, "dog": 3, ...}`, entries in a seeded order (the entries are pointer_v1's statements). The dict
is the first code line in every family, so its entries sit at the same tokens; the families differ in how the key is
found (plain names in reports: "where the bridge comes from -> where the answer comes from"):
  DK   named -> prompt:              print(lockers["cow"])
  IX   list position -> prompt:      names = ["dog", "cow", ...] (all N keys); print(lockers[names[1]])
  CH2  2-variable chain -> prompt:   w = "cow"; k = "dog"; h = w; q = k (a distractor chain); print(lockers[h])
  CH3  3-variable chain -> prompt:   the same with three variables per chain, lines interleaved in a seeded order
  RK   memory -> prompt:             no print; "What number does lockers store for the animal known for mooing?"
  RR   memory -> memory:             RK's code; "How many legs does the animal known for mooing have?" (contrast)

Prompt (suite_v1's chat format, character for character the suite's CODE layout): one user turn
"<context>\\n<question> <instruction>", thinking off, "Answer:" prefilled. context = "```python\\n" + the code lines up to
the query; question = the query and what follows it: "print(...)\\n```\\nWhat does this Python code print?" (DK, IX,
CH) or "```\\n<question>" (RK, RR). So pointer_swap's groups mean what they mean on pointer_v1 (question = the query
line, the closing fence and the question; final = everything after), and only entries, selector lines (IX's list, CH's
chain) and the question differ between a base and its sources; the template never does.

Sources (each token-aligned with the base: same length, entries, list items, chain lines and question at the same
tokens). As in pointer_v1, the base queries q_b at dict slot a; "dissoc" queries q_s (which the base binds at slot c)
and puts q_s at slot k of its own dict with a digit absent from the base (the value), where the base has p; its other
entries are reshuffled and redigited. DK and RK name q_s in the question; IX's dissoc list has q_s at the queried index
i (the question is the base's, token for token); CH's dissoc chain has q_s at the head of the printed chain (variable
names, line order and the distractor chain unchanged). Predictions, the same four on every lookup family of a scene:
  none d_b(q_b)   identity d_b(q_s)   position d_b(p) (the base digit at slot k)   value d_s(q_s)
RR: rec(q_b), rec(q_s), rec(p); value = identity by construction. IX's index i is the same in base and source, so a
pointer to the list slot predicts "none"; CH's variables and line order are the same, so a pointer to the chain's
lines predicts "none". The digit the distractor chain would give, d_b(r), is recorded (item["code"]).

Controls in the data (as pointer_v1): "same" (q_b at slot a with its digit; the other entries reshuffled and
redigited; IX's list reshuffled with q_b kept at i; CH's distractor head redrawn): every hypothesis predicts the base
answer, so a change is damage. "redigit" (the base program with q_b's digit replaced by the value): only H-value
predicts a change. Run-time controls are pointer_swap's (matched-norm random direction, another domain's item).

Digits 0-9 (single tokens). IX's index i is never a lookup digit of the scene (base or source), so a copied index is
never a prediction. Recalled-digit collisions as pointer_v1: hard (no lookup digit equals rec(q_b), rec(q_s), rec(p)),
soft where the pool allows (no lookup digit equals any scene key's recalled digit); "none" at N = 8, which needs 9 of
the 10 digits (there RR's predictions and RK's recall answers also occur as lookup digits; recorded in "collisions").
Slots (a, k) cycle through all ordered pairs of distinct slots, and i through 0..N-1, in seeded blocks.

Domains (keys must be one token inside quotes, with no leading space; checked by make/check): animals = pointer_v1's
animals that are one token there (dog, cat, frog, cow, horse, mouse, wolf, pig, lion, duck, bee; sheep, goose, chicken,
turkey and spider are two) plus owl ("hooting"), legs recalled; months = pointer_v1's seven, number in the calendar
recalled (planets and elements: one single-token key each). Cues and RR/hop wording are pointer_v1's. Animals have nine
4-legged keys, so RR's distinct-legs rule (pointer_v1's pick_entities) puts duck, owl or bee in a critical role in most
scenes (main: p is bee in 244 of 400; check_<set>.json counts the roles). N = 8 exists for animals only (seven months),
so pointer_swap's "other" control (another domain's item) has no other domain there. At N = 3 the distractor chain's
head can only be p, so CH's "position" prediction is also what following the distractor chain gives.

Spans (D1/D2): item["spans"] and every source's "spans", [start, end) char offsets in the user turn's content
(context + "\\n" + question + " " + instruction; in a rendered prompt add text.index(content)): code (the fenced block),
entries (dict order), list (IX, list order), chain (CH, line order), query (the print line; RK/RR: the cue),
question (= item["question"]), nl_question (the natural-language sentence), tail (the instruction; a rendered prompt
continues with the chat template's assistant prefix and "Answer:").

Sets (each (set, level, domain) has its own seed): main N = 5, 400 scenes per domain, seed 721; dev (pilot, never a
headline) N = 3 and N = 8 (animals only), 60 scenes per cell, seed 722. Files:
data/code_pointer_v1/<set>/<domain>_<family>_<level>.json, one item per line (pointer_v1's item schema plus "spans" and
"code"; levels keep pointer_v1's e<N>f0 names so pointer_swap's N = int(level[1]) holds).

Gate (competence; fixed before any 27B run, jobs/d3/code_competence_27b.yaml): a (domain, family) cell enters the
patching runs iff its clean Wilson 95% lower bound >= 0.85 (suite_v1's rule); an item is eligible iff every prompt of
it is right (base, dissoc, same, redigit, hop1, hop2).

Stages:  make --set S (write-once; tokenizer only)   verify (regenerates every set, must equal its files)
         check --set S (tokenizer only: alignment, single-token keys, spans, execution, predictions, collisions)
         manifest --set S [S ...] --name N --why W [--limit K]
         competence --name N (GPU: every prompt unedited; greedy 8 tokens and the answer read, as pointer_v1)
         examples --name N [--k 3] [--seed 0]   figures --name N (per-family accuracy, a new analysis-<stamp>/)
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import io
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "code_pointer_v1"
DATA = pins.DATA_DIR / EXP
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("DK", "IX", "CH2", "CH3", "RK", "RR")
FAMILY_LABEL = {  # display rule (user, 2026-10-21): where the bridge comes from -> where the answer comes from
    "DK": "named → prompt",
    "IX": "list position → prompt",
    "CH2": "2-variable chain → prompt",
    "CH3": "3-variable chain → prompt",
    "RK": "memory → prompt",
    "RR": "memory → memory",
}
CHAIN_DEPTH = {"CH2": 2, "CH3": 3}
SOURCES = PV.SOURCES
HYPOTHESES = PV.HYPOTHESES
DIGITS = tuple(range(10))
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 721, "n": 400, "levels": {"e5f0": 5}},
    "dev": {"seed": 722, "n": 60, "levels": {"e3f0": 3, "e8f0": 8}},
}
DICT, LIST = "lockers", "names"
FENCE_OPEN, FENCE_CLOSE = "```python\n", "```"
NL_PRINT = S.WORDINGS["A"]["CODE"]  # "What does this Python code print?"
VARS = tuple("abcdefghjkmnpqrstuvwxyz")  # chain variables: one letter, no i / l / o
INSTRUCTION = S.INSTRUCTION

# ---- domains --------------------------------------------------------------------------------------------------------
ANIMALS = {
    a: PV.ANIMALS[a] for a in ("dog", "cat", "frog", "cow", "horse", "mouse", "wolf", "pig", "lion", "duck", "bee")
}
ANIMALS["owl"] = (2, "hooting")
DOMAINS: dict[str, dict[str, Any]] = {
    "animals": {
        "entities": ANIMALS,
        # "number", not "value": the 0.8B smoke read "What value does lockers hold for ..." as asking for the key
        "RK": "What number does lockers store for the animal known for {cue}?",
        "RR": PV.DOMAINS["animals"]["RR"],
        "hop_cue": PV.DOMAINS["animals"]["hop_cue"],
        "hop_recall": "How many legs does {a_e} have?",  # pointer_v1's, with "an" before a vowel (owl)
    },
    "months": {
        "entities": dict(PV.MONTHS),
        "RK": "What number does lockers store for {cue}?",
        "RR": PV.DOMAINS["months"]["RR"],
        "hop_cue": PV.DOMAINS["months"]["hop_cue"],
        "hop_recall": PV.DOMAINS["months"]["hop_recall"],
    },
}


def rec(domain: str, e: str) -> int:
    return DOMAINS[domain]["entities"][e][0]


def cue(domain: str, e: str) -> str:
    return DOMAINS[domain]["entities"][e][1]


def hop_recall(domain: str, e: str) -> str:
    a_e = ("an " if e[0].lower() in "aeiou" else "a ") + e
    return DOMAINS[domain]["hop_recall"].format(e=e, a_e=a_e)


# ---- scenes ---------------------------------------------------------------------------------------------------------


def index_plan(rng: random.Random, n: int, n_ent: int) -> list[int]:
    """IX's queried list index per scene, cycling through 0..N-1 in seeded blocks."""
    out: list[int] = []
    while len(out) < n:
        block = list(range(n_ent))
        rng.shuffle(block)
        out += block
    return out[:n]


def pick_entities(rng: random.Random, domain: str, n_ent: int) -> tuple[str, str, str, list[str]]:
    """pointer_v1's rule on this domain's pool: q_b and q_s with different recalled digits, p with a recalled digit
    unlike both when the pool has one, and n_ent - 3 more."""
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


def digit_pool(domain: str, scene: list[str], critical: list[str], n_ent: int, index: int) -> tuple[list[int], str]:
    """The lookup digits a scene may use and the collision policy that applied (docstring); never IX's index."""
    base = [d for d in DIGITS if d != index]
    soft = [d for d in base if d not in {rec(domain, e) for e in scene}]
    if len(soft) >= n_ent + 1:
        return soft, "soft"
    hard = [d for d in base if d not in {rec(domain, e) for e in critical}]
    if len(hard) >= n_ent + 1:
        return hard, "hard"
    assert len(base) >= n_ent + 1, f"{domain}: not enough lookup digits for {n_ent} entries"
    return base, "none"


def merge_order(rng: random.Random, depth: int) -> list[list[Any]]:
    """A seeded interleaving of the target and distractor chains' assignments, each chain's lines in order."""
    left = {"target": 0, "distractor": 0}
    out: list[list[Any]] = []
    while len(out) < 2 * depth:
        ch = rng.choice([c for c in ("target", "distractor") if left[c] < depth])
        out.append([ch, left[ch]])
        left[ch] += 1
    return out


def make_scene(rng: random.Random, domain: str, n_ent: int, a: int, k: int, ix: int) -> dict[str, Any]:
    """One scene: pointer_v1's dict scene (base, dissoc, same, redigit), IX's lists and CH's chains for each."""
    q_b, q_s, p, more = pick_entities(rng, domain, n_ent)
    c = rng.choice([s for s in range(n_ent) if s not in (a, k)])
    order: list[str] = [""] * n_ent
    order[a], order[k], order[c] = q_b, p, q_s
    free = [s for s in range(n_ent) if not order[s]]
    for s, e in zip(free, rng.sample(more, len(more)), strict=True):
        order[s] = e
    pool, policy = digit_pool(domain, order, [q_b, q_s, p], n_ent, ix)
    digits = rng.sample(pool, n_ent)
    value = rng.choice([d for d in pool if d not in digits])
    others = rng.sample([e for e in order if e != q_s], n_ent - 1)
    s_order = list(others)
    s_order.insert(k, q_s)
    s_digits = rng.sample([d for d in pool if d != value], n_ent - 1)
    s_digits.insert(k, value)
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

    def with_at(e: str) -> list[str]:
        out = rng.sample([x for x in order if x != e], n_ent - 1)
        out.insert(ix, e)
        return out

    base_list = with_at(q_b)
    dissoc_list = with_at(q_s)
    while True:
        same_list = with_at(q_b)
        if same_list != base_list:
            break
    letters = rng.sample(VARS, 6)
    r = rng.choice([e for e in order if e not in (q_b, q_s, p)] or [p])  # the distractor chain's head
    r_same = rng.choice([e for e in order if e not in (q_b, r)])
    merges = {d: merge_order(rng, d) for d in (2, 3)}
    return {
        "q_b": q_b, "q_s": q_s, "p": p, "slots": {"query": a, "identity": c, "position": k}, "index": ix,
        "order": order, "digits": digits, "value": value, "policy": policy,
        "dicts": {"base": (order, digits), "dissoc": (s_order, s_digits), "same": (m_order, m_digits),
                  "redigit": (list(order), r_digits)},
        "lists": {"base": base_list, "dissoc": dissoc_list, "same": same_list, "redigit": list(base_list)},
        "vars": {"target": letters[:3], "distractor": letters[3:]}, "merges": merges,
        "heads": {"base": [q_b, r], "dissoc": [q_s, r], "same": [q_b, r_same], "redigit": [q_b, r]},
    }  # fmt: skip


# ---- programs and spans ---------------------------------------------------------------------------------------------


class Doc:
    """A string built piece by piece, returning each piece's [start, end) span."""

    def __init__(self) -> None:
        self.text = ""

    def add(self, s: str) -> list[int]:
        a = len(self.text)
        self.text += s
        return [a, len(self.text)]


def content_of(context: str, question: str) -> str:
    """The user turn's text, as suite_v1.render puts it in the chat template."""
    return f"{context}\n{question} {INSTRUCTION}"


def chain_lines(fam: str, sc: dict, which: str) -> list[str]:
    depth = CHAIN_DEPTH[fam]
    heads = dict(zip(("target", "distractor"), sc["heads"][which], strict=True))
    out = []
    for ch, j in sc["merges"][depth]:
        v = sc["vars"][ch]
        out.append(f'{v[j]} = "{heads[ch]}"' if j == 0 else f"{v[j]} = {v[j - 1]}")
    return out


def print_query(fam: str, sc: dict, query: str) -> str | None:
    """The print line of a print family (None for RK, RR)."""
    if fam == "DK":
        return f'print({DICT}["{query}"])'
    if fam == "IX":
        return f"print({DICT}[{LIST}[{sc['index']}]])"
    if fam in CHAIN_DEPTH:
        return f"print({DICT}[{sc['vars']['target'][CHAIN_DEPTH[fam] - 1]}])"
    return None


def nl_question(fam: str, domain: str, query: str) -> tuple[str, str | None]:
    """(the natural-language question, its cue) for a family; the print families ask the suite's CODE question."""
    if fam in ("RK", "RR"):
        c = cue(domain, query)
        return DOMAINS[domain][fam].format(cue=c), c
    return NL_PRINT, None


def program(fam: str, domain: str, sc: dict, which: str, query: str) -> dict[str, Any]:
    """context, question and spans (content offsets) of one prompt: family `fam`, scene part `which` (base or a
    source), the question naming `query` (DK, RK, RR; IX and CH select it in the code)."""
    order, digits = sc["dicts"][which]
    doc = Doc()
    doc.add(FENCE_OPEN + f"{DICT} = {{")
    entries = []
    for j, (e, d) in enumerate(zip(order, digits, strict=True)):
        if j:
            doc.add(", ")
        entries.append(doc.add(f'"{e}": {d}'))
    doc.add("}")
    spans: dict[str, Any] = {"entries": entries}
    code: dict[str, Any] = {}
    if fam == "IX":
        doc.add(f"\n{LIST} = [")
        items = []
        for j, e in enumerate(sc["lists"][which]):
            if j:
                doc.add(", ")
            items.append(doc.add(f'"{e}"'))
        doc.add("]")
        spans["list"] = items
        code = {"index": sc["index"], "list": list(sc["lists"][which])}
    if fam in CHAIN_DEPTH:
        lines = []
        for line in chain_lines(fam, sc, which):
            doc.add("\n")
            lines.append(doc.add(line))
        spans["chain"] = lines
        depth = CHAIN_DEPTH[fam]
        target, distractor = sc["heads"][which]
        code = {"depth": depth, "lines": chain_lines(fam, sc, which), "order": sc["merges"][depth],
                "vars": {ch: v[:depth] for ch, v in sc["vars"].items()}, "printed": sc["vars"]["target"][depth - 1],
                "heads": {"target": target, "distractor": distractor}}  # fmt: skip
    context = doc.text
    doc.add("\n")
    q0 = len(doc.text)
    line = print_query(fam, sc, query)
    text, c = nl_question(fam, domain, query)
    if line is not None:
        spans["query"] = doc.add(line)
        fence_end = doc.add("\n" + FENCE_CLOSE)[1]
        doc.add("\n")
        spans["nl_question"] = doc.add(text)
    else:
        fence_end = doc.add(FENCE_CLOSE)[1]
        doc.add("\n")
        spans["nl_question"] = doc.add(text)
        assert c is not None
        at = spans["nl_question"][0] + text.index(c)
        spans["query"] = [at, at + len(c)]
    spans["question"] = [q0, len(doc.text)]
    spans["tail"] = doc.add(" " + INSTRUCTION)
    spans["code"] = [0, fence_end]
    question = doc.text[q0 : spans["question"][1]]
    assert doc.text == content_of(context, question)
    return {"context": context, "question": question, "spans": spans, "code": code}


def scene_items(sc: dict[str, Any], domain: str, scene_id: str, level: str) -> dict[str, dict]:
    """Every family's item on one scene: pointer_v1's item schema plus "spans" and "code"."""
    q_b, q_s, p = sc["q_b"], sc["q_s"], sc["p"]
    order, digits = sc["order"], sc["digits"]
    look = dict(zip(order, digits, strict=True))
    recalled = {e: rec(domain, e) for e in order}
    collisions = sorted({x for x in digits if x in recalled.values()})
    out = {}
    for fam in FAMILIES:
        lookup = fam != "RR"
        answer = look[q_b] if lookup else rec(domain, q_b)
        base = program(fam, domain, sc, "base", q_b)
        sources = {}
        for src in SOURCES:
            s_order, s_digits = sc["dicts"][src]
            s_look = dict(zip(s_order, s_digits, strict=True))
            s_query = q_s if src == "dissoc" else q_b
            if src == "dissoc":
                pred = (
                    {"none": look[q_b], "identity": look[q_s], "position": look[p], "value": s_look[q_s]}
                    if lookup
                    else {"none": rec(domain, q_b), "identity": rec(domain, q_s), "position": rec(domain, p),
                          "value": rec(domain, q_s)}
                )  # fmt: skip
            else:
                pred = {h: answer for h in HYPOTHESES}
                if src == "redigit" and lookup:
                    pred["value"] = s_look[q_b]
            prog = program(fam, domain, sc, src, s_query)
            sources[src] = {
                "context": prog["context"], "question": prog["question"],
                "answer": str(s_look[s_query] if lookup else rec(domain, s_query)),
                "entities": list(s_order), "digits": list(s_digits), "query": s_query,
                "query_slot": s_order.index(s_query), "predictions": {h: str(v) for h, v in pred.items()},
                "spans": prog["spans"], "code": prog["code"],
            }  # fmt: skip
        pd = sources["dissoc"]["predictions"]
        keys = HYPOTHESES if lookup else ("none", "identity", "position")
        code = dict(base["code"])
        if fam in CHAIN_DEPTH:
            code["distractor_digit"] = str(look[code["heads"]["distractor"]])
        item = {
            "id": f"{domain}-{fam}-{scene_id}", "family": fam, "domain": domain, "level": level,
            "scene": f"{domain}-{scene_id}", "n_entities": len(order), "n_filler": 0,
            "entities": list(order), "digits": list(digits), "recalled": recalled, "query": q_b,
            "cue": {"DK": q_b, "IX": f"{LIST}[{sc['index']}]"}.get(fam, code.get("printed") or cue(domain, q_b)),
            "slots": dict(sc["slots"]),
            "context": base["context"], "question": base["question"], "answer": str(answer), "answer_kind": "digit",
            "sources": sources, "distinct": len({pd[h] for h in keys}) == len(keys),
            "digit_policy": sc["policy"], "collisions": collisions,
            "spans": base["spans"], "code": code,
        }  # fmt: skip
        named = f'print({DICT}["{q_b}"])\n{FENCE_CLOSE}\n{NL_PRINT}'  # DK's base question: the lookup alone
        if fam == "IX":
            hop1 = f"print({LIST}[{sc['index']}])\n{FENCE_CLOSE}\n{NL_PRINT}"
        elif fam in CHAIN_DEPTH:
            hop1 = f"print({code['printed']})\n{FENCE_CLOSE}\n{NL_PRINT}"
        else:
            hop1 = FENCE_CLOSE + "\n" + DOMAINS[domain]["hop_cue"].format(cue=cue(domain, q_b))
        if fam != "DK":
            item["hop1"] = {"question": hop1, "answer": q_b, "kind": domain}
            hop2 = named if lookup else FENCE_CLOSE + "\n" + hop_recall(domain, q_b)
            item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
        out[fam] = item
    return out


def generate_cell(seed: int, domain: str, level: str, n_ent: int, n: int) -> dict[str, list[dict]]:
    """n scenes of one domain at one level, every family on each; dict lines never repeat within the cell."""
    rng = random.Random(seed)
    plan = PV.slot_plan(rng, n, n_ent)
    ixs = index_plan(rng, n, n_ent)
    out: dict[str, list[dict]] = {f: [] for f in FAMILIES}
    seen: set[tuple] = set()
    i = 0
    while i < n:
        a, k = plan[i]
        sc = make_scene(rng, domain, n_ent, a, k, ixs[i])
        key = (tuple(sc["order"]), tuple(sc["digits"]))
        if key in seen:
            continue
        seen.add(key)
        for fam, item in scene_items(sc, domain, f"{level}-{i:04d}", level).items():
            out[fam].append(item)
        i += 1
    return out


def cell_seed(which: str, level: str, domain: str) -> int:
    spec = SETS[which]
    return spec["seed"] * 1000 + 10 * list(spec["levels"]).index(level) + list(DOMAINS).index(domain)


def cells(which: str) -> list[tuple[str, str, int]]:
    """(level, domain, N) of a set; a domain enters a level only if its pool has N keys (months: 7)."""
    spec = SETS[which]
    return [(lv, d, n_ent) for lv, n_ent in spec["levels"].items() for d in DOMAINS
            if len(DOMAINS[d]["entities"]) >= n_ent]  # fmt: skip


def generate(which: str, n: int | None = None) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note) for a set; tokenizer-free (make/check assert the token properties)."""
    out = {}
    for level, domain, n_ent in cells(which):
        seed = cell_seed(which, level, domain)
        fams = generate_cell(seed, domain, level, n_ent, n or SETS[which]["n"])
        note = f"scripts/{EXP}.py make --set {which} (seed {seed}: {domain}, {n_ent} entries)"
        for fam in FAMILIES:
            label = f"{domain}_{fam}_{level}"
            out[label] = (DATA / which / f"{label}.json", fams[fam], note)
    return out


def set_files(which: str) -> dict[str, Path]:
    return {f"{d}_{f}_{lv}": DATA / which / f"{d}_{f}_{lv}.json" for lv, d, _ in cells(which) for f in FAMILIES}


def load_file(path: Path) -> list[dict]:
    return json.loads(path.read_text())["items"]


# ---- execution ------------------------------------------------------------------------------------------------------


def python_source(context: str, question: str) -> str:
    """The code a prompt shows: the fenced lines, and the print line for the print families."""
    lines = context.removeprefix(FENCE_OPEN).split("\n")
    first = question.split("\n")[0]
    if first.startswith("print("):
        lines.append(first)
    return "\n".join(lines) + "\n"


def run_python(source: str) -> tuple[str, dict]:
    """Execute generated code (literals, assignments and print only) with print as the only builtin: (stdout, names)."""
    names: dict[str, Any] = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(source, {"__builtins__": {"print": print}}, names)  # our own generated literals and print only
    return buf.getvalue(), names


def executes(item: dict) -> bool:
    """The base and every source compute their recorded answer: printed (DK, IX, CH) or stored under the cued key (RK);
    RR's code holds the dict and its answer is the recalled fact."""
    prompts = [(item["context"], item["question"], item["answer"], item["query"])]
    prompts += [(s["context"], s["question"], s["answer"], s["query"]) for s in item["sources"].values()]
    for ctx, q, ans, query in prompts:
        stdout, names = run_python(python_source(ctx, q))
        if item["family"] in ("RK", "RR"):
            got = str(names[DICT][query]) if item["family"] == "RK" else str(rec(item["domain"], query))
            if stdout or got != ans:
                return False
        elif stdout != ans + "\n":
            return False
    return True


# ---- tokenizer checks -----------------------------------------------------------------------------------------------


def tokenizer():
    return PV.tokenizer()


def check_pools(tok) -> dict[str, Any]:
    """Every key one token inside quotes (no leading space); one cue length per domain; cues name no key, digit or
    number word; the chain variables and list indices single tokens."""
    from bridge_jspace.tokens import raw_encoding

    def quoted_single(e: str) -> bool:  # e is one token inside quotes, first and later in a dict and in a list
        text = f'{DICT} = {{"{e}": 5, "{e}": 3}}\n{LIST} = ["{e}", "{e}"]\nx = "{e}"'
        offs = {tuple(o) for o in raw_encoding(tok, text, offsets=True)["offset_mapping"]}
        starts = [m.start() + 1 for m in re.finditer(f'"{e}"', text)]
        return len(starts) == 5 and all((s, s + len(e)) in offs for s in starts)

    report = {}
    words = set(PV.NUMBER_WORDS) | set(PV.ORDINALS)
    for domain, d in DOMAINS.items():
        ents = d["entities"]
        bad = [e for e in ents if len(S.ids(tok, e)) != 1 or not quoted_single(e)]
        assert not bad, f"{domain}: not one token inside quotes: {bad}"
        lengths = {e: len(S.ids(tok, " " + c)) for e, (_, c) in ents.items()}
        assert len(set(lengths.values())) == 1, f"{domain}: cue lengths differ: {lengths}"
        for _, c in ents.values():
            toks = set(re.findall(r"[a-z]+|\d", c.lower()))
            assert not toks & {x.lower() for x in ents}, f"{domain}: cue {c!r} names a key"
            assert not toks & words, f"{domain}: cue {c!r} has a number word"
            assert not re.search(r"\d", c), f"{domain}: cue {c!r} has a digit"
        assert len({c for _, c in ents.values()}) == len(ents), f"{domain}: two keys share a cue"
        report[domain] = {"keys": len(ents), "cue_tokens": next(iter(lengths.values())),
                          "recalled": dict(collections.Counter(r for r, _ in ents.values()))}  # fmt: skip
    assert all(len(S.ids(tok, v)) == 1 and len(S.ids(tok, " " + v)) == 1 for v in VARS), "a variable is 2 tokens"
    assert all(len(S.ids(tok, str(x))) == 1 for x in DIGITS), "a digit is 2 tokens"
    return report


def layout(tok, ctx: str, question: str, spans: dict[str, Any]) -> dict[str, Any]:
    """ids, offsets and the token positions of every span of one rendered prompt."""
    from bridge_jspace.tokens import raw_encoding

    text = S.render(tok, ctx, question)
    content = content_of(ctx, question)
    assert text.count(content) == 1, "the content is not found once in the rendered prompt"
    off = text.index(content)
    enc = raw_encoding(tok, text, offsets=True)
    offs = [tuple(o) for o in enc["offset_mapping"]]

    def toks(span: list[int]) -> list[int]:
        s, e = span[0] + off, span[1] + off
        return [i for i, (a, b) in enumerate(offs) if a < e and b > s]

    pos: dict[str, Any] = {}
    for role, v in spans.items():
        pos[role] = [toks(x) for x in v] if v and isinstance(v[0], list) else toks(v)
    return {"text": text, "content": content, "off": off, "ids": list(enc["input_ids"]), "offsets": offs, "pos": pos}


def flat(pos: dict[str, Any], roles: tuple[str, ...]) -> set[int]:
    out: set[int] = set()
    for r in roles:
        v = pos.get(r)
        if v is None:
            continue
        for x in v:
            out |= set(x) if isinstance(x, list) else {x}
    return out


def standalone(lay: dict, start: int, text: str) -> bool:
    """The chars [start, start + len(text)) of the content are exactly one token."""
    s = lay["off"] + start
    return (s, s + len(text)) in lay["offsets"]


def spans_ok(tok, lay: dict, part: dict, fam: str) -> dict[str, bool]:
    """Spans decode to what they name; keys, list items, chain heads and digits are standalone tokens."""
    c, sp = lay["content"], part["spans"]
    entries = [f'"{e}": {d}' for e, d in zip(part["entities"], part["digits"], strict=True)]
    text_ok = [c[s:e] for s, e in sp["entries"]] == entries
    tokens_ok = all(
        standalone(lay, s + 1, e) and standalone(lay, s + len(e) + 4, str(d))
        for (s, _), e, d in zip(sp["entries"], part["entities"], part["digits"], strict=True)
    )
    if fam == "IX":
        lst = part["code"]["list"]
        text_ok &= [c[s:e] for s, e in sp["list"]] == [f'"{e}"' for e in lst]
        tokens_ok &= all(standalone(lay, s + 1, e) for (s, _), e in zip(sp["list"], lst, strict=True))
    if fam in CHAIN_DEPTH:
        lines = part["code"]["lines"]
        text_ok &= [c[s:e] for s, e in sp["chain"]] == lines
        for (s, _), line in zip(sp["chain"], lines, strict=True):
            if '"' in line:
                tokens_ok &= standalone(lay, s + line.index('"') + 1, line.split('"')[1])
    first = part["question"].split("\n")[0]
    query = first if first.startswith("print(") else None
    text_ok &= c[slice(*sp["question"])] == part["question"]
    text_ok &= c[slice(*sp["tail"])] == " " + INSTRUCTION and sp["tail"][1] == len(c)
    text_ok &= c[slice(*sp["code"])].startswith(FENCE_OPEN) and c[slice(*sp["code"])].endswith(FENCE_CLOSE)
    text_ok &= c[slice(*sp["nl_question"])] == part["question"].split("\n")[-1]
    if query is not None:
        text_ok &= c[slice(*sp["query"])] == query
    decoded = all(
        c[s:e] in tok.decode([lay["ids"][i] for i in idx])
        for (s, e), idx in zip(sp["entries"], lay["pos"]["entries"], strict=True)
    )
    return {"spans_text": text_ok, "keys_single_token": tokens_ok, "spans_decode": decoded}


ROLES_ALIGNED = ("entries", "list", "chain", "query", "question", "nl_question", "tail", "code")


def check_item(tok, item: dict) -> dict[str, Any]:
    """Token alignment of every source with the base, the spans, execution, and the item's bookkeeping (predictions,
    permutations, collision policy, IX's index). Returns per-check booleans."""
    fam = item["family"]
    base = layout(tok, item["context"], item["question"], item["spans"])
    out: dict[str, Any] = {}
    sp_ok = spans_ok(tok, base, item, fam)
    allowed = flat(base["pos"], ("entries", "list", "chain", "question"))
    q1 = base["off"] + item["spans"]["question"][1]
    final = [i for i, (s, _) in enumerate(base["offsets"]) if s >= q1]
    for src, s in item["sources"].items():
        lay = layout(tok, s["context"], s["question"], s["spans"])
        for k, v in spans_ok(tok, lay, s, fam).items():
            sp_ok[k] &= v
        same_len = len(lay["ids"]) == len(base["ids"])
        diff = S.changed(base["ids"], lay["ids"]) if same_len else None
        out[f"{src}_aligned"] = (
            same_len
            and all(lay["pos"].get(r) == base["pos"].get(r) for r in ROLES_ALIGNED)
            and diff is not None
            and bool(diff)
            and set(diff) <= allowed  # only entries, selector lines and the question differ; the template never
            and all(lay["ids"][i] == base["ids"][i] for i in final)
        )
    out |= sp_ok
    out["executes"] = executes(item)
    look = dict(zip(item["entities"], item["digits"], strict=True))
    sl = item["slots"]
    ents, dg = item["entities"], item["digits"]
    d = item["sources"]["dissoc"]
    lookup = fam != "RR"
    pd = d["predictions"]
    q_s = d["query"]
    p = ents[sl["position"]]
    perm = (
        ents[sl["query"]] == item["query"]
        and ents[sl["identity"]] == q_s
        and d["entities"][sl["position"]] == q_s
        and d["query_slot"] == sl["position"]
        and sorted(d["entities"]) == sorted(ents)
        and len(set(ents)) == len(ents)
        and len({sl["query"], sl["identity"], sl["position"]}) == 3
    )
    if lookup:
        perm = perm and pd == {"none": str(look[item["query"]]), "identity": str(dg[sl["identity"]]),
                               "position": str(dg[sl["position"]]), "value": str(d["digits"][sl["position"]])}  # fmt: skip
        value_absent = int(pd["value"]) not in dg
        distinct = len(set(pd.values())) == 4
    else:
        perm = (
            perm
            and pd["none"] == str(item["recalled"][item["query"]])
            and pd["identity"] == pd["value"] == str(rec(item["domain"], q_s))
            and pd["position"] == str(rec(item["domain"], p))
        )
        value_absent = True
        distinct = pd["none"] != pd["identity"]
    critical = {rec(item["domain"], e) for e in (item["query"], q_s, p)}
    all_digits = set(dg) | {x for s in item["sources"].values() for x in s["digits"]}
    same, redigit = item["sources"]["same"], item["sources"]["redigit"]
    out |= {
        "permutation": perm,
        "value_absent": value_absent,
        "predictions_distinct": distinct,
        "hard_collision_free": not (all_digits & critical),
        "soft_collision_free": not (set(dg) & set(item["recalled"].values())),
        "hard_promised": item["digit_policy"] in ("soft", "hard"),
        "soft_promised": item["digit_policy"] == "soft",
        "same_noop": same["entities"][sl["query"]] == item["query"]
        and same["digits"][sl["query"]] == look[item["query"]]
        and same["context"] != item["context"]
        and len(set(same["predictions"].values())) == 1,
        "redigit_one_change": [x != y for x, y in zip(redigit["digits"], dg, strict=True)].count(True) == 1
        and redigit["entities"] == ents,
    }
    if fam == "IX":
        ix = item["code"]["index"]
        lists = {k: v["code"]["list"] for k, v in item["sources"].items()} | {"base": item["code"]["list"]}
        out["selector"] = (
            lists["base"][ix] == item["query"]
            and lists["dissoc"][ix] == q_s
            and lists["same"][ix] == item["query"]
            and lists["same"] != lists["base"]
            and lists["redigit"] == lists["base"]
            and all(sorted(v) == sorted(ents) for v in lists.values())
            and ix not in all_digits  # a copied index is never a lookup digit
            and all(v["code"]["index"] == ix for v in item["sources"].values())
        )
    elif fam in CHAIN_DEPTH:
        h = {k: v["code"]["heads"] for k, v in item["sources"].items()} | {"base": item["code"]["heads"]}
        r = h["base"]["distractor"]
        out["selector"] = (
            h["base"]["target"] == item["query"]
            and h["dissoc"] == {"target": q_s, "distractor": r}
            and h["same"]["target"] == item["query"]
            and h["same"]["distractor"] != r
            and h["redigit"] == h["base"]
            and r not in (item["query"], q_s)
            and (r != p or len(ents) == 3)
            and item["code"]["distractor_digit"] == str(look[r])
            and all(v["code"]["order"] == item["code"]["order"] for v in item["sources"].values())
        )
    else:
        out["selector"] = True
    return out


MUST = ("dissoc_aligned", "same_aligned", "redigit_aligned", "spans_text", "keys_single_token", "spans_decode",
        "executes", "permutation", "value_absent", "predictions_distinct", "same_noop", "redigit_one_change",
        "selector")  # fmt: skip


# ---- stages: data ---------------------------------------------------------------------------------------------------


def stage_make(which: str) -> None:
    tok = tokenizer()
    print(json.dumps(check_pools(tok)))
    for _label, (path, items, note) in generate(which).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        head = {"family": items[0]["family"], "label": FAMILY_LABEL[items[0]["family"]], "domain": items[0]["domain"],
                "level": items[0]["level"], "generator": note,
                "format": (__doc__ or "").split("\n\n")[2]}  # fmt: skip
        body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)  # one item per line: grep-able, compact
        path.write_text(json.dumps(head, indent=1, ensure_ascii=False)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    """Every set regenerated from this code equals its files."""
    for which in SETS:
        for label, (path, items, _) in generate(which).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    from bridge_jspace.utils import progress

    tok = tokenizer()
    report: dict[str, Any] = {"pools": check_pools(tok), "files": {}}
    for label, path in progress(list(set_files(which).items()), f"check {which}"):
        items = load_file(path)
        stats: collections.Counter = collections.Counter()
        slots = {k: collections.Counter() for k in ("query", "identity", "position")}
        roles = {k: collections.Counter() for k in ("q_b", "q_s", "p")}
        answers, values, policies, index = (collections.Counter() for _ in range(4))
        prompts, lengths = set(), []
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
            for k in slots:
                slots[k][it["slots"][k]] += 1
            d = it["sources"]["dissoc"]
            for k, e in (("q_b", it["query"]), ("q_s", d["query"]), ("p", it["entities"][it["slots"]["position"]])):
                roles[k][e] += 1
            answers[it["answer"]] += 1
            values[d["predictions"]["value"]] += 1
            policies[it["digit_policy"]] += 1
            if "index" in it["code"]:
                index[it["code"]["index"]] += 1
            text = S.render(tok, it["context"], it["question"])
            prompts.add(text)
            lengths.append(len(S.ids(tok, text)))
        n = len(items)
        r = {"n": n, **stats, "unique_prompts": len(prompts),
             "prompt_tokens(min,median,max)": (min(lengths), statistics.median(lengths), max(lengths)),
             "slots": {k: dict(sorted(v.items())) for k, v in slots.items()}, "ix_index": dict(sorted(index.items())),
             "answers": dict(sorted(answers.items())), "values": dict(sorted(values.items())),
             "policies": dict(policies), "roles": {k: dict(v.most_common()) for k, v in roles.items()}}  # fmt: skip
        print(label, json.dumps(r))
        for k in MUST:
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert stats["hard_collision_free"] >= stats["hard_promised"], f"{label}: hard policy broken"
        assert stats["soft_collision_free"] >= stats["soft_promised"], f"{label}: soft policy broken"
        assert len(prompts) == n, f"{label}: repeated prompts"
        report["files"][label] = r
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out)


# ---- stages: competence ---------------------------------------------------------------------------------------------

PROMPT_KINDS = PV.PROMPT_KINDS  # clean, src_dissoc, src_same, src_redigit, hop1, hop2


def said(text: str, kind: str) -> str | None:
    """The first answer of the kind in the first non-empty line: a digit (digits, number words, ordinals) or a key of
    the domain named by `kind`."""
    if kind == "digit":
        return PV.said(text, "digit")
    lower = {w.lower(): w for w in DOMAINS[kind]["entities"]}
    return next((lower[t] for t in re.findall(r"[a-z]+", S.first_line(text)) if t in lower), None)


def stage_manifest(name: str, why: str, sets: list[str], limit: int | None) -> None:
    pins.check_run_name(name)
    from bridge_jspace.data import sha256_of

    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"{s}/{label}": f for s in sets for label, f in set_files(s).items()}
    manifest = {
        "exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
        "model": pins.model_pin(), "switches": switches(), "sets": sets,
        "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
        "limit": limit, "family_labels": FAMILY_LABEL,
        "format": "suite_v1's: chat template, thinking off, 'Answer:' prefilled; the context, a newline, the question and "
        f"'{INSTRUCTION}' in one user turn (the suite's CODE layout: fenced code, then the question)",
        "prompts": "base; each source (dissoc, same, redigit) with its own context and question; hop1 (the key alone: "
        "names[i], the chain's last variable, or the cue -> key) and hop2 (the lookup with the key named, or the recalled "
        "fact) with the base context, for every family but DK",
        "judge": "the first answer of the item's kind in the first non-empty line of 8 greedy tokens (digits, number words "
        "and ordinals for digits; the domain's keys otherwise)",
        "answer_read": "suite_v1's: one forward with a digit answer's space token appended; p and margin of the answer's "
        "first token; whether the read's top token is the greedy answer",
        "gate": (__doc__ or "").split("Gate (competence")[1].split("Stages:")[0].strip(),
    }  # fmt: skip
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.stats import wilson
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    for f, pin in manifest["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []
    labels = list(manifest["items"])
    for label in labels:
        for it in load_file(pins.REPO_ROOT / manifest["items"][label]["file"])[: manifest.get("limit")]:
            for kind, (ctx, q, ans, akind) in PV.item_prompts(it).items():
                prompts.append({"label": label, "family": it["family"], "domain": it["domain"], "level": it["level"],
                                "id": it["id"], "kind": kind, "expected": ans,
                                "answer_kind": "digit" if akind == "digit" else "word", "judge": akind,
                                "ids": S.ids(tok, S.render(tok, ctx, q))})  # fmt: skip
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    chunks = [g[i : i + 64] for g in by_len.values() for i in range(0, len(g), 64)]
    for chunk in progress(chunks, "generate"):
        texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
        for p, text in zip(chunk, texts, strict=True):
            p["continuation"] = text
            p["said"] = said(text, p["judge"])
            p["correct"] = (p["said"] or "").lower() == p["expected"].lower()
    t_gen = time.time() - t0
    S.read_answers(model, tok, prompts)
    t_read = time.time() - t0 - t_gen
    rows = [{k: v for k, v in p.items() if k not in ("ids", "forced")} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary: dict[str, Any] = {"labels": {}, "seconds_generate": round(t_gen), "seconds_read": round(t_read)}
    for label in labels:
        fr = [r for r in rows if r["label"] == label]
        per_item: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in fr:
            per_item[r["id"]][r["kind"]] = r["correct"]
        cells_ = {}
        for kind in PROMPT_KINDS:
            got = [v[kind] for v in per_item.values() if kind in v]
            if got:
                cells_[kind] = dict(zip(("rate", "lo", "hi"), wilson(sum(got), len(got)), strict=True)) | {
                    "k": sum(got)
                }
        clean = [r for r in fr if r["kind"] == "clean"]
        summary["labels"][label] = {
            "family": fr[0]["family"], "family_label": FAMILY_LABEL[fr[0]["family"]], "domain": fr[0]["domain"],
            "level": fr[0]["level"], "n": len(per_item), "cells": cells_,
            "eligible": sum(all(v.values()) for v in per_item.values()),
            "passes_gate": cells_["clean"]["lo"] >= 0.85,
            "clean_median_p_answer": statistics.median(r["p_answer"] for r in clean),
            "read_agrees_with_greedy": statistics.mean((r["said"] or "").lower().startswith(r["read_top"].lower())
                                                       if r["read_top"] else False for r in fr),
        }  # fmt: skip
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    lines = ["| label | family | n | " + " | ".join(PROMPT_KINDS) + " | eligible | gate | median p | read = greedy |",
             "|---" * (len(PROMPT_KINDS) + 7) + "|"]  # fmt: skip
    for label, s in summary["labels"].items():
        c = s["cells"]
        cols = [
            f"{100 * c[k]['rate']:.0f}% [{100 * c[k]['lo']:.0f},{100 * c[k]['hi']:.0f}]" if k in c else "-"
            for k in PROMPT_KINDS
        ]
        lines.append(f"| {label} | {s['family_label']} | {s['n']} | " + " | ".join(cols) + f" | {s['eligible']} | "
                     f"{'pass' if s['passes_gate'] else 'FAIL'} | {s['clean_median_p_answer']:.3f} | "
                     f"{100 * s['read_agrees_with_greedy']:.1f}% |")  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


# ---- stages: examples and figures -----------------------------------------------------------------------------------

EXAMPLE_GROUPS = {
    "eligible": ("Every prompt right", "org prompt, the three alt prompts and both steps alone answered right (the item "
                 "can enter the patching runs)"),
    "clean_wrong": ("Org prompt wrong", "the unedited org prompt answered wrong"),
    "source_wrong": ("An alt prompt wrong", "org prompt right, at least one alt prompt wrong (shown: the first wrong "
                     "one)"),
    "step_wrong": ("A step alone wrong", "org and alt prompts right, a step alone wrong (shown: the first wrong step)"),
}  # fmt: skip
KIND_TERM = {  # plain words for the competence prompt kinds (figure_terms.md)
    "clean": "org prompt",
    "src_dissoc": "alt prompt (bridge alt at another entry, its own digit)",
    "src_same": "control prompt (same bridge and digit, the other entries reshuffled)",
    "src_redigit": "control prompt (org prompt with the bridge's digit changed)",
    "hop1": "step 1 alone (find the key)",
    "hop2": "step 2 alone (look up or recall with the key named)",
}


def prompt_part(it: dict, kind: str) -> tuple[str, str, dict | None, dict]:
    """(context, question, spans or None, the part's dict: entities / digits / code) of one competence prompt kind."""
    if kind.startswith("src_"):
        s = it["sources"][kind[4:]]
        return s["context"], s["question"], s["spans"], s
    if kind in ("hop1", "hop2"):
        return it["context"], it[kind]["question"], None, it
    return it["context"], it["question"], it["spans"], it


def rendered_spans(text: str, ctx: str, question: str, spans: dict | None, part: dict, it: dict) -> list[dict]:
    """The examples.json spans of one prompt: char offsets in the rendered prompt, one role each."""
    off = text.index(content_of(ctx, question))
    if spans is None:  # a step alone: the base context's spans hold up to the question
        part, q0 = it, len(ctx) + 1
        spans = {k: v for k, v in it["spans"].items() if k in ("entries", "list", "chain")}
        spans |= {
            "question": [q0, q0 + len(question)],
            "tail": [q0 + len(question), q0 + len(question) + 1 + len(INSTRUCTION)],
        }
    sl = it["slots"]
    named = {sl["query"]: "bridge entry (base query, slot a)", sl["identity"]: "identity entry (slot c)",
             sl["position"]: "position entry (slot k)"} if part is it else {part["query_slot"]: "queried entry"}  # fmt: skip
    out = []
    for j, (s, e) in enumerate(spans["entries"]):
        role = f"entry {j}: {part['entities'][j]}" + (f" = {named[j]}" if j in named else "")
        out.append({"start": off + s, "end": off + e, "role": role})
    for j, (s, e) in enumerate(spans.get("list", [])):
        out.append({"start": off + s, "end": off + e, "role": f"list item {j}"})
    for j, (s, e) in enumerate(spans.get("chain", [])):
        out.append({"start": off + s, "end": off + e, "role": f"chain line {j}"})
    for role in ("query", "question", "tail"):
        if role in spans:
            out.append({"start": off + spans[role][0], "end": off + spans[role][1], "role": role})
    return out


def stage_examples(name: str, k: int, seed: int) -> None:
    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (out_dir / "items.jsonl").read_text().splitlines()]
    by_id: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        by_id[r["id"]][r["kind"]] = r
    items = {it["id"]: it for pin in manifest["items"].values() for it in load_file(pins.REPO_ROOT / pin["file"])}
    tok = tokenizer()
    grouped: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for iid, kinds in by_id.items():
        ok = {kd: r["correct"] for kd, r in kinds.items()}
        wrong_src = next((kd for kd in PROMPT_KINDS[1:4] if kd in ok and not ok[kd]), None)
        wrong_hop = next((kd for kd in ("hop1", "hop2") if kd in ok and not ok[kd]), None)
        if all(ok.values()):
            grouped["eligible"].append((iid, "clean"))
        elif not ok["clean"]:
            grouped["clean_wrong"].append((iid, "clean"))
        elif wrong_src:
            grouped["source_wrong"].append((iid, wrong_src))
        elif wrong_hop:
            grouped["step_wrong"].append((iid, wrong_hop))
    rng = random.Random(seed)
    examples = []
    for g in EXAMPLE_GROUPS:
        for fam in FAMILIES:
            pool = sorted(x for x in grouped[g] if items[x[0]]["family"] == fam)
            for iid, kind in rng.sample(pool, min(k, len(pool))):
                it, r = items[iid], by_id[iid][kind]
                ctx, q, spans, part = prompt_part(it, kind)
                text = S.render(tok, ctx, q)
                expected = {"correct": r["expected"]}
                if kind == "src_dissoc":
                    expected |= {f"if patched into the base: {h}": v for h, v in part["predictions"].items()}
                examples.append({
                    "group": g, "family": fam, "family_label": FAMILY_LABEL[fam], "item_id": iid, "prompt": text,
                    "spans": rendered_spans(text, ctx, q, spans, part, it),
                    "condition": f"unedited: {KIND_TERM[kind]} ({it['domain']}, {it['n_entities']} dict entries)",
                    "answers": {"clean": r["said"], "edited": None, "expected": expected},
                    "numbers": {"correct": r["correct"], "p_answer": r.get("p_answer"), "margin": r.get("margin"),
                                "read_top": r.get("read_top"), "continuation": r["continuation"],
                                "item_prompts_right": {kd: x["correct"] for kd, x in by_id[iid].items()}},
                    "why": f"{EXAMPLE_GROUPS[g][1]}; this {KIND_TERM[kind]} was answered {r['said']!r}, expected "
                           f"{r['expected']!r}",
                })  # fmt: skip
    doc = {"exp": EXP, "run": name, "k": k, "seed": seed, "k_per": "group and family",
           "groups": [{"key": g, "title": t, "definition": d, "n_total": len(grouped[g])}
                      for g, (t, d) in EXAMPLE_GROUPS.items()],
           "examples": examples}  # fmt: skip
    (out_dir / "examples.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out_dir / "examples.json", len(examples), "examples")


FIG_SERIES = (  # (key, legend, colour: validated categorical slots 1-2, marker as the second encoding, y offset)
    ("clean", "org prompt right (the gate's measure)", "#2a78d6", "o", -0.14),
    ("eligible", "every prompt of the item right (eligible for patching)", "#eb6834", "s", 0.14),
)
GATE = 0.85


def example_row(manifest: dict) -> str:
    """The figure's Example row: a real list-position item of the run, shortened, with its answer."""
    first = next(p for k, p in manifest["items"].items() if "_IX_" in k)
    it = load_file(pins.REPO_ROOT / first["file"])[0]
    lines = [*it["context"].removeprefix(FENCE_OPEN).split("\n"), it["question"].split("\n")[0]]
    return (
        f"{'; '.join(lines)} -> answer {it['answer']}. 'Every prompt right' adds the alt prompts and each step alone."
    )


def stage_figures(name: str) -> None:
    """Per-family accuracy of a competence run: one panel per (size, domain), Wilson 95% intervals, the gate. One
    figures folder per run (the user's rule): earlier analysis-*-figures folders of the run are replaced."""
    import shutil

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import GRID, INK, MUTED, finish, percent_axis, style_axes
    from bridge_jspace.stats import wilson

    run = RESULTS / name
    summary = json.loads((run / "summary.json").read_text())
    manifest = json.loads((run / "manifest.json").read_text())
    for old in run.glob("analysis-*-figures"):
        shutil.rmtree(old)
    out = run / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    out.mkdir()
    panels: dict[tuple[str, str], dict[str, dict]] = collections.defaultdict(dict)
    for label, s in summary["labels"].items():
        panels[(label.split("/")[0] + " " + s["level"], s["domain"])][s["family"]] = s
    rows = sorted({r for r, _ in panels}, key=lambda r: (r.split()[0] != "main", r))
    cols = [d for d in DOMAINS if any(c == d for _, c in panels)]
    fig, axes = plt.subplots(len(rows), len(cols), figsize=(5.4 * len(cols), 0.5 + 2.7 * len(rows)), squeeze=False)
    for i, r in enumerate(rows):
        for j, d in enumerate(cols):
            ax = axes[i][j]
            cell = panels.get((r, d))
            if not cell:
                ax.axis("off")
                continue
            style_axes(ax)
            fams = [f for f in FAMILIES if f in cell]
            for y, f in enumerate(fams):
                s = cell[f]
                rates = {"clean": (s["cells"]["clean"]["rate"], s["cells"]["clean"]["lo"], s["cells"]["clean"]["hi"]),
                         "eligible": tuple(wilson(s["eligible"], s["n"]))}  # fmt: skip
                for key, _, colour, marker, dy in FIG_SERIES:
                    rate, lo, hi = rates[key]
                    ax.plot([lo, hi], [y + dy] * 2, color=colour, lw=2, solid_capstyle="round")
                    ax.plot([rate], [y + dy], marker=marker, ms=8, color=colour, mec="white", mew=1.5, ls="none")
            ax.axvline(GATE, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=1)
            ax.set_yticks(range(len(fams)), [FAMILY_LABEL[f] for f in fams], color=INK, fontsize=9)
            ax.set_ylim(len(fams) - 0.5, -0.5)
            ax.set_xlim(-0.03, 1.03)  # markers at 0% and 100% stay whole
            percent_axis(ax, "x")
            ax.grid(False, axis="y")
            ax.grid(True, axis="x", color=GRID, lw=0.6)
            n = max(s["n"] for s in cell.values())
            which, level = r.split()
            size = f"{int(level[1])} dict entries" + ("" if which == "main" else ", pilot")
            ax.set_title(f"{d}, {size} (n = {n} per family)", fontsize=10, color=INK, loc="left")
            if i == len(rows) - 1 or not panels.get((rows[i + 1], d)):
                ax.set_xlabel("% of items answered right (95% Wilson interval)", color=MUTED, fontsize=9)
    handles = [Line2D([], [], color=c, marker=m, ms=8, lw=2, label=lab) for _, lab, c, m, _ in FIG_SERIES]
    handles.append(Line2D([], [], color=MUTED, lw=1, ls=(0, (4, 3)), label="gate: a family enters if its org-prompt lower "
                          "bound >= 85%"))  # fmt: skip
    model = manifest["model"]["repo"].split("/")[-1]
    explain = [
        ("What we did", "Asked each item's Python lookup unedited: the dict key named, found by list position, through "
         "a chain of variables, or recalled from a cue (memory → memory asks a recalled fact instead)."),
        ("Example", example_row(manifest)),
        ("How to read", "Blue = the org prompt answered right; orange = every prompt of the item right. A family is "
         "usable for the patching runs if its blue lower end is right of the dashed line."),
        ("Control", "Each step alone (the key alone; the lookup with the key named): a family can fail while its steps "
         "pass, which means the model cannot chain them."),
    ]  # fmt: skip
    n_note = ", ".join(sorted({str(s["n"]) for s in summary["labels"].values()}))
    note = f"{model}; {n_note} items per family and panel; bars are Wilson 95% intervals."
    paths = []
    stem = out / "competence_by_family"
    finish(fig, stem.with_suffix(".png"), "Can the model run these Python lookups, family by family?", note, handles,
           ncols=1, explain=explain)  # fmt: skip
    paths.append(str(stem.with_suffix(".png")))
    print("wrote", *paths)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence", "examples", "figures"])
    ap.add_argument("--set", dest="sets", nargs="+", choices=list(SETS), default=["main"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items per file (a smoke run)")
    ap.add_argument("--k", type=int, default=3, help="examples: per group and family")
    ap.add_argument("--seed", type=int, default=0, help="examples: sampling seed")
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
    elif args.stage == "competence":
        assert args.name, "competence needs --name"
        stage_competence(args.name)
    elif args.stage == "examples":
        assert args.name, "examples needs --name"
        stage_examples(args.name, args.k, args.seed)
    else:
        assert args.name, "figures needs --name"
        stage_figures(args.name)
