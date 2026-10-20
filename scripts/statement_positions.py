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
FAMILIES = SUITE + COUNTRIES
CUE_ONLY = ("RL", "RR", "R")  # C changes only the cue in the question: every statement precedes C's change
BOUND = ("BL", "BR", "BLR", "BRL", "B")
LOOKUP_USED_BOUND = ("BL", "BLR")
POSITIVE = ("B", "BR")  # the positive control at the statements, in order of preference
PAIRS = (("BL", "BR"), ("BLR", "BRL"))  # same scenes, same statements: one patch, two readers
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


def statements(c: dict) -> dict[str, Any]:
    """The context's sentences by role, as the item generators wrote them (suite_v1 wording A; exp09's countries)."""
    fam = c["family"]
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
    st = statements(c)
    ctx = c["context_text"]
    assert rendered.count(ctx) == 1, f"{c['id']}: the context is not once in the prompt"
    base = rendered.index(ctx)
    found = sorted((find_sentence(ctx, s), s) for s in st["all"])
    assert " ".join(s for _, s in found) == ctx, f"{c['id']}: the statements do not tile the context"

    def span(sentence: str) -> tuple[int, int]:
        i = base + find_sentence(ctx, sentence)
        return (i, i + len(sentence))

    marks: dict[str, list[tuple[int, int]]] = {"bind_bridge": [span(st["bind_bridge"])]}
    sent, (b0, _) = st["bind_bridge"], marks["bind_bridge"][0]
    assert sent.endswith(f"{c['bridge']}."), f"{c['id']}: {sent!r} does not end with the bridge"
    w0 = b0 + sent.rindex(c["bridge"])
    marks["bridge_word"] = [(w0, w0 + len(c["bridge"]))]
    marks["bind_other"] = [span(s) for s in st["bind_other"]]
    marks["lookup_bridge"] = [span(st["lookup_bridge"])] if st["lookup_bridge"] else []
    marks["lookup_x"] = [span(st["lookup_x"])] if st["lookup_x"] else []
    marks["context"] = [(base, base + len(ctx))]
    sets = {k: sorted({i for a, b in v for i in tokens_in(offsets, a, b)}) for k, v in marks.items()}
    every = sorted({i for at, sentence in found for i in tokens_in(offsets, base + at, base + at + len(sentence))})
    question = list(c["groups"]["question"])
    im_end = rendered.rindex("<|im_end|>")
    final = [i for i, (s, e) in enumerate(offsets) if e > s and s >= im_end]
    sets["question"] = question
    sets["final"] = final
    sets["q_words"] = [i for i in question if i not in set(final)]
    marks["question"] = [(offsets[question[0]][0], offsets[question[-1]][1])]
    marks["final"] = [(offsets[final[0]][0], offsets[final[-1]][1])]
    marks["q_words"] = [(offsets[sets["q_words"][0]][0], offsets[sets["q_words"][-1]][1])] if sets["q_words"] else []
    check_sets(c, sets, every, len(offsets))
    return sets, marks


def check_sets(c: dict, sets: dict[str, list[int]], every: list[int], n_tokens: int) -> None:
    """Disjointness, containment and the counterfactuals' footprint (asserts)."""
    name = c["id"]
    statement_parts = ("bind_bridge", "bind_other", "lookup_bridge", "lookup_x")
    for a in statement_parts:
        for b in statement_parts:
            assert a == b or not set(sets[a]) & set(sets[b]), f"{name}: {a} and {b} overlap"
    for k in ("bind_bridge", "bridge_word", "bind_other", "context", "question", "q_words", "final"):
        assert sets[k], f"{name}: {k} is empty"
    if c["family"] in SUITE:
        assert sets["lookup_bridge"], f"{name}: the bridge's lookup statement is missing"
        assert sets["lookup_x"], f"{name}: X's lookup statement is missing"
    assert set(sets["bridge_word"]) <= set(sets["bind_bridge"]), f"{name}: the bridge word is outside its statement"
    assert sets["context"] == every, f"{name}: the context is not exactly its statements"
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


def build_cases(tok, n: int, families: list[str]) -> tuple[list[dict], dict]:
    """Every case with its position sets (asserted), in family order."""
    suite = [f for f in families if f in SUITE]
    countries = [f for f in families if f in COUNTRIES]
    cases, counts = [], {}
    if suite:
        got, counts["suite"] = suite_cases(tok, n, suite)
        cases += got
    if countries:
        got, counts["countries"] = country_cases(tok, n, countries)
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


def reload_cases(m: dict, tok) -> list[dict]:
    """The map's cases, rebuilt (deterministic) and checked against its cases.jsonl."""
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["plan", "map", "parts", "readwrite", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--map", help="parts / readwrite: the map run whose transit cells to use")
    ap.add_argument("--parts", help="readwrite: the parts run, for the combined decision")
    ap.add_argument("--n", type=int, default=N_CASES, help="cases per family (a smoke run: few)")
    ap.add_argument("--families", nargs="+", default=list(FAMILIES), choices=list(FAMILIES))
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
    else:
        stage_examples(args.name, args.k, args.seed)
