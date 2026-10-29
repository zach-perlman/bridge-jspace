"""x51_answer (batch 51, test 51.12; jobs/c3/batch51.yaml addendum_4 and addendum_4_amendment (Dan 20:20), design and
rules fixed in advance; Q51.12 in predictions/2026-10-28_dan.md): is it the bridge or the answer that moves through the
lens? The answer-direction control on three sets, each with its own items, gate, layer, change and read (imported,
unchanged):

  z2   Zach's never-named bridge (x50_zach --part z2): the change at the description's last token, per reader (K = lookup,
       M = recall: the K and M passages differ before it, so each reader has its own Δ); 9B L12, 27B L32. Items: the
       stored run's chosen passages (x50_zach.RUNS["z2"]), rebuilt on the tokenizer by x50_zach.encode and checked id by
       id; read: x50_zach's (the top token after the prompt, no prefill, against the answer's first token).
  e1   the main test (x0_necessity; X0's items, gate and chat read): the change at the bridge word, one Δ from the
       lookup's prompts (both readers' prompts agree through it); 9B L12, 27B L32, Muse L26. Items: the stored X0 run's
       (x45b_binding.MAIN_RUN, the runs 49.1 / 48.1 used) chat items at L, rebuilt by x0_necessity.build_cases and
       checked id by id.
  z1k / z1p / z2p (batch 52 / 53 coverage sets, read as z2): Zach's named bridge with true facts (Z1's PK / PM), with
       made-up facts (Z1-P's PP / PM), and his described bridge with made-up facts (53.1b's MP / MM, x50_zach --part
       z2p); verdict --jsuite puts PP beside MP (9B, 27B).
  cue  47.3's described bridge in locker scenes (x47_cue): the change at the cue token, one Δ from the lookup's
       prompts; 9B L12, 27B L32. Items: the stored run's chosen scenes (x47_cue.RUNS), rebuilt by x47_cue.scenes from its
       kept cues and checked id by id; the lookup's switch is x47_cue's (it follows the change: identity, position or
       value).

The gate is each source run's (asserted from its gate.json; a failed gate means "not tested").

Answer directions A (per item; amendment 20:20): J++ lens atoms (JLens.vectors(L, ids), unit rows: the very rows of
the letter-token dictionary X0's OMP uses; not the unembedding) of letter tokens only, so digits are never in A.
  e1 / cue  the NUMBER WORDS of the answers ("six" for 6): e1 both readers' O and S answers (the lookup's are its
            lockers); cue the recall's O / S legs and the lookup's four lockers (a = O's answer, b, c, e = S's answer:
            x47_cue's lookup switch counts b, c and e). Per word its variants (as is, leading space, capitalised, both),
            each kept where it is exactly one letter token.
  z2        O's and S's answers (the same for K and M): the first token of each answer word and of each variant (where
            the tokenizer splits the full word, only its first token: "Greece" -> "G").
P_A = the orthogonal projector on span(A) (SVD of the atoms, rank kept above 1e-6 of the top singular value).

Parts of Δ = h_S - h_O at the edited token at L: P_J Δ = X0's 25-atom signed OMP part over the J++ letter-token atoms
(x0_necessity.fit, the stored runs' path); (I - P_A) P_J Δ = the J++ part with A projected out ("remove only the lens
directions that are not answer directions": the J++ part's component in span(A) is kept in the state, everything else
of the J++ part is removed); P_A Δ = the answer directions alone. Arms (each added at the edited token at L on O,
X0's AddRows), each against a random part of its own share (x6_routes.removal_arms: statement_positions.
random_subspace_part over X0's random basis, seed 888 + L, the same basis for every arm):

  whole             Δ
  no_jpp            Δ - P_J Δ                 arm 1 (as run; must reproduce the stored runs' no_jpp / no_part)
  no_jpp_rand       Δ - R(P_J Δ's share)
  no_jpp_A          Δ - (I - P_A) P_J Δ       arm 2
  no_jpp_A_rand     Δ - R((I - P_A) P_J Δ's share)
  no_A              Δ - P_A Δ                 arm 3
  no_A_rand         Δ - R(P_A Δ's share)      arm 4 ("without a random part of A's share" = arm 3's random twin)
  no_F (z2 only)    Δ - P_F Δ                 arm 3's frequency-matched control (amendment 20:20): F = one unrelated
                                              letter atom per atom of A, matched on the BPE id (merge order, a corpus
                                              frequency proxy) and the J++ readout norm (freq_match)

Lens readout check (amendment 20:20; the run records the ranks in readout.jsonl from the forwards that give Δ, no
states are cached; the verdict computes the shares on CPU): per reader, the rank of its own answer word (the best of its
A-style variant tokens) in the J++ readout over the vocabulary at the edited token at L, on O (O's answer) and on S
(S's answer), beside the bridge entity's rank; the share of items with it in the top 10 / top 50. If it ranks > 50 on
both O and S for >= 90 % of items, the verdict is "the answer word is not read at the bridge word" (arms beside); else
the arm-based rule decides.

Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader (switch: the set's own). Rules (fixed in
advance, per model and reader; point estimates decide, EPS 1e-9 at the bars; cluster bootstrap over the bridge entity,
10,000 resamples, seed 0, paired): "the lens effect is the entity": e2 >= 0.7 e1 and e3 <= 0.10; "the lens effect is the
answer": e2 <= 0.3 e1 and e3 >= 0.5 e1; else mixed (both shares e2 / e1 and e3 / e1 reported); e1 <= 0 or undefined:
can't tell. On z2 arm 3 is read against both its controls (e3 against no_A_rand, e3f = (S_noF - S_noA) / S_whole): a
label holds only if it holds against both (entity: max(e3, e3f) <= 0.10; answer: min(e3, e3f) >= 0.5 e1). Beside
(descriptive): per item |A|, how many of Δ's 25 OMP atoms are in A, Δ's energy share along span(A) (norms.jsonl); the
lens readout's top-1 class at the edited token on O and on S (own answer / own bridge entity / neither); arm 1 against
the stored runs item by item (agreement.json).

SEALED: the run writes per-item outputs and the arm-1 agreement only; verdict and view refuse until
predictions/2026-10-28_dan.md holds Dan's Q51.12 answer at HEAD.

uv run python scripts/x51_answer.py plan --set e1                                             # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_answer.py run --set e1 --name qwen35_9b_x51_12_e1_r2   # GPU (sealed)
uv run python scripts/x51_answer.py verdict                                                    # CPU, after Q51.12
uv run python scripts/x51_answer.py view                                                       # CPU, after Q51.12
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
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x48_heads as H

EXP = "x51_answer"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.12"
SETS = ("z2", "e1", "cue")  # 51.12's design sets
NAMED_SETS = ("z1k", "z1p")  # batch 52, Dan's morning brief item 2 (coverage runs only)
MP_SETS = ("z2p",)  # batch 53, 53.1b: Zach's described bridge with his made-up facts (MP / MM; coverage runs only)
ALL_SETS = SETS + NAMED_SETS + MP_SETS
# Zach's passages: each reader's own Δ at the patch token, word answers, his read
ZACH_SETS = ("z2", "z1k", "z1p", "z2p")
Z1_SOURCE = {"z1k": "z1", "z1p": "z1p"}  # x50_zach part each Z1 set rebuilds from (K: Z1's PK / PM; P: Z1-P's PP / PM)
Z2_SOURCE = {"z2": "z2", "z2p": "z2p"}  # x50_zach part each Z2-design set rebuilds from (K: Z2's MK / MM; P: MP / MM)
SET_TEXT = {"z2": "Z2 (Zach's never-named bridge, the description's last token)",
            "z1k": "Zach's named bridge, true facts (Z1's K passages; the pointer name's last token)",
            "z1p": "Zach's named bridge, made-up facts (Z1-P's P passages; the pointer name's last token)",
            "z2p": "Zach's described bridge, made-up facts (MP / MM passages: Z2's design with the lookup reading P; the "
                   "description's last token)",
            "e1": "the main test E1 (the bridge word)", "cue": "47.3's described bridge (the cue token, locker scenes)"}  # fmt: skip
# r2 (amendment 20:20): new run names; the r1 runs (digit A, no frequency control) stay as records
RUNS = {
    "z2": {"qwen3.5-9b": "qwen35_9b_x51_12_z2_r2", "qwen3.6-27b": "x51_12_z2_27b_r2"},
    "e1": {"qwen3.5-9b": "qwen35_9b_x51_12_e1_r2", "qwen3.6-27b": "x51_12_e1_27b_r2",
           "muse-glimmer-30b": "muse30_x51_12_e1_r2"},
    "cue": {"qwen3.5-9b": "qwen35_9b_x51_12_cue_r2", "qwen3.6-27b": "x51_12_cue_27b_r2"},
}  # fmt: skip
TAGS = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse"}
SPEC_IDS = {s: {t: f"x51_12_{s}_{TAGS[t]}_r2" for t in RUNS.get(s, {})} for s in SETS}
SPEC_IDS["z2p"] = {"qwen3.5-9b": "x53_1b_jsuite_9b", "qwen3.6-27b": "x53_1b_jsuite_27b"}  # batch 53, 53.1b
# Batch 52 C coverage (jobs/c3/batch52.yaml, amendment 3): the same rules on Lightning, no Q-line; read by verdict
# --coverage (RUNS and 51.12's own verdict unchanged)
COVERAGE_RUNS = {
    "e1": {"nemotron-3.5-lightning": "nem35l_x52_answer"},
    "cue": {"nemotron-3.5-lightning": "nem35l_x52_cue_answer"},  # cue: on 47.3's Lightning run
    "z2": {"nemotron-3.5-lightning": "nem35l_x52_answer_z2"},  # z2: on Lightning's Z2 run (morning brief 3)
}
# Dan's morning brief (29 Oct) item 2: 51.12's arms on Zach's named passages, K and P (his missing cell: the bridge named
# before the question, word answers), on the 9B, 27B and Lightning at the committed L; rules verbatim, no prediction
for _s in ("z1k", "z1p"):
    COVERAGE_RUNS[_s] = {"qwen3.5-9b": f"qwen35_9b_x52_answer_{_s}", "qwen3.6-27b": f"x52_answer_{_s}_27b",
                         "nemotron-3.5-lightning": f"nem35l_x52_answer_{_s}"}  # fmt: skip
# Batch 53, 53.1b (jobs/c3/batch53.yaml standing_rules_0950: "jsuite PP vs MP, 51.12's arms + readout, 9B then 27B"):
# PP = the z1p runs above (Z1-P's lookup), MP = these (z2p's lookup); rules verbatim, no prediction; verdict --jsuite
COVERAGE_RUNS["z2p"] = {"qwen3.5-9b": "qwen35_9b_x53_answer_z2p", "qwen3.6-27b": "x53_answer_z2p_27b"}
JSUITE = {"sets": ("z1p", "z2p"), "targets": ("qwen3.5-9b", "qwen3.6-27b"),
          "cells": {"z1p": {"K": "PP", "M": "PM"}, "z2p": {"K": "MP", "M": "MM"}}}  # fmt: skip
NO_PREDICTION_JSUITE = "no prediction (batch 53, 53.1b: 51.12's rules verbatim)"
# Batch 52, Dan's morning queue (29 Oct) item 1: 51.12's cue set on Lightning below 47.3's gate (exploratory, hollow):
# --below-gate reads the below-gate 47.3 run (x47_cue.BELOW_RUNS) and writes these runs
BELOW = False
BELOW_RUNS = {"cue": {"nemotron-3.5-lightning": "nem35l_x52_cue_answer_below"}}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_answer/x51_12-20261028T201842Z"  # 51.12's rules first scored (r2)


def runs_of(set_name: str) -> dict[str, str]:
    """51.12's runs of a set and the batch 52 coverage runs."""
    return {**RUNS.get(set_name, {}), **COVERAGE_RUNS.get(set_name, {})}


ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_jpp_A", "no_jpp_A_rand", "no_A", "no_A_rand")
F_ARM = "no_F"
# the amendment's frequency-matched control: Z2, and Zach's other passages (word answers too: the amendment's reason,
# common word starts, applies; a label then needs both controls: conservative)
FREQ_SETS = ("z2", "z1k", "z1p", "z2p")
NUMBER_SETS = ("e1", "cue")  # A = the answers' number words
PAIRS = {1: ("no_jpp", "no_jpp_rand"), 2: ("no_jpp_A", "no_jpp_A_rand"), 3: ("no_A", "no_A_rand")}
PAIR_F = ("no_A", F_ARM)  # arm 3 against its frequency-matched control
ARM_TEXT = {
    "whole": "Δ = h_S - h_O at the edited token at L",
    "no_jpp": "arm 1: Δ - P_J Δ (P_J Δ: X0's 25-atom signed OMP part over the J++ letter-token atoms at L)",
    "no_jpp_A": "arm 2: Δ - (I - P_A) P_J Δ (the J++ part with the answer directions A projected out)",
    "no_A": "arm 3: Δ - P_A Δ (the answer directions alone)",
    "*_rand": "each arm's random twin: Δ minus X0's random subspace part of the removed part's share of ||Δ||^2 (seed "
              "888 + L); no_A_rand is arm 4, 'without a random part of A's share'",
    F_ARM: "Z2 only: arm 3's frequency-matched control, Δ - P_F Δ (F: per atom of A one unrelated letter atom with its "
           "BPE id within a factor 2 and the closest J++ readout norm)",
}  # fmt: skip
ENTITY_KEEP, ENTITY_A_MAX = 0.7, 0.10
ANSWER_KEEP, ANSWER_A_MIN = 0.3, 0.5
EPS = 1e-9
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0
RANK_TOL = 1e-6
FREQ_BAND = 2.0  # F's id within a factor FREQ_BAND of the answer token's (doubled until a candidate exists)
MIN_RELATED = 3  # keys of at least this many characters count as related by containment
NORM_CHUNK = 32768
TOP_K = (10, 50)
NOT_READ_RANK, NOT_READ_SHARE = 50, 0.90
LABELS = {"entity": "the lens effect is the entity", "answer": "the lens effect is the answer", "mixed": "mixed",
          "na": "can't tell (arm 1 has no extra loss beyond random)",
          "not_read": "the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)"}  # fmt: skip
RULE = ('Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1\'s extra loss and arm 3 '
        'costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone '
        "costs >= 0.5 of arm 1. Else: mixed, report both shares. Amendment (Dan 20:20): before the arms, the lens "
        "readout check at the bridge word; the verdict says which case held, either 'the answer word is not read at the "
        "bridge word (lens rank > 50 on >= 90 % of items)' or the arm-based entity / answer / mixed (never 'void by "
        "construction'). Z2: arm 3 is read against its controls (a same-size random part and a frequency-matched part), "
        "not against zero.")  # fmt: skip
AS_COMPUTED = (
    "Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader over the source run's items (switch: the "
    "set's own read; 47.3's lookup: follows the change, identity / position / value). e1, e2, e3 = arms 1, 2, 3; arm 4 "
    "(no_A_rand) is arm 3's random twin. 'Keeps >= 0.7 of arm 1' = e2 / e1 >= 0.7; 'costs <= 0.10 beyond random' = e3 "
    "<= 0.10; 'falls to <= 0.3 of arm 1' = e2 / e1 <= 0.3; 'costs >= 0.5 of arm 1' = e3 / e1 >= 0.5. Z2: arm 3 against "
    "both its controls, e3 (vs no_A_rand) and e3f = (S_noF - S_noA) / S_whole (vs no_F); 'entity' needs max(e3, e3f) "
    "<= 0.10, 'answer' needs min(e3, e3f) >= 0.5 e1 (a label holds only against both controls). Point estimates decide "
    "(EPS 1e-9); e1 <= 0 or undefined (no switch under the whole change) -> can't tell; CIs from X0's cluster bootstrap "
    "over the bridge entity (10,000, seed 0), paired across arms (ratios on the same draws). Readout case first: per "
    "reader the rank (1 + tokens with a strictly higher lens logit, full vocabulary) of its own answer word (best of its "
    "A-style variant tokens) at the edited token at L, O's answer on O's state and S's on S's (z2: the reader's own "
    "state; e1 / cue: the lookup's, shared through the edited token); an item is 'not read' when it ranks > 50 on both; "
    ">= 90 % of items not read -> 'the answer word is not read at the bridge word', the arms reported beside; else the "
    "arm-based label. A: J++ unit atoms of letter tokens (the OMP dictionary); e1 / cue the answers' number words "
    "(suite_v1.WORDS: 6 -> 'six'), each of its variants (as is, leading space, capitalised, both) kept where it is one "
    "letter token; z2 the first token of each answer word and variant (where the tokenizer splits the full word, its "
    "first token only). Frequency-matched control F (z2): per atom a of A, the letter token f with |log((id_f + 1) / "
    "(id_a + 1))| <= log 2 (a BPE id is its merge rank, earlier = more frequent in the tokenizer's training corpus; the "
    "factor doubles until a candidate exists) and the closest log J++ readout norm ||(g * W_U[t]) J_L|| (ties: lower "
    "id); unrelated = its key (decode, stripped, lower-cased) equals no key of the set's answer words, A tokens, bridge "
    "entities' tokens / names or edited tokens, and (keys of >= 3 characters) neither contains nor is contained in one; "
    "never twice in one item. no_F = Δ - P_F Δ, P_F the projector on span(F). Decisive cells for Q51.12: Z2 both "
    "readers; E1 the recall (the lookup beside); 47.3 both readers. Projected out: (I - P_A) P_J Δ, P_A the orthogonal "
    "projector on the span of the item's answer atoms (the J++ part minus its component along span(A))."
)  # fmt: skip
READER_NAME = {"PP": "lookup", "PM": "recall", "K": "lookup", "M": "recall"}
ALNUM = re.compile(r"[^\W_]")  # a letter or a digit
LETTER = re.compile(r"[^\W\d_]")  # bridge_jspace.model._HAS_LETTER: the OMP dictionary's tokens


def arms_of(set_name: str) -> tuple[str, ...]:
    return ARMS + ((F_ARM,) if set_name in FREQ_SETS else ())


# ---- answer directions and parts (CPU-testable) --------------------------------------------------------------------


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def variants(w: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys((w, " " + w, cap(w), " " + cap(w))))


def number_word(answer: str) -> str:
    """The number word of a single-digit answer (suite_v1.WORDS: "6" -> "six")."""
    from scripts import suite_v1 as S

    a = str(answer).strip()
    assert len(a) == 1, f"not a single digit: {answer!r}"
    assert a.isdigit(), f"not a single digit: {answer!r}"
    return S.WORDS[int(a)]


def word_ids(tok, words: list[str], whole: bool) -> list[int]:
    """A's token ids for answer words: per word each variant (as is, leading space, capitalised, both); whole (number
    words): the variant only if it is exactly one token; else (z2) the variant's first token (the first token of the full
    word where the tokenizer splits it). Letter tokens only (the OMP dictionary); sorted, unique."""
    from scripts import suite_v1 as S

    out = set()
    for w in words:
        for v in variants(str(w)):
            ids = S.ids(tok, v)
            if not ids or (whole and len(ids) != 1):
                continue
            if LETTER.search(tok.decode([ids[0]])):
                out.add(int(ids[0]))
    return sorted(out)


def variant_ids(tok, words: list[str]) -> list[int]:
    """The first token of each word and of its obvious variants (leading space, capitalised), whitespace-only or
    letterless-and-digitless first tokens dropped; sorted, unique (the readout's answer-as-stated and bridge tokens)."""
    from scripts import suite_v1 as S

    out = set()
    for w in words:
        for v in variants(str(w)):
            ids = S.ids(tok, v)
            if ids and ALNUM.search(tok.decode([ids[0]])):
                out.add(int(ids[0]))
    return sorted(out)


def answer_basis(vecs):
    """An orthonormal basis [d, r] of the span of the rows of vecs [m, d] (SVD in float64 on the CPU, singular values
    above RANK_TOL x the largest kept); [d, 0] for no rows."""
    import torch

    v = vecs.detach().double().cpu()
    if v.shape[0] == 0:
        return torch.zeros(v.shape[1], 0, dtype=torch.float32)
    u, s, _ = torch.linalg.svd(v.T, full_matrices=False)
    keep = s > RANK_TOL * s.max()
    return u[:, keep].float()


def span_part(x, bases: list):
    """Per row i of x [n, d] with basis Q_i [d, r_i]: Q_i Q_i^T x_i (the component along the span)."""
    import torch

    out = torch.empty_like(x, dtype=torch.float32)
    for i, q in enumerate(bases):
        q = q.to(x.device, torch.float32)
        out[i] = q @ (q.T @ x[i].float())
    return out


def answer_parts(delta, pj, bases: list) -> tuple[Any, Any]:
    """Per row i of Δ [n, d] with basis Q_i [d, r_i]: (I - P_A) P_J Δ (the J++ part with A projected out) and P_A Δ."""
    return pj.float() - span_part(pj, bases), span_part(delta, bases)


def omp_support(dic, x, k: int):
    """exp04_brew_parts.signed_omp's greedy selection, returning the chosen atom indices [m, k] and the approximation
    (signed_omp returns only the approximation; the run asserts the two approximations agree)."""
    import torch

    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    for _ in range(k):
        scores = ((x - approx) @ dic.T).abs()
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dic[chosen].double()
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
    return chosen, approx


def all_arms(delta, pj, bases: list, basis, f_bases: list | None = None) -> tuple[dict, dict]:
    """The arms (ARMS order, then no_F where f_bases are given) and the per-row shares of the removed parts
    (x6_routes.removal_arms: each part removed and, against it, X0's random part of its own share; no_F has no random
    twin, it is itself arm 3's control)."""
    from scripts import x6_routes as R

    pja, pa = answer_parts(delta, pj, bases)
    more, sh = R.removal_arms(delta, {"jpp": pj, "jpp_A": pja, "A": pa}, basis)
    arms = {"whole": delta, **more}
    assert tuple(arms) == ARMS, tuple(arms)
    sq = (delta.float().norm(dim=-1) ** 2).clamp_min(1e-30)
    sh["A_in_jpp"] = (pj.float() - pja).norm(dim=-1) ** 2 / sq
    if f_bases is not None:
        pf = span_part(delta, f_bases)
        arms[F_ARM] = delta - pf
        sh["F"] = pf.norm(dim=-1) ** 2 / sq
    return arms, sh


# ---- the frequency-matched control (Z2; CPU-testable) ---------------------------------------------------------------


def key_of(s: str) -> str:
    return s.strip().lower()


def related_keys(tok, items: list[dict], toks: list[dict]) -> set[str]:
    """The set's answer words, A tokens, bridge entities (names and tokens) and edited tokens, as keys."""
    keys = set()
    for it, tk in zip(items, toks, strict=True):
        ids = tk["A"] + tk["bridge"]["org"] + tk["bridge"]["alt"]
        ids += [rd["ids"][v][rd["pos"]] for rd in it["readers"].values() for v in ("org", "alt")]
        keys |= {key_of(tok.decode([int(t)])) for t in ids}
        keys |= {key_of(w) for w in (*tk["A_words"], it["entity"], it["cf_entity"])}
    keys.discard("")
    return keys


def related_mask(keys: list[str], related: set[str], min_len: int = MIN_RELATED) -> np.ndarray:
    """True where a token's key is related to the set: equal to a related key, or (both at least min_len characters)
    contained in one or containing one."""
    long = {k for k in related if len(k) >= min_len}
    joined = "\x00".join(sorted(long))
    top = max((len(k) for k in long), default=0)
    out = np.zeros(len(keys), dtype=bool)
    for i, k in enumerate(keys):
        if k in related:
            out[i] = True
        elif len(k) >= min_len and long:
            n = len(k)
            out[i] = k in joined or any(
                k[a:b] in long for a in range(n) for b in range(a + min_len, min(n, a + top) + 1)
            )
    return out


def freq_match(a_ids: list[int], letter_ids: np.ndarray, log_norm: np.ndarray, banned: np.ndarray,
               band: float = FREQ_BAND) -> list[dict]:  # fmt: skip
    """Per answer token a (in order): the letter token f, not banned, not in A and not already taken for this item, with
    its id within a factor `band` of a's ((id + 1) ratio; the band multiplied by `band` until a candidate exists) and,
    among those, the closest log J++ readout norm (ties: the lower id). letter_ids sorted ascending, log_norm aligned."""
    assert (np.diff(letter_ids) > 0).all(), "letter ids must be sorted and unique"
    lid = letter_ids.astype(np.float64) + 1.0
    where = [int(np.searchsorted(letter_ids, a)) for a in a_ids]
    for a, i in zip(a_ids, where, strict=True):
        found = i < len(letter_ids) and int(letter_ids[i]) == int(a)
        assert found, f"answer token {a} is not a letter token"
    taken = np.zeros(len(letter_ids), dtype=bool)
    taken[where] = True
    out = []
    for a, i in zip(a_ids, where, strict=True):
        dist = np.abs(np.log(lid / (int(a) + 1.0)))
        f = band
        while True:
            free = (dist <= math.log(f) + 1e-12) & ~banned & ~taken
            if free.any():
                break
            assert f < 1e12, "no unrelated letter token to match"
            f *= band
        cand = np.flatnonzero(free)
        d = np.abs(log_norm[cand] - log_norm[i])
        j = int(cand[np.lexsort((letter_ids[cand], d))[0]])
        taken[j] = True
        out.append({"a": int(a), "f": int(letter_ids[j]), "band": f,
                    "id_ratio": round(float(lid[j] / (int(a) + 1.0)), 4),
                    "norm_ratio": round(float(math.exp(log_norm[j] - log_norm[i])), 4)})  # fmt: skip
    return out


# ---- items: each set's own code, rebuilt and checked against the stored run (tokenizer only) -----------------------


def layer_of(set_name: str, target: str) -> int:
    from scripts import x50_zach as Z

    return Z.LAYERS[target][0] if set_name in ZACH_SETS else X.PREDICTED[target]


def source_of(set_name: str, target: str) -> Path:
    from scripts import x45b_binding as B
    from scripts import x47_cue as CUE
    from scripts import x50_zach as Z

    if set_name in ZACH_SETS:
        part = Z1_SOURCE.get(set_name, set_name)
        return Z.RESULTS / {**Z.RUNS.get(part, {}), **Z.COVERAGE_RUNS.get(part, {})}[target]  # batch 52: Lightning's
    if set_name == "e1":
        return X.RESULTS / B.MAIN_RUN[target]
    if BELOW:
        return CUE.RESULTS / CUE.BELOW_RUNS[target]
    return CUE.RESULTS / {**CUE.RUNS, **CUE.COVERAGE_RUNS}[target]  # batch 52 C: Lightning's 47.3 run (nem35l_x52_cue)


def unit(set_name: str, c: dict, key: str, entity: str, cf_entity: str, extra_words: dict[str, list[str]]) -> dict:
    """One item in this script's shape: per reader its prompts, edited position, answer tokens, read suffix and the
    reader whose prompts give its Δ (z2: its own; e1 / cue: the lookup's, identical through the edited token)."""
    readers = {}
    for w, rd in c["readers"].items():
        pos = rd["pos"] if set_name in ZACH_SETS else c["pos"]
        src = w if set_name in ZACH_SETS else X.LOOKUP
        readers[w] = {**{k: v for k, v in rd.items() if k not in ("context", "cf_context")}, "pos": pos, "src": src,
                      "suffix": [] if set_name in ZACH_SETS else c["space"],
                      "words_A": [rd["answer"], rd["cf_answer"], *extra_words.get(w, [])]}  # fmt: skip
    out = {
        "set": set_name,
        "key": key,
        "scene": c["scene"],
        "entity": entity,
        "cf_entity": cf_entity,
        "readers": readers,
    }
    if set_name == "cue":
        out["route_tokens"] = c["route_tokens"]
        out["expect"] = c["expect"]
    if set_name in ZACH_SETS:
        out["source_set"] = c["set"]
    if set_name in Z2_SOURCE:
        out["desc"], out["cf_desc"] = c["desc"], c["cf_desc"]
    if set_name in Z1_SOURCE:
        out["stratum"] = c.get("stratum")
    return out


def z2_items(tok, target: str, set_name: str = "z2") -> tuple[list[dict], dict, dict]:
    """Zach's described-bridge passages (z2: Z2's run, MK / MM; z2p: 53.1b's MP / MM run): the source run's chosen
    passages rebuilt by x50_zach.encode (its part) and checked id by id."""
    from scripts import x50_zach as Z

    part = Z2_SOURCE[set_name]
    src = source_of(set_name, target)
    gate = json.loads((src / "gate.json").read_text())
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m.get("part", "z2") == part, f"{src.name} is a {m.get('part')} run, not {part}"
    assert layer_of(set_name, target) in m["layers"], f"{src.name} has no L{layer_of(set_name, target)}"
    stored = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    passages = {}
    for s in sorted({s for s, _ in gate["order"]}):
        ps, _ = Z.load_pairs(s, part)
        passages.update({(s, p[Z.LOOKUP]["scene"]): p for p in ps})
    items, drops = [], collections.Counter()
    for s, scene in gate["order"]:
        old = stored[(s, scene)]
        c, why = Z.encode(tok, part, passages[(s, scene)], old["cf_bridge"], old["cf_desc"])
        assert c is not None, f"{s} {scene}: does not rebuild ({why})"
        c["set"] = s
        for w in Z.READERS:
            assert c["readers"][w]["ids"] == old["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {src.name}"
            assert c["readers"][w]["pos"] == old["readers"][w]["pos"], f"{scene}: {w}'s patch token moved"
        c["desc"], c["cf_desc"] = old["desc"], old["cf_desc"]
        items.append(unit(set_name, c, f"{s}|{scene}", c["bridge"], c["cf_bridge"], {}))
    g = {"pass": bool(gate["pass"]), "chosen": gate["chosen"], "org_read_accuracy": gate["org_read_accuracy"],
         "gate": gate["gate"]}  # fmt: skip
    return items, g, {"source": src.name, "items": len(items), "drops": dict(drops),
                      "sets": dict(collections.Counter(it["source_set"] for it in items))}  # fmt: skip


def e1_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    from scripts import x45b_binding as B
    from scripts import x47_cumulative as C

    src = source_of("e1", target)
    layer = layer_of("e1", target)
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["predicted"] == layer, f"{src.name}: layer {m['predicted']}, not {layer}"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {src.name}"
    scenes, _ = C.stored_whole(src, layer)
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    with B.x0_alt(m.get("alt") or "cf", ("chat",)):
        cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    items = []
    for s in scenes:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the bridge position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        it = unit("e1", c, s, c["bridge"], c["cf_bridge"], {})
        it["domain"] = c["domain"]
        items.append(it)
    gate = json.loads((src / "gate.json").read_text())["gate"]["chat"]
    g = {"pass": bool(gate["pass"]) and bool(gate["enough"]), "chosen": len(items),
         "org_read_accuracy": gate["org_accuracy"], "gate": X.GATE, "eligible": gate["eligible"]}  # fmt: skip
    return items, g, {"source": src.name, "set": m["set"], "items": len(items)}


def cue_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    from scripts import x47_cue as CUE

    src = source_of("cue", target)
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["layer"] == layer_of("cue", target), f"{src.name}: layer {m['layer']}"
    cues = json.loads((src / "cues.json").read_text())
    gate = json.loads((src / "gate.json").read_text())
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    cases, _ = CUE.scenes(tok, cues["kept"])
    rebuilt = {c["scene"]: c for c in cases}
    items = []
    for s in gate["order"]:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the cue position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        routes = [str(c["expect"][k]) for k in ("identity", "position")]  # a (original) and e (value) are O's / S's
        items.append(unit("cue", c, s, c["bridge"], c["cf_bridge"], {X.LOOKUP: routes}))
    g = {"pass": (bool(gate["pass"]) or BELOW) and cues["status"] == "ok", "chosen": gate["chosen"],
         "org_read_accuracy": gate["org_read_accuracy"], "gate": gate["gate"],
         **({"below_gate": True, "source_gate_pass": bool(gate["pass"])} if BELOW else {})}  # fmt: skip
    return items, g, {"source": src.name, "items": len(items), "cues_kept": len(cues["kept"])}


def z1_items(tok, target: str, set_name: str) -> tuple[list[dict], dict, dict]:
    """Zach's named passages (K: Z1's run; P: Z1-P's run): the source run's chosen passages rebuilt by x50_zach.encode
    (its part) and checked id by id, as z2_items."""
    from scripts import x50_zach as Z

    part = Z1_SOURCE[set_name]
    src = source_of(set_name, target)
    gate = json.loads((src / "gate.json").read_text())
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["part"] == part, f"{src.name} is a {m['part']} run, not {part}"
    assert layer_of(set_name, target) in m["layers"], f"{src.name} has no L{layer_of(set_name, target)}"
    stored = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    passages = {}
    for s_ in sorted({s_ for s_, _ in gate["order"]}):
        ps, _ = Z.load_pairs(s_, part)
        passages.update({(s_, p[Z.LOOKUP]["scene"]): p for p in ps})
    items = []
    for s_, scene in gate["order"]:
        old = stored[(s_, scene)]
        c, why = Z.encode(tok, part, passages[(s_, scene)], old["cf_bridge"])
        assert c is not None, f"{s_} {scene}: does not rebuild ({why})"
        c["set"] = s_
        for w in Z.READERS:
            assert c["readers"][w]["ids"] == old["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {src.name}"
            assert c["readers"][w]["pos"] == old["readers"][w]["pos"], f"{scene}: {w}'s patch token moved"
        items.append(unit(set_name, c, f"{s_}|{scene}", c["bridge"], c["cf_bridge"], {}))
    g = {"pass": bool(gate["pass"]), "chosen": gate["chosen"], "org_read_accuracy": gate["org_read_accuracy"],
         "gate": gate["gate"]}  # fmt: skip
    return items, g, {"source": src.name, "items": len(items),
                      "sets": dict(collections.Counter(it["source_set"] for it in items))}  # fmt: skip


BUILD = {"z2": z2_items, "e1": e1_items, "cue": cue_items, "z1k": lambda tok, t: z1_items(tok, t, "z1k"),
         "z1p": lambda tok, t: z1_items(tok, t, "z1p"), "z2p": lambda tok, t: z2_items(tok, t, "z2p")}  # fmt: skip


def item_tokens(tok, it: dict) -> dict:
    """Per item: A's token ids and words (number words on e1 / cue, the answer words on z2; letter tokens only), the
    answer words the tokenizer splits (no leading space), and per variant (org / alt) per reader its own answer word's
    tokens (A-style: the readout check), its own answer's tokens as stated or as a word (the top-1 class) and the own
    bridge entity's tokens."""
    from scripts import suite_v1 as S

    num = it["set"] in NUMBER_SETS
    word = number_word if num else str
    a_words = list(dict.fromkeys(word(x) for rd in it["readers"].values() for x in rd["words_A"]))
    field = {"org": "answer", "alt": "cf_answer"}
    own_word = {v: {w: word_ids(tok, [word(rd[f])], num) for w, rd in it["readers"].items()} for v, f in field.items()}
    own = {v: {w: sorted(set(variant_ids(tok, [rd[f]])) | set(own_word[v][w])) for w, rd in it["readers"].items()}
           for v, f in field.items()}  # fmt: skip
    bridge = {"org": variant_ids(tok, [it["entity"]]), "alt": variant_ids(tok, [it["cf_entity"]])}
    return {"A": word_ids(tok, a_words, num), "A_words": a_words,
            "split_words": [w for w in a_words if len(S.ids(tok, w)) > 1], "own": own, "own_word": own_word,
            "bridge": bridge}  # fmt: skip


def size_summary(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": int(min(values)), "median": float(np.median(values)), "max": int(max(values)),
            "mean": round(float(np.mean(values)), 3), "hist": dict(sorted(collections.Counter(values).items()))}  # fmt: skip


def mark(decode, ids: list[int], pos: int) -> str:
    return decode(ids[:pos]) + "⟦" + decode(ids[pos : pos + 1]) + "⟧" + decode(ids[pos + 1 :])


def stored_atoms(set_name: str, target: str) -> tuple[str | None, dict[str, list[int]]]:
    """Δ's 25 OMP atoms (token ids) per scene from a stored x0_atoms run on the same source run, layer and letter
    dictionary (CPU; e1 only: x0_atoms fitted the same Δ, its share_k25 = the source run's); (None, {}) if none."""
    root = pins.RESULTS_DIR / "x0_atoms"
    if set_name != "e1" or not root.exists():
        return None, {}
    src, layer = source_of(set_name, target).name, layer_of(set_name, target)
    for d in sorted(root.iterdir()):
        m = json.loads((d / "manifest.json").read_text()) if (d / "manifest.json").exists() else {}
        if (m.get("source"), m.get("layer"), m.get("vocab")) == (src, layer, "letters"):
            out: dict[str, list[int]] = {}
            for r in X.read_jsonl(d / "atoms.jsonl"):
                out.setdefault(r["scene"], [int(a["token_id"]) for a in r["atoms"] if a["rank"] <= X.K_MAIN])
            return d.name, out
    return None, {}


def stage_plan(set_name: str, plan_dir: str | None = None, k_prompts: int = N_PROMPTS) -> Path:
    """Tokenizer and stored runs only: the items (rebuilt and checked against the source run), the source gate, |A| per
    item, the number-word variants (or z2's split answer words), Δ's 25 OMP atoms in A where a stored x0_atoms run has
    them, the arms and reads, and k rendered prompts (seed 0)."""
    from bridge_jspace.utils import git_state
    from scripts import suite_v1 as S
    from scripts import x45m

    target = pins.TARGET
    assert target in runs_of(set_name), f"51.12 {set_name} runs on {sorted(runs_of(set_name))}, not {target}"
    tok = x45m.tokenizer()
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    items, gate, counts = BUILD[set_name](tok, target)
    toks = [item_tokens(tok, it) for it in items]
    sizes = [len(t["A"]) for t in toks]
    num = set_name in NUMBER_SETS
    words = collections.Counter(w for tk in toks for w in tk["A_words"])
    forms = {w: {v: [decode([t]) for t in S.ids(tok, v)] for v in variants(w)} for w in sorted(words)}
    missing = sum(not ids for tk in toks for per in tk["own_word"].values() for ids in per.values())
    run_atoms, atoms = stored_atoms(set_name, target)
    hits = [len(set(atoms[it["key"]]) & set(tk["A"])) for it, tk in zip(items, toks, strict=True) if it["key"] in atoms]
    names = arms_of(set_name)
    reads = len(items) * len(next(iter(items))["readers"]) * (1 + len(names)) if items else 0
    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    chosen = sorted(random.Random(VIEW_SEED).sample(range(len(items)), min(k_prompts, len(items))))
    blob = {"set": set_name, "target": target, "layer": layer_of(set_name, target), "run": runs_of(set_name)[target],
            "spec": SPEC_IDS.get(set_name, {}).get(target), "code": git_state(), "source_gate": gate, "counts": counts,
            "entities": len({it["entity"] for it in items}), "arms": list(names), "reads": reads,
            "delta_forwards": len(items) * 2 * len({rd["src"] for rd in items[0]["readers"].values()}) if items else 0,
            "A_kind": "number words, one-token letter variants" if num else "answer words, first token of each variant",
            "A_tokens_per_item": size_summary(sizes), "A_words_per_item": size_summary([len(t["A_words"]) for t in toks]),
            "A_words_most_common": words.most_common(30),
            "A_tokens_most_common": collections.Counter(decode([t]) for tk in toks for t in tk["A"]).most_common(30),
            "variant_tokens": forms if num else None,
            "split_answer_words": dict(collections.Counter(w for tk in toks for w in tk["split_words"]).most_common()),
            "split_answer_words_tokens": {w: forms[w][w] for w in sorted({w for tk in toks for w in tk["split_words"]})},
            "items_with_a_split_answer_word": sum(bool(tk["split_words"]) for tk in toks),
            "own_answer_word_missing": missing,
            "answer_atoms_in_omp_25": {"source": run_atoms, "items": len(hits), **size_summary(hits)} if run_atoms
                                      else "not computable on CPU: needs Δ at L (GPU forwards) and no stored x0_atoms "
                                           "run fits these items; reported by the run (norms.jsonl n_answer_atoms_in_25)",
            "frequency_control": ("matched in the run: needs the J++ readout norms of every letter token (GPU)"
                                  if set_name in FREQ_SETS else None),
            "prompts": [{"key": items[i]["key"], "bridge": f"{items[i]['entity']} -> {items[i]['cf_entity']}",
                         "A": [decode([t]) for t in toks[i]["A"]],
                         **{f"{READER_NAME[w]}_{v}": mark(decode, rd["ids"][v] + rd["suffix"], rd["pos"])
                            for w, rd in items[i]["readers"].items() for v in ("org", "alt")}} for i in chosen]}  # fmt: skip
    stem = f"plan-{set_name}-{TAGS.get(target, target)}"
    (out / f"{stem}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan (r2, amendment 20:20): {SET_TEXT[set_name]} on {target} (tokenizer and stored runs only; "
             "UNVERIFIED)", "",
             f"Source {counts['source']}, L{blob['layer']}, gate {gate}; items {len(items)} ({blob['entities']} bridge "
             f"entities); arms {list(names)}; reads {reads}; A = {blob['A_kind']}; |A| tokens per item "
             f"{blob['A_tokens_per_item']}; answer words per item {blob['A_words_per_item']}; items whose own answer "
             f"word has no letter token: {missing}; Δ's 25 OMP atoms in A: {blob['answer_atoms_in_omp_25']}.", "",
             "Answer tokens (most common): " + ", ".join(f"{t!r} x{n}" for t, n in blob["A_tokens_most_common"]), "",
             f"Split answer words (A keeps their first token): {blob['split_answer_words_tokens']}", ""]  # fmt: skip
    if num:
        lines += ["Number-word variants as tokens: " + "; ".join(f"{w}: {f}" for w, f in forms.items()), ""]
    for p in blob["prompts"]:
        lines += [f"## {p['key']}: {p['bridge']}; A = {p['A']}", ""]
        for k, v in p.items():
            if k.endswith(("_org", "_alt")):
                lines += [f"{k}:", "", "```", v, "```", ""]
    (out / f"{stem}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in blob.items() if k not in ("prompts", "code")}, indent=1, ensure_ascii=False))
    print("wrote", out / stem, flush=True)
    return out


# ---- GPU -----------------------------------------------------------------------------------------------------------


def rank_of(logits, t: int) -> int:
    return int((logits > logits[t]).sum()) + 1


def readout_row(it: dict, toks: dict, src: str, v: str, logits, digit_ids: list[int]) -> dict:
    """The lens readout at the edited token of one prompt (v: org / alt) from one source reader's state: top-1, its
    class (own answer / own bridge / neither), whose answer it is, the other prompt's answer or bridge, the ranks of each
    reader's own answer word (the readout check: best of its A-style tokens) and of its answer token as read (over the
    vocabulary and among the digits), and the bridge entity's rank."""
    other = "alt" if v == "org" else "org"
    top = int(logits.argmax())
    own_ans = {w: top in ids for w, ids in toks["own"][v].items()}
    is_ans, is_bridge = any(own_ans.values()), top in toks["bridge"][v]
    dl = logits[digit_ids]
    ranks, drank = {}, {}
    for w, rd in it["readers"].items():
        t = int(rd["tok_A"] if v == "org" else rd["tok_b"])
        ranks[w] = rank_of(logits, t)
        if t in digit_ids:
            drank[w] = int((dl > logits[t]).sum()) + 1
    words = {w: min((rank_of(logits, t) for t in ids), default=None) for w, ids in toks["own_word"][v].items()}
    return {"key": it["key"], "entity": it["entity"], "source": src, "variant": v, "top": top,
            "class": "answer" if is_ans else "bridge" if is_bridge else "neither", "both": bool(is_ans and is_bridge),
            "own_answer_of": [w for w, x in own_ans.items() if x],
            "other_answer": any(top in ids for ids in toks["own"][other].values()),
            "other_bridge": top in toks["bridge"][other], "answer_word_rank": words, "answer_rank": ranks,
            "answer_digit_rank": drank, "bridge_rank": min((rank_of(logits, t) for t in toks["bridge"][v]), default=None),
            "top_digit": int(digit_ids[int(dl.argmax())])}  # fmt: skip


def switch_of(set_name: str, reader: str, row: dict) -> int:
    """The set's switch: 47.3's lookup follows the change (identity / position / value); otherwise the top token is S's
    answer's first token."""
    from scripts import x47_cue as CUE

    if set_name == "cue" and reader == X.LOOKUP:
        return int(row["route"] in CUE.FOLLOW)
    return int(row["switched"])


def read_item(model, set_name: str, it: dict, layer: int, arms: dict, i: int, digits, ws) -> list[dict]:
    """Every arm (and O unedited) on the item's O prompt, each reader, with the set's own read and route."""
    import torch

    from scripts import x6_routes as R
    from scripts import x50_zach as Z
    from scripts.exp04_brew_parts import AddRows

    names = arms_of(set_name)
    rows = []
    for w, rd in it["readers"].items():
        edits = [{}] + [{layer: AddRows(arms[rd["src"]][a][i : i + 1], [rd["pos"]])} for a in names]
        logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
        if set_name in ZACH_SETS:
            cands = torch.tensor(sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}),
                                 device=model.device)  # fmt: skip
        else:
            cands = digits
        for a, lg in zip(("none", *names), logits, strict=True):
            row = X.read_row(lg, rd, cands)
            if set_name in ZACH_SETS:
                row["route"] = Z.route(row["top"], rd)
            elif set_name == "cue" and w == X.LOOKUP:
                row["route"] = R.classify(row["top"], it)
            else:
                row["route"] = None
            rows.append({"key": it["key"], "scene": it["scene"], "entity": it["entity"], "reader": w, "arm": a,
                         **row, "sw": switch_of(set_name, w, row)})  # fmt: skip
    return rows


def stored_rows(set_name: str, src: Path, layer: int) -> dict[tuple[str, str, str], dict]:
    """The source run's rows of the arms this run repeats (none, whole, no_jpp, no_jpp_rand), keyed (key, reader,
    arm), with the set's switch."""
    out = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if set_name == "e1":
            if r["rendering"] != "chat" or r["layer"] != layer:
                continue
            if r["arm"] in ("none", "whole"):
                arm = r["arm"]
            elif (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed") and r["arm"] in ("no_part", "no_rand"):
                arm = {"no_part": "no_jpp", "no_rand": "no_jpp_rand"}[r["arm"]]
            else:
                continue
            key = r["scene"]
        else:
            if set_name in ZACH_SETS and r["layer"] != layer:
                continue
            if r["arm"] not in ("none", "whole", "no_jpp", "no_jpp_rand"):
                continue
            arm, key = r["arm"], (f"{r['set']}|{r['scene']}" if set_name in ZACH_SETS else r["scene"])
        # the 9B's X0 run (24 Oct) predates the stored top token: None there, and agree_top counts what is stored
        out[(key, r["reader"], arm)] = {"switched": int(r["switched"]), "top": r.get("top"),
                                        "sw": switch_of(set_name, r["reader"], r) if set_name == "cue" else int(r["switched"])}  # fmt: skip
    return out


def excess(sw: dict[str, list[int]], arm: str, rand: str) -> float:
    """X0's excess (S_rand - S_arm) / S_whole on point estimates (nan when nothing switched under the whole change)."""
    whole = float(np.mean(sw["whole"]))
    return (float(np.mean(sw[rand])) - float(np.mean(sw[arm]))) / whole if whole > 0 else math.nan


def agreement(set_name: str, rows: list[dict], stored: dict) -> dict:
    """Arm 1 (and none / whole / its random twin) of this run against the stored run, item by item, per reader."""
    out: dict[str, Any] = {}
    readers = sorted({r["reader"] for r in rows})
    for w in readers:
        per: dict[str, Any] = {}
        sw_new: dict[str, list[int]] = {}
        sw_old: dict[str, list[int]] = {}
        for a in ("none", "whole", "no_jpp", "no_jpp_rand"):
            mine = [r for r in rows if r["reader"] == w and r["arm"] == a]
            pairs = [(r["sw"], stored.get((r["key"], w, a)), r["top"]) for r in mine]
            have = [(x, y, t) for x, y, t in pairs if y is not None]
            per[a] = {"n": len(mine), "matched": len(have), "agree_switch": sum(x == y["sw"] for x, y, _ in have),
                      "agree_top": sum(t == y["top"] for _, y, t in have if y["top"] is not None),
                      "top_stored": sum(y["top"] is not None for _, y, _ in have), "rerun": sum(x for x, _, _ in have),
                      "stored": sum(y["sw"] for _, y, _ in have)}  # fmt: skip
            sw_new[a] = [x for x, _, _ in have]
            sw_old[a] = [y["sw"] for _, y, _ in have]
        per["extra_loss_arm1"] = {"rerun": excess(sw_new, "no_jpp", "no_jpp_rand") if sw_new["whole"] else math.nan,
                                  "stored": excess(sw_old, "no_jpp", "no_jpp_rand") if sw_old["whole"] else math.nan}  # fmt: skip
        out[READER_NAME[w]] = per
    return out


def manifest(name: str, set_name: str, target: str, layer: int, src: Path) -> dict:
    from bridge_jspace.utils import git_state
    from scripts import suite_split as SUITE

    files = ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl") + (
        ("cues.json",) if set_name == "cue" else ()
    )
    return {"exp": EXP, "run": name, "test": "51.12", "set": set_name, "set_text": SET_TEXT[set_name],
            "spec": f"jobs/c3/batch51.yaml (addendum_4 and addendum_4_amendment, 51.12); "
                    f"jobs/c3/{SPEC_IDS.get(set_name, {}).get(target, 'x52_lightning_answer')}.yaml",
            "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                       for p in (SPEC, *(src / f for f in files)) if p.exists()},
            "source": src.name, "layer": layer, "arms": list(arms_of(set_name)), "arm_text": ARM_TEXT, "k": X.K_MAIN,
            "omp": "signed", "pairs": {str(k): list(v) for k, v in PAIRS.items()}
                                      | ({"3f": list(PAIR_F)} if set_name in FREQ_SETS else {}),
            "answer_directions": "JLens.vectors(L, ids), unit rows, letter tokens only (the OMP dictionary; digits never "
                                 "in A); e1 / cue: the answers' number words (e1 both readers' O / S answers; cue the "
                                 "recall's O / S legs and the lookup's a, b, c, e), each variant (as is, leading space, "
                                 "capitalised, both) kept where it is one letter token; z2: the first token of each "
                                 f"answer word and variant; span by SVD (float64, rank tol {RANK_TOL})",
            "projected_out": "(I - P_A) P_J Δ: the J++ part minus its component along span(A)",
            "frequency_control": (f"no_F = Δ - P_F Δ; per atom a of A the letter token f with |log((id_f + 1) / "
                                  f"(id_a + 1))| <= log {FREQ_BAND} (widened by x{FREQ_BAND} until non-empty) and the "
                                  "closest log J++ readout norm ||(g * W_U[t]) J_L||, ties to the lower id; unrelated: "
                                  "its key equals no answer word / A token / bridge entity / edited token key of the "
                                  f"set and (>= {MIN_RELATED} characters) neither contains nor is contained in one; "
                                  "never twice in an item" if set_name in FREQ_SETS else None),
            "read": "z2: x50_zach's (top token after the prompt, no prefill); e1 / cue: X0's chat read (top token after "
                    "the digit's space token); 47.3's lookup switch = follows the change (identity / position / value)",
            "delta": "z2: per reader from its own O / S prompts; e1 / cue: from the lookup's prompts",
            "readout": "lens readout (JLens.readout) at the edited token on O and S, from the forwards that give Δ: top-1 "
                       "over the vocabulary, class own answer / own bridge / neither; the readout check's ranks (each "
                       "reader's own answer word, best A-style variant; the bridge entity's); shares in the verdict (CPU)",
            "gate": "the source run's (asserted from its gate.json)", "rule": RULE, "as_computed": AS_COMPUTED,
            "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED, "view": VIEW_SEED},
            "order": {"items": "the source run's item order", "reads": f"per item and reader: O unedited then the "
                      f"{len(arms_of(set_name))} arms in order, batches of at most {SUITE.BATCH} rows (BJ_SUITE_BATCH)"},
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip


def freq_controls(tok, lens, layer: int, letters, items: list[dict], toks: list[dict]) -> tuple[list[list[dict]], dict]:
    """F per item (freq_match) over the letter dictionary: the J++ readout norms of every letter token (chunked; only
    the norms are kept), the set's related keys banned."""
    import torch

    lid = letters.cpu().numpy().astype(np.int64)
    with torch.no_grad():
        rn = torch.cat([lens.vectors(layer, letters[s : s + NORM_CHUNK], unit=False).norm(dim=-1).cpu()
                        for s in range(0, len(letters), NORM_CHUNK)])  # fmt: skip
    log_norm = np.log(rn.double().numpy().clip(1e-30))
    keys = [key_of(tok.decode([int(t)])) for t in lid]
    banned = related_mask(keys, related_keys(tok, items, toks))
    match = [freq_match(tk["A"], lid, log_norm, banned) for tk in toks]
    return match, {"letters": len(lid), "banned": int(banned.sum()),
                   "median_abs_log_norm_ratio": float(np.median([abs(math.log(m["norm_ratio"])) for fm in match for m in fm]))
                   if any(match) else None}  # fmt: skip


def stage_run(name: str, set_name: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    pins.check_run_name(name)
    target = pins.TARGET
    if BELOW:
        assert target in BELOW_RUNS.get(set_name, {}), f"below gate: {BELOW_RUNS}, not {set_name} / {target}"
    else:
        assert target in runs_of(set_name), f"51.12 {set_name} runs on {sorted(runs_of(set_name))}, not {target}"
    layer, src = layer_of(set_name, target), source_of(set_name, target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, set_name, target, layer, src)
    if BELOW:  # batch 52, Dan's morning queue item 1
        from scripts import x47_cue as CUE

        m |= {"question": CUE.BELOW_GATE, "below_gate": CUE.BELOW_GATE, "batch": 52, "rules_first_scored": SCORED,
              "sealed": "none (below gate, exploratory); verdict --coverage --below-gate"}  # fmt: skip
    elif set_name in MP_SETS:  # batch 53, 53.1b: no Q-line, opened when it lands
        m |= {"question": NO_PREDICTION_JSUITE, "batch": 53, "test": "53.1b", "sealed": "none (53.1b); verdict --jsuite",
              "rules_first_scored": SCORED}  # fmt: skip
    elif target in COVERAGE_RUNS.get(set_name, {}):  # batch 52: no Q-line, opened when it lands
        m |= {"question": NO_PREDICTION, "batch": 52, "sealed": "none (batch 52 coverage); verdict --coverage",
              "rules_first_scored": SCORED}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    items, gate, counts = BUILD[set_name](tok, target)
    toks = [item_tokens(tok, it) for it in items]
    tested = gate["pass"] and bool(items)
    (out / "plan.json").write_text(json.dumps(counts, indent=1) + "\n")
    (out / "gate.json").write_text(json.dumps({"source": src.name, "gate": gate, "tested": tested,
                                              "order": [it["key"] for it in items],
                                              "hub_kernels": loaded_hub_kernels()}, indent=1) + "\n")  # fmt: skip
    if not tested:
        X.write_jsonl(out / "cases.jsonl", [{**it, "tokens": tk} for it, tk in zip(items, toks, strict=True)])
        print("not tested: the source run's gate failed or no items; see gate.json", flush=True)
        return out
    ws = X.whitespace_mask(model)
    digit_list = X.digit_ids(tok)
    digits = torch.tensor(digit_list, device=dev)
    sources = sorted({rd["src"] for it in items for rd in it["readers"].values()})
    names = arms_of(set_name)
    with torch.no_grad():
        # Δ per source reader and the lens readout of O's and S's states at the edited token (the readout check's ranks)
        deltas: dict[str, list] = {s: [] for s in sources}
        readout = []
        for it, tk in zip(
            progress(items, f"51.12 {set_name}: Δ and the lens readout at L{layer} (item)"), toks, strict=False
        ):
            for s in sources:
                rd = it["readers"][s]
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][rd["pos"]].float().clone()
                     for v in ("org", "alt")}  # fmt: skip
                deltas[s].append(h["alt"] - h["org"])
                for v in ("org", "alt"):
                    lg = lens.readout(h[v][None], layer)[0].float()
                    readout.append(readout_row(it, tk, s, v, lg, digit_list))
        X.write_jsonl(out / "readout.jsonl", readout)
        letters = model.letter_token_ids()
        pos_of = {int(t): i for i, t in enumerate(letters.tolist())}
        outside = sorted({t for tk in toks for t in tk["A"]} - set(pos_of))
        assert not outside, f"A tokens outside the OMP dictionary (letter tokens): {outside[:10]}"
        fmatch, f_bases, finfo = None, None, None
        if set_name in FREQ_SETS:
            fmatch, finfo = freq_controls(tok, lens, layer, letters, items, toks)
            f_bases = [answer_basis(lens.vectors(layer, torch.tensor([x["f"] for x in fm], dtype=torch.long, device=dev)))
                       for fm in fmatch]  # fmt: skip
            print("frequency-matched control:", json.dumps(finfo), flush=True)
        X.write_jsonl(out / "cases.jsonl", [{**it, "tokens": tk, **({"F": fmatch[i]} if fmatch else {})}
                                            for i, (it, tk) in enumerate(zip(items, toks, strict=True))])  # fmt: skip
        jdic = lens.vectors(layer, letters).to(dev)
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        bases = [answer_basis(lens.vectors(layer, torch.tensor(tk["A"], dtype=torch.long, device=dev))) for tk in toks]
        arms, norms = {}, []
        for s in sources:
            x = torch.stack(deltas[s]).to(dev)
            pj = X.fit(jdic, x, X.K_MAIN, "signed").to(dev)  # the stored runs' path (arm 1)
            chosen, approx = omp_support(jdic, x, X.K_MAIN)
            assert torch.allclose(approx, pj, atol=1e-4 * float(pj.abs().max()) + 1e-6), "OMP support does not match"
            arms[s], sh = all_arms(x, pj, bases, basis, f_bases)
            assert tuple(arms[s]) == names, tuple(arms[s])
            for i, (it, tk) in enumerate(zip(items, toks, strict=True)):
                a_pos = {pos_of[t] for t in tk["A"]}
                hits = [int(letters[j]) for j in chosen[i].tolist() if j in a_pos]
                f_row = {}
                if fmatch is not None and f_bases is not None:
                    f_row = {"F_ids": [m_["f"] for m_ in fmatch[i]], "F_rank": int(f_bases[i].shape[1]),
                             "F_match": fmatch[i]}  # fmt: skip
                norms.append({"key": it["key"], "entity": it["entity"], "source": s, "norm": round(float(x[i].norm()), 4),
                              **{f"share_{k}": round(float(v[i]), 6) for k, v in sh.items()},
                              "A_tokens": len(tk["A"]), "A_rank": int(bases[i].shape[1]), "A_ids": tk["A"],
                              "A_words": tk["A_words"], "n_answer_atoms_in_25": len(hits), "answer_atoms_in_25": hits,
                              **f_row})  # fmt: skip
        del jdic
        torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        rows = []
        for i, it in enumerate(
            progress(items, f"51.12 {set_name}: {len(names)} arms + O x readers at L{layer} (item)")
        ):
            rows += read_item(model, set_name, it, layer, arms, i, digits, ws)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    agree = agreement(set_name, rows, stored_rows(set_name, src, layer))
    (out / "agreement.json").write_text(json.dumps(agree, indent=1) + "\n")
    print(json.dumps(agree, indent=1), flush=True)
    m["items"] = len(items)
    if finfo:
        m["frequency_control_summary"] = finfo
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU, sealed) -----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.12 at `rev` (x48_heads.parse_answer: 'Dan:' / 'Dan (27B):' lines and bullet
    continuations), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return H.parse_answer(text, QUESTION)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def ok(z: float | None) -> bool:
    return z is not None and not math.isnan(z)


def rule(e1: float, e2: float, e3: float, e3f: float | None = None) -> dict:
    """The rules fixed in advance on point estimates (EPS at the bars). With e3f (z2's frequency-matched control) arm 3
    is read against both controls: entity needs max(e3, e3f) <= 0.10, answer min(e3, e3f) >= 0.5 e1."""
    s3f = math.nan
    if not ok(e1) or e1 <= EPS:
        return {"label": LABELS["na"], "key": "na", "share2": math.nan, "share3": math.nan, "share3f": s3f,
                "entity": False, "answer": False}  # fmt: skip
    e3s = [e3] if e3f is None else [e3, e3f]
    good3 = all(ok(x) for x in e3s)
    s2 = e2 / e1 if ok(e2) else math.nan
    s3 = e3 / e1 if ok(e3) else math.nan
    if e3f is not None and ok(e3f):
        s3f = e3f / e1
    entity = ok(s2) and good3 and s2 >= ENTITY_KEEP - EPS and max(e3s) <= ENTITY_A_MAX + EPS
    answer = ok(s2) and good3 and s2 <= ANSWER_KEEP + EPS and min(e3s) / e1 >= ANSWER_A_MIN - EPS
    key = "entity" if entity else "answer" if answer else "mixed"
    return {"label": LABELS[key], "key": key, "share2": s2, "share3": s3, "share3f": s3f, "entity": bool(entity),
            "answer": bool(answer)}  # fmt: skip


def reader_numbers(rows: list[dict], reader: str, n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """One reader: switch rate per arm, the extra losses and shares (paired cluster-bootstrap CIs; z2 also arm 3
    against its frequency-matched control, "3f"), the rule's label, X0's validity bar beside."""
    mine = [r for r in rows if r["reader"] == reader]
    by = {(r["key"], r["arm"]): r for r in mine}
    keys = list(dict.fromkeys(r["key"] for r in mine if r["arm"] == "whole"))
    arms = list(dict.fromkeys(r["arm"] for r in mine))
    ent = {r["key"]: r["entity"] for r in rows}
    ents = [ent[k] for k in keys]
    sw = {a: [int(by[(k, a)]["sw"]) for k in keys] for a in arms}
    rr = X.resampled_rates(sw, ents, n_boot, seed)
    pt = {a: float(np.mean(v)) for a, v in sw.items()}
    pairs = {**PAIRS, **({"3f": PAIR_F} if F_ARM in sw else {})}
    e_pt, e_dr = {}, {}
    for k, (arm, rand) in pairs.items():
        e_pt[k] = excess(sw, arm, rand)
        e_dr[k] = X.dependence(rr["whole"], rr[arm]) - X.dependence(rr["whole"], rr[rand])
    with np.errstate(divide="ignore", invalid="ignore"):
        s2, s3 = e_dr[2] / e_dr[1], e_dr[3] / e_dr[1]
        s3f = e_dr["3f"] / e_dr[1] if "3f" in e_dr else None
    r = rule(e_pt[1], e_pt[2], e_pt[3], e_pt.get("3f"))
    return {"n": len(keys), "entities": len(set(ents)), "rate": {a: [pt[a], *X.interval(rr[a])] for a in sw},
            "hits": {a: int(sum(v)) for a, v in sw.items()},
            "extra": {str(k): [e_pt[k], *X.interval(e_dr[k])] for k in pairs},
            "share2": [r["share2"], *X.interval(s2)], "share3": [r["share3"], *X.interval(s3)],
            "share3f": [r["share3f"], *X.interval(s3f)] if s3f is not None else None,
            "valid": pt["whole"] >= X.VALID_S and sum(sw["whole"]) >= X.VALID_N, "label": r["label"], "key": r["key"],
            "clauses": {"entity": r["entity"], "answer": r["answer"]}}  # fmt: skip


def share_ci(values: list[int], ents: list[str], n_boot: int) -> list[float]:
    if not values:
        return [math.nan, math.nan, math.nan]
    rr = X.resampled_rates({"s": values}, ents, n_boot)["s"]
    return [float(np.mean(values)), *X.interval(rr)]


def readout_check(readout: list[dict], reader: str, n_boot: int) -> dict:
    """The amendment's readout check for one reader: on its state at the edited token (z2: its own; e1 / cue: the
    lookup's), the rank of its own answer word on O and on S against the bridge entity's; shares of items with the
    word in the top 10 / 50 (per prompt and on either), the share not read (rank > 50 on both) and the case."""
    srcs = {r["source"] for r in readout}
    src = reader if reader in srcs else X.LOOKUP
    by = {(r["key"], r["variant"]): r for r in readout if r["source"] == src}
    keys = list(dict.fromkeys(k for k, _ in by))
    ent = {k: r["entity"] for (k, _), r in by.items()}

    def rank(k: str, v: str) -> int | None:
        r = by.get((k, v))
        return None if r is None else r.get("answer_word_rank", {}).get(reader)

    pairs = {k: (rank(k, "org"), rank(k, "alt")) for k in keys}
    known = {k: (o, s) for k, (o, s) in pairs.items() if o is not None and s is not None}
    have = list(known)
    ents = [ent[k] for k in have]
    best = [min(o, s) for o, s in known.values()]
    out: dict[str, Any] = {"source": src, "n": len(have), "missing": len(keys) - len(have)}
    for j, (v, nm) in enumerate((("org", "O"), ("alt", "S"))):
        rk = [known[k][j] for k in have]
        br = [by[(k, v)]["bridge_rank"] for k in have]
        for t in TOP_K:
            out[f"top{t}_{nm}"] = share_ci([int(x <= t) for x in rk], ents, n_boot)
        out[f"median_rank_{nm}"] = float(np.median(rk)) if rk else math.nan
        out[f"median_bridge_rank_{nm}"] = float(np.median([b for b in br if b is not None])) if any(
            b is not None for b in br) else math.nan  # fmt: skip
        out[f"above_bridge_{nm}"] = share_ci([int(b is not None and x < b) for x, b in zip(rk, br, strict=True)], ents,
                                             n_boot)  # fmt: skip
    for t in TOP_K:
        out[f"top{t}_either"] = share_ci([int(b <= t) for b in best], ents, n_boot)
    out["not_read"] = share_ci([int(b > NOT_READ_RANK) for b in best], ents, n_boot)
    out["case"] = "not_read" if have and out["not_read"][0] >= NOT_READ_SHARE - EPS else "arms"
    return out


def readout_numbers(readout: list[dict], n_boot: int) -> dict:
    """Per source reader and prompt (O / S): the shares of items whose lens top-1 at the edited token is the own answer,
    the own bridge entity or neither; per reader's own answer separately; the other prompt's answer / bridge; the
    median rank of each reader's answer token and answer word (and among the digits, the share where it is the top
    digit)."""
    out: dict[str, Any] = {}
    for s in sorted({r["source"] for r in readout}):
        for v in ("org", "alt"):
            rs = [r for r in readout if r["source"] == s and r["variant"] == v]
            ents = [r["entity"] for r in rs]
            cell: dict[str, Any] = {
                c: share_ci([int(r["class"] == c) for r in rs], ents, n_boot) for c in ("answer", "bridge", "neither")
            }
            readers = sorted({w for r in rs for w in r["answer_rank"]})
            cell |= {f"top1_is_{READER_NAME[w]}_answer": share_ci([int(w in r["own_answer_of"]) for r in rs], ents, n_boot)
                     for w in readers}  # fmt: skip
            cell["other_prompt_answer"] = share_ci([int(r["other_answer"]) for r in rs], ents, n_boot)
            cell["other_prompt_bridge"] = share_ci([int(r["other_bridge"]) for r in rs], ents, n_boot)
            cell["median_answer_rank"] = {
                READER_NAME[w]: float(np.median([r["answer_rank"][w] for r in rs])) for w in readers
            }
            cell["median_answer_word_rank"] = {
                READER_NAME[w]: float(np.median(ws)) if (ws := [r["answer_word_rank"][w] for r in rs
                                                               if r.get("answer_word_rank", {}).get(w) is not None])
                else math.nan for w in readers
            }  # fmt: skip
            dig = {w: [int(r["answer_digit_rank"][w] == 1) for r in rs if w in r["answer_digit_rank"]] for w in readers}
            cell["top_digit_is_answer"] = {READER_NAME[w]: share_ci(d, [r["entity"] for r in rs if w in r["answer_digit_rank"]], n_boot)
                                           for w, d in dig.items() if d}  # fmt: skip
            cell["n"] = len(rs)
            out[f"{READER_NAME.get(s, s)}'s prompt, {'O' if v == 'org' else 'S'}"] = cell
    return out


def atom_numbers(norms: list[dict]) -> dict:
    """Per source reader: |A| (tokens, rank) per item, how many of Δ's 25 OMP atoms are in A, the median shares of
    ||Δ||^2 (A, J++ part, ...), and z2's frequency match (id and readout-norm ratios)."""
    out = {}
    for s in sorted({n["source"] for n in norms}):
        ns = [n for n in norms if n["source"] == s]
        cell = {"A_tokens": size_summary([n["A_tokens"] for n in ns]), "A_rank": size_summary([n["A_rank"] for n in ns]),
                "answer_atoms_in_25": size_summary([n["n_answer_atoms_in_25"] for n in ns]),
                "items_with_an_answer_atom_in_25": sum(n["n_answer_atoms_in_25"] > 0 for n in ns),
                "share_median": {k: float(np.median([n[k] for n in ns])) for k in ns[0] if k.startswith("share_")}}  # fmt: skip
        fm = [x for n in ns for x in n.get("F_match", [])]
        if fm:
            cell["F_match"] = {"pairs": len(fm), "median_id_ratio": float(np.median([x["id_ratio"] for x in fm])),
                               "median_norm_ratio": float(np.median([x["norm_ratio"] for x in fm])),
                               "widened": sum(x["band"] > FREQ_BAND for x in fm)}  # fmt: skip
        out[READER_NAME.get(s, s)] = cell
    return out


def model_result(set_name: str, target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"set": set_name, "target": target, "run": run, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is not {target}'s"
    assert m["set"] == set_name, f"{run} is not a {set_name} run"
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    if not gate.get("tested") or not rows:
        return {"set": set_name, "target": target, "run": run, "status": "not tested", "gate": gate.get("gate"),
                "why": "the source gate failed, no items, or the run did not finish"}  # fmt: skip
    readout = X.read_jsonl(src / "readout.jsonl")
    readers = {}
    for w in dict.fromkeys(r["reader"] for r in rows):
        r = reader_numbers(rows, w, n_boot)
        r["check"] = readout_check(readout, w, n_boot)
        r["arm_label"], r["arm_key"] = r["label"], r["key"]
        if r["check"]["case"] == "not_read":
            r["label"], r["key"] = LABELS["not_read"], "not_read"
        readers[READER_NAME[w]] = r
    agree = json.loads((src / "agreement.json").read_text()) if (src / "agreement.json").exists() else {}
    return {"set": set_name, "target": target, "run": run, "status": "tested", "layer": m["layer"],
            "source": m["source"], "gate": gate.get("gate"), "readers": readers,
            "readout": readout_numbers(readout, n_boot), "atoms": atom_numbers(X.read_jsonl(src / "norms.jsonl")),
            "agreement": agree}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None or not ok(v[0]) else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


DECISIVE = {"z2": ("lookup", "recall"), "e1": ("recall",), "cue": ("lookup", "recall"), "z1k": ("lookup", "recall"),
            "z1p": ("lookup", "recall"), "z2p": ("lookup", "recall")}  # fmt: skip


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.12: is it the bridge or the answer that moves through the lens? (r2, amendment 20:20; UNVERIFIED)", "",
             f"Batch 51, test 51.12 (jobs/c3/batch51.yaml addendum_4 and addendum_4_amendment; {QUESTION}, Dan: "
             f"{answer}). Cluster bootstrap over the bridge entity ({n_boot}, seed {X.BOOT_SEED}), paired across arms.",
             "", f"Rule (fixed in advance): {RULE}", "", f"As computed: {AS_COMPUTED}", "",
             "Which case held, per cell: first the readout check (the reader's own answer word at the edited token at "
             "L; 'not read' = rank > 50 on both O and S), then the arms.", "",
             "| set | model | reader | n | answer word top-50 O | top-50 S | not read | case | e1 (no J++) | e2 (no J++, "
             "A kept) | e3 (no A vs random) | e3f (no A vs freq.) | e2/e1 | e3/e1 | verdict | decisive |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['set']} | {m['target']} | | {m['status']} ({m['why']}) |" + " |" * 12)
            continue
        for w, r in m["readers"].items():
            c = r["check"]
            verdict = r["label"] + (f" ({c['not_read'][0]:.0%} of {c['n']} items; arms beside: {r['arm_label']})"
                                    if r["key"] == "not_read" else "")  # fmt: skip
            lines.append(f"| {m['set']} | {m['target']} | {w} | {r['n']} | {fmt(c['top50_O'])} | {fmt(c['top50_S'])} | "
                         f"{fmt(c['not_read'])} | {c['case']} | {fmt(r['extra']['1'])} | {fmt(r['extra']['2'])} | "
                         f"{fmt(r['extra']['3'])} | {fmt(r['extra'].get('3f'))} | {fmt(r['share2'])} | "
                         f"{fmt(r['share3'])} | **{verdict}** | {'yes' if w in DECISIVE[m['set']] else 'beside'} |")  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        arms = list(next(iter(m["readers"].values()))["rate"])
        lines += ["", f"## {m['set']} on {m['target']} ({m['run']}, L{m['layer']}, source {m['source']})", "",
                  f"Source gate: {m['gate']}.", "", "Readout check (the answer word at the edited token):", ""]  # fmt: skip
        for w, r in m["readers"].items():
            c = r["check"]
            lines.append(f"- {w} (state: {READER_NAME.get(c['source'], c['source'])}'s prompts; n {c['n']}, no letter "
                         f"token for the word {c['missing']}): top-10 O {fmt(c['top10_O'])}, S {fmt(c['top10_S'])}, "
                         f"either {fmt(c['top10_either'])}; top-50 O {fmt(c['top50_O'])}, S {fmt(c['top50_S'])}, either "
                         f"{fmt(c['top50_either'])}; median rank O {c['median_rank_O']}, S {c['median_rank_S']} vs the "
                         f"bridge entity's O {c['median_bridge_rank_O']}, S {c['median_bridge_rank_S']}; above the "
                         f"bridge O {fmt(c['above_bridge_O'])}, S {fmt(c['above_bridge_S'])}; not read "
                         f"{fmt(c['not_read'])} -> case {c['case']}")  # fmt: skip
        lines += ["", "| arm | " + " | ".join(m["readers"]) + " |", "|---|" + "---|" * len(m["readers"])]
        for a in arms:
            lines.append(f"| {a} | " + " | ".join(fmt(r["rate"][a]) for r in m["readers"].values()) + " |")
        for w, r in m["readers"].items():
            lines.append(f"- {w}: X0's validity bar {r['valid']}; whole {r['hits']['whole']} of {r['n']}; arm rule: "
                         f"{r['arm_label']}; e3f/e1 {fmt(r['share3f'])}")  # fmt: skip
        lines += ["", "Answer directions and OMP atoms (per item):", ""]
        for s, a in m["atoms"].items():
            lines.append(f"- Δ from the {s}'s prompts: |A| tokens {a['A_tokens']}; rank {a['A_rank']}; answer atoms "
                         f"among the 25: {a['answer_atoms_in_25']} ({a['items_with_an_answer_atom_in_25']} items with "
                         f"at least one); median shares of ||Δ||^2 "
                         f"{ {k: round(v, 5) for k, v in a['share_median'].items()} }"
                         + (f"; frequency match {a['F_match']}" if "F_match" in a else ""))  # fmt: skip
        lines += ["", "Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):", "",
                  "| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | "
                  "top digit = reader's answer |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for k, c in m["readout"].items():
            per = "; ".join(f"{kk[8:]}: {fmt(v)}" for kk, v in c.items() if kk.startswith("top1_is_"))
            dig = "; ".join(f"{w}: {fmt(v)}" for w, v in c["top_digit_is_answer"].items()) or "-"
            lines.append(f"| {k} | {c['n']} | {fmt(c['answer'])} | {fmt(c['bridge'])} | {fmt(c['neither'])} | {per} | "
                         f"{fmt(c['other_prompt_answer'])} | {dig} |")  # fmt: skip
        lines += ["", "Arm 1 against the stored run, item by item (agreement.json):", ""]
        for w, per in m["agreement"].items():
            el = per.get("extra_loss_arm1", {})
            lines.append(f"- {w}: " + "; ".join(f"{a} {v['agree_switch']}/{v['matched']} agree (rerun {v['rerun']}, "
                                                f"stored {v['stored']})" for a, v in per.items() if a != "extra_loss_arm1")
                         + f"; arm 1's extra loss rerun {el.get('rerun')} vs stored {el.get('stored')}")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def all_runs(sets: tuple[str, ...] = SETS, coverage: bool = False) -> list[tuple[str, str, str]]:
    runs = BELOW_RUNS if BELOW else COVERAGE_RUNS if coverage else RUNS
    return [(s, t, r) for s in sets for t, r in runs.get(s, {}).items()]


def jsuite_runs() -> list[tuple[str, str, str]]:
    """53.1b's cells: PP / PM (the z1p runs) and MP / MM (the z2p runs) on the 9B and the 27B."""
    return [(s, t, COVERAGE_RUNS[s][t]) for s in JSUITE["sets"] for t in JSUITE["targets"]]


def jsuite_cells(models: list[dict]) -> dict[str, dict[str, str]]:
    """Per model, each of 53.1b's four cells' 51.12 label (with n), or why it has none."""
    by = {(m["set"], m["target"]): m for m in models}
    out: dict[str, dict[str, str]] = {}
    for t in JSUITE["targets"]:
        out[t] = {}
        for s in JSUITE["sets"]:
            m = by.get((s, t))
            for w, code in JSUITE["cells"][s].items():
                if m is None or m["status"] != "tested":
                    out[t][code] = m["status"] if m else "missing"
                else:
                    r = m["readers"][READER_NAME[w]]
                    out[t][code] = f"{r['label']} (n {r['n']})"
    return out


def jsuite_lines(cells: dict[str, dict[str, str]]) -> list[str]:
    lines = ["## 53.1b: PP vs MP on Zach's passages (51.12's label per cell; the recall beside)", "",
             "PP = P start (the passage names the bridge), P final (the made-up value stated); MP = M start (the "
             "question describes the bridge), P final. PM / MM = the same passages' recall (M final).", "",
             "| model | PP (lookup) | MP (lookup) | PM (recall) | MM (recall) |", "|---|---|---|---|---|"]  # fmt: skip
    for t, c in cells.items():
        lines.append(f"| {t} | {c['PP']} | {c['MP']} | {c['PM']} | {c['MM']} |")
    return [*lines, ""]


def stage_verdict(n_boot: int = X.N_BOOT, sets: tuple[str, ...] = SETS, coverage: bool = False,
                  jsuite: bool = False) -> Path:  # fmt: skip
    """51.12's verdict (sealed until Q51.12), or with coverage (batch 52) the same rules on COVERAGE_RUNS, no seal
    guard, "no prediction" in place of Dan's answer, written to x52_answer-<UTC>/; with jsuite (batch 53, 53.1b) the
    same rules on PP / PM and MP / MM (9B, 27B), written to x53_jsuite-<UTC>/."""
    if BELOW:
        from scripts import x47_cue as CUE
    if jsuite:
        answer = f"{NO_PREDICTION_JSUITE} (rules first scored in {SCORED})"
        models = [model_result(s, t, r, n_boot) for s, t, r in jsuite_runs()]
        stem = "x53_jsuite"
    else:
        answer = (f"{CUE.BELOW_GATE if BELOW else NO_PREDICTION} (rules first scored in {SCORED})" if coverage
                  else unsealed())  # fmt: skip
        models = [model_result(s, t, r, n_boot) for s, t, r in all_runs(sets, coverage)]
        stem = "x52_answer_below" if BELOW else "x52_answer" if coverage else "x51_12"
    out = RESULTS / f"{stem}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if jsuite:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 53, 53.1b, ")
        cells = jsuite_cells(models)
        lines[3:3] = ["", *jsuite_lines(cells)]
    elif coverage:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ")
    per = {f"{m['set']}|{m['target']}|{w}": r["label"] for m in models if m["status"] == "tested"
           for w, r in m["readers"].items()}  # fmt: skip
    blob = {
        "dan": answer,
        "rule": RULE,
        "as_computed": AS_COMPUTED,
        "labels": LABELS,
        "models": models,
        "per_cell": per,
        **({"jsuite_cells": cells, "status": "UNVERIFIED"} if jsuite else {}),
    }
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(set_name: str, target: str, run: str, decode, k_prompts: int = N_PROMPTS, k_rows: int = N_ROWS,
               seed: int = VIEW_SEED) -> list[str]:  # fmt: skip
    """The verify pack of one run: k_prompts items' prompts as read (O and S per reader, the edited token marked) and
    k_rows random rows per arm (seed 0)."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    rows = X.read_jsonl(src / "outcomes.jsonl")
    lines = [f"## {SET_TEXT[set_name]}: {target}, {run}", "",
             f"### {min(k_prompts, len(items))} rendered items of {len(items)} (seed {seed})", ""]  # fmt: skip
    for i in sorted(random.Random(seed).sample(range(len(items)), min(k_prompts, len(items)))):
        it = items[i]
        f = f"; F = {[decode([x['f']]) for x in it['F']]}" if it.get("F") else ""
        lines += [f"#### {it['key']}: {it['entity']} -> {it['cf_entity']}; A = {[decode([t]) for t in it['tokens']['A']]}"
                  f"{f}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}**: O's answer {rd['answer']}, S's answer {rd['cf_answer']}", ""]
            for v in ("org", "alt"):
                lines += [f"{'O' if v == 'org' else 'S'}:", "", "```", mark(decode, rd["ids"][v] + rd["suffix"], rd["pos"]),
                          "```", ""]  # fmt: skip
    for a in ("none", *arms_of(set_name)):
        mine = [r for r in rows if r["arm"] == a]
        pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
        lines += [f"### {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                  "| item | reader | top token | route | switch |", "|---|---|---|---|---|"]  # fmt: skip
        lines += [f"| {mine[j]['key']} | {READER_NAME[mine[j]['reader']]} | {decode([mine[j]['top']])!r} | "
                  f"{mine[j]['route']} | {mine[j]['sw']} |" for j in pick]  # fmt: skip
        lines.append("")
    return lines


def stage_view(sets: tuple[str, ...] = SETS, decode_for=None) -> Path:
    from scripts import x47_atoms as A

    unsealed()
    out = RESULTS / f"x51_12-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.12 view (verify pack): prompts exactly as the model reads them; ⟦...⟧ the edited token, where each "
             "arm adds its vector at L. UNVERIFIED.", ""]  # fmt: skip
    for s, t, r in all_runs(sets):
        gate = RESULTS / r / "gate.json"
        if not gate.exists() or not json.loads(gate.read_text()).get("tested"):
            lines += [f"## {s} {t}: {r} not here or not tested", ""]
            continue
        lines += view_lines(s, t, r, (decode_for or A.default_decode)(t))
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--set", choices=ALL_SETS, help="plan / run: the set; verdict / view: one set (default all)")
    ap.add_argument("--name", help="run: the run name (results/x51_answer/<name>/)")
    ap.add_argument("--plan-dir", help="plan: the folder to write into (default a new plan-<UTC>/)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52's coverage runs ('{NO_PREDICTION}')")
    ap.add_argument("--below-gate", action="store_true",
                    help="run / verdict (with --coverage): batch 52, the cue set on Lightning below 47.3's gate (exploratory)")  # fmt: skip
    ap.add_argument("--jsuite", action="store_true",
                    help="verdict: batch 53, 53.1b (PP / PM from z1p, MP / MM from z2p; 9B and 27B) -> x53_jsuite-<UTC>/")  # fmt: skip
    a = ap.parse_args()
    global BELOW
    BELOW = a.below_gate
    if a.stage == "plan":
        assert a.set, "plan needs --set"
        stage_plan(a.set, a.plan_dir)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        assert a.set, "run needs --set"
        stage_run(a.name, a.set)
    elif a.stage == "view":
        stage_view((a.set,) if a.set else SETS)
    else:
        stage_verdict(a.n_boot, (a.set,) if a.set else SETS, a.coverage, a.jsuite)


if __name__ == "__main__":
    main()
