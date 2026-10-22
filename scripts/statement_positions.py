"""statement_positions (D1): where does the lookup read the bridge: at the positions where the bridge is stated, or at
the question tokens?

Why: every measure so far (suite_split's copy split, read_write's lens read and write) was taken at the question tokens.
A bound bridge ("Jack's pet is a cow.") is stated in the context and only referred to in the question ("Jack's pet");
there the lens reads BL's bridge 7% and the J-space part of the copy flips 0%. "Lookup-used bridges live outside the
J-space" may be a measurement-location artefact (H-loc) or hold wherever the bridge is in transit (H-around).

Families: suite_v1 wording A BL, BR, RL, RR (main set) and BLR, BRL (tie-breakers), on read_write's cases (the first n
per family of suite_split's map_A8_v1, so BL/BR/RL/RR share scenes and BLR/BRL share scenes); countries R and B
(data/bind_recall.json, exp09's chat_prefill, the first n per family of control_split's map_v1; the positive control:
the lens writes them at the question tokens).

Position sets, per prompt, from character offsets of the generator's own sentences (asserted to tile the context):
  bind_bridge    the binding statement that states the bridge (bound families: the queried person's)
  bridge_word    its bridge-entity token(s) alone
  bind_other     the other persons' binding statements (in B families C also changes X's owner's)
  lookup_bridge  the bridge's lookup statement ("The cow's locker is 5."; BLR its friend row, BRL its legs row; none
                 for countries, whose capital is recalled)
  lookup_x       X's lookup statement (the row C's re-binding points the question to: a copy at the bridge's row
                 alone cannot redirect the lookup)
  context        every context token (all statements: the statement route's ceiling)
  question       suite_split's question group, exactly (the question's tokens after C's changed ones through the end)
  q_words        question minus final
  final          the template after the user turn: <|im_end|>, the assistant header, the empty think block, "Answer:"
For RL, RR and countries R, C changes only the cue in the question, so every statement position precedes C's change:
copying C there is an exact no-op (a built-in check). O's change (the lockers / friends / rows / holders of X and Z)
also comes after every binding statement in the suite, so O's copy at the binding statements is exactly zero there.

Stages (manifest.json written first, write-once, under results/statement_positions/<name>/):
  plan       tokenizer only: the cases, their position sets and the map's job counts (for GPU-time estimates)
  map        for each set and layer (every 4th layer plus every layer in the handoff window, 32-52 on the 27B: below
             28 no question-token copy moves any family, from 52 BL's question copy flips 88-99%; the window holds the
             question-token measures at 32-40 and the answer onset at 44), copy C's block output into the clean run at
             that set only (exp04's AddRows, as suite_split) and read the answer as suite_split does (one forward,
             a digit's space token appended; role of the top token, ld = logit(b) - logit(A), frac of the way from
             clean to C). Controls at the same cell: O's copy (off-path change; where O's delta is non-zero) and C's
             copy with each row replaced by a random direction at its norm (rand). Sanity, per case: the clean run's own
             residual copied at every position (identity) changes nothing; C's residual copied at every position at
             layer 0 reproduces C's read; zero-delta cells (by causality) are verified exactly zero and, for the first
             cases of each cue-only family, read anyway. The first cases per family also generate 8 greedy tokens per
             edit (read vs greedy agreement, as suite_split).
  parts      at each family's transit cells (below), C's copy split exactly as suite_split's parts with --calibrate:
             J-space part (25-atom signed OMP over the frozen J++'s letter-token vectors) and the rest, lens2 (the
             bridge's and X's own lens vectors) and the rest, the J-space part without the own words, a 25-atom OMP over
             a random dictionary (the fitting null), each part's random-direction null, and the matched-size pieces.
  readwrite  at the same cells: the lens read (the bridge's best rank among word tokens over the set's positions, X
             as the floor) and the lens write (v_X - v_I per position at the norm of C's copy there, 0.5-16x, and a
             random direction at the same norms; C's copy itself), as read_write at the question tokens.
  examples   k examples per outcome group of a finished run (random, fixed seed), as examples.json.

Transit (fixed before the 27B run): a cell (family, set, layer) is in transit if C's copy gives X's answer in at least
TRANSIT_FLIPS = 50% of cases and its Wilson 95% lower bound is above the upper bound of every control's change rate
(O's copy where it is non-zero; the random-direction copy). Zero-delta cases count as unchanged (the copy is the
identity). parts / readwrite run at transit cells on the coarse grid between N/4 and the answer onset (16-40 on the
27B); primary layers N/2 to the onset (32-40, where the question-token measures were taken), secondary 16-40.

Decision rule (fixed before the 27B run; per family, set and window, primary layers decide):
  J-space verdict (frac): inside if the concentration's lower bound > INSIDE (1.2) and above the random-dictionary
  null's upper bound; around if its upper bound < OUTSIDE (1.0) and not_jspace - jspace > 0 (paired bootstrap lower
  bound); else inconclusive. suite_split's own rule (inside above 2.0) is reported as verdict_strict.
  Lens write: written if at some scale <= 4x the lens direction flips >= 30% and beats the random direction (paired
  bootstrap lower bound of the flip difference > 0); not written if at every scale (0.5-16x) the difference's upper
  bound is < 0.10; else inconclusive.
  H-loc (location artefact) is supported for a lookup-used bound family (BL, BLR) if at a statement set in transit at
  the primary layers its J-space verdict is inside and the lens writes it there. H-around is supported if at every
  statement set in transit at the primary layers its J-space verdict is around and the lens does not write it, while
  the positive control at the same set and layers (countries B, else BR) is inside; without a passing positive control
  an 'around' result at the statements is not interpretable. No statement set of BL in transit at the primary layers:
  H-loc's location premise fails at the question-token layers (the secondary layers are reported, not decisive).
  Paired readers: at statement sets BL and BR (and BLR and BRL) get the identical patch on the same scenes (the context
  precedes the question), so their concentration difference isolates what the reader uses; reported with a scene
  bootstrap.

  python scripts/statement_positions.py plan --name N [--n K]
  python scripts/statement_positions.py map --name M --why W [--n K] [--families ...] [--layers ...]
  python scripts/statement_positions.py parts --name P --map M --why W [--force SET:LAYER ...]
  python scripts/statement_positions.py readwrite --name R --map M --why W [--parts P] [--force SET:LAYER ...]
  python scripts/statement_positions.py examples --name RUN [--k 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.tokens import raw_encoding
from bridge_jspace.utils import git_state, progress
from scripts import control_split as C
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp

EXP = "statement_positions"
RESULTS = pins.RESULTS_DIR / EXP
SUITE = ("BL", "BR", "RL", "RR", "BLR", "BRL")
COUNTRIES = ("R", "B")  # bind_recall's families (countries), as control_split names them
# tasks_v2 (Zach's generator, scripts/tasks_v2.py) PP and PM on one scene ("Grace picked delta. ... The locker of delta
# is 8."; PP: "Which locker belongs to Grace's pick?", PM: "Which position in the Greek alphabet does Grace's pick
# have?"): suite BL / BR in other topics (animals, planets, elements, Greek letters), opt-in with --tasks-set (22 Oct)
TASKS = ("PP", "PM")
FAMILIES = SUITE + COUNTRIES + TASKS
DEFAULT_FAMILIES = SUITE + COUNTRIES
CUE_ONLY = ("RL", "RR", "R")  # C changes only the cue in the question: every statement precedes C's change
BOUND = ("BL", "BR", "BLR", "BRL", "B", "PP", "PM")
LOOKUP_USED_BOUND = ("BL", "BLR", "PP")
POSITIVE = ("B", "BR", "PM")  # the positive control at the statements, in order of preference
PAIRS = (("BL", "BR"), ("BLR", "BRL"), ("PP", "PM"))  # same scenes, same statements: one patch, two readers
TASKS_SET: str | None = None  # --tasks-set: the tasks_v2 data set of the PP / PM cases
TASKS_COMP: str | None = None  # --tasks-competence: its competence run (scenes right on every prompt of PP and PM)
STATEMENT_SETS = ("bind_bridge", "bridge_word", "bind_other", "lookup_bridge", "lookup_x", "context")
QUESTION_SETS = ("question", "q_words", "final")
SETS = STATEMENT_SETS + QUESTION_SETS
SOURCES = ("clean", "cf", "off")
N_LAYERS = pins.N_LAYERS
COARSE = P.MAP_LAYERS  # suite_split's grid: every 4th layer on the 27B (0-60)
WINDOW = tuple(range(N_LAYERS * 32 // 64, N_LAYERS * 52 // 64 + 1))  # every layer of the handoff window (32-52)
MAP_LAYERS = tuple(sorted(set(COARSE) | set(WINDOW)))
ONSET = P.ANSWER_ONSET  # 44 on the 27B (exp12): parts and readwrite stay below it, as suite_split's
SPLIT_LO, PRIMARY_LO = N_LAYERS // 4, N_LAYERS // 2  # parts / readwrite layers: [16, 44) on the 27B, primary [32, 44)
TRANSIT_FLIPS = 0.5
INSIDE, OUTSIDE = 1.2, 1.0
WRITTEN_FLIPS, WRITE_MAX_SCALE, NOT_WRITTEN = 0.30, 4.0, 0.10
SCALES = (0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
N_CASES = 80  # per family: read_write dose_v1's cases (its first 80 per family)
N_VALIDATE = 10  # cases per family whose every edit also generates 8 greedy tokens
N_NOOP_READ = 5  # cases per cue-only family whose zero-delta statement copies are read anyway
NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLES_SEED, K_EXAMPLES = 0, 0, 2000, 0, 3
SUITE_MAP, COUNTRY_MAP = "map_A8_v1", "map_v1"  # suite_split's and control_split's case lists (27B eligibility)
H_NAMES = ("H-loc", "H-around")
CELL_SETS: tuple[str, ...] = SETS  # parts / readwrite: the sets whose transit cells run (--sets: a budget run)
SUB_N: int | None = None  # parts / readwrite: the first SUB_N cases per family of the map's (--sub-n: a budget run)


# ---- cases and position sets (tokenizer only) ---------------------------------------------------------------------


def load_tokenizer():
    """The target's tokenizer; on a machine with an incomplete model snapshot, its cached tokenizer files alone."""
    from bridge_jspace.tokens import load_tokenizer as load

    try:
        return load()
    except Exception:  # the Mac: tokenizer files cached, weights not
        from huggingface_hub import try_to_load_from_cache
        from transformers import AutoTokenizer

        path = try_to_load_from_cache(pins.MODEL_REPO, "tokenizer.json", revision=pins.MODEL_REVISION)
        assert isinstance(path, str), f"{pins.MODEL_REPO}: tokenizer not cached"
        return AutoTokenizer.from_pretrained(str(Path(path).parent))


def tasks_statements(c: dict) -> dict[str, Any]:
    """A tasks_v2 PP / PM prose context (level 0: picks and lockers only, no filler) by role: "<person> picked
    <thing>." and "The locker of <thing> is <number>.", things written as the domain refers to them ("the eagle")."""
    sents = [s if s.endswith(".") else s + "." for s in c["context"].split(". ")]
    picks, lockers = {}, {}
    for s in sents:
        if " picked " in s:
            person, thing = s[:-1].split(" picked ", 1)
            picks[person] = (thing.removeprefix("the "), s)
        else:
            assert s.startswith("The locker of "), f"{c['id']}: {s!r} is neither a pick nor a locker"
            thing = s[len("The locker of ") : s.rindex(" is ")]
            lockers[thing.removeprefix("the ")] = s
    holders = [p for p in picks if f"{p}'s pick" in c["question"]]
    assert len(holders) == 1, f"{c['id']}: the question names {holders}"
    holder = holders[0]
    assert picks[holder][0] == c["bridge"], f"{c['id']}: {holder} picked {picks[holder][0]}, not {c['bridge']}"
    return {"holder": holder, "bind_bridge": picks[holder][1],
            "bind_other": [s for p, (_, s) in picks.items() if p != holder],
            "lookup_bridge": lockers.get(c["bridge"]), "lookup_x": lockers.get(c["cf_bridge"]), "all": sents}  # fmt: skip


def statements(c: dict) -> dict[str, Any]:
    """The context's sentences by role, as the item generators wrote them (suite_v1 wording A; exp09's countries;
    tasks_v2's prose for PP / PM)."""
    fam = c["family"]
    if fam in TASKS:
        return tasks_statements(c)
    rows: dict[Any, str] = {}
    key_i: Any = None
    key_x: Any = None
    if fam in COUNTRIES:
        people, held = c["people"], c["countries"]
        own = {p: f"{p} lives in {x}." for p, x in zip(people, held, strict=True)}
        owner = dict(zip(held, people, strict=True))
    else:
        w = S.WORDINGS["A"]
        people, pets = c["people"], c["pets"]
        own = {p: w["own"].format(p=p, a=a) for p, a in zip(people, pets, strict=True)}
        owner = dict(zip(pets, people, strict=True))
        if fam == "BLR":
            rows = {a: w["friend"].format(a=a, f=f) for a, f in c["friends"].items()}
            key_i, key_x = c["bridge"], c["cf_bridge"]
        elif fam == "BRL":
            rows = {int(k): w["row"].format(k=k, d=d) for k, d in c["leg_lockers"].items()}
            key_i, key_x = int(c["mid"]), int(c["cf_mid"])
        else:
            rows = {a: w["locker"].format(a=a, d=d) for a, d in c["lockers"].items()}
            key_i, key_x = c["bridge"], c["cf_bridge"]
    holder = owner[c["bridge"]]
    if fam in BOUND:
        assert c["cue"] == holder, f"{c['id']}: the question asks about {c['cue']}, the bridge's holder is {holder}"
    return {
        "holder": holder,
        "bind_bridge": own[holder],
        "bind_other": [own[p] for p in people if p != holder],
        "lookup_bridge": rows.get(key_i),
        "lookup_x": rows.get(key_x),
        "all": [*own.values(), *rows.values()],
    }


def find_sentence(context: str, sentence: str) -> int:
    """The one start of `sentence` in `context` at sentence boundaries (so 'Dan's pet' never matches in 'Jordan's')."""
    hits = [
        i
        for i in range(len(context) - len(sentence) + 1)
        if context.startswith(sentence, i)
        and (i == 0 or context[i - 1] == " ")
        and (i + len(sentence) == len(context) or context[i + len(sentence)] == " ")
    ]
    assert len(hits) == 1, f"{sentence!r} found {len(hits)} times in the context"
    return hits[0]


def tokens_in(offsets: list[tuple[int, int]], start: int, end: int) -> list[int]:
    """Token positions whose character span overlaps [start, end) (zero-width tokens never do)."""
    return [i for i, (s, e) in enumerate(offsets) if e > s and s < end and e > start]


def position_sets(
    c: dict, rendered: str, offsets: list[tuple[int, int]]
) -> tuple[dict[str, list[int]], dict[str, list[tuple[int, int]]]]:
    """Token positions of every set (module docstring) and the character spans they were cut from."""
    ctx = c["context_text"]
    assert rendered.count(ctx) == 1, f"{c['id']}: the context is not once in the prompt"
    base = rendered.index(ctx)
    structured = c["family"] in TASKS and c.get("format", "prose") != "prose"
    if structured:  # tasks_v2 tables / tool-output JSON: rows and objects, with headers in between
        marks, spans = tasks_structured_marks(c, base)
    else:
        st = statements(c)
        found = sorted((find_sentence(ctx, s), s) for s in st["all"])
        assert " ".join(s for _, s in found) == ctx, f"{c['id']}: the statements do not tile the context"

        def span(sentence: str) -> tuple[int, int]:
            i = base + find_sentence(ctx, sentence)
            return (i, i + len(sentence))

        marks = {"bind_bridge": [span(st["bind_bridge"])]}
        sent, (b0, _) = st["bind_bridge"], marks["bind_bridge"][0]
        assert sent.endswith(f"{c['bridge']}."), f"{c['id']}: {sent!r} does not end with the bridge"
        w0 = b0 + sent.rindex(c["bridge"])
        marks["bridge_word"] = [(w0, w0 + len(c["bridge"]))]
        marks["bind_other"] = [span(s) for s in st["bind_other"]]
        marks["lookup_bridge"] = [span(st["lookup_bridge"])] if st["lookup_bridge"] else []
        marks["lookup_x"] = [span(st["lookup_x"])] if st["lookup_x"] else []
        spans = [(base + at, base + at + len(sentence)) for at, sentence in found]
    marks["context"] = [(base, base + len(ctx))]
    sets = {k: sorted({i for a, b in v for i in tokens_in(offsets, a, b)}) for k, v in marks.items()}
    every = sorted({i for a, b in spans for i in tokens_in(offsets, a, b)})
    question = list(c["groups"]["question"])
    im_end = turn_end(rendered, c)
    final = [i for i, (s, e) in enumerate(offsets) if e > s and s >= im_end]
    sets["question"] = question
    sets["final"] = final
    sets["q_words"] = [i for i in question if i not in set(final)]
    marks["question"] = [(offsets[question[0]][0], offsets[question[-1]][1])]
    marks["final"] = [(offsets[final[0]][0], offsets[final[-1]][1])]
    marks["q_words"] = [(offsets[sets["q_words"][0]][0], offsets[sets["q_words"][-1]][1])] if sets["q_words"] else []
    check_sets(c, sets, every, len(offsets), exact_context=not structured)
    return sets, marks


def turn_end(rendered: str, c: dict) -> int:
    """Where the user turn ends: Qwen's / OLMo's <|im_end|>, else (Gemma) right after the user content (the question
    and its instruction)."""
    if "<|im_end|>" in rendered:
        return rendered.rindex("<|im_end|>")
    from scripts import tasks_v2 as T

    q_end = rendered.rindex(c["question"]) + len(c["question"])
    for instr in (T.DIGIT_INSTRUCTION, S.INSTRUCTION):
        j = rendered.find(instr, q_end)
        if 0 <= j - q_end <= 2:
            return j + len(instr)
    raise AssertionError(f"{c['id']}: no end of the user turn found")


def tasks_structured_marks(c: dict, base: int) -> tuple[dict[str, list[tuple[int, int]]], list[tuple[int, int]]]:
    """A tasks_v2 table / JSON context's statement spans (attn_knockout's rows and objects): the queried person's pick
    (bind_bridge), the bridge's cell in it (bridge_word), the other picks, the bridge's and X's locker rows; and every
    row / object (the statements; the headers between them are context, not statements)."""
    from scripts import attn_knockout as AK

    item = {**c, "context": c["context_text"]}
    sp, facts = AK.tasks_spans(item), AK.tasks_facts(item)
    holders = [p for p in facts["pick"] if f"{p}'s pick" in c["question"]]
    assert len(holders) == 1, f"{c['id']}: the question names {holders}"
    holder = holders[0]
    assert facts["pick"][holder] == c["bridge"], (
        f"{c['id']}: {holder} picked {facts['pick'][holder]}, not {c['bridge']}"
    )

    def at(s: tuple[int, int]) -> tuple[int, int]:
        return (base + s[0], base + s[1])

    a, b = sp["pick"][holder]["span"]
    w0 = a + c["context_text"][a:b].rindex(c["bridge"])
    lock = sp["locker"]
    marks = {"bind_bridge": [at((a, b))], "bridge_word": [at((w0, w0 + len(c["bridge"])))],
             "bind_other": [at(v["span"]) for p, v in sp["pick"].items() if p != holder],
             "lookup_bridge": [at(lock[c["bridge"]]["span"])] if c["bridge"] in lock else [],
             "lookup_x": [at(lock[c["cf_bridge"]]["span"])] if c["cf_bridge"] in lock else []}  # fmt: skip
    return marks, [at(v["span"]) for v in (*sp["pick"].values(), *lock.values())]


def check_sets(
    c: dict, sets: dict[str, list[int]], every: list[int], n_tokens: int, exact_context: bool = True
) -> None:
    """Disjointness, containment and the counterfactuals' footprint (asserts)."""
    name = c["id"]
    statement_parts = ("bind_bridge", "bind_other", "lookup_bridge", "lookup_x")
    for a in statement_parts:
        for b in statement_parts:
            assert a == b or not set(sets[a]) & set(sets[b]), f"{name}: {a} and {b} overlap"
    for k in ("bind_bridge", "bridge_word", "bind_other", "context", "question", "q_words", "final"):
        assert sets[k], f"{name}: {k} is empty"
    if c["family"] in SUITE + TASKS:
        assert sets["lookup_bridge"], f"{name}: the bridge's lookup statement is missing"
        assert sets["lookup_x"], f"{name}: X's lookup statement is missing"
    assert set(sets["bridge_word"]) <= set(sets["bind_bridge"]), f"{name}: the bridge word is outside its statement"
    if exact_context:  # prose: the statements tile the context; tables / JSON: headers sit between them
        assert sets["context"] == every, f"{name}: the context is not exactly its statements"
    else:
        assert set(every) < set(sets["context"]), f"{name}: a statement outside the context"
    assert max(sets["context"]) < min(sets["question"]), f"{name}: a statement token sits in the question"
    assert sorted(sets["q_words"] + sets["final"]) == sets["question"], f"{name}: question != q_words + final"
    assert sets["final"] == list(range(sets["final"][0], n_tokens)), f"{name}: final is not the prompt's tail"
    cf = c["changed"]["cf"]
    if c["family"] in CUE_ONLY:
        assert max(sets["context"]) < min(cf), f"{name}: C changes a statement in a cue-only family"
    else:
        footprint = set(sets["bind_bridge"]) | set(sets["bind_other"])
        assert set(cf) <= footprint, f"{name}: C changes more than the binding statements"
        assert set(cf) & set(sets["bridge_word"]), f"{name}: C does not change the bridge word"


def suite_cases(tok, n: int, families: list[str], map_run: str = SUITE_MAP) -> tuple[list[dict], dict]:
    """The first n cases per family of a suite_split map run (read_write's selection); cases whose C or O does not
    line up in this tokenizer are skipped and counted."""
    rows = [json.loads(line) for line in (P.RESULTS / map_run / "cases.jsonl").read_text().splitlines()]
    items = {f: {it["id"]: it for it in S.load(f)} for f in families}
    seen: collections.Counter = collections.Counter()
    skipped: collections.Counter = collections.Counter()
    out = []
    for r in rows:
        fam = r["family"]
        if fam not in families or seen[fam] >= n:
            continue
        it = items[fam][r["id"]]
        try:
            prep = P.prepare(it, tok)
        except AssertionError:
            skipped[fam] += 1
            continue
        seen[fam] += 1
        out.append(
            {**it, **prep, "rendered": S.render(tok, it["context"], it["question"]), "context_text": it["context"]}
        )
    return out, {"suite_map": map_run, "n": dict(seen), "unaligned_skipped": dict(skipped)}


def country_cases(tok, n: int, families: list[str], map_run: str = COUNTRY_MAP) -> tuple[list[dict], dict]:
    """The first n cases per family of a control_split map run (read_write's country selection)."""
    picked = [json.loads(line)["id"] for line in (C.RESULTS / map_run / "cases.jsonl").read_text().splitlines()]
    items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(items)}
    seen: collections.Counter = collections.Counter()
    skipped: collections.Counter = collections.Counter()
    out = []
    for uid in picked:
        index, item = by_uid[uid]
        fam = item["family"]
        if fam not in families or seen[fam] >= n:
            continue
        prep = E.prepare(item, index, tok, "chat_prefill")
        tok_a, tok_b = (S.answer_token(tok, a, "word") for a in (item["answer"], item["target_answer"]))
        if prep["status"] != "ok" or tok_a == tok_b:
            skipped[fam] += 1
            continue
        seen[fam] += 1
        c = {**item, **prep, "id": uid, "scene": uid, "cf_bridge": item["target"], "cf_answer": item["target_answer"],
             "answer_kind": "word", "tok_A": tok_a, "tok_b": tok_b, "read_ids": prep["ids"],
             "rendered": E.render(item["prompt"], "chat_prefill", tok),
             "context_text": chat.split_context(item["prompt"])[0]}  # fmt: skip
        out.append(c)
    return out, {"country_map": map_run, "n": dict(seen), "unaligned_skipped": dict(skipped)}


def tasks_cases(tok, n: int, families: list[str]) -> tuple[list[dict], dict]:
    """The first n scenes of TASKS_SET whose PP and PM the competence run TASKS_COMP got right on every prompt (whole,
    each step, C and O; tasks_v2.eligible at level 0), both families on the same scenes; scenes whose C or O does not
    line up in this tokenizer are skipped and counted."""
    from scripts import tasks_v2 as T

    assert TASKS_SET, "PP / PM need --tasks-set"
    assert TASKS_COMP, "PP / PM need --tasks-competence"
    items = T.eligible(TASKS_SET, TASKS_COMP, list(TASKS), 10**6, level="0")
    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in items:
        by_scene[it["scene"]][it["word"]] = it
    seen, skipped, out = 0, collections.Counter(), []
    for scene in sorted(by_scene):
        pair = by_scene[scene]
        if seen >= n or not set(families) <= set(pair):
            continue
        try:
            preps = {w: T.prepare(pair[w], tok) for w in families}
        except AssertionError:
            skipped["unaligned"] += 1
            continue
        seen += 1
        for w in families:
            it = pair[w]
            out.append({**it, **preps[w], "family": w, "rendered": T.render(tok, it), "context_text": it["context"]})
    return out, {"tasks_set": TASKS_SET, "competence": TASKS_COMP, "scenes": seen, "skipped": dict(skipped)}


def build_cases(tok, n: int, families: list[str]) -> tuple[list[dict], dict]:
    """Every case with its position sets (asserted), in family order."""
    suite = [f for f in families if f in SUITE]
    countries = [f for f in families if f in COUNTRIES]
    tasks = [f for f in families if f in TASKS]
    cases, counts = [], {}
    if suite:
        got, counts["suite"] = suite_cases(tok, n, suite)
        cases += got
    if countries:
        got, counts["countries"] = country_cases(tok, n, countries)
        cases += got
    if tasks:
        got, counts["tasks"] = tasks_cases(tok, n, tasks)
        cases += got
    for c in cases:
        enc = raw_encoding(tok, c["rendered"], offsets=True)
        assert enc["input_ids"] == c["ids"]["clean"], f"{c['id']}: the rendered prompt is not the run's"
        c["offsets"] = enc["offset_mapping"]
        c["sets"], c["marks"] = position_sets(c, c["rendered"], c["offsets"])
    order = {f: i for i, f in enumerate(families)}
    cases.sort(key=lambda c: order[c["family"]])
    return cases, counts


def zero_by_causality(pos: list[int], changed: list[int]) -> bool:
    """A copy at positions that all precede the first changed token is exactly zero at every layer (causal model)."""
    return max(pos) < min(changed)


def map_plan(c: dict, layers: tuple[int, ...]) -> list[tuple[str, int, str]]:
    """(set, layer, source) cells of one case that the map reads: C and its random-direction copy where C's delta is
    non-zero, O where O's is (zero cells are skipped)."""
    cells = []
    for s in SETS:
        pos = c["sets"][s]
        if not pos:
            continue
        zero = {src: zero_by_causality(pos, c["changed"][src]) for src in ("cf", "off")}
        for la in layers:
            if not zero["cf"]:
                cells += [(s, la, "cf"), (s, la, "rand")]
            if not zero["off"]:
                cells.append((s, la, "off"))
    return cells


# ---- reading edited runs (GPU) ------------------------------------------------------------------------------------


def unedited(model, c: dict) -> None:
    """suite_split's unedited_ld (the clean and C reads, the ends of frac), plus their top tokens."""
    ids = torch.tensor([c["read_ids"]["clean"], c["read_ids"]["cf"]], device="cuda")
    _, logits = model.generate_batch(ids, 1, [{}, {}], first_logits=True)
    c["ld_clean"], c["ld_cf"] = (float(lg[c["tok_b"]] - lg[c["tok_A"]]) for lg in logits)
    c["top_clean"], c["top_cf"] = (int(lg.argmax()) for lg in logits)


def read(model, c: dict, jobs: list[tuple[dict, dict]], outcomes: list[dict], validate: bool = False) -> None:
    """suite_split's read_jobs (one forward per edit, batched; role, ld, frac; 8 greedy tokens with `validate`), with
    the top token id kept for the examples."""
    read_ids = torch.tensor([c["read_ids"]["clean"]], device="cuda")
    gen_ids = torch.tensor([c["ids"]["clean"]], device="cuda")
    span = c["ld_cf"] - c["ld_clean"]
    judge = C.judge if c["family"] in COUNTRIES else None
    for start in range(0, len(jobs), P.BATCH):
        chunk = jobs[start : start + P.BATCH]
        edits = [e for _, e in chunk]
        _, logits = model.generate_batch(read_ids, 1, edits, first_logits=True)
        texts = model.generate_batch(gen_ids, 8, edits) if validate else None
        for row, (tags, _) in enumerate(chunk):
            lg = logits[row]
            top = int(lg.argmax())
            ld = float(lg[c["tok_b"]] - lg[c["tok_A"]])
            frac = (ld - c["ld_clean"]) / span if span else float("nan")  # span 0: only on a degenerate smoke case
            o = {"family": c["family"], "name": c["id"], "scene": c["scene"], **tags, "role": P.role(top, c),
                 "ld": round(ld, 3), "frac": round(frac, 4), "top": top, "top_text": model.decoded[top]}  # fmt: skip
            if texts is not None:
                said = judge(texts[row]) if judge else S.said(texts[row], c["answer_kind"])
                said = said.lower() if said else None
                o["greedy"] = texts[row]
                o["greedy_role"] = (
                    "b" if said == c["cf_answer"].lower() else "A" if said == c["answer"].lower() else "other"
                )
            outcomes.append(o)


def case_row(c: dict, tok) -> dict:
    """What a run keeps of a case: ids, answers, the prompt as read, its position sets and their character spans."""
    keep = ("id", "family", "scene", "bridge", "cf_bridge", "answer", "cf_answer", "answer_kind", "cue", "ld_clean",
            "ld_cf", "top_clean", "top_cf", "tok_A", "tok_b", "changed", "sets", "marks")  # fmt: skip
    row = {k: c[k] for k in keep if k in c}
    row["prompt"] = c["rendered"] + (" " if c["answer_kind"] == "digit" else "")  # exactly the read's text
    row["offsets"] = c["offsets"]
    for k in ("top_clean", "top_cf"):
        if k in c:
            row[f"{k}_text"] = tok.decode([c[k]])
    return row


def zero_delta(delta: torch.Tensor) -> bool:
    return not bool(torch.any(delta != 0))


# ---- manifests ----------------------------------------------------------------------------------------------------


def run_dir(name: str) -> Path:
    return RESULTS / name


def manifest_common(name: str, why: str, kind: str, families: list[str], n: int) -> dict:
    pins.check_run_name(name)
    suite_files = {f: S.DATA / f"{f}.json" for f in families if f in SUITE}
    inputs = {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in suite_files.values()}
    if any(f in SUITE for f in families):
        p = P.RESULTS / SUITE_MAP / "cases.jsonl"
        inputs[str(p.relative_to(pins.REPO_ROOT))] = sha256_of(p)
    if any(f in COUNTRIES for f in families):
        p = C.RESULTS / COUNTRY_MAP / "cases.jsonl"
        inputs[str(p.relative_to(pins.REPO_ROOT))] = sha256_of(p)
        inputs[str(pins.BIND_RECALL_FILE.relative_to(pins.REPO_ROOT))] = pins.BIND_RECALL_SHA256
    tasks = None
    if any(f in TASKS for f in families):
        for p in (pins.DATA_DIR / "tasks_v2" / str(TASKS_SET) / "items.jsonl",
                  pins.RESULTS_DIR / "tasks_v2" / str(TASKS_COMP) / "items.jsonl"):  # fmt: skip
            inputs[str(p.relative_to(pins.REPO_ROOT))] = sha256_of(p)
        tasks = {"set": TASKS_SET, "competence": TASKS_COMP}
    return {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "code": git_state(),
        "families": families,
        "n_per_family": n,
        "inputs": inputs,
        **({"tasks": tasks} if tasks else {}),
        "cases": f"suite: the first n per family of suite_split/{SUITE_MAP}'s cases (read_write's selection; "
        f"BL/BR/RL/RR and BLR/BRL share scenes); countries: the first n per family of control_split/{COUNTRY_MAP}'s",
        "sets": (__doc__ or "").split("\n\n")[3],
        "read": "suite_split's: one forward of the edited clean prompt (a digit's space token appended), the top "
        "token's role (b: X's answer, A: the bridge's, other), ld = logit(b) - logit(A), frac = (ld - ld_clean) / "
        "(ld_C - ld_clean)",
        "seeds": {"null": NULL_SEED, "bootstrap": BOOT_SEED, "random_dictionary": "777 + layer (suite_split's)"},
    }  # fmt: skip


def write_manifest(m: dict) -> Path:
    out = run_dir(m["run"])
    out.mkdir(parents=True, exist_ok=True)
    path = out / "manifest.json"
    assert not path.exists(), f"{path} exists; manifests are written once"
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path, flush=True)
    return out


def check_inputs(m: dict) -> None:
    for rel, sha in m["inputs"].items():
        assert sha256_of(pins.REPO_ROOT / rel) == sha, f"{rel} changed since the manifest"


# ---- plan (tokenizer only) ----------------------------------------------------------------------------------------


def stage_plan(n: int, families: list[str], layers: tuple[int, ...], reads_per_s: float) -> None:
    """Cases, set sizes and the map's job counts; with an assumed read throughput, the map's GPU hours."""
    tok = load_tokenizer()
    cases, counts = build_cases(tok, n, families)
    print(json.dumps(counts))
    per_fam: dict[str, list[int]] = collections.defaultdict(list)
    sizes: dict[str, dict[str, list[int]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in cases:
        per_fam[c["family"]].append(len(map_plan(c, layers)) + 3)  # + identity x2 and all@0
        for s in SETS:
            sizes[c["family"]][s].append(len(c["sets"][s]))
    total = sum(sum(v) for v in per_fam.values())
    for fam, v in per_fam.items():
        print(f"{fam}: {len(v)} cases, map reads per case {statistics.mean(v):.0f}; set sizes (median tokens): "
              + ", ".join(f"{s} {statistics.median(x):g}" for s, x in sizes[fam].items()))  # fmt: skip
    print(
        f"map: {len(layers)} layers, {total} edited reads; at {reads_per_s:g} reads/s: {total / reads_per_s / 3600:.2f} h"
    )


# ---- map ----------------------------------------------------------------------------------------------------------


def stage_map(name: str, why: str, n: int, families: list[str], layers: tuple[int, ...]) -> None:
    m = manifest_common(name, why, "map", families, n)
    m["question"] = "Where, by position set and layer, does each family carry its bridge (lens-free)?"
    m["layers"] = list(layers)
    m["layer_grid"] = {"coarse": list(COARSE), "window": list(WINDOW)}
    m["sources"] = {"cf": "C's block output copied at the set (AddRows of h_C - h_clean)",
                    "off": "O's, the same way, where O's delta is non-zero",
                    "rand": "C's delta with each row replaced by a random direction at that row's norm (null_rows, "
                            f"seed {NULL_SEED} + 1e9 x set index + 1e5 x case index + layer)"}  # fmt: skip
    m["sanity"] = {"identity": "AddRows of zero at every position (layers: the first and last map layer): no change",
                   "all0": "C's delta at every position at the first map layer: reproduces C's read",
                   "zero_cells": "cells whose positions all precede the first changed token are verified exactly zero "
                                 f"and skipped; for the first {N_NOOP_READ} cases of each cue-only family the zero C "
                                 "copies at the statements are read anyway (exact no-ops)",
                   "validation": f"8 greedy tokens for every edit of the first {N_VALIDATE} cases per family"}  # fmt: skip
    m["decision"] = {"transit": f"C's copy gives X's answer in >= {TRANSIT_FLIPS:.0%} of cases and its Wilson 95% lower "
                                "bound is above the upper bound of every control's change rate (O where non-zero, "
                                "rand); zero-delta cases count as unchanged",
                     "handoff": "per family and statement set, the last transit layer; per family, the first layer at "
                                "which the question set is in transit",
                     "fixed": "before the 27B run (the 0.8B smoke checks the code path only)"}  # fmt: skip
    out = write_manifest(m)
    run_map(out, m, layers)


@torch.no_grad()
def run_map(out: Path, m: dict, layers: tuple[int, ...]) -> None:
    from bridge_jspace.model import load_model

    assert not (out / "outcomes.jsonl").exists(), f"{out} has results; runs are written once"
    check_inputs(m)
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    cases, counts = build_cases(tok, m["n_per_family"], m["families"])
    print(json.dumps(counts), flush=True)
    record = tuple(layers)
    outcomes: list[dict] = []
    zeros: list[dict] = []
    causality: list[dict] = []
    seen: collections.Counter = collections.Counter()
    for k, c in enumerate(progress(cases, "map cases")):
        fam = c["family"]
        unedited(model, c)
        h = {s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=record)[1] for s in SOURCES}
        everywhere = list(range(len(c["ids"]["clean"])))
        zero_all = torch.zeros_like(h["clean"][layers[0]])
        jobs: list[tuple[dict, dict]] = [({"check": "unedited", "layer": None}, {})]  # same batch as identity
        jobs += [
            ({"check": "identity", "layer": la}, {la: AddRows(zero_all, everywhere)}) for la in (layers[0], layers[-1])
        ]
        all0 = h["cf"][layers[0]] - h["clean"][layers[0]]
        jobs.append(({"check": "all0", "layer": layers[0]}, {layers[0]: AddRows(all0, everywhere)}))
        for si, s in enumerate(SETS):
            pos = c["sets"][s]
            if not pos:
                continue
            for la in layers:
                for source in ("cf", "off"):
                    delta = h[source][la][pos] - h["clean"][la][pos]
                    predicted = zero_by_causality(pos, c["changed"][source])
                    is_zero = zero_delta(delta)
                    if predicted and not is_zero:
                        causality.append({"name": c["id"], "set": s, "layer": la, "source": source,
                                          "max_abs": float(delta.abs().max())})  # fmt: skip
                    tags = {"set": s, "layer": la, "source": source}
                    if is_zero:  # the copy is the identity: skipped (read anyway for the first cue-only cases)
                        if source == "cf" and fam in CUE_ONLY and seen[fam] < N_NOOP_READ:
                            jobs.append(({**tags, "noop_check": True}, {la: AddRows(delta, pos)}))
                        else:
                            zeros.append({"family": fam, "name": c["id"], **tags})
                        if source == "cf":  # its random-direction copy is zero too
                            zeros.append({"family": fam, "name": c["id"], **tags, "source": "rand"})
                        continue
                    jobs.append((tags, {la: AddRows(delta, pos)}))
                    if source == "cf":
                        seed = NULL_SEED + 1_000_000_000 * si + 100_000 * k + la
                        noise = null_rows(delta, torch.Generator(device="cuda").manual_seed(seed))
                        jobs.append(({**tags, "source": "rand"}, {la: AddRows(noise, pos)}))
        read(model, c, jobs, outcomes, validate=seen[fam] < N_VALIDATE)
        seen[fam] += 1
    write_jsonl(out / "cases.jsonl", [case_row(c, tok) for c in cases])
    write_jsonl(out / "outcomes.jsonl", outcomes)
    write_jsonl(out / "zero_cells.jsonl", zeros)
    summary = summarize_map(outcomes, zeros, cases, layers)
    summary.update(counts=counts, seconds=round(time.time() - t0), causality_violations=causality[:50],
                   n_causality_violations=len(causality), reads=len(outcomes))  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_map_md(out / "summary.md", m["run"], summary, layers)
    print((out / "summary.md").read_text())


def summarize_map(outcomes: list[dict], zeros: list[dict], cases: list[dict], layers: tuple[int, ...]) -> dict:
    n_cases = collections.Counter(c["family"] for c in cases)
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    n_zero = collections.Counter((z["family"], z["set"], z["layer"], z["source"]) for z in zeros)
    for o in outcomes:
        if o.get("noop_check"):  # a zero-delta copy read as a check: the identity, counted as unchanged
            n_zero[(o["family"], o["set"], o["layer"], o["source"])] += 1
        elif "set" in o:
            cells[(o["family"], o["set"], o["layer"], o["source"])].append(o)
    rates, transit = [], {}
    for fam in n_cases:
        n = n_cases[fam]
        for s in SETS:
            for la in layers:
                key = (fam, s, la, "cf")
                if not cells[key] and not n_zero[key]:
                    continue
                row: dict[str, Any] = {"family": fam, "set": s, "layer": la, "n": n}
                ctrl_hi = []
                for src in ("cf", "off", "rand"):
                    rows, z = cells[(fam, s, la, src)], n_zero[(fam, s, la, src)]
                    assert len(rows) + z == n, f"{fam}/{s}/{la}/{src}: {len(rows)} reads + {z} zero cells != {n}"
                    flips = sum(o["role"] == "b" for o in rows)
                    changed = sum(o["role"] != "A" for o in rows)
                    row[src] = {"flips": wilson(flips, n), "changed": wilson(changed, n), "zero": z,
                                "frac": sum(o["frac"] for o in rows) / n}  # fmt: skip
                    if src != "cf" and rows:
                        ctrl_hi.append(row[src]["changed"][2])
                f = row["cf"]["flips"]
                row["transit"] = bool(f[0] >= TRANSIT_FLIPS and f[1] > max(ctrl_hi, default=0.0))
                rates.append(row)
                if row["transit"]:
                    transit.setdefault(fam, {}).setdefault(s, []).append(la)
    handoff = {
        fam: {"last_statement_transit": {s: max(v) for s, v in t.items() if s in STATEMENT_SETS},
              "first_question_transit": min(t["question"]) if "question" in t else None}
        for fam, t in transit.items()
    }  # fmt: skip
    return {"rates": rates, "transit": transit, "handoff": handoff, "sanity": sanity(outcomes, cases),
            "validation": P.validation(outcomes)}  # fmt: skip


def sanity(outcomes: list[dict], cases: list[dict]) -> dict:
    by_name = {c["id"]: c for c in cases}
    ident = [o for o in outcomes if o.get("check") == "identity"]
    plain = {o["name"]: o["ld"] for o in outcomes if o.get("check") == "unedited"}
    all0 = [o for o in outcomes if o.get("check") == "all0"]
    noop = [o for o in outcomes if o.get("noop_check")]
    ident_ld = {o["name"]: o["ld"] for o in ident if o["layer"] == min(x["layer"] for x in ident)}
    out: dict[str, Any] = {}
    if ident:
        out["identity"] = {"n": len(ident), "max_abs_ld_minus_clean": max(abs(o["ld"] - by_name[o["name"]]["ld_clean"]) for o in ident),
                           "max_abs_ld_minus_unedited_same_batch": max(abs(o["ld"] - plain[o["name"]]) for o in ident),
                           "top_is_clean_top": statistics.mean(o["top"] == by_name[o["name"]]["top_clean"] for o in ident)}  # fmt: skip
    if all0:
        out["all0"] = {"n": len(all0), "max_abs_ld_minus_C": max(abs(o["ld"] - by_name[o["name"]]["ld_cf"]) for o in all0),
                       "top_is_C_top": statistics.mean(o["top"] == by_name[o["name"]]["top_cf"] for o in all0)}  # fmt: skip
    if noop:
        out["noop_statements"] = {"n": len(noop), "families": sorted({o["family"] for o in noop}),
                                  "max_abs_ld_minus_identity": max(abs(o["ld"] - ident_ld[o["name"]]) for o in noop),
                                  "top_is_clean_top": statistics.mean(o["top"] == by_name[o["name"]]["top_clean"] for o in noop)}  # fmt: skip
    return out


def write_map_md(path: Path, run: str, s: dict, layers: tuple[int, ...]) -> None:
    lines = [f"# {EXP} / {run}", "", f"Cases: {json.dumps(s.get('counts'))}", f"Sanity: {json.dumps(s['sanity'])}",
             f"Read vs greedy: {json.dumps(s['validation'])}",
             f"Causality violations (predicted-zero cells with a non-zero delta): {s.get('n_causality_violations')}", "",
             f"Transit (C flips >= {TRANSIT_FLIPS:.0%}, above the controls): {json.dumps(s['transit'])}",
             f"Handoff: {json.dumps(s['handoff'])}", "",
             "C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); "
             "max control change rate (O or random) per row", ""]  # fmt: skip
    by = {(r["family"], r["set"], r["layer"]): r for r in s["rates"]}
    for fam in dict.fromkeys(r["family"] for r in s["rates"]):
        lines += [f"## {fam}", "", "| set | " + " | ".join(str(la) for la in layers) + " | max control |",
                  "|---" * (len(layers) + 2) + "|"]  # fmt: skip
        for st in SETS:
            cells, ctrl = [], 0.0
            for la in layers:
                r = by.get((fam, st, la))
                if r is None:
                    cells.append("-")
                    continue
                if r["cf"]["zero"] == r["n"]:
                    cells.append(".")
                else:
                    cells.append(f"{100 * r['cf']['flips'][0]:.0f}{'*' if r['transit'] else ''}")
                ctrl = max([ctrl] + [r[x]["changed"][0] for x in ("off", "rand")])
            if any(x != "-" for x in cells):
                lines.append(f"| {st} | " + " | ".join(cells) + f" | {100 * ctrl:.0f} |")
        lines.append("")
    path.write_text("\n".join(lines) + "\n")


# ---- cells for parts / readwrite ----------------------------------------------------------------------------------


def parse_force(force: list[str] | None) -> dict[str, list[int]] | None:
    """--force SET:LAYER ... (smoke runs): the cells for every family, bypassing the map's transit rule."""
    if not force:
        return None
    out: dict[str, list[int]] = collections.defaultdict(list)
    for f in force:
        s, la = f.split(":")
        assert s in SETS, f"unknown set {s}"
        out[s].append(int(la))
    return dict(out)


def stage_cells(map_name: str, families: list[str], force: dict[str, list[int]] | None) -> tuple[dict, dict]:
    """Per family and set, the map's transit layers on the coarse grid in [N/4, onset) (or the forced cells)."""
    summary_path = run_dir(map_name) / "summary.json"
    blob = json.loads(summary_path.read_text())
    if force is not None:
        cells = {f: {s: sorted(v) for s, v in force.items()} for f in families}
    else:
        cells = {
            f: {
                s: [la for la in v if la in COARSE and SPLIT_LO <= la < ONSET]
                for s, v in blob["transit"].get(f, {}).items()
            }
            for f in families
        }
        cells = {f: {s: v for s, v in d.items() if v and s in CELL_SETS} for f, d in cells.items()}
    return cells, {"run": map_name, "summary_sha256": sha256_of(summary_path), "forced": force,
                   "sets": list(CELL_SETS), "sub_n": SUB_N, "layers_from": SPLIT_LO}  # fmt: skip


def windows_of(layers: list[int]) -> dict[str, list[int]]:
    return {"primary": [la for la in layers if la >= PRIMARY_LO], "secondary": list(layers)}


def use_tasks(m: dict) -> None:
    """A map run's tasks_v2 set and competence run (PP / PM) for the stages that rebuild its cases."""
    global TASKS_SET, TASKS_COMP
    if "tasks" in m:
        TASKS_SET, TASKS_COMP = m["tasks"]["set"], m["tasks"]["competence"]


def reload_cases(m: dict, tok) -> list[dict]:
    """The map's cases, rebuilt (deterministic) and checked against its cases.jsonl."""
    use_tasks(m)
    cases, _ = build_cases(tok, m["n_per_family"], m["families"])
    mine = [json.loads(line)["id"] for line in (run_dir(m["map"]["run"]) / "cases.jsonl").read_text().splitlines()]
    assert [c["id"] for c in cases] == mine, "the rebuilt cases are not the map's"
    if SUB_N is None:
        return cases
    seen: collections.Counter = collections.Counter()
    kept = []
    for c in cases:
        seen[c["family"]] += 1
        if seen[c["family"]] <= SUB_N:
            kept.append(c)
    return kept


# ---- parts --------------------------------------------------------------------------------------------------------

CALIBRATION = ("jspace_wo_own", "rand_omp")


def stage_parts(name: str, map_name: str, why: str, force: dict[str, list[int]] | None) -> None:
    mm = json.loads((run_dir(map_name) / "manifest.json").read_text())
    use_tasks(mm)
    m = manifest_common(name, why, "parts", mm["families"], mm["n_per_family"])
    cells, m["map"] = stage_cells(map_name, mm["families"], force)
    m["cells"] = cells
    m["question"] = "Where the copy carries the bridge (transit cells), which part carries it: the J-space or the rest?"
    m["lens"] = {pins.FROZEN_LENS: list(pins.LENS_SOURCES[pins.FROZEN_LENS]), "sha256": pins.FROZEN_LENS_SHA256}
    m["parts"] = "suite_split's parts with --calibrate: full (C), O's full copy, lens2 / not_lens2, jspace / not_jspace, " \
        f"jspace_wo_own, rand_omp ({K_ATOMS}-atom signed OMP), each with its random-direction null, lens2_matched and " \
        "jspace_matched (exp02's matched-alignment pieces)"  # fmt: skip
    m["windows"] = {"primary": f"layers [{PRIMARY_LO}, {ONSET})", "secondary": f"layers [{SPLIT_LO}, {ONSET})"}
    m["decision"] = (__doc__ or "").split("\n\n")[6]
    out = write_manifest(m)
    run_parts(out, m)


@torch.no_grad()
def run_parts(out: Path, m: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    assert not (out / "outcomes.jsonl").exists(), f"{out} has results; runs are written once"
    check_inputs(m)
    map_dir = run_dir(m["map"]["run"])
    assert sha256_of(map_dir / "summary.json") == m["map"]["summary_sha256"], "the map changed since the manifest"
    cells = m["cells"]
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    cases = reload_cases(m, tok)
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    layers = sorted({la for f in cells.values() for v in f.values() for la in v})
    assert layers, "no transit cell in any family"
    work = [(la, k) for la in layers for k, c in enumerate(cases) if any(la in v for v in cells[c["family"]].values())]
    outcomes: list[dict] = []
    fve: list[dict] = []
    current, dictionary, rdict = None, None, None
    for la, k in progress(work, "parts (layer, case)"):
        if la != current:  # one layer's dictionaries at a time: two [letters, d] fp32 maps fit next to the 27B
            dictionary = rdict = None
            torch.cuda.empty_cache()
            dictionary = lens.vectors(la, letters)
            gen = torch.Generator(device="cuda").manual_seed(777 + la)
            rdict = torch.nn.functional.normalize(torch.randn(dictionary.shape, device="cuda", generator=gen), dim=-1)
            g = torch.Generator(device="cuda").manual_seed(BOOT_SEED + la)
            x = torch.randn(P.CHANCE_DRAWS, dictionary.shape[1], device="cuda", generator=g)
            share = (signed_omp(dictionary, x, K_ATOMS).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
            fve.append({"layer": la, "what": "chance", "share": round(float(share), 4)})
            current = la
        assert dictionary is not None
        assert rdict is not None
        c = cases[k]
        if "ld_clean" not in c:
            unedited(model, c)
        h = {s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=(la,))[1][la] for s in SOURCES}
        pair = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])], device="cuda")
        jobs: list[tuple[dict, dict]] = []
        for si, s in enumerate(SETS):
            if la not in cells[c["family"]].get(s, []):
                continue
            pos = c["sets"][s]
            delta = h["cf"][pos] - h["clean"][pos]
            total = float(delta.norm() ** 2)
            if total == 0:
                continue
            base = {"set": s, "layer": la}
            jobs.append(({**base, "part": "full", "source": "cf", "null": False}, {la: AddRows(delta, pos)}))
            off = h["off"][pos] - h["clean"][pos]
            if not zero_delta(off):
                jobs.append(({**base, "part": "full", "source": "off", "null": False}, {la: AddRows(off, pos)}))
            lens2 = lens2_part(delta, lens.vectors(la, pair))
            jspace = signed_omp(dictionary, delta, K_ATOMS)
            parts = {"lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace, "not_jspace": delta - jspace,
                     "jspace_wo_own": signed_omp(dictionary, delta - lens2, K_ATOMS),
                     "rand_omp": signed_omp(rdict, delta, K_ATOMS)}  # fmt: skip
            for what in ("lens2", "jspace", *CALIBRATION):
                fve.append({"family": c["family"], "name": c["id"], "scene": c["scene"], "set": s, "layer": la,
                            "what": what, "share": round(float(parts[what].norm() ** 2) / total, 4)})  # fmt: skip
            for pi, (pname, part) in enumerate(parts.items()):
                seed = NULL_SEED + 1_000_000_000 * si + 100_000 * k + 100 * la + pi
                noise = null_rows(part, torch.Generator(device="cuda").manual_seed(seed))
                jobs.append(({**base, "part": pname, "source": "cf", "null": False}, {la: AddRows(part, pos)}))
                jobs.append(({**base, "part": pname, "source": "cf", "null": True}, {la: AddRows(noise, pos)}))
            for mi, pname in enumerate(("lens2", "jspace")):
                gen = torch.Generator(device="cuda").manual_seed(
                    NULL_SEED + 1_000_000_000 * si + 100_000 * k + 100 * la + 50 + mi
                )
                matched = P.matched_rows(parts[pname], delta, gen)
                jobs.append(
                    ({**base, "part": f"{pname}_matched", "source": "cf", "null": False}, {la: AddRows(matched, pos)})
                )
        read(model, c, jobs, outcomes)
    write_jsonl(out / "cases.jsonl", [case_row(c, tok) for c in cases])
    write_jsonl(out / "outcomes.jsonl", outcomes)
    write_jsonl(out / "fve.jsonl", fve)
    summary = summarize_parts(outcomes, fve, cells)
    summary["seconds"] = round(time.time() - t0)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_parts_md(out / "summary.md", m["run"], summary)
    print((out / "summary.md").read_text())


def d1_verdict(conc: tuple[float, ...], null_conc: tuple[float, ...] | None, rest_minus_j: tuple[float, ...]) -> str:
    """The manifest's J-space verdict for one family, set and window (frac)."""
    if conc[1] > INSIDE and (null_conc is None or conc[1] > null_conc[2]):
        return "inside"
    if conc[2] < OUTSIDE and rest_minus_j[1] > 0:
        return "around"
    return "inconclusive"


def scene_scores(rows: list[dict], fve: list[dict], part: str) -> tuple[dict, dict, dict]:
    """Per scene: the part's effect, the full copy's effect (frac, averaged over layers) and the part's variance share."""
    eff: dict[str, list[float]] = collections.defaultdict(list)
    full: dict[str, list[float]] = collections.defaultdict(list)
    for o in rows:
        if o["source"] == "cf" and not o["null"]:
            if o["part"] == part:
                eff[o["scene"]].append(o["frac"])
            elif o["part"] == "full":
                full[o["scene"]].append(o["frac"])
    share: dict[str, list[float]] = collections.defaultdict(list)
    for f in fve:
        if f.get("what") == part:
            share[f["scene"]].append(f["share"])
    mean = statistics.mean
    return (
        {s: mean(v) for s, v in eff.items()},
        {s: mean(v) for s, v in full.items()},
        {s: mean(v) for s, v in share.items()},
    )


def concentration_diff(a: tuple[dict, dict, dict], b: tuple[dict, dict, dict]) -> tuple[float, ...]:
    """Concentration of b minus a over their common scenes, scenes resampled jointly (paired readers)."""
    scenes = sorted(set.intersection(*(set(d) for d in (*a, *b))))
    if not scenes:
        return (float("nan"),) * 3
    arr = {
        k: np.array([d[s] for s in scenes]) for k, d in zip(("pa", "fa", "sa", "pb", "fb", "sb"), (*a, *b), strict=True)
    }
    idx = np.random.default_rng(BOOT_SEED).integers(0, len(scenes), size=(N_BOOT, len(scenes)))

    def conc(p, f, s, i=None):
        p, f, s = (p, f, s) if i is None else (p[i], f[i], s[i])
        return p.sum(-1) / np.maximum((s * f).sum(-1), 1e-12)

    point = conc(arr["pb"], arr["fb"], arr["sb"]) - conc(arr["pa"], arr["fa"], arr["sa"])
    boots = conc(arr["pb"], arr["fb"], arr["sb"], idx) - conc(arr["pa"], arr["fa"], arr["sa"], idx)
    return (float(point), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))


def summarize_parts(outcomes: list[dict], fve: list[dict], cells: dict) -> dict:
    out: dict[str, Any] = {"cells": {}}
    for fam, by_set in cells.items():
        for s, layers in by_set.items():
            for wname, win in windows_of(layers).items():
                if not win:
                    continue
                rows = [o for o in outcomes if o["family"] == fam and o.get("set") == s and o["layer"] in win]
                mine = [f for f in fve if f.get("family") == fam and f.get("set") == s and f["layer"] in win]
                if not rows:
                    continue
                cell: dict[str, Any] = {"layers": win, "n": len({o["name"] for o in rows})}
                for measure in ("frac", "flip"):
                    cell[measure] = P.verdicts(rows, measure, mine)
                full = P.scores(rows, "frac", part="full", null=False, source="cf")
                calib = {}
                for p in CALIBRATION:
                    eff = P.scores(rows, "frac", part=p, null=False, source="cf")
                    per: dict[str, list[float]] = collections.defaultdict(list)
                    for f in mine:
                        if f["what"] == p:
                            per[f["name"]].append(f["share"])
                    calib[p] = {"mean": statistics.mean(eff.values()),
                                "concentration": P.concentration(eff, full, {k: statistics.mean(v) for k, v in per.items()})}  # fmt: skip
                cell["calibration"] = calib
                j = cell["frac"]["jspace"]
                cell["verdict"] = d1_verdict(
                    j["concentration"], calib["rand_omp"]["concentration"], j["not_jspace - jspace"]
                )
                cell["verdict_strict"] = j["verdict"]
                cell["share_median"] = {w: statistics.median(f["share"] for f in mine if f["what"] == w)
                                        for w in ("jspace", "lens2", *CALIBRATION) if any(f["what"] == w for f in mine)}  # fmt: skip
                out["cells"][f"{fam}/{s}/{wname}"] = cell
    out["pairs"] = pair_contrasts(outcomes, fve, cells)
    out["chance_share"] = statistics.median(f["share"] for f in fve if f["what"] == "chance") if fve else None
    out["claims"] = parts_claims(out["cells"])
    return out


def pair_contrasts(outcomes: list[dict], fve: list[dict], cells: dict) -> dict:
    """Paired readers at statement sets: the same patch (identical C delta: the statements precede the question), two
    questions. Concentration of the recall-used family minus the lookup-used one, scene bootstrap."""
    out = {}
    for a, b in PAIRS:
        for s in STATEMENT_SETS:
            la_a, la_b = cells.get(a, {}).get(s, []), cells.get(b, {}).get(s, [])
            common = [la for la in la_a if la in la_b and la >= PRIMARY_LO]
            if not common:
                continue
            got = []
            for fam in (a, b):
                rows = [o for o in outcomes if o["family"] == fam and o.get("set") == s and o["layer"] in common]
                mine = [f for f in fve if f.get("family") == fam and f.get("set") == s and f["layer"] in common]
                got.append(scene_scores(rows, mine, "jspace"))
            shares = [{(f["scene"], f["layer"]): f["share"] for f in fve
                       if f.get("family") == fam and f.get("set") == s and f.get("what") == "jspace"} for fam in (a, b)]  # fmt: skip
            same = [abs(shares[0][key] - shares[1][key]) for key in set(shares[0]) & set(shares[1])]
            out[f"{b}-{a}/{s}"] = {"layers": common, "concentration_diff": concentration_diff(got[0], got[1]),
                                   "same_patch_max_share_diff": max(same) if same else None}  # fmt: skip
    return out


def parts_claims(cells: dict) -> dict:
    """The J-space half of the decision rule (the lens-write half is readwrite's)."""
    claims: dict[str, Any] = {}
    for fam in LOOKUP_USED_BOUND:
        prim = {k.split("/")[1]: v["verdict"] for k, v in cells.items()
                if k.startswith(f"{fam}/") and k.endswith("/primary") and k.split("/")[1] in STATEMENT_SETS}  # fmt: skip
        if not prim:
            claims[fam] = "no statement set in transit at the primary layers: H-loc's location premise fails there"
            continue
        pos_ok = {}
        for s in prim:
            pc = next((cells[f"{p}/{s}/primary"]["verdict"] for p in POSITIVE if f"{p}/{s}/primary" in cells), None)
            pos_ok[s] = pc
        claims[fam] = {"statement_verdicts": prim, "positive_control": pos_ok,
                       "jspace_half": "H-loc" if "inside" in prim.values() else
                       "H-around" if all(v == "around" for v in prim.values()) and all(pos_ok.get(s) == "inside" for s in prim)
                       else "H-around but positive control fails (not interpretable)" if all(v == "around" for v in prim.values())
                       else "mixed / inconclusive"}  # fmt: skip
    return claims


def write_parts_md(path: Path, run: str, s: dict) -> None:
    lines = [f"# {EXP} / {run}", "", f"Claims (J-space half): {json.dumps(s['claims'])}", "",
             "| family/set/window | layers | n | full (frac / flips) | J-space part | rest | J matched | concentration | "
             "rand-dict null | verdict (strict) |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, c in s["cells"].items():
        fm, fl = c["frac"]["means"], c["flip"]["means"]
        conc, null = c["frac"]["jspace"]["concentration"], c["calibration"]["rand_omp"]["concentration"]
        lines.append(f"| {key} | {c['layers']} | {c['n']} | {100 * fm['full']:.0f}% / {100 * fl['full']:.0f}% | "
                     f"{100 * fm['jspace']:.1f}% / {100 * fl['jspace']:.0f}% | {100 * fm['not_jspace']:.0f}% | "
                     f"{100 * fm['jspace_matched']:.1f}% | {conc[0]:.2f} [{conc[1]:.2f}, {conc[2]:.2f}] | "
                     f"{null[0]:.2f} [{null[1]:.2f}, {null[2]:.2f}] | {c['verdict']} ({c['verdict_strict']}) |")  # fmt: skip
    lines += ["", f"Paired readers (concentration difference, recall-used minus lookup-used): {json.dumps(s['pairs'])}",
              f"Chance share: {s['chance_share']}"]  # fmt: skip
    path.write_text("\n".join(lines) + "\n")


# ---- readwrite ----------------------------------------------------------------------------------------------------


def stage_readwrite(name: str, map_name: str, why: str, parts: str | None, force: dict[str, list[int]] | None) -> None:
    mm = json.loads((run_dir(map_name) / "manifest.json").read_text())
    use_tasks(mm)
    m = manifest_common(name, why, "readwrite", mm["families"], mm["n_per_family"])
    cells, m["map"] = stage_cells(map_name, mm["families"], force)
    m["cells"] = cells
    m["question"] = "At the transit cells, does the J-lens read the bridge, and can its direction write it?"
    m["lens"] = {pins.FROZEN_LENS: list(pins.LENS_SOURCES[pins.FROZEN_LENS]), "sha256": pins.FROZEN_LENS_SHA256}
    m["scales"] = list(SCALES)
    m["read"] = "J-lens readout of the clean run at the set's positions: the bridge's best rank among word tokens " \
        "(any single-token surface; formatting tokens removed) over the positions; X's the same (the floor)"  # fmt: skip
    m["write"] = "v_X - v_I (unit lens vectors), per position scaled to the norm of C's copy there times each scale; " \
        "control: a random direction per position at the same norm; C's copy itself"  # fmt: skip
    m["windows"] = {"primary": f"layers [{PRIMARY_LO}, {ONSET})", "secondary": f"layers [{SPLIT_LO}, {ONSET})"}
    m["decision"] = (__doc__ or "").split("\n\n")[6]
    if parts:
        p = run_dir(parts) / "summary.json"
        m["parts"] = {"run": parts, "summary_sha256": sha256_of(p)}
    out = write_manifest(m)
    run_readwrite(out, m)


@torch.no_grad()
def run_readwrite(out: Path, m: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    assert not (out / "outcomes.jsonl").exists(), f"{out} has results; runs are written once"
    check_inputs(m)
    assert sha256_of(run_dir(m["map"]["run"]) / "summary.json") == m["map"]["summary_sha256"], "the map changed"
    cells = m["cells"]
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    cases = reload_cases(m, tok)
    lens = JLens(model, pins.FROZEN_LENS)
    reads, outcomes = [], []
    for k, c in enumerate(progress(cases, "readwrite cases")):
        mine = cells[c["family"]]
        rec = tuple(sorted({la for v in mine.values() for la in v}))
        if not rec:
            continue
        unedited(model, c)
        h = {s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=rec)[1] for s in ("clean", "cf")}
        i_tok, x_tok = model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])
        i_ids, x_ids = model.surface_ids(c["bridge"]), model.surface_ids(c["cf_bridge"])
        jobs: list[tuple[dict, dict]] = []
        for si, s in enumerate(SETS):
            for la in mine.get(s, []):
                pos = c["sets"][s]
                logits = lens.readout(h["clean"][la][pos], la)
                ri = [model.word_rank(row, i_ids) for row in logits] if i_ids else []
                rx = [model.word_rank(row, x_ids) for row in logits] if x_ids else []
                reads.append({"family": c["family"], "name": c["id"], "scene": c["scene"], "set": s, "layer": la,
                              "rank_bridge": min(ri) if ri else None, "rank_x": min(rx) if rx else None,
                              "best_position": pos[int(np.argmin(ri))] if ri else None})  # fmt: skip
                delta = h["cf"][la][pos] - h["clean"][la][pos]
                if zero_delta(delta):
                    continue
                norms = delta.norm(dim=-1, keepdim=True)
                v = lens.vectors(la, torch.tensor([i_tok, x_tok], device="cuda"))
                direction = torch.nn.functional.normalize(v[1] - v[0], dim=-1).expand_as(delta)
                gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_000_000 * si + 100_000 * k + la)
                edits = {"copy": delta}
                for sc in SCALES:
                    edits[f"lens_x{sc:g}"] = sc * norms * direction
                    edits[f"random_x{sc:g}"] = null_rows(sc * norms * direction, gen)
                for pname, vec in edits.items():
                    jobs.append(
                        ({"set": s, "layer": la, "part": pname, "source": "cf", "null": False}, {la: AddRows(vec, pos)})
                    )
        read(model, c, jobs, outcomes)
    write_jsonl(out / "cases.jsonl", [case_row(c, tok) for c in cases])
    write_jsonl(out / "reads.jsonl", reads)
    write_jsonl(out / "outcomes.jsonl", outcomes)
    summary = summarize_readwrite(reads, outcomes, cells)
    if "parts" in m:
        ps = json.loads((run_dir(m["parts"]["run"]) / "summary.json").read_text())
        summary["claims"] = d1_claims(ps, summary)
    summary["seconds"] = round(time.time() - t0)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_readwrite_md(out / "summary.md", m["run"], summary)
    print((out / "summary.md").read_text())


def write_verdict(rows: list[dict]) -> tuple[str, dict]:
    """The manifest's lens-write verdict from one cell's outcomes (flips; paired over cases)."""
    per = {}
    for sc in SCALES:
        lens_f = {o["name"]: float(o["role"] == "b") for o in rows if o["part"] == f"lens_x{sc:g}"}
        rand_f = {o["name"]: float(o["role"] == "b") for o in rows if o["part"] == f"random_x{sc:g}"}
        names = sorted(set(lens_f) & set(rand_f))
        if not names:
            continue
        lf = statistics.mean(lens_f[x] for x in names)
        diff = paired_bootstrap_diff([lens_f[x] for x in names], [rand_f[x] for x in names], N_BOOT, BOOT_SEED)
        per[f"x{sc:g}"] = {"lens_flips": lf, "random_flips": statistics.mean(rand_f[x] for x in names), "diff": diff}
    if not per:
        return "no data", per
    written = any(
        v["lens_flips"] >= WRITTEN_FLIPS and v["diff"][1] > 0 for k, v in per.items() if float(k[1:]) <= WRITE_MAX_SCALE
    )
    not_written = all(v["diff"][2] < NOT_WRITTEN for v in per.values())
    return ("written" if written else "not written" if not_written else "inconclusive"), per


def summarize_readwrite(reads: list[dict], outcomes: list[dict], cells: dict) -> dict:
    out: dict[str, Any] = {"cells": {}}
    for fam, by_set in cells.items():
        for s, layers in by_set.items():
            for wname, win in windows_of(layers).items():
                if not win:
                    continue
                rd = [r for r in reads if r["family"] == fam and r["set"] == s and r["layer"] in win]
                best: dict[str, int] = {}
                best_x: dict[str, int] = {}
                for r in rd:
                    if r["rank_bridge"] is not None:
                        best[r["name"]] = min(best.get(r["name"], 10**9), r["rank_bridge"])
                    if r["rank_x"] is not None:
                        best_x[r["name"]] = min(best_x.get(r["name"], 10**9), r["rank_x"])
                rows = [o for o in outcomes if o["family"] == fam and o["set"] == s and o["layer"] in win]
                verdict, per = write_verdict(rows)
                write = {}
                for pname in dict.fromkeys(o["part"] for o in rows):
                    sel = [o for o in rows if o["part"] == pname]
                    write[pname] = {"frac": statistics.mean(o["frac"] for o in sel),
                                    "flips": statistics.mean(o["role"] == "b" for o in sel)}  # fmt: skip
                out["cells"][f"{fam}/{s}/{wname}"] = {
                    "layers": win, "n": len(best),
                    "read_top10": statistics.mean(v <= 10 for v in best.values()) if best else None,
                    "read_top1": statistics.mean(v <= 1 for v in best.values()) if best else None,
                    "x_top10": statistics.mean(v <= 10 for v in best_x.values()) if best_x else None,
                    "write": write, "by_scale": per, "verdict": verdict,
                }  # fmt: skip
    return out


def d1_claims(parts_summary: dict, rw: dict) -> dict:
    """Both halves of the decision rule, per lookup-used bound family."""
    claims = {}
    for fam in LOOKUP_USED_BOUND:
        jhalf = parts_summary["claims"].get(fam)
        if not isinstance(jhalf, dict):
            claims[fam] = jhalf
            continue
        sets = list(jhalf["statement_verdicts"])
        lens = {s: rw["cells"].get(f"{fam}/{s}/primary", {}).get("verdict") for s in sets}
        loc = any(jhalf["statement_verdicts"][s] == "inside" and lens[s] == "written" for s in sets)
        around = jhalf["jspace_half"] == "H-around" and all(lens[s] == "not written" for s in sets)
        claims[fam] = {"jspace": jhalf, "lens_write": lens,
                       "verdict": "H-loc supported" if loc else "H-around supported" if around else "neither (mixed)"}  # fmt: skip
    return claims


def write_readwrite_md(path: Path, run: str, s: dict) -> None:
    lines = [f"# {EXP} / {run}", "", f"Claims: {json.dumps(s.get('claims'))}", "",
             "| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | "
             "lens x16 | write verdict |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip

    def pct(x):
        return "-" if x is None else f"{100 * x:.0f}%"

    for key, c in s["cells"].items():
        w = c["write"]

        def f(k, w=w):
            return f"{100 * w[k]['frac']:.0f}% ({100 * w[k]['flips']:.0f}%)" if k in w else "-"

        lines.append(f"| {key} | {c['layers']} | {c['n']} | {pct(c['read_top10'])} / {pct(c['read_top1'])} | "
                     f"{pct(c['x_top10'])} | {f('copy')} | {f('lens_x1')} | {f('lens_x4')} | {f('random_x4')} | "
                     f"{f('lens_x16')} | {c['verdict']} |")  # fmt: skip
    lines += ["", "Write cells: mean frac of the way to C (flips)."]
    path.write_text("\n".join(lines) + "\n")


# ---- examples -----------------------------------------------------------------------------------------------------


def expected(case: dict, o: dict, kind: str) -> dict[str, str | None]:
    """What each hypothesis predicts this edit answers (None: no prediction), from the job specs' predictions."""
    clean, x = case["answer"], case["cf_answer"]
    fam, s, la = case["family"], o.get("set"), o.get("layer")
    statement = s in STATEMENT_SETS
    primary = isinstance(la, int) and PRIMARY_LO <= la < ONSET
    if o.get("check") == "identity" or o.get("noop_check") or o.get("source") in ("off", "rand"):
        return dict.fromkeys(H_NAMES, clean)
    if o.get("check") == "all0":
        return dict.fromkeys(H_NAMES, x)
    lookup_stmt = fam in LOOKUP_USED_BOUND and statement and primary
    if kind == "map":
        return {"H-loc": x if lookup_stmt else None, "H-around": None}
    part = o.get("part", "")
    if part in ("full", "copy") or o.get("null"):
        return dict.fromkeys(H_NAMES, x if part in ("full", "copy") else clean)
    if kind == "parts" and part in ("jspace", "not_jspace") and fam in LOOKUP_USED_BOUND:
        return {"H-loc": x if part == "jspace" else None, "H-around": clean if part == "jspace" else x}
    if kind == "readwrite" and part.startswith("lens_x") and fam in LOOKUP_USED_BOUND:
        return {"H-loc": x, "H-around": clean}
    if part.startswith("random_x"):
        return dict.fromkeys(H_NAMES, clean)
    return dict.fromkeys(H_NAMES, None)


def condition_text(case: dict, o: dict, kind: str) -> str:
    if o.get("check") == "identity":
        return f"the clean run's own block-{o['layer']} output copied at every position (identity)"
    if o.get("check") == "all0":
        return f"C's block-{o['layer']} output copied at every position (the hook's positive control)"
    where = f"at {o['set']} ({len(case['sets'][o['set']])} tokens), block output of layer {o['layer']}"
    if kind == "map":
        what = {"cf": "C's residual copied into the clean run", "off": "O's residual copied into the clean run",
                "rand": "C's copy with each row replaced by a random direction at its norm"}[o["source"]]  # fmt: skip
        return f"{what} {where}" + (" (zero delta: an exact no-op)" if o.get("noop_check") else "")
    part = o["part"]
    if kind == "parts":
        name = {"full": "C's full copy" if o["source"] == "cf" else "O's full copy", "jspace": "the J-space part of C's copy",
                "not_jspace": "C's copy minus its J-space part", "lens2": "C's copy projected on the bridge's and X's lens vectors",
                "not_lens2": "C's copy minus that projection", "rand_omp": "C's copy fitted on a random dictionary",
                "jspace_wo_own": "the J-space part after the own words are projected out"}.get(part, part)  # fmt: skip
        return f"{name}{' (random direction at its norms)' if o['null'] else ''} added {where}"
    if part == "copy":
        return f"C's copy added {where}"
    sc = part.split("_x")[1]
    return (f"the lens direction v_X - v_I at {sc}x the copy's per-position norm added {where}" if part.startswith("lens")
            else f"a random direction at {sc}x the copy's per-position norm added {where}")  # fmt: skip


def example_groups(kind: str) -> list[dict]:
    if kind == "map":
        return [
            {"key": "stmt_flip", "title": "Statement copy gives X's answer",
             "definition": "C's copy at a statement set, at a primary-window layer, makes the top token X's answer"},
            {"key": "stmt_hold", "title": "Statement copy leaves the answer",
             "definition": "C's copy at a statement set, at a primary-window layer, keeps the bridge's answer"},
            {"key": "question_flip", "title": "Question copy gives X's answer",
             "definition": "C's copy at question, q_words or final, at a primary-window layer, gives X's answer"},
            {"key": "control_changed", "title": "A control changed the answer",
             "definition": "O's copy or the random-direction copy moved the top token off the bridge's answer"},
            {"key": "noop", "title": "Exact no-op (cue-only family, statement set)",
             "definition": "RL, RR or countries R: C's copy at a statement set is exactly zero; read anyway"},
            {"key": "sanity", "title": "Hook checks", "definition": "identity copy (no change) and C at every position "
             "at the first layer (reproduces C)"},
        ]  # fmt: skip
    if kind == "parts":
        return [
            {"key": "jspace_flips", "title": "J-space part alone gives X's answer",
             "definition": "the J-space part of C's copy at a transit cell makes the top token X's answer"},
            {"key": "rest_flips_jspace_not", "title": "The rest gives X's answer, the J-space part does not",
             "definition": "same case and cell: not_jspace flips, jspace keeps the bridge's answer"},
            {"key": "full_flips_neither_part", "title": "Only the full copy flips",
             "definition": "the full copy flips, neither part alone does"},
        ]  # fmt: skip
    return [
        {"key": "lens_flips", "title": "Lens direction writes X",
         "definition": "v_X - v_I at <= 4x the copy's norm makes the top token X's answer"},
        {"key": "copy_flips_lens_not", "title": "The copy flips, the lens direction at 4x does not",
         "definition": "same case and cell: C's copy gives X's answer, the lens push at 4x does not"},
        {"key": "random_changed", "title": "Random direction changed the answer",
         "definition": "the random direction at the same norms moved the top token off the bridge's answer"},
    ]  # fmt: skip


def group_of(o: dict, kind: str, index: dict) -> list[str]:
    """The example groups an outcome row belongs to (`index`: (name, set, layer, part) -> row, for paired groups)."""
    la, s = o.get("layer"), o.get("set")
    primary = isinstance(la, int) and PRIMARY_LO <= la < ONSET
    if kind == "map":
        if "check" in o:
            return ["sanity"] if o["check"] != "unedited" else []
        if o.get("noop_check"):
            return ["noop"]
        if o["source"] in ("off", "rand"):
            return ["control_changed"] if o["role"] != "A" else []
        if primary and s in STATEMENT_SETS:
            return ["stmt_flip"] if o["role"] == "b" else ["stmt_hold"] if o["role"] == "A" else []
        if primary and s in QUESTION_SETS and o["role"] == "b":
            return ["question_flip"]
        return []
    if kind == "parts":
        if o["null"] or o["source"] != "cf":
            return []
        key = (o["name"], s, la)
        if o["part"] == "jspace" and o["role"] == "b":
            return ["jspace_flips"]
        rest, j = index.get((*key, "not_jspace")), index.get((*key, "jspace"))
        if o["part"] == "not_jspace" and o["role"] == "b" and j is not None and j["role"] == "A":
            return ["rest_flips_jspace_not"]
        if (
            o["part"] == "full"
            and o["role"] == "b"
            and rest is not None
            and j is not None
            and "b" not in (rest["role"], j["role"])
        ):
            return ["full_flips_neither_part"]
        return []
    if o["part"].startswith("lens_x") and float(o["part"][6:]) <= WRITE_MAX_SCALE and o["role"] == "b":
        return ["lens_flips"]
    if o["part"] == "copy" and o["role"] == "b":
        lens4 = index.get((o["name"], s, la, "lens_x4"))
        return ["copy_flips_lens_not"] if lens4 is not None and lens4["role"] != "b" else []
    if o["part"].startswith("random_x") and o["role"] != "A":
        return ["random_changed"]
    return []


def merged_spans(offsets: list, positions: list[int]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for i in positions:
        s, e = offsets[i]
        if spans and spans[-1][1] >= s:
            spans[-1] = (spans[-1][0], max(spans[-1][1], e))
        else:
            spans.append((s, e))
    return spans


def stage_examples(name: str, k: int, seed: int) -> None:
    out = run_dir(name)
    m = json.loads((out / "manifest.json").read_text())
    path = out / "examples.json"
    assert not path.exists(), f"{path} exists; examples are written once"
    kind = m["kind"]
    cases = {c["id"]: c for c in (json.loads(line) for line in (out / "cases.jsonl").read_text().splitlines())}
    rows = [json.loads(line) for line in (out / "outcomes.jsonl").read_text().splitlines()]
    index = {(o["name"], o.get("set"), o.get("layer"), o.get("part")): o for o in rows if "part" in o}
    groups = example_groups(kind)
    members: dict[str, list[dict]] = {g["key"]: [] for g in groups}
    for o in rows:
        for g in group_of(o, kind, index):
            members[g].append(o)
    rng = random.Random(seed)
    examples = []
    for g in groups:
        g["n_total"] = len(members[g["key"]])
        for o in rng.sample(members[g["key"]], min(k, len(members[g["key"]]))):
            c = cases[o["name"]]
            marks = {key: [tuple(x) for x in v] for key, v in c["marks"].items()}
            spans = [{"start": a, "end": b, "role": role} for role in ("bind_bridge", "bridge_word", "lookup_bridge",
                     "lookup_x", "question", "final") for a, b in marks.get(role, [])]  # fmt: skip
            patched = list(range(len(c["offsets"]))) if "check" in o else c["sets"][o["set"]]
            spans += [{"start": a, "end": b, "role": "patched"} for a, b in merged_spans(c["offsets"], patched)]
            spans += [
                {"start": a, "end": b, "role": "cf_changed"} for a, b in merged_spans(c["offsets"], c["changed"]["cf"])
            ]
            numbers = {x: o[x] for x in ("ld", "frac", "role") if x in o}
            numbers.update(ld_clean=c["ld_clean"], ld_C=c["ld_cf"], flip=o["role"] == "b")
            if "greedy" in o:
                numbers["greedy"] = o["greedy"]
            examples.append({
                "group": g["key"], "family": c["family"], "item_id": c["id"], "prompt": c["prompt"], "spans": spans,
                "condition": condition_text(c, o, kind),
                "answers": {"clean": c.get("top_clean_text", c["answer"]), "edited": o.get("top_text"),
                            "edited_role": o["role"], "bridge_answer": c["answer"], "x_answer": c["cf_answer"],
                            "expected": expected(c, o, kind)},
                "numbers": numbers,
                "why": f"{g['title']}: {o.get('set', 'all positions')}, layer {o.get('layer')}, read role {o['role']}",
            })  # fmt: skip
    blob = {"exp": EXP, "run": name, "kind": kind, "k": k, "seed": seed, "groups": groups, "examples": examples}
    path.write_text(json.dumps(blob, indent=1) + "\n")
    print("wrote", path, {g["key"]: g["n_total"] for g in groups})


# ---- analysis and figures (CPU, saved outputs only) ---------------------------------------------------------------

SEQ = ("#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b")  # one hue, light->dark
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1-3 (validated all-pairs, light)
CONTROL, CONTROL2 = "#898781", "#b5b4ad"  # controls in muted greys (figure_terms.md), told apart by marker too
FAMILY_DESC = {  # what the prompt does, in words (figures and reports never show the family codes)
    "BL": "pet stated, its locker looked up",
    "BR": "pet stated, its legs from memory",
    "RL": "animal recalled from a clue, its locker looked up",
    "RR": "animal recalled from a clue, its legs from memory",
    "BLR": "pet stated, its friend looked up, legs from memory",
    "BRL": "pet stated, legs from memory, locker looked up",
    "R": "a city's country recalled, its capital from memory",
    "B": "a person's country stated, its capital from memory",
}
SET_TITLE = {  # the position sets in the outside reader's terms (figure_terms.md)
    "bind_bridge": "sentence stating bridge org",
    "bridge_word": "the bridge org word",
    "bind_other": "other people's sentences",
    "lookup_bridge": "bridge org's table row",
    "lookup_x": "bridge alt's table row",
    "context": "the whole context",
    "question": "question and all after it",
    "q_words": "the question words",
    "final": "last tokens before the answer",
}
PATCH = "patch from the alt prompt"
FLIPS = "% of original answers that become the alternative answer (answer org → answer alt)"  # plotting.TERM["flips"]
JPART = "lens-readable part"
FLIPS_WRAPPED = "% of original answers that become\nthe alternative answer (answer org → answer alt)"


def example_short(c: dict) -> str:
    """The 'Example' caption row: a real item, shortened, with answer org and what the alt prompt changes."""
    text = c["prompt"].split("user\n", 1)[1].split("<|im_end|>")[0]
    question = text.split("\n")[-1].replace(" " + S.INSTRUCTION, "")
    fam = c["family"]
    if fam in SUITE and fam not in CUE_ONLY:
        stated = f"{c['cue']}'s pet is a {c['bridge']}."
        if fam in ("BL", "RL"):
            stated += f" ... The {c['bridge']}'s locker is {c['answer']}."
        alt = f"“{c['cue']}'s pet is a {c['cf_bridge']}.” (two pets swapped)"
    elif fam == "B":
        stated = f"{c['cue']} lives in {c['bridge']}."
        alt = f"“{c['cue']} lives in {c['cf_bridge']}.” (two countries swapped)"
    else:
        stated, alt = "", f"the clue in the question names bridge alt ({c['cf_bridge']})"
    org = f"“... {stated} ... {question}”" if stated else f"“... {question}”"
    return (f"{fam_label(fam)}: org prompt {org} → answer org {c['answer']} (bridge org {c['bridge']}); alt prompt: "
            f"{alt} → answer alt {c['cf_answer']}.")  # fmt: skip


def example_note(c: dict) -> str:
    """One real item in the outside reader's terms: the org prompt's user text, bridge org / alt, answer org / alt."""
    text = c["prompt"].split("user\n", 1)[1].split("<|im_end|>")[0].replace("\n", " ")
    fam = c["family"]
    if fam in CUE_ONLY:
        change = f"the clue in the question names bridge alt ({c['cf_bridge']}) instead"
    elif fam in SUITE:
        change = f"“{c['cue']}'s pet is a {c['cf_bridge']}.” (two pets swapped)"
    else:
        change = f"“{c['cue']} lives in {c['cf_bridge']}.” (two countries swapped)"
    return (f"Example ({fam_label(fam)}): org prompt “{text}” → answer org {c['answer']} (bridge org {c['bridge']}). "
            f"Alt prompt: the same but {change} → answer alt {c['cf_answer']} (bridge alt {c['cf_bridge']}).")  # fmt: skip


def fam_label(code: str) -> str:
    """The display name of a family: where the bridge comes from -> where the answer comes from."""
    from bridge_jspace.plotting import family_label

    return family_label(code)


def fam_title(code: str) -> str:
    return f"{fam_label(code)}  ({FAMILY_DESC[code]})"


def cell_label(fam: str, s: str) -> str:
    return f"{fam_label(fam)}: {SET_TITLE[s]}"


def plain(d: Any) -> Any:
    """A summary fragment keyed by family codes and set keys, with display names instead (for reports)."""
    if isinstance(d, dict):
        out = {}
        for k, v in d.items():
            key = k
            if isinstance(k, str):
                parts = k.split("/")
                parts = [fam_label(p) if p in FAMILIES else SET_TITLE.get(p, p) for p in parts]
                key = " / ".join(parts)
            out[key] = plain(v)
        return out
    if isinstance(d, list):
        return [plain(x) for x in d]
    return d


CELL_ORDER = ("BL", "BLR", "RL", "PP", "BR", "BRL", "RR", "PM", "B", "R")  # lookup-used first, then recall-used
HEAT_ORDER = ("BL", "BR", "BLR", "BRL", "RL", "RR", "B", "R")  # paired readers side by side


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def as_json(x: Any) -> Any:
    return json.loads(json.dumps(x))


def stage_analyze(name: str) -> dict:
    """Re-applies the run's pre-registered rule to its saved outputs (no model) and compares with its summary.json."""
    out = run_dir(name)
    m = json.loads((out / "manifest.json").read_text())
    saved = json.loads((out / "summary.json").read_text())
    outcomes = read_jsonl(out / "outcomes.jsonl")
    cases = read_jsonl(out / "cases.jsonl")
    extra: dict[str, Any] = {}
    if m["kind"] == "map":
        zeros = read_jsonl(out / "zero_cells.jsonl")
        s = summarize_map(outcomes, zeros, cases, tuple(m["layers"]))
        same = {k: as_json(s[k]) == saved[k] for k in ("transit", "handoff", "sanity", "validation")}
    elif m["kind"] == "parts":
        fve = read_jsonl(out / "fve.jsonl")
        s = summarize_parts(outcomes, fve, m["cells"])
        extra["fve"] = fve
        same = {"claims": as_json(s["claims"]) == saved["claims"],
                "verdicts": {k: v["verdict"] for k, v in s["cells"].items()} == {k: v["verdict"] for k, v in saved["cells"].items()},
                "concentrations": all(as_json(s["cells"][k]["frac"]["jspace"]["concentration"]) == v["frac"]["jspace"]["concentration"]
                                      for k, v in saved["cells"].items())}  # fmt: skip
    else:
        reads = read_jsonl(out / "reads.jsonl")
        s = summarize_readwrite(reads, outcomes, m["cells"])
        if "parts" in m:
            s["claims"] = d1_claims(json.loads((run_dir(m["parts"]["run"]) / "summary.json").read_text()), s)
        extra["reads"] = reads
        same = {"verdicts": {k: v["verdict"] for k, v in s["cells"].items()} == {k: v["verdict"] for k, v in saved["cells"].items()},
                "claims": as_json(s.get("claims")) == saved.get("claims")}  # fmt: skip
    print(name, "recomputed == saved:", json.dumps(same), flush=True)
    return {
        "manifest": m,
        "summary": s,
        "saved": saved,
        "same_as_saved": same,
        "outcomes": outcomes,
        "cases": cases,
        **extra,
    }


def new_figure_folder(name: str, out: str | None = None) -> Path:
    """results/statement_positions/<run>/analysis-<stamp>-figures/ (or under `out`, for a draft outside results/). One
    figures folder per run (the user's rule): this stage's earlier analysis-*-figures folders of the run are removed
    first; nothing the run itself wrote is touched."""
    import shutil

    base = Path(out) / name if out else run_dir(name)
    for old in sorted(base.glob("analysis-*-figures")) if base.exists() else []:
        assert old.is_dir(), old
        assert old.parent == base, old
        shutil.rmtree(old)
        print("removed", old)
    folder = base / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    folder.mkdir(parents=bool(out), exist_ok=False)
    return folder


def caption(
    fig,
    folder: Path,
    stem: str,
    made: list[str],
    title: str,
    rows: list[tuple[str, str]],
    data: str,
    handles: list | None = None,
    ncols: int | None = None,
    foot: float | None = None,
    after: Any = None,
) -> None:
    """The caption format of figure_terms.md (bridge_jspace.plotting.finish's labelled rows: What we did / Example /
    How to read / Control / Data, one short sentence each), then tight layout and PNG at 200 dpi + SVG (finish saves
    one 150-dpi PNG). `foot`: inches kept free under the panels (legend, colour bar)."""
    import textwrap

    from bridge_jspace.plotting import INK, MUTED

    h, w = fig.get_figheight(), fig.get_figwidth()
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=INK)
    label_w, y = 1.05, 0.38
    for label, text in [*rows, ("Data", data)]:
        lines = textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]
        fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=INK, fontweight="bold")
        fig.text(label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=MUTED,
                 linespacing=1.4)  # fmt: skip
        y += 0.155 * len(lines) + 0.05
    head = y + 0.1
    n_rows = -(-len(handles) // (ncols or len(handles))) if handles else 0
    if handles:
        fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=8.5,
                   labelcolor=INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    foot = foot if foot is not None else (0.2 + 0.25 * n_rows if handles else 0.1)
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    if after is not None:  # artists placed in the reserved foot after the layout (a colour bar)
        after(fig)
    save(fig, folder, stem, made)


def save(fig, folder: Path, stem: str, made: list[str]) -> None:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import SURFACE

    for ext in ("png", "svg"):
        fig.savefig(folder / f"{stem}.{ext}", dpi=200, facecolor=SURFACE)
    plt.close(fig)
    made.append(f"{stem}.png")


def model_note(m: dict) -> str:
    """The model, as figure notes name it (commit and run names stay in report.md and summary.json)."""
    return m["model"]["repo"].split("/")[-1]


SPLIT_PLAIN = {"inside": "carried by the lens-readable part", "around": "carried around it", "inconclusive": "unclear"}
WRITE_PLAIN = {"written": "changes the answer", "not written": "does not change it", "inconclusive": "unclear",
               "no data": "not tested"}  # fmt: skip


def map_cell(summary: dict, fam: str, s: str, la: int) -> dict | None:
    return next((r for r in summary["rates"] if r["family"] == fam and r["set"] == s and r["layer"] == la), None)


def map_cells(summary: dict, fam: str, s: str, layers: list[int]) -> list[dict]:
    cells = [map_cell(summary, fam, s, la) for la in layers]
    assert all(c is not None for c in cells), f"{fam}/{s}: a layer is missing from the map"
    return [c for c in cells if c is not None]


def draw_heat(ax, summary: dict, fam: str, layers: list[int], show_rows: bool) -> Any:
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.patches import Rectangle

    from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE

    grid = np.full((len(SETS), len(layers)), np.nan)
    for i, s in enumerate(SETS):
        for j, la in enumerate(layers):
            r = map_cell(summary, fam, s, la)
            if r is None:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=SURFACE, edgecolor="none"))
            elif r["cf"]["zero"] == r["n"]:  # C identical here: an exact no-op
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=SURFACE, edgecolor=GRID, hatch="////", lw=0))
            else:
                grid[i, j] = r["cf"]["flips"][0]
    im = ax.imshow(np.ma.masked_invalid(grid), cmap=LinearSegmentedColormap.from_list("seq", SEQ), vmin=0, vmax=1,
                   aspect="auto", interpolation="nearest")  # fmt: skip
    for i, s in enumerate(SETS):
        for j, la in enumerate(layers):
            r = map_cell(summary, fam, s, la)
            if r is not None and r["transit"]:
                ax.scatter(j, i, s=16, c=SURFACE, edgecolors=INK, linewidths=0.7, zorder=3)
    ax.set_xticks(range(len(layers)), [str(la) for la in layers], fontsize=7, color=MUTED)
    ax.set_yticks(range(len(SETS)), [SET_TITLE[s] for s in SETS], fontsize=7.5, color=MUTED)
    ax.tick_params(labelleft=show_rows)  # shared rows: labels on the first column only
    ax.set_xticks(np.arange(-0.5, len(layers)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(SETS)), minor=True)
    ax.grid(which="minor", color=SURFACE, lw=1.5)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title(f"{fam_label(fam)}\n({FAMILY_DESC[fam]})", fontsize=8.5, color=INK, loc="left")
    return im


def map_figures(a: dict, folder: Path, against: str | None) -> list[str]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE, percent_axis, style_axes

    m, s = a["manifest"], a["summary"]
    layers = list(m["layers"])
    fams = [f for f in HEAT_ORDER if f in m["families"]]
    n = m["n_per_family"]
    made: list[str] = []
    # 1. the heat map: every family, set and layer (paired readers side by side: BL|BR, BLR|BRL; then RL, RR, B, R)
    fig, axes = plt.subplots(2, 4, figsize=(17, 10.4), sharey=True)
    im = None
    for k, (ax, fam) in enumerate(zip(axes.flat, fams, strict=False)):
        im = draw_heat(ax, s, fam, layers, show_rows=k % 4 == 0)
        ax.set_xlabel("layer", fontsize=7.5, color=MUTED)
    from matplotlib.ticker import PercentFormatter

    assert im is not None

    def colour_bar(fig, im=im) -> None:
        cax = fig.add_axes((0.06, 0.62 / fig.get_figheight(), 0.25, 0.12 / fig.get_figheight()))
        cb = fig.colorbar(im, cax=cax, orientation="horizontal")
        cb.ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        cb.set_label(FLIPS, fontsize=8, color=MUTED)
        cb.ax.tick_params(labelsize=7, colors=MUTED)
        cb.outline.set_visible(False)

    handles = [Line2D([], [], marker="o", ls="", markerfacecolor=SURFACE, markeredgecolor=INK, label="transit cell"),
               Patch(facecolor=SURFACE, edgecolor=GRID, hatch="////", label="no-op by construction")]  # fmt: skip
    caption(fig, folder, "heatmap_copy_flips", made, "Where in the prompt, and up to which layer, is the bridge carried?",
            [("What we did", "Took the alt prompt's hidden states at one layer and pasted them into the org prompt at "
              "one group of positions only (one row), then read the answer."),
             ("Example", example_short(first_case(a, "BL"))),
             ("How to read", f"Each cell: {FLIPS}. Dark = that place still carries the bridge at that layer; dot = "
              "transit cell (at least 50% and above both controls)."),
             ("Control", "The off-path control's paste and a random push of the same size at every cell (both stay "
              "near 0%). Hatched: the alt prompt is identical there (only its question differs), so nothing changes.")],
            f"{model_note(m)}; {n} items per family; seed 0.", handles=handles, foot=1.25, after=colour_bar)  # fmt: skip
    # 2. three sets per family with their Wilson intervals and the largest control change
    fig, axes = plt.subplots(2, 4, figsize=(17, 9.8), sharey=True, sharex=True)
    lines = (("bind_bridge", BLUE, "o"), ("context", ORANGE, "s"), ("question", AQUA, "D"))
    for ax, fam in zip(axes.flat, fams, strict=False):
        style_axes(ax)
        ctrl = []
        for st, color, marker in lines:
            rows = [map_cell(s, fam, st, la) for la in layers]
            if all(r is None or r["cf"]["zero"] == r["n"] for r in rows):
                continue
            y = np.array([r["cf"]["flips"][0] if r else np.nan for r in rows])
            lo = np.array([r["cf"]["flips"][1] if r else np.nan for r in rows])
            hi = np.array([r["cf"]["flips"][2] if r else np.nan for r in rows])
            ax.fill_between(layers, lo, hi, color=color, alpha=0.12, lw=0)
            ax.plot(layers, y, color=color, lw=2, marker=marker, ms=4, label=SET_TITLE[st])
            ctrl.append([max([r[c]["changed"][0] for c in ("off", "rand") if r[c]["zero"] < r["n"]] or [0.0]) if r else 0.0
                         for r in rows])  # fmt: skip
        if ctrl:
            ax.plot(layers, np.max(ctrl, axis=0), color=MUTED, lw=1.2, ls="-", marker="",
                    label="control: largest change (off-path control or random push)")  # fmt: skip
        else:
            ax.text(0.5, 0.5, "pastes at the statements change nothing\n(the alt prompt differs only in the question)",
                    transform=ax.transAxes, ha="center", color=MUTED)  # fmt: skip
        ax.set_title(f"{fam_label(fam)}\n({FAMILY_DESC[fam]})", fontsize=8.5, color=INK, loc="left")
        ax.set_ylim(-0.03, 1.03)
        percent_axis(ax)
    for ax in axes[1]:
        ax.set_xlabel("layer", fontsize=8, color=MUTED)
    for ax in axes[:, 0]:
        ax.set_ylabel(FLIPS_WRAPPED, fontsize=7.5, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, lw=2, label=SET_TITLE[st]) for st, c, mk in lines]
    handles.append(
        Line2D([], [], color=MUTED, lw=1.2, label="control: largest change (off-path control or random push)")
    )
    caption(fig, folder, "copy_flips_by_layer", made,
            "Up to which layer does the sentence stating bridge org decide the answer, and when does the question take over?",
            [("What we did", f"Pasted the alt prompt's hidden states into the org prompt ({PATCH}) at one place, one "
              "layer at a time."),
             ("Example", example_short(first_case(a, "BL"))),
             ("How to read", f"Each line: {FLIPS}, by the layer of the paste. A line that drops to 0 means that place "
              "no longer carries the bridge by that layer."),
             ("Control", "Grey: the larger change of the off-path control's paste and a random push of the same size "
              "(should stay near 0%).")],
            f"{model_note(m)}; {n} items per family; bands: Wilson 95%.", handles=handles, ncols=4)  # fmt: skip
    if against:
        made += confirm_figure(a, against, folder)
    return made


def first_case(a: dict, fam: str) -> dict:
    """The run's first case of a family (for the example line), else its first case."""
    return next((c for c in a["cases"] if c["family"] == fam), a["cases"][0])


def transit_agreement(s_new: dict, s_old: dict) -> dict:
    """Cell by cell, on the layers both maps ran: is the transit verdict the same?"""
    old = {(r["family"], r["set"], r["layer"]): r for r in s_old["rates"]}
    out: dict[str, list] = {"both": [], "only_old": [], "only_new": [], "neither": []}
    for r in s_new["rates"]:
        q = old.get((r["family"], r["set"], r["layer"]))
        if q is None or r["cf"]["zero"] == r["n"]:
            continue
        key = (
            "both"
            if r["transit"] and q["transit"]
            else "only_old"
            if q["transit"]
            else "only_new"
            if r["transit"]
            else "neither"
        )
        out[key].append((r["family"], r["set"], r["layer"], q["cf"]["flips"], r["cf"]["flips"]))
    return out


def confirm_figure(a: dict, against: str, folder: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import GRID, MUTED, percent_axis, style_axes

    old = json.loads((run_dir(against) / "summary.json").read_text())
    om = json.loads((run_dir(against) / "manifest.json").read_text())
    agree = transit_agreement(a["summary"], old)
    a["agreement"] = {k: len(v) for k, v in agree.items()}
    a["disagreements"] = {k: [f"{cell_label(f, s)}, layer {la}: {100 * o[0]:.0f}% -> {100 * nw[0]:.0f}%"
                              for f, s, la, o, nw in v] for k, v in agree.items() if k.startswith("only")}  # fmt: skip
    fig, ax = plt.subplots(figsize=(8.5, 9.2))
    style_axes(ax)
    ax.plot([0, 1], [0, 1], color=GRID, lw=1)
    ax.axhline(TRANSIT_FLIPS, color=GRID, lw=1)
    ax.axvline(TRANSIT_FLIPS, color=GRID, lw=1)
    styles = {"neither": (MUTED, "o", 12, "transit in neither"), "both": (BLUE, "o", 30, "transit in both"),
              "only_old": (ORANGE, "s", 40, f"transit only at n={om['n_per_family']}"),
              "only_new": (AQUA, "D", 40, f"transit only at n={a['manifest']['n_per_family']}")}  # fmt: skip
    for key, (color, marker, size, label) in styles.items():
        pts = agree[key]
        if not pts:
            continue
        x = [o[0] for *_, o, _ in pts]
        y = [nw[0] for *_, nw in pts]
        ax.errorbar(x, y, xerr=[[o[0] - o[1] for *_, o, _ in pts], [o[2] - o[0] for *_, o, _ in pts]],
                    yerr=[[nw[0] - nw[1] for *_, nw in pts], [nw[2] - nw[0] for *_, nw in pts]], fmt="none",
                    ecolor=color, alpha=0.25, lw=0.8)  # fmt: skip
        ax.scatter(
            x, y, s=size, c=color, marker=marker, edgecolors="white", linewidths=1, label=f"{label} ({len(pts)})"
        )
    listed = [f"{'n=32 only' if key == 'only_old' else 'n=80 only'}: {cell_label(f, st)}, layer {la} "
              f"({100 * o[0]:.0f}% -> {100 * nw[0]:.0f}%)" for key in ("only_old", "only_new") for f, st, la, o, nw in agree[key]]  # fmt: skip
    if listed:
        ax.text(0.02, 0.98, "Cells that changed verdict:\n" + "\n".join(listed), transform=ax.transAxes, va="top",
                fontsize=7, color=MUTED, linespacing=1.4)  # fmt: skip
    percent_axis(ax, "x")
    percent_axis(ax)
    ax.set_xlabel(f"{FLIPS_WRAPPED}\nfirst map ({om['n_per_family']} items per family)", fontsize=8, color=MUTED)
    ax.set_ylabel(f"{FLIPS_WRAPPED}\nconfirmatory map ({a['manifest']['n_per_family']} items per family)", fontsize=8,
                  color=MUTED)  # fmt: skip
    handles, _ = ax.get_legend_handles_labels()
    common = sorted(set(a["manifest"]["layers"]) & set(om["layers"]))
    made: list[str] = []
    caption(fig, folder, "map_confirmation", made, "Does a larger map find the same transit cells?",
            [("What we did", f"Ran the same paste map again with {a['manifest']['n_per_family']} items per family "
              f"(the first {om['n_per_family']} are the first map's) at layers {common[0]}-{common[-1]}."),
             ("How to read", "Each point: one family x place x layer; on the diagonal = both maps agree. Grey lines at "
              "50% = the transit threshold."),
             ("Control", "Cells that changed verdict are listed; a real disagreement would sit far from 50%.")],
            f"{model_note(a['manifest'])}; bars: Wilson 95%.", handles=handles, ncols=2)  # fmt: skip
    return made


def part_concentration(outcomes: list[dict], fve: list[dict], fam: str, s: str, win: list[int], part: str,
                       share_of: str = "jspace") -> tuple[float, ...]:  # fmt: skip
    """suite_split's concentration of one part (its effect / (its variance share x the full copy's effect))."""
    rows = [o for o in outcomes if o["family"] == fam and o.get("set") == s and o["layer"] in win]
    mine = [f for f in fve if f.get("family") == fam and f.get("set") == s and f["layer"] in win]
    per: dict[str, list[float]] = collections.defaultdict(list)
    for f in mine:
        if f["what"] == share_of:
            per[f["name"]].append(f["share"])
    full = P.scores(rows, "frac", part="full", null=False, source="cf")
    eff = P.scores(rows, "frac", part=part, null=False, source="cf")
    return P.concentration(eff, full, {k: statistics.mean(v) for k, v in per.items()})


def concentration_rows(a: dict) -> list[dict]:
    s, outcomes, fve = a["summary"], a["outcomes"], a["fve"]
    rows = []
    for key, c in s["cells"].items():
        fam, st, wname = key.split("/")
        if wname != "primary":
            continue
        rows.append({"family": fam, "set": st, "layers": c["layers"], "n": c["n"], "verdict": c["verdict"],
                     "jspace": c["frac"]["jspace"]["concentration"], "null": c["calibration"]["rand_omp"]["concentration"],
                     "matched": part_concentration(outcomes, fve, fam, st, c["layers"], "jspace_matched"),
                     "full_flips": c["flip"]["means"]["full"], "jspace_flips": c["flip"]["means"]["jspace"],
                     "full_frac": c["frac"]["means"]["full"], "jspace_frac": c["frac"]["means"]["jspace"],
                     "share": c["share_median"]["jspace"]})  # fmt: skip
    rows.sort(key=lambda r: (CELL_ORDER.index(r["family"]), SETS.index(r["set"])))
    return rows


def draw_concentration(ax, rows: list[dict], labels: bool = True, verdicts: bool = True) -> None:
    from bridge_jspace.plotting import GRID, MUTED, style_axes

    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.axvline(1.0, color=GRID, lw=1.2)
    ax.axvline(INSIDE, color=MUTED, lw=0.8, ls=(0, (2, 2)))
    for i, r in enumerate(rows):
        for key, color, marker, dy in (
            ("jspace", BLUE, "o", 0.0),
            ("matched", CONTROL2, "D", 0.22),
            ("null", CONTROL, "s", -0.22),
        ):
            c = r[key]
            ax.plot([c[1], c[2]], [i + dy, i + dy], color=color, lw=2, solid_capstyle="round")
            ax.scatter([c[0]], [i + dy], s=36, c=color, marker=marker, edgecolors="white", linewidths=1, zorder=3)
        if verdicts:
            ax.annotate(SPLIT_PLAIN[r["verdict"]], (1.0, i), xycoords=("axes fraction", "data"), xytext=(4, 0),
                        textcoords="offset points", va="center", fontsize=7.5, color=MUTED)  # fmt: skip
    ax.set_yticks(range(len(rows)), [f"{cell_label(r['family'], r['set'])}, layers {','.join(map(str, r['layers']))}"
                                     for r in rows] if labels else [])  # fmt: skip
    ax.invert_yaxis()
    ax.set_xlabel("concentration: effect of the part ÷ its share of the patch\n(relative to the whole patch's effect); "
                  "1 = its fair share", fontsize=8, color=MUTED)  # fmt: skip


def parts_figures(a: dict, folder: Path) -> list[str]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, MUTED, percent_axis, style_axes
    from bridge_jspace.stats import bootstrap_mean

    m = a["manifest"]
    rows = concentration_rows(a)
    a["concentration_rows"] = rows
    made: list[str] = []
    fig, ax = plt.subplots(figsize=(12, 0.45 * len(rows) + 4.2))
    draw_concentration(ax, rows)
    handles = [Line2D([], [], color=c, marker=mk, lw=2, label=lab) for c, mk, lab in
               ((BLUE, "o", JPART), (CONTROL2, "D", "control: matched piece"),
                (CONTROL, "s", "control: random-dictionary fit (null)"))]  # fmt: skip
    caption(fig, folder, "jspace_concentration", made,
            "Where the bridge is in transit, does the lens-readable part of the patch carry its fair share?",
            [("What we did", f"Split the {PATCH} into the part the J++ lens can read (its {JPART}: a 25-word fit) and "
              "the rest, and pasted the lens-readable part alone at the same place and layer."),
             ("Example", example_short(first_case(a, "BL"))),
             ("How to read", "Concentration = effect of the part ÷ its share of the patch; 1 = its fair share; right of "
              "the dashed line (1.2) = the bridge rides on the lens-readable part. Right: the pre-registered verdict."),
             ("Control", "A matched piece of the same size and angle, and the same fit over a random dictionary; both "
              "should stay near or below 1.")],
            f"{model_note(m)}; {m['n_per_family']} items per family; the transit cells at layers 32-40; bars: case "
            "bootstrap 95%.", handles=handles, ncols=3)  # fmt: skip
    # paired readers: the identical context patch, a lookup question vs a recall question
    pairs = [
        (x, y)
        for x, y in PAIRS
        if f"{x}/context/primary" in a["summary"]["cells"] and f"{y}/context/primary" in a["summary"]["cells"]
    ]
    if pairs:
        fig, axes = plt.subplots(1, len(pairs), figsize=(7.5 * len(pairs), 6.6), sharey=True, squeeze=False)
        parts = (("full", False, "whole patch"), ("jspace", False, JPART), ("not_jspace", False, "the rest"),
                 ("jspace_matched", False, "control:\nmatched piece"), ("jspace", True, "control: random\npush, same size"))  # fmt: skip
        stats_out = {}
        for ax, (lk, rc) in zip(axes[0], pairs, strict=True):
            style_axes(ax)
            common = [la for la in a["summary"]["cells"][f"{lk}/context/primary"]["layers"]
                      if la in a["summary"]["cells"][f"{rc}/context/primary"]["layers"]]  # fmt: skip
            for fam, color, marker, dx in ((lk, BLUE, "o", -0.12), (rc, ORANGE, "s", 0.12)):
                rows_f = [
                    o
                    for o in a["outcomes"]
                    if o["family"] == fam and o.get("set") == "context" and o["layer"] in common
                ]
                for j, (p, null, _) in enumerate(parts):
                    vals = list(P.scores(rows_f, "frac", part=p, null=null, source="cf").values())
                    mean, lo, hi = bootstrap_mean(vals, N_BOOT, BOOT_SEED)
                    stats_out[f"{fam}/{p}{'/null' if null else ''}"] = (mean, lo, hi, len(vals))
                    ax.plot([j + dx, j + dx], [lo, hi], color=color, lw=2)
                    ax.scatter([j + dx], [mean], c=color, marker=marker, s=40, edgecolors="white", linewidths=1, zorder=3,
                               label=fam_title(fam) if j == 0 else None)  # fmt: skip
            ax.set_xticks(range(len(parts)), [lab for *_, lab in parts], fontsize=8, color=MUTED)
            ax.set_title(f"{fam_label(lk)} vs {fam_label(rc)}\nthe whole context, layers {','.join(map(str, common))}",
                         fontsize=9, color=INK, loc="left")  # fmt: skip
            percent_axis(ax)
            ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16))
        axes[0][0].set_ylabel("way moved from answer org to answer alt\n(logit margin, 100% = all the way)", fontsize=8,
                              color=MUTED)  # fmt: skip
        a["paired_means"] = stats_out
        c0 = first_case(a, "BL")
        caption(fig, folder, "paired_readers", made,
                "Same paste, two questions: does a lookup in the prompt use the lens-readable part of the stated bridge?",
                [("What we did", "Pasted the alt prompt's states over the whole context into two prompts that differ only "
                  "in the question, then pasted only the lens-readable part, or only the rest."),
                 ("Example", f"“... {c0['cue']}'s pet is a {c0['bridge']}. ... Which locker belongs to {c0['cue']}'s "
                  f"pet?” ({fam_label('BL')}) vs “... How many legs does {c0['cue']}'s pet have?” ({fam_label('BR')}); "
                  f"alt prompt: “{c0['cue']}'s pet is a {c0['cf_bridge']}.” in both."),
                 ("How to read", "Each point: how far the answer moves from answer org to answer alt. Same paste, very "
                  "different use of its lens-readable part = the question decides what is read."),
                 ("Control", "A matched piece of the lens-readable part's size and a random push of that size; both "
                  "should stay near 0.")],
                f"{model_note(m)}; {m['n_per_family']} items per family, the same scenes in both; bars: bootstrap 95% "
                "over items. The pasted states are identical for the two-step pair; in the three-step pair the tables "
                "differ, so only the sentences stating the pets are shared.", foot=0.15)  # fmt: skip
    return made


def write_rows(a: dict) -> list[dict]:
    out = []
    for key, c in a["summary"]["cells"].items():
        fam, st, wname = key.split("/")
        if wname != "primary":
            continue
        rows = [o for o in a["outcomes"] if o["family"] == fam and o["set"] == st and o["layer"] in c["layers"]]
        per = {}
        for pname in ("copy", *(f"{w}_x{sc:g}" for w in ("lens", "random") for sc in SCALES)):
            sel = [o for o in rows if o["part"] == pname]
            per[pname] = wilson(sum(o["role"] == "b" for o in sel), len(sel))
        out.append({"family": fam, "set": st, "layers": c["layers"], "n": c["n"], "verdict": c["verdict"], "flips": per,
                    "read_top10": c["read_top10"], "x_top10": c["x_top10"]})  # fmt: skip
    out.sort(key=lambda r: (CELL_ORDER.index(r["family"]), SETS.index(r["set"])))
    return out


def readwrite_figures(a: dict, folder: Path) -> list[str]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, percent_axis, style_axes

    m = a["manifest"]
    rows = write_rows(a)
    a["write_rows"] = rows
    made: list[str] = []
    ncol = 4
    nrow = (len(rows) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(16, 3.4 * nrow + 3.2), sharey=True, squeeze=False)
    xs = np.log2(SCALES)
    for ax, r in zip(axes.flat, rows, strict=False):
        style_axes(ax)
        for w, color, marker, lab in (
            ("lens", BLUE, "o", "lens push (bridge alt − bridge org)"),
            ("random", CONTROL, "s", "control: random push (same size)"),
        ):
            c = [r["flips"][f"{w}_x{sc:g}"] for sc in SCALES]
            ax.fill_between(xs, [x[1] for x in c], [x[2] for x in c], color=color, alpha=0.12, lw=0)
            ax.plot(xs, [x[0] for x in c], color=color, lw=2, marker=marker, ms=4, label=lab)
        ax.axhline(r["flips"]["copy"][0], color=ORANGE, lw=1.2, ls=(0, (3, 2)), label=f"reference: the {PATCH}")
        ax.set_xticks(xs, [f"{sc:g}x" for sc in SCALES], fontsize=7.5)
        ax.set_ylim(-0.03, 1.03)
        percent_axis(ax)
        ax.set_title(f"{cell_label(r['family'], r['set'])}\nlayers {','.join(map(str, r['layers']))}: the lens push "
                     f"{WRITE_PLAIN[r['verdict']]}",
                     fontsize=8.5, color=INK, loc="left")  # fmt: skip
    for ax in axes.flat[len(rows) :]:
        ax.set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel(FLIPS_WRAPPED, fontsize=7.5, color=MUTED)
    for ax in axes[-1]:
        ax.set_xlabel("push size (times the paste's size at each position)", fontsize=8, color=MUTED)
    handles, _ = axes.flat[0].get_legend_handles_labels()
    caption(fig, folder, "lens_write", made,
            "Can a lens push (bridge alt − bridge org) change the answer where the bridge is in transit?",
            [("What we did", "Added the J++ lens's direction bridge alt − bridge org at the positions and layers where "
              "the bridge is in transit, at 0.5 to 16 times the size of the paste from the alt prompt there."),
             ("Example", example_short(first_case(a, "BL"))),
             ("How to read", f"Blue: {FLIPS} after the lens push; orange dashed: what the full paste does. Panel "
              "titles end with the pre-registered verdict."),
             ("Control", "Grey: a random push of the same size (should stay near 0% unless the push is so big it "
              "breaks the answer).")],
            f"{model_note(m)}; {m['n_per_family']} items per family; the transit cells at layers 32-40; bands: Wilson "
            "95%.", handles=handles, ncols=3)  # fmt: skip
    if "parts" in m and "BL" in m["families"]:  # the headline is the animal suite's (BL / BR, its layers)
        made += headline_figure(a, folder)
    return made


def headline_figure(a: dict, folder: Path) -> list[str]:
    """The thread's headline: where BL's bridge travels (map), and at those cells the J-space split and the lens write."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, MUTED, percent_axis, shade_band, style_axes

    m = a["manifest"]
    mp = stage_analyze(m["map"]["run"])
    pa = stage_analyze(m["parts"]["run"])
    crows = concentration_rows(pa)
    wrows = {(r["family"], r["set"]): r for r in a["write_rows"]}
    layers = list(mp["manifest"]["layers"])
    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(18, 9.0), gridspec_kw={"width_ratios": [1.0, 0.75, 0.6]})
    style_axes(ax0)
    shade_band(ax0, 32, 40, label=False)
    for st, color, marker in (("bind_bridge", BLUE, "o"), ("context", ORANGE, "s"), ("question", AQUA, "D")):
        rows = map_cells(mp["summary"], "BL", st, layers)
        ax0.fill_between(layers, [r["cf"]["flips"][1] for r in rows], [r["cf"]["flips"][2] for r in rows], color=color,
                         alpha=0.12, lw=0)  # fmt: skip
        ax0.plot(
            layers, [r["cf"]["flips"][0] for r in rows], color=color, lw=2, marker=marker, ms=4, label=SET_TITLE[st]
        )
    br = map_cells(mp["summary"], "BR", "bind_bridge", layers)
    ax0.plot(layers, [r["cf"]["flips"][0] for r in br], color=BLUE, lw=1.2, ls=(0, (3, 2)),
             label=f"for comparison, {fam_label('BR')}: sentence stating bridge org")  # fmt: skip
    ax0.set_ylim(-0.03, 1.03)
    percent_axis(ax0)
    ax0.set_xlabel("layer", fontsize=8, color=MUTED)
    ax0.set_ylabel(FLIPS_WRAPPED, fontsize=7.5, color=MUTED)
    ax0.set_title(f"A. Paste from the alt prompt at one place ({fam_label('BL')})", fontsize=9.5, color=INK,
                  loc="left")  # fmt: skip
    ax0.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0, -0.1), ncol=2)
    keep = [r for r in crows if r["set"] in ("context", "question")]
    draw_concentration(ax1, keep, verdicts=False)
    ax1.set_title("B. Is the bridge carried by\nthe lens-readable part there?", fontsize=9.5, color=INK, loc="left")
    ax1.set_xlabel("concentration\n(1 = its fair share)", fontsize=8, color=MUTED)
    style_axes(ax2)
    ax2.grid(axis="y", visible=False)
    for i, r in enumerate(keep):
        w = wrows.get((r["family"], r["set"]))
        if w is None:
            continue
        for key, color, marker, dy in (("copy", ORANGE, "D", -0.27), ("lens_x1", BLUE, "o", -0.09), ("lens_x4", BLUE, "^", 0.09),
                                       ("random_x4", CONTROL, "s", 0.27)):  # fmt: skip
            c = w["flips"][key]
            ax2.plot([c[1], c[2]], [i + dy, i + dy], color=color, lw=2)
            ax2.scatter([c[0]], [i + dy], c=color, marker=marker, s=34, edgecolors="white", linewidths=1, zorder=3)
        ax2.annotate(f"bridge {SPLIT_PLAIN[r['verdict']]};\nlens push {WRITE_PLAIN[w['verdict']]}", (1.0, i),
                     xycoords=("axes fraction", "data"),
                     xytext=(5, 0), textcoords="offset points", va="center", fontsize=7, color=MUTED)  # fmt: skip
    ax2.set_yticks(range(len(keep)), [])
    ax2.set_ylim(len(keep) - 0.5, -0.5)
    ax2.set_xlim(-0.03, 1.03)
    percent_axis(ax2, "x")
    ax2.set_xlabel(FLIPS_WRAPPED, fontsize=7.5, color=MUTED)
    ax2.set_title("C. Can a lens push\n(bridge alt − bridge org) do it?", fontsize=9.5, color=INK, loc="left")
    handles = [Line2D([], [], color=c, marker=mk, lw=2, label=lab) for c, mk, lab in
               ((BLUE, "o", f"B: {JPART} / C: lens push at the paste's size"), (BLUE, "^", "C: lens push, 4x"),
                (ORANGE, "D", "C: the full paste from the alt prompt"), (CONTROL2, "D", "B, control: matched piece"),
                (CONTROL, "s", "B, control: random-dictionary fit (null) / C, control: random push, 4x"))]  # fmt: skip
    made: list[str] = []
    caption(fig, folder, "headline_d1", made,
            "Is 'prompt lookups go around the lens' an artefact of measuring only at the question?",
            [("What we did", "Pasted the alt prompt's hidden states into the org prompt at one place (A); where that "
              "flips the answer, pasted only the part the lens can read (B), or pushed along the lens's direction (C)."),
             ("Example", example_short(first_case(mp, "BL"))),
             ("How to read", f"A: {FLIPS} by layer; the sentence stating bridge org stops mattering by layer 28, the "
              "whole context carries the bridge to layer 44, the question only from 52. B: 1 = the lens-readable part "
              "does its fair share; right of the dashed line (1.2) = the bridge rides on it. C: flips; right: verdicts."),
             ("Control", "B: a matched piece and a random-dictionary fit (grey). C: a random push of the same size "
              "(grey). Both should stay low.")],
            f"{model_note(m)}; map: {mp['manifest']['n_per_family']} items per family, layers 0-60; B and C: the transit "
            f"cells at layers 32-40 (grey band in A), {m['n_per_family']} items per family; Wilson / bootstrap 95%.",
            handles=handles, ncols=3, after=lambda fig: close_gap(ax1, ax2, 0.05))  # fmt: skip
    return made


def close_gap(left, right, gap: float = 0.015) -> None:
    """Pull `right` next to `left` (tight_layout spaces every column for the widest tick labels: B's row names)."""
    lp, rp = left.get_position(), right.get_position()
    right.set_position((lp.x1 + gap, rp.y0, rp.width * 1.15, rp.height))


def stage_figures(name: str, against: str | None, out: str | None = None) -> None:
    a = stage_analyze(name)
    folder = new_figure_folder(name, out)
    kind = a["manifest"]["kind"]
    if kind == "map":
        made = map_figures(a, folder, against)
    elif kind == "parts":
        made = parts_figures(a, folder)
    else:
        made = readwrite_figures(a, folder)
    blob = {"exp": EXP, "run": name, "kind": kind, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "recomputed_equals_saved": a["same_as_saved"], "figures": made}  # fmt: skip
    for key in ("agreement", "disagreements", "concentration_rows", "paired_means", "write_rows"):
        if key in a:
            blob[key] = as_json(a[key])
    s = a["summary"]
    if kind == "map":
        blob.update(transit=s["transit"], handoff=s["handoff"], sanity=s["sanity"], validation=s["validation"])
    else:
        blob["claims"] = s.get("claims")
    (folder / "summary.json").write_text(json.dumps(blob, indent=2) + "\n")
    (folder / "report.md").write_text(run_report(a, blob, folder))
    print("wrote", folder, made)


def gates(s: dict, kind: str) -> list[str]:
    if kind != "map":
        return ["no gate of its own (reads without greedy validation); the map run's gates apply"]
    san, v = s["sanity"], s["validation"]
    return [
        f"identity (the org prompt's own states patched back in) keeps the org prompt's top token: "
        f"{san['identity']['top_is_clean_top']:.0%} of {san['identity']['n']}; logit-margin difference from an unedited "
        f"read in the same batch: max {san['identity']['max_abs_ld_minus_unedited_same_batch']}",
        f"the alt prompt's states patched at every position at the first map layer give the alt prompt's top token: "
        f"{san['all0']['top_is_C_top']:.0%} of {san['all0']['n']} (logit-margin difference max "
        f"{san['all0']['max_abs_ld_minus_C']}, bf16 batch rounding)",
        f"memory-bridge families (alt prompt differs only in the question): patches at the statements are exactly zero "
        f"(causality violations: {s.get('n_causality_violations', 0)}); {san['noop_statements']['n']} of them read anyway: "
        f"difference from the identity max {san['noop_statements']['max_abs_ld_minus_identity']}",
        f"read vs greedy agreement: {v['agree']:.2%} of {v['n']} edited runs (rule: >= 99%)",
    ]  # fmt: skip


CLAIM_TESTED = {
    "map": "Where in the prompt (which positions) and up to which layer does a patch from the alt prompt change the "
    "answer to answer alt?",
    "parts": "Where the bridge is in transit, is the patch's effect carried by its lens-readable part?",
    "readwrite": "Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt "
    "− bridge org) change the answer?",
}


def claims_text(claims: dict | None) -> list[str]:
    """The decision rule's per-family outcome in the outside reader's terms."""
    out = []
    for fam, c in (claims or {}).items():
        if not isinstance(c, dict):
            out.append(f"- {fam_label(fam)}: {c}")
            continue
        half = c.get("jspace", c)
        sets = half["statement_verdicts"]
        parts = [f"at {SET_TITLE[s]}: bridge {SPLIT_PLAIN[v]} (rule: {v}); positive control "
                 f"({fam_label('B')}) there: {SPLIT_PLAIN.get(half['positive_control'].get(s) or '', 'not in transit')}"
                 for s, v in sets.items()]  # fmt: skip
        if "lens_write" in c:
            parts += [f"lens push at {SET_TITLE[s]}: {WRITE_PLAIN[v]} (rule: {v})" for s, v in c["lens_write"].items()]
            parts.append(f"combined verdict: {c['verdict']}")
        else:
            parts.append(f"split half of the rule: {half['jspace_half']}")
        out.append(f"- {fam_label(fam)}: " + "; ".join(parts))
    return out


def run_report(a: dict, blob: dict, folder: Path) -> str:
    """The AGENTS.md report block for one run, from the recomputed summary (numbers only from saved files)."""
    m, s, kind = a["manifest"], a["summary"], a["manifest"]["kind"]
    rel = folder.relative_to(pins.REPO_ROOT) if folder.is_relative_to(pins.REPO_ROOT) else folder
    lines = [f"# {EXP} / {m['run']}: analysis", "",
             f"EXP {EXP}/{m['run']} @ {m['code']['sha'][:7]}{' (dirty tree)' if m['code']['dirty'] else ''} | model "
             f"{m['model']['repo']} | n={m['n_per_family']} per family ({'; '.join(map(fam_label, m['families']))}) | seeds=[0]",
             f"Claim tested: {CLAIM_TESTED[kind]}", ""]  # fmt: skip
    if kind == "map":
        bl = {la: map_cell(s, "BL", "context", la) for la in m["layers"]}
        q = {la: map_cell(s, "BL", "question", la) for la in m["layers"]}
        mid = [la for la in m["layers"] if PRIMARY_LO <= la < ONSET]
        if mid:
            la = mid[len(mid) // 2]
            c, qq = bl[la], q[la]
            if c is not None and qq is not None:
                f, g = c["cf"]["flips"], qq["cf"]["flips"]
                r = c["rand"]["changed"]
                lines.append(f"Headline ({fam_label('BL')}): {FLIPS} after a {PATCH} at the whole context, layer {la} "
                             f"= {f[0]:.0%} [{f[1]:.0%}, {f[2]:.0%}]   Baseline (the same patch at the question and all "
                             f"after it): {g[0]:.0%} [{g[1]:.0%}, {g[2]:.0%}]   Control (random push, same size): "
                             f"{r[0]:.0%} [{max(0.0, r[1]):.0%}, {r[2]:.0%}]")  # fmt: skip
        lines += ["", f"Transit cells (rule: {FLIPS} >= {TRANSIT_FLIPS:.0%}, Wilson lower bound above every control): "
                  f"{json.dumps(plain(s['transit']), ensure_ascii=False)}",
                  f"Handoff: {json.dumps(plain(s['handoff']), ensure_ascii=False)}"]  # fmt: skip
        if "agreement" in a:
            lines += ["", f"Against the first map: {json.dumps(a['agreement'])}; disagreements: "
                      f"{json.dumps(a['disagreements'], ensure_ascii=False)}"]  # fmt: skip
    elif kind == "parts":
        for r in a.get("concentration_rows", []):
            if r["family"] in LOOKUP_USED_BOUND or r["family"] in POSITIVE:
                lines.append(f"- {cell_label(r['family'], r['set'])} (layers {r['layers']}): concentration of the "
                             f"{JPART} {r['jspace'][0]:.2f} [{r['jspace'][1]:.2f}, {r['jspace'][2]:.2f}]; random-dictionary "
                             f"fit (null) {r['null'][0]:.2f} [{r['null'][1]:.2f}, {r['null'][2]:.2f}]; matched piece "
                             f"(control) {r['matched'][0]:.2f} [{r['matched'][1]:.2f}, {r['matched'][2]:.2f}]; {FLIPS}: "
                             f"{JPART} alone {r['jspace_flips']:.0%}, whole patch {r['full_flips']:.0%}; bridge "
                             f"{SPLIT_PLAIN[r['verdict']]} (rule: {r['verdict']})")  # fmt: skip
        for key, v in s["pairs"].items():
            fams, st = key.split("/")
            hi_fam, lo_fam = fams.split("-")
            d = v["concentration_diff"]
            lines.append(f"- Same patch, two questions ({SET_TITLE[st]}, layers {v['layers']}): concentration of "
                         f"{fam_label(hi_fam)} minus {fam_label(lo_fam)} = {d[0]:.2f} [{d[1]:.2f}, {d[2]:.2f}] (scene "
                         f"bootstrap); largest share difference between the two patches {v['same_patch_max_share_diff']}")  # fmt: skip
        lines += ["", "Split half of the decision rule:", *claims_text(s["claims"])]
    else:
        for r in a.get("write_rows", []):
            fl = r["flips"]
            lines.append(f"- {cell_label(r['family'], r['set'])} (layers {r['layers']}), {FLIPS}: {PATCH} "
                         f"{fl['copy'][0]:.0%}; lens push 1x {fl['lens_x1'][0]:.0%} [{fl['lens_x1'][1]:.0%}, "
                         f"{fl['lens_x1'][2]:.0%}], 4x {fl['lens_x4'][0]:.0%}, 16x {fl['lens_x16'][0]:.0%}; random push "
                         f"(control) 4x {fl['random_x4'][0]:.0%}, 16x {fl['random_x16'][0]:.0%}; lens reads bridge org in "
                         f"its top 10 {r['read_top10']:.0%} (bridge alt {r['x_top10']:.0%}); the lens push "
                         f"{WRITE_PLAIN[r['verdict']]} (rule: {r['verdict']})")  # fmt: skip
        lines += ["", "Combined decision rule (with the split run):", *claims_text(s.get("claims"))]
    lines += ["", f"Figures: {', '.join(f'{rel}/{f}' for f in blob['figures'])}", "", "Gates:"]
    lines += [f"- {g}" for g in gates({**s, **{k: a["saved"].get(k) for k in ("n_causality_violations",)}}, kind)]
    lines += ["", f"Recomputed from the saved outputs == the run's summary.json: {json.dumps(a['same_as_saved'])}",
              "", "Status: UNVERIFIED", ""]  # fmt: skip
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["plan", "map", "parts", "readwrite", "examples", "analyze", "figures"])
    ap.add_argument("--against", default=None, help="figures, map runs: an earlier map to compare transit cells with")
    ap.add_argument("--out", default=None, help="figures: write the folder under this directory (a draft)")
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--map", help="parts / readwrite: the map run whose transit cells to use")
    ap.add_argument("--parts", help="readwrite: the parts run, for the combined decision")
    ap.add_argument("--n", type=int, default=N_CASES, help="cases per family (a smoke run: few)")
    ap.add_argument("--families", nargs="+", default=list(DEFAULT_FAMILIES), choices=list(FAMILIES))
    ap.add_argument("--tasks-set", default=None, help="PP / PM: the tasks_v2 data set (data/tasks_v2/<set>)")
    ap.add_argument("--tasks-competence", default=None, help="PP / PM: its competence run (results/tasks_v2/<run>)")
    ap.add_argument("--layers", nargs="+", type=int, default=None, help="map: override the layer grid (smoke)")
    ap.add_argument(
        "--force", nargs="+", default=None, help="parts / readwrite: SET:LAYER cells for every family (smoke)"
    )
    ap.add_argument("--k", type=int, default=K_EXAMPLES)
    ap.add_argument("--seed", type=int, default=EXAMPLES_SEED)
    ap.add_argument("--reads-per-s", type=float, default=25.0, help="plan: assumed edited reads per second")
    ap.add_argument("--sets", nargs="+", default=None, choices=list(SETS), help="parts / readwrite: sets to run")
    ap.add_argument("--sub-n", type=int, default=None, help="parts / readwrite: first K cases per family of the map's")
    ap.add_argument("--lo", type=int, default=None, help="parts / readwrite: lowest layer of the cells (default N/4)")
    args = ap.parse_args()
    if args.lo is not None:  # a budget run: cells from this layer up (the manifest records the windows)
        SPLIT_LO = args.lo
    if args.sets:
        CELL_SETS = tuple(args.sets)
    SUB_N = args.sub_n
    TASKS_SET, TASKS_COMP = args.tasks_set, args.tasks_competence
    grid = tuple(sorted(args.layers)) if args.layers else MAP_LAYERS
    if args.stage == "plan":
        stage_plan(args.n, args.families, grid, args.reads_per_s)
    elif args.stage == "map":
        assert args.why, "map needs --why"
        stage_map(args.name, args.why, args.n, args.families, grid)
    elif args.stage == "parts":
        assert args.why, "parts needs --why"
        assert args.map, "parts needs --map"
        stage_parts(args.name, args.map, args.why, parse_force(args.force))
    elif args.stage == "readwrite":
        assert args.why, "readwrite needs --why"
        assert args.map, "readwrite needs --map"
        stage_readwrite(args.name, args.map, args.why, args.parts, parse_force(args.force))
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name, args.against, args.out)
    else:
        stage_examples(args.name, args.k, args.seed)
