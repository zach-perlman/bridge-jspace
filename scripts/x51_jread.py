"""x51_jread (batch 51, test 51.10, addendum 2; jobs/c3/batch51.yaml `addendum_2:`, design and rules fixed in advance;
Q51.10 in predictions/2026-10-28_dan.md): does the intermediate pass through J-space? Read / write statistics per
position, per reader.

Items: the main test (x0_necessity, alt cf: two people swap their picks; chat), each model's X0 run at L (12 / 32 / 26),
rebuilt by x47_cumulative.select (x49_gain.SOURCES; the source run's gate, 0.80 per reader on O unedited and >= 150
eligible, asserted). The read statistics use every item of the run (all groups; the probes need the rows) and are
decided on the locker-first items (x45m.group_of, 49.1's items: x49_gain.select_items); the write and remove arms run on
the locker-first items only. Both readers (lookup PP, recall PM), O and S prompts as read (X0's chat read: the prompt
with a digit's space token appended).

Positions, per reader's prompt and per variant (O / S): P1 the bridge word (X0's position; the readers' prompts agree
through it); P2 the question's "pick" token (the last token of "pick" in "<Name>'s pick"); P3 the last token, the
read's appended space token (whose next token is the answer). The question is identical in O and S: P2 and P3 in S
are P2 and P3 in O counted from the end (asserted token by token).

Layers: the 9B every 2nd layer L2-L30 (the brief's "L2-L38" runs past the 9B's 32 layers, 0-31: cut at L30); the 27B
and Muse every 4th layer from L4 (to L60 / L48) plus L and L +- 2 (L = 32 / 26). Coverage (no prediction): Lightning
on Muse's grid around its committed L14 (batch 52); the 122B (48 blocks) every 4th layer from L4 to L44 plus L and
L +- 2 (L = 33, X0's layer: the 27B's relative depth carried over), items from its X0 main-test run (batch 53, Dan 12:20).

Run (GPU, sealed: no statistic is printed, no label written):
  1. cache: one forward of each prompt (item x reader x O/S) recording every layer: the block outputs at P1 / P2 / P3
     at the cached layers (fp16 in states.npz, gitignored); at P3 the plain logit lens (model.unembed of the block
     output) at every layer: the top token and the ranks of O's and S's answers; the clean read's top-10 tokens (his
     protected rows, x47_twodefs.protected_rows).
  2. lens: per cached layer, his read directions (x49_ladder.band_dictionaries: ablate.LensDictionary over W_g =
     W_U[letters] x gain, J_l of the J++ lens; letter tokens): the rank of the bridge entity's token (O's on O, S's on S;
     the other entity beside) among the letter tokens by lens logit; the same over the whole vocabulary
     (JLens.readout) with its top token; and the projection of the state onto the span of his top-10 directions there
     (ablate.top_span_removal, never a protected row): the "through the lens" input (states.npz).
  3. the read peak for the removal (no label): per reader, the cached layer before the answer digit's layer with the
     highest through-the-lens probe accuracy at P3 on the locker-first rows (the read stage's code; peak.json).
  4. write, at P1 / P2 / P3 one layer at a time, on O, each arm's vector added at that position and layer (AddRows):
       swap       his J-part swap: h_O - J10(h_O) + J10(h_S) (jswap's swap: each state's own top-10 span, O's protected
                  rows for both, top_span_removal)
       swap_rand  a random part of Δ = h_S - h_O at the swap's share ||J10(h_S) - J10(h_O)||^2 / ||Δ||^2 (capped at 1;
                  the swap's decisive twin, as instructed)
       swap_rot   beside: his own control, jswap's swap_rot (the swap's change turned by the layer's random rotation,
                  seed 888 + layer: the same size even where the swap's change is larger than Δ)
       jpp1/jpp2 the J++ part of the change at gain 1 / 2: X0's 25-atom signed OMP part of Δ (x49_gain.lens_parts)
       rand1/2    X0's random part of Δ at the J++ part's share, gain 1 / 2 (random basis seed 888 + layer)
       whole      the whole state patched: h_O <- h_S (Δ added; the upper bound at that position and layer)
     read by both readers (switch = the top token is S's answer's first token; "changed to another digit" = the top
     token is a digit other than O's and S's answers), plus O unedited; plain-text loss at P1 and P2 (-log p(O's next
     token) at the position, O's prompt cut after it); P3 has no plain-text next token (its next token is the answer).
  5. remove, at P3 only, on O: his knock-out (top-10 per layer, at P3 only, every layer of the band peak +- 2) and the
     J++-25 removal at the peak layer (the state minus its projection on the span of Δ's 25 OMP atoms at P3, 47.5's
     zeroing), each beside a random subspace of the same share (seed 888 + layer); kept = the top token is O's answer.
Read (CPU, on the cached states; not sealed: statistics only, no label): per reader, position and layer the lens top-1
/ top-5 shares, three probes for the bridge entity (one-hot ridge, x0_probe.ridge; one probe per family = domain,
classes = that family's entities, chance = 1 / classes; 5 folds by scene, a scene's O and S rows together, inner CV
over the training folds for the penalty) on the projection onto his top-10 span (through the lens), the full residual
(readable at all) and the residual minus the projection (outside the lens), out of fold on every row, accuracy on the
locker-first rows (all rows beside); the answer digit's layer at P3 (per item the layer from which O's answer is the
logit lens's top token through the last layer; per reader the lower median over the locker-first items).

Rules (fixed in advance, per reader and model; point estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs
over bridge items, 10,000, seed 0, beside):
  read        "in J-space at the last token" (read): through-the-lens probe >= 0.8 and lens top-5 >= 0.5 at some
              layer before the answer digit's layer, while the full-residual probe >= 0.9 there
  write       "writable through J-space": at the read peak (the layer before the answer layer with the highest
              through-the-lens accuracy), his swap or the J++ part (gain <= 2) switches >= 0.5 of what the whole-state
              patch switches at that layer, with that arm's random part <= 0.10 (the whole patch switching nothing: no;
              the swap's twin swap_rand; with swap_rot as its twin reported beside)
  (a) read and write; (b) "readable, not used": read, no write; (c) "routes around J-space": through-the-lens < 0.5
  at every layer before the answer while the full residual >= 0.9 at some layer before it, and no write; (d) "not
  represented at the last token at all": the full residual < 0.5 at every layer before the answer. Same clauses at
  P2 (the answer layer is P3's). P1: the swap for both readers beside 49.1's J(α,0).

SEALED: run and read write no label; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's Q51.10
answer at HEAD.

uv run python scripts/x51_jread.py plan                                                   # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_jread.py run --name qwen35_9b_x51_10       # GPU (sealed)
uv run python scripts/x51_jread.py read --name qwen35_9b_x51_10                           # CPU, cached states
uv run python scripts/x51_jread.py verdict                                                 # CPU, after Dan's Q51.10
uv run python scripts/x51_jread.py view                                                    # CPU, after Dan's Q51.10
"""

from __future__ import annotations

import argparse
import collections
import json
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
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x0_probe as PR
from scripts import x48_heads as H
from scripts import x49_gain as G

EXP = "x51_jread"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.10"
MODELS = G.MODELS
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_10", "qwen3.6-27b": "x51_10_27b", "muse-glimmer-30b": "muse30_x51_10"}
STATES_FILE = "states.npz"
N_LAYERS = {"qwen3.5-9b": 32, "qwen3.6-27b": 64, "muse-glimmer-30b": 52, "nemotron-3.5-lightning": 52,
            "qwen3.5-122b-a10b": 48}  # fmt: skip
LAYERS = {
    "qwen3.5-9b": tuple(range(2, 31, 2)),  # every 2nd from L2; the brief's L38 is past the 9B's last layer (31)
    "qwen3.6-27b": tuple(sorted({*range(4, 61, 4), 30, 32, 34})),  # every 4th from L4, plus L and L +- 2 (L = 32)
    "muse-glimmer-30b": tuple(sorted({*range(4, 49, 4), 24, 26, 28})),  # every 4th from L4, plus L and L +- 2 (L = 26)
    # batch 52 C coverage: Muse's 52-block grid with Lightning's committed L = 14 (every 4th from L4, plus L and L +- 2)
    "nemotron-3.5-lightning": tuple(sorted({*range(4, 49, 4), 12, 14, 16})),
    # batch 53 coverage (Dan 12:20, fallback_1220): the 27B / Muse grid on 48 blocks (every 4th from L4 to the last
    # multiple of 4 four blocks before the end, as L60 of 64 and L48 of 52), plus L and L +- 2 (L = 33, X0's layer)
    "qwen3.5-122b-a10b": tuple(sorted({*range(4, 45, 4), 31, 33, 35})),
}
# batch 52 (Lightning) and batch 53 (the 122B): verdict --coverage; RUNS unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_jread", "qwen3.5-122b-a10b": "qwen35_122b_x51_10"}
COVERAGE_BATCH = {"nemotron-3.5-lightning": 52, "qwen3.5-122b-a10b": 53}
# the main test's X0 run per model (x49_gain's SOURCES), plus the 122B's: its X0 run at L33 (chat, alt cf; the first
# attempt, qwen35_122b_x0_necessity, stopped before its outcomes; r2 is the complete one)
SOURCES = {**G.SOURCES, "qwen3.5-122b-a10b": "qwen35_122b_x0_necessity_r2"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_jread/x51_10-20261028T190608Z"  # 51.10's rules first scored
POS = ("P1", "P2", "P3")
POS_TEXT = {"P1": "the bridge word", "P2": "the question's \"pick\" token", "P3": "the last token (the read's appended "
            "space token, before the answer)"}  # fmt: skip
VARIANTS = ("org", "alt")
READER_NAME = G.READER_NAME
RIDX = {X.LOOKUP: 0, X.RECALL: 1}
WRITE_ARMS = ("swap", "swap_rand", "swap_rot", "jpp1", "rand1", "jpp2", "rand2", "whole")
TWIN = {"swap": "swap_rand", "jpp1": "rand1", "jpp2": "rand2"}  # decisive
TWIN_ROT = {"swap": "swap_rot", "jpp1": "rand1", "jpp2": "rand2"}  # beside: his own same-size control for the swap
NONE = "none"
REMOVE_ARMS = ("none", "ko", "ko_rand", "jrm", "jrm_rand")
ARM_TEXT = {
    "swap": "his J-part swap: h_O - J10(h_O) + J10(h_S), J10 the projection on the state's own top-10 lens directions "
            "(O's protected rows; jswap's swap)",
    "swap_rand": "a random part of Δ = h_S - h_O at the swap's share of ||Δ||^2 (capped at 1; seed 888 + layer)",
    "swap_rot": "his own control (jswap's swap_rot): h_O + (J10(h_S) - J10(h_O)) R^T, R the layer's random orthogonal "
                "matrix (seed 888 + layer): the swap's change at its own size in a random direction",
    "jpp1": "h_O + P_J Δ, the change's 25-atom signed OMP J++ part (49.1's J(1,0))",
    "rand1": "h_O + R Δ, X0's random part of Δ at P_J Δ's share (49.1's R(1,0))",
    "jpp2": "h_O + 2 P_J Δ (49.1's J(2,0))", "rand2": "h_O + 2 R Δ (49.1's R(2,0))",
    "whole": "h_O <- h_S (Δ added; the whole state patched)",
    "ko": "his knock-out at P3: the top-10 lens span removed at every layer of the band (peak +- 2)",
    "ko_rand": "a random subspace part of the share his removal takes, at P3, every band layer",
    "jrm": "at the peak layer, P3's state minus its projection on Δ's 25 OMP atoms there (47.5's zeroing)",
    "jrm_rand": "a random subspace of the same share of ||h_O||^2 (47.5's random)",
}  # fmt: skip
K = X.K_MAIN  # 25
K_TOP = 10
BAND_HALF = 2
INPUTS = ("thru", "full", "out")
INPUT_TEXT = {"thru": "the projection on his top-10 span (through the lens)", "full": "the full residual (readable at "
              "all)", "out": "the residual minus that projection (outside the lens)"}  # fmt: skip
K_OUTER = 5
RELS = PR.RELS
THRU_MIN, TOP5_MIN, FULL_MIN = 0.8, 0.5, 0.9  # read
WRITE_RATIO, RAND_MAX = 0.5, 0.10  # write
THRU_FAIL, FULL_FAIL = 0.5, 0.5  # (c), (d)
EPS = G.EPS
N_PROMPTS = 5
N_ROWS = 10
CHUNK = 384  # lens rows per chunk (32 items x 12 rows)
LABELS = {"a": "(a) in J-space (read and write)", "b": "(b) readable, not used", "c": "(c) routes around J-space",
          "d": "(d) not represented at this position"}  # fmt: skip
RULE = {
    "read": "through-the-lens probe >= 0.8 and lens top-5 >= 0.5 at some layer before the answer digit's layer, while "
            "the full-residual probe >= 0.9 there",
    "write": "at the layer of the read peak, his swap or the J++ part of the change (gain <= 2) switches >= 0.5 of what "
             "the whole-state patch switches at that layer, with the random part <= 0.10",
    "a": "in J-space: read holds and write holds", "b": "readable, not used: read holds, write fails",
    "c": "routes around J-space: through-the-lens < 0.5 at every layer before the answer while the full residual >= "
         "0.9 at some layer, and write fails",
    "d": "not represented: the full-residual probe < 0.5 at every layer before the answer",
}  # fmt: skip


class Dropped(ValueError):
    """An item whose positions cannot be placed (counted in the plan)."""


# ---- positions (tokenizer only, CPU-testable) ----------------------------------------------------------------------


def pick_position(text: str, question: str, offsets: list) -> int:
    """The question's "pick" token: the last token overlapping "pick" in the question's last "'s pick"."""
    from scripts import statement_positions as SP

    if question not in text:
        raise Dropped("the question is not in the prompt")
    q0 = text.rindex(question)
    hits = list(re.finditer(r"'s (pick)\b", question))
    if not hits:
        raise Dropped('no "\'s pick" in the question')
    toks = SP.tokens_in([tuple(o) for o in offsets], q0 + hits[-1].start(1), q0 + hits[-1].end(1))
    if not toks:
        raise Dropped('no token over the question\'s "pick"')
    return toks[-1]


def tail_position(org: list[int], alt: list[int], p: int) -> int:
    """A position of O's prompt counted from the end in S's; O and S must agree from it to the end."""
    tail = len(org) - p
    if tail > len(alt) or alt[len(alt) - tail :] != org[p:]:
        raise Dropped("O and S differ after the question's pick token")
    return len(alt) - tail


def item_positions(tok, it: dict) -> dict[str, dict[str, dict[str, int]]]:
    """Per reader: P1 / P2 / P3 in O and S (the read prompt: the ids with the digit's space token appended)."""
    from bridge_jspace.tokens import raw_encoding

    out = {}
    for w, rd in it["readers"].items():
        text = rd["text"]["org"]
        enc = raw_encoding(tok, text, offsets=True)
        assert list(enc["input_ids"]) == rd["ids"]["org"], f"{it['scene']} {w}: the rendered prompt's ids differ"
        p2 = pick_position(text, rd["question"], enc["offset_mapping"])
        if "pick" not in tok.decode([rd["ids"]["org"][p2]]):
            raise Dropped("the question's pick token does not decode to 'pick'")
        out[w] = positions_of(rd["ids"], it["pos"], p2, len(it["space"]))
    return out


def positions_of(ids: dict[str, list[int]], p1: int, p2: int, n_space: int) -> dict[str, dict[str, int]]:
    """P1 (the bridge word, the same in O and S), P2 (O's, placed in S from the end), P3 (the read's last token)."""
    if not p1 < p2:
        raise Dropped("the pick token is not after the bridge word")
    return {"P1": {"org": p1, "alt": p1}, "P2": {"org": p2, "alt": tail_position(ids["org"], ids["alt"], p2)},
            "P3": {v: len(ids[v]) + n_space - 1 for v in VARIANTS}}  # fmt: skip


def select(tok, target: str) -> tuple[list[dict], dict]:
    """Every main-test item of the target's X0 run at L (x47_cumulative.select, x49_gain's source), its positions,
    whether it is one of 49.1's locker-first items; counts after every filter."""
    from scripts import x47_cumulative as C

    items, counts = C.select(tok, "main", SOURCES[target], X.PREDICTED[target])
    out, dropped = [], collections.Counter()
    for it in items:
        try:
            out.append({**it, "jpos": item_positions(tok, it), "lf": it["group"] == G.GROUP})
        except Dropped as e:
            dropped[str(e)] += 1
    lf = [it for it in out if it["lf"]]
    counts = {**counts, "positions_dropped": dict(dropped), "items_read": len(out),
              "entities_read": len({it["entity"] for it in out}),
              "families": dict(collections.Counter(it["domain"] for it in out)),
              "classes_per_family": {d: len({e for it in out if it["domain"] == d for e in (it["entity"], it["cf_bridge"])})
                                     for d in sorted({it["domain"] for it in out})},
              "items_locker_first": len(lf), "entities_locker_first": len({it["entity"] for it in lf})}  # fmt: skip
    return out, counts


def write_names(layers: tuple[int, ...]) -> list[tuple[str, int, str]]:
    """(position, layer, arm) of every write read per item and reader, in read order (after O unedited)."""
    return [(p, la, a) for p in POS for la in layers for a in WRITE_ARMS]


def loss_names(layers: tuple[int, ...]) -> list[tuple[str, int, str]]:
    return [(p, la, a) for p in ("P1", "P2") for la in layers for a in WRITE_ARMS]


def marked(decode, ids: list[int], marks: dict[int, str]) -> str:
    """The prompt decoded token by token, each marked position as ⟦name:token⟧."""
    return "".join(f"⟦{marks[i]}:{decode([t])}⟧" if i in marks else decode([t]) for i, t in enumerate(ids))


def as_read(decode, it: dict, reader: str, variant: str = "org") -> str:
    ids = it["readers"][reader]["ids"][variant] + it["space"]
    return marked(decode, ids, {it["jpos"][reader][p][variant]: p for p in POS})


def stage_plan(k_prompts: int = N_PROMPTS) -> Path:
    """Tokenizer only: the items after every filter, the layers, the arms and the read counts, k rendered prompts (seed
    0) with P1 / P2 / P3 marked."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    gate = G.source_gate(SOURCES[target])
    items, counts = select(tok, target)
    lf = [it for it in items if it["lf"]]
    layers = LAYERS[target]
    n_w = 1 + len(write_names(layers))
    same_x49 = ([it["scene"] for it in lf] == [it["scene"] for it in G.select_items(tok, target)[0]]
                if target in G.SOURCES else None)  # the 122B: 49.1 has no source there  # fmt: skip
    blob = {"target": target, "L": X.PREDICTED[target], "prefix": pins.RUN_PREFIX,
            "run": RUNS.get(target, COVERAGE_RUNS.get(target)),
            "source": SOURCES[target], "source_gate": gate, "gate_passes": G.gate_passes(gate), "counts": counts,
            "layers": list(layers), "n_layers_model": N_LAYERS[target], "write_arms": list(WRITE_ARMS),
            "remove_arms": list(REMOVE_ARMS), "cache_forwards": len(items) * 2 * 2,
            "state_rows": len(items) * 2 * 2 * len(POS) * len(layers),
            "write_reads": len(lf) * 2 * n_w, "loss_reads": len(lf) * 2 * len(loss_names(layers)),
            "remove_reads": len(lf) * 2 * len(REMOVE_ARMS),
            "same_items_as_x49": same_x49,
            "probe_rows": 2 * len(items), "probe_rows_locker_first": 2 * len(lf),
            "probe_lf_rows_class_unseen_in_training": len(unseen_rows(probe_rows(items))),
            "prompts": [{"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}", "locker_first": it["lf"],
                         **{f"{READER_NAME[w]}_{v}": as_read(decode, it, w, v) for w in X.READERS for v in VARIANTS}}
                        for it in (items[i] for i in G.example_indices(len(items), k_prompts))]}  # fmt: skip
    print(json.dumps({k: v for k, v in blob.items() if k != "prompts"}, indent=1, ensure_ascii=False))
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan on {target} (tokenizer only): {len(blob['prompts'])} rendered prompts (seed 0), as read (the "
             "digit's space token appended); ⟦P1:…⟧ the bridge word, ⟦P2:…⟧ the question's pick token, ⟦P3:…⟧ the last "
             "token", ""]  # fmt: skip
    for p in blob["prompts"]:
        lines += [f"## {p['scene']} ({p['bridge']}; locker-first: {p['locker_first']})", ""]
        for k, v in p.items():
            if k.endswith(VARIANTS):
                lines += [f"{k}:", "", "```", v, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- the parts and edits (CPU-testable) ----------------------------------------------------------------------------


def write_parts(jdic, dic, h_o, h_s, groups, basis) -> dict[str, Any]:
    """Per row (h_o, h_s [m, d] at one position and layer): Δ, the J++ part P_J Δ and its random twin (x49_gain.
    lens_parts), his swap's change J10(h_S) - J10(h_O) (top_span_removal over his dictionary, O's protected rows for
    both: groups) and its random twin (a random part of Δ at the swap's share, capped at 1)."""
    from bridge_jspace.ablate import top_span_removal
    from scripts import statement_positions as SP

    delta = (h_s - h_o).float()
    pj, rj = G.lens_parts(jdic, delta, K, basis)
    c = top_span_removal(dic, h_s.float(), K_TOP, protected=groups) - top_span_removal(dic, h_o.float(), K_TOP,
                                                                                        protected=groups)  # fmt: skip
    share_c = G.share(c, delta)
    rc = SP.random_subspace_part(delta, share_c.clamp(max=1.0), basis)
    # jswap's swap_rot: the change turned by the layer's Haar rotation (ablate.rotation(d, 888 + l) is the same draw)
    return {"delta": delta, "pj": pj, "rj": rj, "c": c, "rc": rc, "crot": c @ basis.T, "share_c": share_c}


def arm_vector(parts: dict[str, Any], arm: str, row: int):
    """The vector an arm adds to h_O at its position and layer, for one row of write_parts."""
    name, gain = {"swap": ("c", 1.0), "swap_rand": ("rc", 1.0), "swap_rot": ("crot", 1.0), "jpp1": ("pj", 1.0),
                  "rand1": ("rj", 1.0),
                  "jpp2": ("pj", 2.0), "rand2": ("rj", 2.0), "whole": ("delta", 1.0)}[arm]  # fmt: skip
    return gain * parts[name][row]


def norm_record(parts: dict[str, Any], row: int) -> dict:
    d = parts["delta"][row : row + 1]
    sh = {k: float(G.share(parts[k][row : row + 1], d)[0]) for k in ("pj", "rj", "c", "rc")}
    return {"norm_delta": round(float(d.norm()), 4), "share_J": round(sh["pj"], 6), "share_J_rand": round(sh["rj"], 6),
            "share_swap": round(sh["c"], 6), "share_swap_rand": round(sh["rc"], 6),
            "swap_share_capped": bool(float(parts["share_c"][row]) > 1.0)}  # fmt: skip


class TopAt:
    """His knock-out at one position (P3): the projection of the state as it arrives on the span of its top-10 lens
    directions there, never a protected row (ablate.top_span_removal, his code path), removed; with a basis, a random
    subspace part of the same share of ||h||^2 removed instead (x49_ladder.ZachRandom's rule at one position). log: the
    share removed per call."""

    def __init__(self, dic, protected, pos: int, basis=None, k: int = K_TOP):
        self.dic, self.protected, self.pos, self.basis, self.k = dic, protected, pos, basis, k
        self.log: list[float] = []

    def __call__(self, h):
        import torch

        from bridge_jspace.ablate import top_span_removal
        from scripts import statement_positions as SP

        x = h.float()
        row = x[self.pos : self.pos + 1]
        groups = [(torch.zeros(1, dtype=torch.long, device=x.device), self.protected.to(x.device))]
        r = top_span_removal(self.dic, row, self.k, protected=groups if self.protected.numel() else None)
        if self.basis is not None:
            r = SP.random_subspace_part(row, G.share(r, row), self.basis.to(x.device, x.dtype))
        self.log.append(float(G.share(r, row)[0]))
        out = x.clone()
        out[self.pos] = row[0] - r[0]
        return out


# ---- probes and the read statistics (CPU) --------------------------------------------------------------------------


def scene_folds(scenes: list[str], labels: list[str], k: int = K_OUTER) -> dict[str, int]:
    """A fold per scene (whole scenes held out: a scene's O and S rows together), every O label spread over the folds
    (x0_probe.folds' round robin by class)."""
    f = PR.folds(labels, scenes, False, k)
    return {s: int(x) for s, x in zip(scenes, f, strict=True)}


def probe_oof(x: np.ndarray, labels: list[str], families: list[str], folds: np.ndarray) -> list[str | None]:
    """Out-of-fold predictions: per outer fold and family, a one-hot ridge (x0_probe.ridge) on the family's training
    rows, classes = the family's training labels; the penalty by leave-one-fold-out over the training folds (ties to
    the larger penalty). A family with one training class predicts it."""
    pred: list[str | None] = [None] * len(labels)
    y = np.array(labels, dtype=object)
    for fam in sorted(set(families)):
        rows = np.array([i for i, f in enumerate(families) if f == fam])
        for f in sorted(set(folds[rows].tolist())):
            tr, te = rows[folds[rows] != f], rows[folds[rows] == f]
            if not len(tr):
                continue
            if len(set(y[tr])) < 2:
                for i in te:
                    pred[i] = y[tr][0]
                continue
            acc = np.zeros(len(RELS))
            for g in sorted(set(folds[tr].tolist())):
                itr, ite = tr[folds[tr] != g], tr[folds[tr] == g]
                if len(set(y[itr])) < 2:
                    continue
                for j, p in enumerate(PR.ridge(x[itr], list(y[itr]), x[ite], RELS)):
                    acc[j] += sum(pi == y[i] for pi, i in zip(p, ite, strict=True))
            best = max(range(len(RELS)), key=lambda j: (acc[j], j))
            for i, p in zip(te, PR.ridge(x[tr], list(y[tr]), x[te], (RELS[best],))[0], strict=True):
                pred[i] = p
    return pred


def probe_rows(items: list[dict]) -> dict[str, Any]:
    """The probe's rows (item x variant, in that order): label (O's bridge on O, S's on S), family, the scene's fold,
    the cluster key (the scene's bridge entity), locker-first, the chance per row (1 / the family's classes)."""
    scenes = [it["scene"] for it in items]
    folds = scene_folds(scenes, [it["entity"] for it in items])
    labels = [e for it in items for e in (it["entity"], it["cf_bridge"])]
    fams = [it["domain"] for it in items for _ in VARIANTS]
    classes = {f: len({lab for lab, g in zip(labels, fams, strict=True) if g == f}) for f in set(fams)}
    return {"labels": labels, "families": fams, "folds": np.array([folds[it["scene"]] for it in items for _ in VARIANTS]),
            "ents": [it["entity"] for it in items for _ in VARIANTS],
            "lf": np.array([it["lf"] for it in items for _ in VARIANTS]),
            "variant": np.array([v for _ in items for v in VARIANTS]),
            "chance": np.array([1.0 / classes[f] for f in fams])}  # fmt: skip


def probe_inputs(h: np.ndarray, proj: np.ndarray, r: int, p: int, li: int) -> dict[str, np.ndarray]:
    """The three inputs [items x 2, d] (float32) at one reader, position and layer of the cache [n, 2, 2, 3, L, d]."""
    full = h[:, r, :, p, li].reshape(-1, h.shape[-1]).astype(np.float32)
    thru = proj[:, r, :, p, li].reshape(-1, h.shape[-1]).astype(np.float32)
    return {"thru": thru, "full": full, "out": full - thru}


def accuracy(right: np.ndarray, ents: list[str], n_boot: int, seed: int = X.BOOT_SEED) -> list[float]:
    if not len(right):
        return [float("nan")] * 3
    if n_boot <= 0:  # the run's read peak: the point only
        return [float(np.mean(right)), float("nan"), float("nan")]
    r = X.resampled_rates({"a": right.tolist()}, ents, n_boot, seed)["a"]
    return [float(np.mean(right)), *X.interval(r)]


def unseen_rows(rows: dict) -> list[int]:
    """The locker-first rows whose class (within their family) is in none of their training folds: the probe cannot
    name them (a ceiling on its accuracy, fixed by the items and the folds alone)."""
    seen = collections.defaultdict(set)
    for i, (y, f) in enumerate(zip(rows["labels"], rows["folds"], strict=True)):
        seen[(rows["families"][i], int(f))].add(y)
    return [i for i in np.flatnonzero(rows["lf"])
            if not any(rows["labels"][i] in seen[(rows["families"][i], g)] for g in range(K_OUTER) if g != rows["folds"][i])]  # fmt: skip


def probe_cell(x: np.ndarray, rows: dict, n_boot: int) -> dict:
    """One probe's out-of-fold accuracy on the locker-first rows (decisive) and on every row, per variant, the chance,
    and how many locker-first rows had a class absent from their training folds."""
    pred = probe_oof(x, rows["labels"], rows["families"], rows["folds"])
    right = np.array([int(p == y) for p, y in zip(pred, rows["labels"], strict=True)])
    lf = rows["lf"]
    ents = np.array(rows["ents"], dtype=object)
    unseen = unseen_rows(rows)
    return {"lf": accuracy(right[lf], list(ents[lf]), n_boot), "all": accuracy(right, list(ents), n_boot),
            "lf_O": float(np.mean(right[lf & (rows["variant"] == "org")])) if (lf & (rows["variant"] == "org")).any() else None,
            "lf_S": float(np.mean(right[lf & (rows["variant"] == "alt")])) if (lf & (rows["variant"] == "alt")).any() else None,
            "chance_lf": float(np.mean(rows["chance"][lf])) if lf.any() else None,
            "chance_all": float(np.mean(rows["chance"])), "lf_class_unseen": len(unseen), "n_lf": int(lf.sum())}  # fmt: skip


def settle_layer(tops: list[int], tok: int) -> int | None:
    """The layer from which tok is the logit lens's top token through the last layer (None if not at the last)."""
    if not tops or tops[-1] != tok:
        return None
    i = len(tops) - 1
    while i > 0 and tops[i - 1] == tok:
        i -= 1
    return i


def answer_layers(ll_rows: list[dict], cases: dict[str, dict]) -> dict[str, dict]:
    """Per reader: each locker-first O prompt's settle layer of O's answer at P3, the lower median (the answer layer);
    S's prompts (S's answer) beside."""
    out = {}
    for w in X.READERS:
        per = {v: [settle_layer(r["top"], r["tok"]) for r in ll_rows
                   if r["reader"] == w and r["variant"] == v and cases[r["scene"]]["lf"]] for v in VARIANTS}  # fmt: skip
        ok = [s for s in per["org"] if s is not None]
        okS = [s for s in per["alt"] if s is not None]
        out[READER_NAME[w]] = {"layer": statistics.median_low(ok) if ok else None, "n": len(per["org"]),
                               "never": len(per["org"]) - len(ok), "per_item": per["org"],
                               "S_layer": statistics.median_low(okS) if okS else None,
                               "quartiles": [float(np.percentile(ok, q)) for q in (25, 50, 75)] if ok else None}  # fmt: skip
    return out


def read_peak(thru: dict[int, float], layers: tuple[int, ...], ans: int | None) -> int | None:
    """The cached layer before the answer layer with the highest through-the-lens accuracy (ties: the earliest)."""
    before = [la for la in layers if ans is None or la < ans]
    if not before:
        return None
    return max(before, key=lambda la: (thru[la], -la))


def lens_shares(lens: dict[str, np.ndarray], mask: np.ndarray, r: int, p: int, li: int) -> dict:
    """Shares over the selected items' O and S rows at one reader, position and layer: the bridge entity (O's on O,
    S's on S) at rank 1 / <= 5 among the letter tokens, the other entity beside, the same over the whole vocabulary,
    and the share whose whole-vocabulary top token is a digit."""
    own, other = lens["rank_own"][mask, r, :, p, li], lens["rank_other"][mask, r, :, p, li]
    fown = lens["rank_own_full"][mask, r, :, p, li]
    dig = lens["top_full_digit"][mask, r, :, p, li]

    def share(a: np.ndarray, k: int) -> float | None:
        a = a[a > 0]
        return float(np.mean(a <= k)) if a.size else None

    return {"top1": share(own, 1), "top5": share(own, 5), "other_top1": share(other, 1), "other_top5": share(other, 5),
            "full_top1": share(fown, 1), "full_top5": share(fown, 5), "full_top_digit": float(np.mean(dig)) if dig.size else None,
            "rank_median": float(np.median(own[own > 0])) if (own > 0).any() else None}  # fmt: skip


def read_stats(h: np.ndarray, proj: np.ndarray, lens: dict, items: list[dict], ll_rows: list[dict],
               layers: tuple[int, ...], n_boot: int = X.N_BOOT, readers=X.READERS, positions=POS,
               inputs=INPUTS) -> dict:  # fmt: skip
    """The read statistics of one run: the answer layers, and per reader, position and layer the lens shares and the
    three probes."""
    from bridge_jspace.utils import progress

    rows = probe_rows(items)
    cases = {it["scene"]: it for it in items}
    lf = np.array([it["lf"] for it in items])
    out: dict[str, Any] = {"answer": answer_layers(ll_rows, cases), "layers": list(layers), "n_items": len(items),
                           "n_lf": int(lf.sum()), "cells": {}}  # fmt: skip
    cells = [(w, p, li) for w in readers for p in positions for li in range(len(layers))]
    for w, p, li in progress(cells, "51.10 read: probes (reader x position x layer)"):
        r, pi = RIDX[w], POS.index(p)
        xs = probe_inputs(h, proj, r, pi, li)
        cell = {"lens": lens_shares(lens, lf, r, pi, li), "lens_all": lens_shares(lens, np.ones_like(lf), r, pi, li)}
        cell |= {k: probe_cell(xs[k], rows, n_boot) for k in inputs}
        out["cells"][f"{READER_NAME[w]}|{p}|{layers[li]}"] = cell
    return out


def thru_curve(stats: dict, reader: str, p: str) -> dict[int, float]:
    return {la: stats["cells"][f"{reader}|{p}|{la}"]["thru"]["lf"][0] for la in stats["layers"]}


# ---- GPU -----------------------------------------------------------------------------------------------------------


def zach_dictionary(model, lens, layer: int, letters):
    """His read directions at one layer (x49_ladder.band_dictionaries: a LensDictionary over W_g = W_U[letters] x gain
    and J_l, its rows cast on demand)."""
    from scripts import x49_ladder as LD

    return LD.band_dictionaries(model, lens, (layer,), letters)[layer]


def cache_states(model, lens, items: list[dict], layers: tuple[int, ...], n_layers: int, digits,
                 zdic=zach_dictionary) -> dict[str, Any]:  # fmt: skip
    """Step 1 and 2 of the run: per item, reader and variant one forward of the prompt as read recording every layer;
    the states at P1 / P2 / P3 at the cached layers [n, 2, 2, 3, L, d] (fp32, CPU), the clean read and its protected
    rows, the logit lens at P3 at every layer; then per cached layer his lens ranks and the projection on his top-10
    span."""
    import torch

    from bridge_jspace.ablate import top_span_removal
    from bridge_jspace.utils import progress
    from scripts import x47_twodefs as TD

    dev = model.device
    letters = model.letter_token_ids()
    vocab = model.hf.lm_head.weight.shape[0]
    row_of = torch.full((vocab,), -1, dtype=torch.long, device=dev)
    row_of[letters.to(dev)] = torch.arange(letters.numel(), device=dev)
    digit_set = torch.zeros(vocab, dtype=torch.bool, device=dev)
    digit_set[digits.to(dev)] = True
    n, nl = len(items), len(layers)
    d = int(model.hf.lm_head.weight.shape[1])
    hst = torch.zeros(n, 2, 2, len(POS), nl, d)
    prot: dict[tuple[int, int, int], Any] = {}
    clean, ll_rows = [], []
    for i, it in enumerate(progress(items, "51.10: cache (item: 2 readers x O / S, every layer)")):
        for w, rd in it["readers"].items():
            r = RIDX[w]
            for v, variant in enumerate(VARIANTS):
                read_ids = rd["ids"][variant] + it["space"]
                logits, rec = model.run(torch.tensor([read_ids], device=dev), record=tuple(range(n_layers)))
                prot[(i, r, v)] = TD.protected_rows(logits, row_of)
                gold = rd["tok_A"] if variant == "org" else rd["tok_b"]
                clean.append({"scene": it["scene"], "reader": w, "variant": variant, "top": int(logits.argmax()),
                              "read_right": int(int(logits.argmax()) == gold),
                              "protected": prot[(i, r, v)].tolist()})  # fmt: skip
                for pi, p in enumerate(POS):
                    q = it["jpos"][w][p][variant]
                    for li, la in enumerate(layers):
                        hst[i, r, v, pi, li] = rec[la][q].float().cpu()  # a copy (memory lesson 2)
                p3 = it["jpos"][w]["P3"][variant]
                lg = model.unembed(torch.stack([rec[la][p3] for la in range(n_layers)]))
                ranks = {k: ((lg > lg[:, t : t + 1]).sum(1) + 1).tolist() for k, t in (("rank_A", rd["tok_A"]),
                                                                                         ("rank_b", rd["tok_b"]))}  # fmt: skip
                ll_rows.append({"scene": it["scene"], "reader": w, "variant": variant, "tok": gold,
                                "top": lg.argmax(1).tolist(), **ranks})  # fmt: skip
                del rec, lg
    # step 2: his lens ranks and top-10 projections, per cached layer (one dictionary at a time)
    proj = torch.zeros_like(hst)
    shape = (n, 2, 2, len(POS), nl)
    lens_arr = {k: np.zeros(shape, dtype=np.int32) for k in ("rank_own", "rank_other", "rank_own_full", "rank_other_full",
                                                             "top_full", "top_full_digit")}  # fmt: skip
    ent = torch.tensor([[it["readers"][X.LOOKUP]["ids"][v][it["pos"]] for v in VARIANTS] for it in items])  # [n, 2]
    meta = np.array([(i, r, v, p) for i in range(n) for r in range(2) for v in range(2) for p in range(len(POS))])
    mi, mv = torch.as_tensor(meta[:, 0]), torch.as_tensor(meta[:, 2])
    own_tok, oth_tok = ent[mi, mv], ent[mi, 1 - mv]
    for li, la in enumerate(progress(layers, "51.10: his lens ranks and top-10 projections (layer)")):
        dic = zdic(model, lens, la, letters)
        flat = hst[:, :, :, :, li].reshape(-1, d)
        out_proj = torch.zeros_like(flat)
        for s in range(0, flat.shape[0], CHUNK):
            x = flat[s : s + CHUNK].to(dev)
            m = meta[s : s + CHUNK]
            ot, tt = own_tok[s : s + CHUNK].to(dev), oth_tok[s : s + CHUNK].to(dev)
            at = tuple(m.T)  # (item, reader, variant, position) into a layer's [n, 2, 2, 3] view
            lg = dic.logits(x)
            for key, t in (("rank_own", ot), ("rank_other", tt)):
                rows = row_of[t]
                val = lg.gather(1, rows.clamp(min=0)[:, None])
                rk = ((lg > val).sum(1) + 1).where(rows >= 0, torch.full_like(rows, -1))
                lens_arr[key][..., li][at] = rk.cpu().numpy()
            del lg
            full = lens.readout(x, la)
            for key, t in (("rank_own_full", ot), ("rank_other_full", tt)):
                lens_arr[key][..., li][at] = ((full > full.gather(1, t[:, None])).sum(1) + 1).cpu().numpy()
            top = full.argmax(1)
            lens_arr["top_full"][..., li][at] = top.cpu().numpy()
            lens_arr["top_full_digit"][..., li][at] = digit_set[top].cpu().numpy()
            del full
            groups = []
            for key in sorted({(int(a), int(b), int(c)) for a, b, c, _ in m}):
                sel = np.flatnonzero((m[:, 0] == key[0]) & (m[:, 1] == key[1]) & (m[:, 2] == key[2]))
                if prot[key].numel():
                    groups.append((torch.tensor(sel, device=dev), prot[key].to(dev)))
            out_proj[s : s + CHUNK] = top_span_removal(dic, x, K_TOP, protected=groups or None).cpu()
        proj[:, :, :, :, li] = out_proj.reshape(n, 2, 2, len(POS), d)
        del dic, flat, out_proj
    return {"h": hst, "proj": proj, "lens": lens_arr, "clean": clean, "logit_lens": ll_rows, "prot": prot}


def write_reads(model, lens, items: list[dict], lf_idx: list[int], cache: dict, layers: tuple[int, ...], digits,
                zdic=zach_dictionary) -> tuple[list, list, list]:  # fmt: skip
    """Step 4: per cached layer the parts of every locker-first item, reader and position (write_parts); then per item
    and reader every write arm read on O (one batch list: O unedited, then position x layer x arm) and the plain-text
    loss at P1 and P2."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    letters = model.letter_token_ids()
    hst, prot = cache["h"], cache["prot"]
    d = hst.shape[-1]
    parts: dict[int, dict] = {}
    norms = []
    for li, la in enumerate(progress(layers, "51.10: the parts per layer (J++ OMP, his swap, random twins)")):
        jdic = lens.vectors(la, letters)
        dic = zdic(model, lens, la, letters)
        basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
        ho = hst[lf_idx, :, 0, :, li].reshape(-1, d).to(dev)  # rows (item, reader, position)
        hs = hst[lf_idx, :, 1, :, li].reshape(-1, d).to(dev)
        groups = [(torch.tensor([(k * 2 + r) * len(POS) + p for p in range(len(POS))], device=dev), prot[(i, r, 0)].to(dev))
                  for k, i in enumerate(lf_idx) for r in range(2) if prot[(i, r, 0)].numel()]  # fmt: skip
        pt = write_parts(jdic, dic, ho, hs, groups or None, basis)
        parts[la] = {k: v.cpu() for k, v in pt.items()}
        del jdic, dic, basis, pt, ho, hs
        for k, i in enumerate(lf_idx):
            for w in X.READERS:
                for pi, p in enumerate(POS):
                    row = (k * 2 + RIDX[w]) * len(POS) + pi
                    norms.append({"scene": items[i]["scene"], "reader": w, "pos": p, "layer": la,
                                  **norm_record(parts[la], row)})  # fmt: skip
    names = write_names(layers)
    lnames = loss_names(layers)
    rows, losses = [], []
    for k, i in enumerate(progress(lf_idx, f"51.10: {1 + len(names)} reads x 2 readers + the loss (item)")):
        it = items[i]
        base = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"]}
        for w, rd in it["readers"].items():
            jp = it["jpos"][w]

            def edit(p: str, la: int, a: str, k=k, w=w, jp=jp):
                row = (k * 2 + RIDX[w]) * len(POS) + POS.index(p)
                return {la: AddRows(arm_vector(parts[la], a, row)[None].to(dev), [jp[p]["org"]])}

            edits = [{}] + [edit(p, la, a) for p, la, a in names]
            logits, _ = X.read_logits(model, rd["ids"]["org"], edits, G.RENDERING, it["space"], None)
            for (p, la, a), lg in zip([(None, None, NONE), *names], logits, strict=True):
                r = X.read_row(lg, rd, digits)
                rows.append({**base, "reader": w, "pos": p, "layer": la, "arm": a, **r,
                             "other_digit": int(r["role"] == "other" and bool((digits == r["top"]).any()))})  # fmt: skip
            for p in ("P1", "P2"):
                q = jp[p]["org"]
                ids = rd["ids"]["org"]
                mine = [(pp, la, a) for pp, la, a in lnames if pp == p]
                lg, _ = X.read_logits(model, ids[: q + 1], [{}] + [edit(pp, la, a) for pp, la, a in mine], G.RENDERING,
                                      [], None)  # fmt: skip
                lp = torch.log_softmax(lg.float(), dim=-1)
                nxt = ids[q + 1]
                losses += [{**base, "reader": w, "pos": p, "layer": la, "arm": a, "next": nxt,
                            "loss": round(float(-row[nxt]), 5), "top_is_next": int(int(row.argmax()) == nxt)}
                           for (_, la, a), row in zip([(p, None, NONE), *mine], lp, strict=True)]  # fmt: skip
    return rows, losses, norms


def remove_reads(model, lens, items: list[dict], lf_idx: list[int], cache: dict, layers: tuple[int, ...],
                 peaks: dict[str, int | None], n_layers: int, digits, zdic=zach_dictionary) -> tuple[list, list]:  # fmt: skip
    """Step 5, per reader at its read peak (P3): his knock-out at P3 over the band peak +- 2 and the J++-25 removal at
    the peak layer, each beside its random twin, read on O; kept = the top token is O's answer."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x47_zero as Z

    dev = model.device
    letters = model.letter_token_ids()
    hst, prot = cache["h"], cache["prot"]
    d = hst.shape[-1]
    sources = set(getattr(lens, "source_layers", range(n_layers)))
    rows, recs = [], []
    for w in X.READERS:
        peak = peaks.get(READER_NAME[w])
        if peak is None:
            continue
        r, li, p3 = RIDX[w], layers.index(peak), POS.index("P3")
        band = tuple(la for la in range(peak - BAND_HALF, peak + BAND_HALF + 1) if 0 <= la < n_layers and la in sources)
        bases = {la: SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev) for la in band}
        dics = {la: zdic(model, lens, la, letters) for la in band}
        jdic = lens.vectors(peak, letters)
        ho = hst[lf_idx, r, 0, p3, li].to(dev)
        hs = hst[lf_idx, r, 1, p3, li].to(dev)
        q, ks, per = Z.layer_parts(jdic, ho, hs, bases[peak])  # the atoms of h_O - h_S = -Δ: Δ's atoms; shares of h_O
        del jdic
        for k, i in enumerate(progress(lf_idx, f"51.10: removal at P3, {READER_NAME[w]}, peak L{peak}, band {band}")):
            it, rd = items[i], items[i]["readers"][w]
            pos = it["jpos"][w]["P3"]["org"]
            pr = prot[(i, r, 0)].to(dev)
            ko = {la: TopAt(dics[la], pr, pos) for la in band}
            kr = {la: TopAt(dics[la], pr, pos, bases[la]) for la in band}
            edits = [
                {},
                ko,
                kr,
                {peak: Z.ProjectOut(q[k], [pos])},
                {peak: Z.ProjectOut(bases[peak][:, : ks[k]], [pos])},
            ]
            logits, _ = X.read_logits(model, rd["ids"]["org"], edits, G.RENDERING, it["space"], None)
            for a, lg in zip(REMOVE_ARMS, logits, strict=True):
                x = X.read_row(lg, rd, digits)
                rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                             "arm": a, "peak": peak, "band": list(band), "kept": int(x["top"] == rd["tok_A"]), **x,
                             "other_digit": int(x["role"] == "other" and bool((digits == x["top"]).any()))})  # fmt: skip
            recs.append({"scene": it["scene"], "reader": w, "peak": peak, "band": list(band),
                         **{key.replace("hS", "hO"): v for key, v in per[k].items()},  # layer_parts' first state: h_O
                         "ko_share": {str(la): round(ko[la].log[0], 6) for la in band},
                         "ko_rand_share": {str(la): round(kr[la].log[0], 6) for la in band}})  # fmt: skip
        del dics, bases
    return rows, recs


def save_states(path: Path, cache: dict, layers: tuple[int, ...]) -> dict:
    """states.npz: h and the projection on his top-10 span [n, reader, O/S, P1-P3, layer, d] in fp16 (finite checked)."""
    h, p = cache["h"].numpy(), cache["proj"].numpy()
    info = {"shape": list(h.shape), "max_abs_h": float(np.abs(h).max()), "max_abs_proj": float(np.abs(p).max())}
    h16, p16 = h.astype(np.float16), p.astype(np.float16)
    assert np.isfinite(h16).all(), f"fp16 overflow in the cached states: {info}"
    assert np.isfinite(p16).all(), f"fp16 overflow in the cached projections: {info}"
    np.savez(path, h=h16, proj=p16, layers=np.array(layers), **{k: v for k, v in cache["lens"].items()})
    return info


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.10 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"51.10 runs on {sorted({*RUNS, *COVERAGE_RUNS})}, not {target}"
    if target in COVERAGE_RUNS:  # Lightning: its fixed layer is the committed one (BJ_PREDICTED_LAYER), in the grid
        assert X.PREDICTED[target] in LAYERS[target], f"L{X.PREDICTED[target]} is not in {LAYERS[target]}"
    layers, source, n_layers = LAYERS[target], SOURCES[target], N_LAYERS[target]
    assert pins.TARGETS[target]["n_layers"] == n_layers, "the model's layer count changed"
    src = X.RESULTS / source
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl"))]
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "51.10",
         "spec": "jobs/c3/batch51.yaml (addendum_2: 51.10)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs}, "source": source,
         "L": X.PREDICTED[target], "layers": list(layers), "n_layers": n_layers, "positions": POS_TEXT,
         "rendering": G.RENDERING, "k": K, "k_top": K_TOP, "band_half": BAND_HALF, "write_arms": list(WRITE_ARMS),
         "remove_arms": list(REMOVE_ARMS), "arm_text": ARM_TEXT, "inputs_text": INPUT_TEXT, "rule": RULE,
         "items_rule": "every item of the source X0 run at L (x47_cumulative.select, as 49.1) for the read statistics "
                       "(probes need the rows), decided on 49.1's locker-first items; write and remove arms on the "
                       "locker-first items only",
         "lens_dictionary": "his read directions: x49_ladder.band_dictionaries (LensDictionary over W_g = W_U[letters] "
                            "x the final norm's gain and J_l of the J++ lens, rows cast on demand), letter tokens; "
                            "protected rows = the prompt's clean read's top-10 (x47_twodefs.protected_rows)",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token; kept = O's",
         "gate": f"the source run's (X0: {X.GATE} per reader on O unedited, >= {X.N_MIN} eligible); asserted",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED, "folds": "x0_probe.folds round robin by O's bridge (deterministic)"},
         "n_boot": X.N_BOOT, "storage": f"{STATES_FILE}: fp16 states and projections, gitignored (> 50 MB)",
         "sealed": f"no label in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52 / 53: no Q-line; read and verdict --coverage after the run
        m |= {
            "question": NO_PREDICTION,
            "batch": COVERAGE_BATCH[target],
            "rules_first_scored": SCORED,
            "sealed": f"none (batch {COVERAGE_BATCH[target]} coverage)",
        }
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    gate = G.source_gate(source)
    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    missing = [la for la in layers if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at {missing}"
    items, counts = select(model.tokenizer, target)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    lf_idx = [i for i, it in enumerate(items) if it["lf"]]
    tested = G.gate_passes(gate) and bool(lf_idx)
    (out / "gate.json").write_text(json.dumps({"source": source, "gate": gate, "tested": tested,
                                              "order": [it["scene"] for it in items],
                                              "hub_kernels": loaded_hub_kernels()}, indent=2) + "\n")  # fmt: skip
    if not tested:
        print(
            "the gate fixed in advance did not pass (or no locker-first items): not tested; see gate.json", flush=True
        )
        return out
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        cache = cache_states(model, lens, items, layers, n_layers, digits)
        X.write_jsonl(out / "clean.jsonl", cache["clean"])
        X.write_jsonl(out / "logit_lens.jsonl", cache["logit_lens"])
        info = save_states(out / STATES_FILE, cache, layers)
        stats = read_stats(cache["h"].numpy(), cache["proj"].numpy(), cache["lens"], items, cache["logit_lens"], layers,
                           n_boot=0, positions=("P3",), inputs=("thru",))  # fmt: skip
        peaks = {READER_NAME[w]: read_peak(thru_curve(stats, READER_NAME[w], "P3"), layers,
                                           stats["answer"][READER_NAME[w]]["layer"]) for w in X.READERS}  # fmt: skip
        (out / "peak.json").write_text(json.dumps({"peaks": peaks, "states": info, "how": "read_peak on P3's "
                                                   "through-the-lens probe (locker-first rows), layers before the "
                                                   "answer layer (answer_layers)"}, indent=2) + "\n")  # fmt: skip
        del stats
        rows, losses, norms = write_reads(model, lens, items, lf_idx, cache, layers, digits)
        X.write_jsonl(out / "outcomes.jsonl", rows)
        X.write_jsonl(out / "losses.jsonl", losses)
        X.write_jsonl(out / "norms.jsonl", norms)
        rem, recs = remove_reads(model, lens, items, lf_idx, cache, layers, peaks, n_layers, digits)
        X.write_jsonl(out / "removal.jsonl", rem)
        X.write_jsonl(out / "removal_norms.jsonl", recs)
    print(
        f"wrote {out}: {len(rows)} write reads, {len(rem)} removal reads of {len(lf_idx)} items (sealed: no label)",
        flush=True,
    )
    return out


# ---- read (CPU, on the cached states; statistics only, no label) ---------------------------------------------------


def load_run(run: str) -> dict[str, Any]:
    src = RESULTS / run
    z = np.load(src / STATES_FILE)
    lens = {
        k: z[k] for k in ("rank_own", "rank_other", "rank_own_full", "rank_other_full", "top_full", "top_full_digit")
    }
    return {"h": z["h"], "proj": z["proj"], "layers": tuple(int(x) for x in z["layers"]), "lens": lens,
            "items": X.read_jsonl(src / "cases.jsonl"), "ll": X.read_jsonl(src / "logit_lens.jsonl"),
            "manifest": json.loads((src / "manifest.json").read_text())}  # fmt: skip


def stage_read(name: str, n_boot: int = X.N_BOOT) -> Path:
    """The read statistics of one run into results/x51_jread/read-<run>-<UTC>/read.json (no label); the run's peak
    re-derived and checked against its peak.json."""
    run = load_run(name)
    stats = read_stats(run["h"], run["proj"], run["lens"], run["items"], run["ll"], run["layers"], n_boot)
    peaks = {
        w: read_peak(thru_curve(stats, w, "P3"), run["layers"], stats["answer"][w]["layer"])
        for w in ("lookup", "recall")
    }
    stored = RESULTS / name / "peak.json"
    stats["peaks_P3"] = peaks
    stats["peak_matches_run"] = json.loads(stored.read_text())["peaks"] == peaks if stored.exists() else None
    stats["run"] = name
    stats["target"] = run["manifest"]["model"]["target"]
    out = RESULTS / f"read-{name}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "read.json").write_text(json.dumps(stats, indent=1) + "\n")
    print("wrote", out, flush=True)
    return out


def latest_read(run: str) -> dict | None:
    found = sorted(RESULTS.glob(f"read-{run}-*/read.json"))
    return json.loads(found[-1].read_text()) if found else None


# ---- the seal ------------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.10 at `rev` (x48_heads.parse_answer: 'Dan:' / 'Dan (27B):' lines and bullet
    continuations), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return H.parse_answer(text, QUESTION)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


# ---- the rules (CPU, on point estimates) ---------------------------------------------------------------------------


def write_at(sw: dict[str, float], twins: dict[str, str] = TWIN) -> dict:
    """The write clause at one layer: some arm of swap / jpp1 / jpp2 switches >= WRITE_RATIO x the whole patch with its
    random twin <= RAND_MAX; the whole patch switching nothing: no."""
    whole = sw["whole"]
    arms = {}
    for a, t in twins.items():
        ratio = sw[a] / whole if whole > 0 else None
        arms[a] = {"switch": sw[a], "twin": sw[t], "ratio": ratio,
                   "ok": ratio is not None and ratio >= WRITE_RATIO - EPS and sw[t] <= RAND_MAX + EPS}  # fmt: skip
    return {"whole": whole, "arms": arms, "holds": any(v["ok"] for v in arms.values())}


def position_rule(cells: dict[int, dict], sw: dict[int, dict[str, float]], layers: list[int], ans: int | None) -> dict:
    """One reader at one position: cells[layer] = {'thru', 'full', 'top5'} (locker-first points), sw[layer][arm] the
    switch rates; ans the answer layer. The read and write clauses, (a)-(d), the read peak and the best layer."""
    before = [la for la in layers if ans is not None and la < ans]
    ok = {la: cells[la]["thru"] >= THRU_MIN - EPS and (cells[la]["top5"] or 0.0) >= TOP5_MIN - EPS
          and cells[la]["full"] >= FULL_MIN - EPS for la in layers}  # fmt: skip
    readable = [la for la in layers if ok[la]]
    out: dict[str, Any] = {"answer_layer": ans, "layers_before": before,
                           "first_readable": readable[0] if readable else None,
                           "first_readable_before_answer": next((la for la in readable if la in before), None)}  # fmt: skip
    if not before:
        return {**out, "label": "undecided", "why": "no cached layer before the answer layer", "read": None,
                "write": None, "peak": None}  # fmt: skip
    read = any(ok[la] for la in before)
    peak = read_peak({la: cells[la]["thru"] for la in layers}, tuple(layers), ans)
    w = write_at(sw[peak])
    routes = all(cells[la]["thru"] < THRU_FAIL - EPS for la in before) and any(
        cells[la]["full"] >= FULL_MIN - EPS for la in before
    )
    notrep = all(cells[la]["full"] < FULL_FAIL - EPS for la in before)
    if notrep:
        key = "d"
    elif read and w["holds"]:
        key = "a"
    elif read:
        key = "b"
    elif routes and not w["holds"]:
        key = "c"
    else:
        key = None
    best = max(layers, key=lambda la: (max(sw[la][a] for a in TWIN), -la))
    return {**out, "read": read, "write": w["holds"], "peak": peak, "at_peak": w, "routes_clause": routes,
            "write_with_his_rotated_control": write_at(sw[peak], TWIN_ROT)["holds"],
            "not_represented_clause": notrep, "label": LABELS[key] if key else
            ("none of the four (writable, not readable)" if w["holds"] else "none of the four"),
            "best_layer": best, "at_best": write_at(sw[best]),
            "whole_max": max(sw[la]["whole"] for la in layers)}  # fmt: skip


def switch_rates(rows: list[dict], reader: str, n_boot: int) -> dict:
    """Per position, layer and arm: the switch rate, 'changed to another digit' and O kept, with cluster-bootstrap CIs
    on the switch; O unedited beside."""
    mine = [r for r in rows if r["reader"] == reader]
    by: dict[tuple, list[dict]] = collections.defaultdict(list)
    for r in mine:
        by[(r["pos"], r["layer"], r["arm"])].append(r)
    out: dict[str, Any] = {}
    for (p, la, a), rs in by.items():
        ents = [r["entity"] for r in rs]
        out[f"{p}|{la}|{a}"] = {"n": len(rs), "switch": accuracy(np.array([r["switched"] for r in rs]), ents, n_boot),
                                "other_digit": float(np.mean([r["other_digit"] for r in rs])),
                                "kept": float(np.mean([r["role"] == "A" for r in rs]))}  # fmt: skip
    return out


def x49_beside(target: str, rows: list[dict], L: int) -> dict | None:
    """P1 at L against 49.1's stored rows on the same items: its J(1,0), J(2,0), R(1,0), R(2,0), J(1,1) and our jpp1,
    jpp2, rand1, rand2, whole (rates and item agreement), per reader."""
    if target not in G.RUNS:  # batch 52's Lightning: 49.1 never ran there, nothing to set beside
        return None
    src = G.RESULTS / G.RUNS[target] / "outcomes.jsonl"
    if not src.exists():
        return None
    old = {(r["scene"], r["reader"], r["arm"]): r["switched"] for r in X.read_jsonl(src)}
    pairs = {"jpp1": "J(1,0)", "jpp2": "J(2,0)", "rand1": "R(1,0)", "rand2": "R(2,0)", "whole": "J(1,1)"}
    out = {}
    for w in X.READERS:
        res = {}
        for a, b in pairs.items():
            mine = {r["scene"]: r["switched"] for r in rows if r["reader"] == w and r["pos"] == "P1" and r["layer"] == L
                    and r["arm"] == a}  # fmt: skip
            both = [(v, old[(s, w, b)]) for s, v in mine.items() if (s, w, b) in old]
            res[a] = {"x49_arm": b, "ours": float(np.mean(list(mine.values()))) if mine else None,
                      "x49": float(np.mean([y for _, y in both])) if both else None,
                      "agree": [sum(x == y for x, y in both), len(both)]}  # fmt: skip
        out[READER_NAME[w]] = res
    return out


def removal_numbers(rows: list[dict], n_boot: int) -> dict:
    """Per reader: kept (O's answer) per removal arm, cost = kept(random) - kept(removal) with paired cluster CIs."""
    out = {}
    for w in X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        if not mine:
            continue
        ents, kept = G.per_item(mine, "kept", list(REMOVE_ARMS))
        boot = X.resampled_rates(kept, ents, n_boot)
        out[READER_NAME[w]] = {"peak": mine[0]["peak"], "band": mine[0]["band"], "n": len(ents),
                               "kept": {a: [float(np.mean(v)), *X.interval(boot[a])] for a, v in kept.items()},
                               "cost_ko": [float(np.mean(kept["ko_rand"]) - np.mean(kept["ko"])),
                                           *X.interval(boot["ko_rand"] - boot["ko"])],
                               "cost_jrm": [float(np.mean(kept["jrm_rand"]) - np.mean(kept["jrm"])),
                                            *X.interval(boot["jrm_rand"] - boot["jrm"])]}  # fmt: skip
    return out


def loss_means(losses: list[dict], reader: str) -> dict:
    by: dict[str, list[float]] = collections.defaultdict(list)
    for r in losses:
        if r["reader"] == reader:
            by[f"{r['pos']}|{r['layer']}|{r['arm']}"].append(r["loss"])
    return {k: float(np.mean(v)) for k, v in by.items()}


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    rows = X.read_jsonl(src / "outcomes.jsonl") if (src / "outcomes.jsonl").exists() else []
    if not gate.get("tested") or not rows:
        return {"target": target, "run": run, "status": "not tested", "gate": gate.get("gate"),
                "why": "the gate fixed in advance failed, no locker-first items, or the run did not finish"}  # fmt: skip
    stats = latest_read(run)
    assert stats is not None, f"{run}: no read folder; run `x51_jread.py read --name {run}` first"
    layers = stats["layers"]
    readers, rules = {}, {}
    for w in X.READERS:
        name = READER_NAME[w]
        sr = switch_rates(rows, w, n_boot)
        readers[name] = {"switch": sr, "loss": loss_means(X.read_jsonl(src / "losses.jsonl"), w)}
        ans = stats["answer"][name]["layer"]
        rules[name] = {}
        for p in ("P3", "P2"):
            cells = {la: {"thru": stats["cells"][f"{name}|{p}|{la}"]["thru"]["lf"][0],
                          "full": stats["cells"][f"{name}|{p}|{la}"]["full"]["lf"][0],
                          "top5": stats["cells"][f"{name}|{p}|{la}"]["lens"]["top5"]} for la in layers}  # fmt: skip
            sw = {la: {a: sr[f"{p}|{la}|{a}"]["switch"][0] for a in WRITE_ARMS} for la in layers}
            rules[name][p] = position_rule(cells, sw, layers, ans)
    rem = X.read_jsonl(src / "removal.jsonl") if (src / "removal.jsonl").exists() else []
    norms = X.read_jsonl(src / "norms.jsonl")
    shares = {f"{p}": {k: float(np.median([n[k] for n in norms if n["pos"] == p]))
                       for k in ("share_J", "share_J_rand", "share_swap", "share_swap_rand")} for p in POS}  # fmt: skip
    capped = sum(n["swap_share_capped"] for n in norms)
    return {"target": target, "run": run, "status": "tested", "L": m["L"], "layers": layers, "n": stats["n_lf"],
            "n_read": stats["n_items"], "answer": {w: {k: v for k, v in a.items() if k != "per_item"}
                                                   for w, a in stats["answer"].items()},
            "rules": rules, "readers": readers, "read": stats, "removal": removal_numbers(rem, n_boot),
            "x49": x49_beside(target, rows, m["L"]), "shares_median": shares, "swap_share_capped": [capped, len(norms)],
            "gate": gate.get("gate"), "read_folder_peaks": stats.get("peaks_P3"),
            "peak_matches_run": stats.get("peak_matches_run")}  # fmt: skip


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, (int, float)):
        return f"{v:.2f}"
    return "-" if v[0] is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def summary_rows(m: dict) -> list[str]:
    """The brief's summary table: per reader, the first layer lens-readable at P3, the peak swap at P3 vs the whole
    patch, the same at P2, and the labels."""
    out = []
    for w in ("lookup", "recall"):
        cells = []
        for p in ("P3", "P2"):
            r = m["rules"][w][p]
            ap = r.get("at_peak") or {}
            sw = (ap.get("arms") or {}).get("swap", {})
            cells += [f"{r['first_readable']}", f"L{r['peak']}: {fmt(sw.get('switch'))} / {fmt(ap.get('whole'))}"
                      if r.get("peak") is not None else "-", f"**{r['label']}**"]  # fmt: skip
        out.append(f"| {m['target']} | {w} | answer L{m['answer'][w]['layer']} | " + " | ".join(cells) + " |")
    return out


def figure(m: dict, path: Path) -> None:
    """Rows P1 / P2 / P3, columns the cached layers, panels lookup / recall: heat = the through-the-lens probe's
    accuracy (locker-first), the number = his swap's switch share, a dashed line at the answer layer, the read peak boxed."""
    from scripts import story_style as S

    plt = S.setup()
    layers = m["layers"]
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH * 1.6, 3.4), squeeze=False)
    for c, w in enumerate(("lookup", "recall")):
        ax = axes[0, c]
        heat = np.array([[m["read"]["cells"][f"{w}|{p}|{la}"]["thru"]["lf"][0] for la in layers] for p in POS])
        im = ax.imshow(heat, vmin=0, vmax=1, cmap="viridis", aspect="auto")
        for pi, p in enumerate(POS):
            for li, la in enumerate(layers):
                s = m["readers"][w]["switch"][f"{p}|{la}|swap"]["switch"][0]
                ax.text(li, pi, f"{s:.2f}".lstrip("0") if s < 1 else "1", ha="center", va="center", fontsize=7,
                        color="white" if heat[pi, li] < 0.6 else "black")  # fmt: skip
        ans = m["answer"][w]["layer"]
        if ans is not None:
            ax.axvline(float(np.interp(ans, layers, range(len(layers)))), color="#d62728", ls="--", lw=1.4)
        for pi, p in ((2, "P3"), (1, "P2")):
            pk = m["rules"][w][p].get("peak")
            if pk is not None:
                ax.add_patch(plt.Rectangle((layers.index(pk) - 0.5, pi - 0.5), 1, 1, fill=False, ec="#d62728", lw=1.6))
        ax.set_yticks(range(len(POS)), [f"{p}" for p in POS])
        ax.set_xticks(range(len(layers)), [str(la) for la in layers], fontsize=7)
        ax.set_xlabel("layer")
        ax.set_title(f"{w}: through-the-lens probe (heat), his swap's switch (number)", fontsize=9)
    fig.colorbar(im, ax=axes[0, :].tolist(), shrink=0.8, label="probe accuracy (locker-first)")
    name = next((n for t, _, n in S.MODELS if t == m["target"]), m["target"])
    fig.suptitle(f"51.10 {name}: the intermediate at P1 / P2 / P3 (n = {m['n']}; dashed: the answer digit's layer, "
                 "box: the read peak). UNVERIFIED.", x=0.01, ha="left", fontsize=10)  # fmt: skip
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.10: does the intermediate pass through J-space? Read / write per position, per reader", "",
             f"Batch 51, test 51.10 (jobs/c3/batch51.yaml addendum_2; {QUESTION}, Dan: {answer}). Main-test items, "
             "chat; read statistics on every item of the run, decided on 49.1's locker-first items (the write and remove "
             f"arms' items); cluster bootstrap over the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             "Rules (fixed in advance):", "", *[f"- {k}: {v}." for k, v in RULE.items()], "",
             "As computed: the answer layer = per reader the lower median over the locker-first O prompts of the layer "
             "from which O's answer is the plain logit lens's top token at P3 through the last layer; 'before' = cached "
             "layers strictly below it; lens top-5 = the share of the locker-first O and S rows whose own bridge entity "
             "ranks <= 5 among the letter tokens by his lens logits; the probes' accuracy on the locker-first rows (O "
             "and S, out of fold, folds by scene); the read peak = the layer before the answer with the highest "
             "through-the-lens accuracy (ties: the earliest); write at the read peak (the best layer beside), the "
             "passing arm's own random twin <= 0.10; (d) before (a)-(c); P2 uses P3's answer layer. Point estimates "
             "decide (EPS 1e-9).", "",
             "| model | reader | answer layer | P3 first readable | P3 peak: swap / whole | P3 label | P2 first readable | "
             "P2 peak: swap / whole | P2 label |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | | | | |")
            continue
        lines += summary_rows(m)
    for m in models:
        if m["status"] != "tested":
            continue
        lines += ["", f"## {m['target']} ({m['run']}, L{m['L']}, n = {m['n']} locker-first of {m['n_read']} read)", "",
                  f"![{m['target']}](jread_{m['target']}.png)", ""]  # fmt: skip
        for w in ("lookup", "recall"):
            a = m["answer"][w]
            lines += [f"### {w}: answer layer L{a['layer']} (quartiles {a['quartiles']}; never settled {a['never']} of "
                      f"{a['n']}; S's prompts L{a['S_layer']})", ""]  # fmt: skip
            for p in ("P3", "P2"):
                r = m["rules"][w][p]
                lines.append(f"- {p}: **{r['label']}**; read {r['read']}, write {r['write']} (with his rotated control "
                             f"as the swap's twin: {r.get('write_with_his_rotated_control')}), peak L{r['peak']}, first "
                             f"readable {r['first_readable']} (before the answer: {r['first_readable_before_answer']}); "
                             f"at the peak {json.dumps(r.get('at_peak'))}; best layer L{r.get('best_layer')} "
                             f"{json.dumps(r.get('at_best'))}")  # fmt: skip
            lines += ["", "| pos | layer | thru | full | out | chance | top1 | top5 | other top5 | "
                      + " | ".join(WRITE_ARMS) + " | loss swap / whole |", "|" + "---|" * (10 + len(WRITE_ARMS))]  # fmt: skip
            for p in POS:
                for la in m["layers"]:
                    c = m["read"]["cells"][f"{w}|{p}|{la}"]
                    sw = m["readers"][w]["switch"]
                    lo = m["readers"][w]["loss"]
                    loss = (f"{lo.get(f'{p}|{la}|swap', float('nan')):.2f} / {lo.get(f'{p}|{la}|whole', float('nan')):.2f}"
                            if p != "P3" else "-")  # fmt: skip
                    lines.append(f"| {p} | {la} | {fmt(c['thru']['lf'])} | {fmt(c['full']['lf'])} | {fmt(c['out']['lf'])} | "
                                 f"{c['thru']['chance_lf']:.2f} | {fmt(c['lens']['top1'])} | {fmt(c['lens']['top5'])} | "
                                 f"{fmt(c['lens']['other_top5'])} | "
                                 + " | ".join(fmt(sw[f"{p}|{la}|{a}"]["switch"][0]) for a in WRITE_ARMS) + f" | {loss} |")  # fmt: skip
        rem = m["removal"]
        lines += ["", "Removal at P3 (O; kept = O's answer; cost = kept(random) - kept(removal)):", "",
                  "| reader | peak | band | none | ko | ko_rand | jrm | jrm_rand | cost ko | cost jrm |",
                  "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for w, x in rem.items():
            lines.append(f"| {w} | L{x['peak']} | {x['band']} | " + " | ".join(fmt(x["kept"][a]) for a in REMOVE_ARMS)
                         + f" | {fmt(x['cost_ko'])} | {fmt(x['cost_jrm'])} |")  # fmt: skip
        if m["x49"]:
            lines += ["", f"P1 at L{m['L']} beside 49.1 (same items):", ""]
            for w, res in m["x49"].items():
                lines.append(f"- {w}: " + "; ".join(f"{a} {fmt(v['ours'])} vs {v['x49_arm']} {fmt(v['x49'])} (agree "
                                                    f"{v['agree'][0]}/{v['agree'][1]})" for a, v in res.items()))  # fmt: skip
        lines.append(f"- shares of ||Δ||^2 (median per position): {json.dumps(m['shares_median'])}; the swap's share "
                     f"capped at 1 for its random twin on {m['swap_share_capped'][0]} of {m['swap_share_capped'][1]} rows; "
                     f"the read folder's P3 peaks {m['read_folder_peaks']} (match the run's: {m['peak_matches_run']})")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".",
              "Probe inputs: " + "; ".join(f"{k} = {v}" for k, v in INPUT_TEXT.items()) + "."]  # fmt: skip
    return lines


def stage_verdict(
    runs: dict[str, str] | None = None, n_boot: int = X.N_BOOT, coverage: bool = False, prefix: str | None = None
) -> Path:
    """51.10's verdict (sealed until Q51.10), or with coverage (batch 52 / 53) the same rules on COVERAGE_RUNS, no seal
    guard, "no prediction" in place of Dan's answer, written to <prefix>-<UTC>/ (default x52_jread; x51_10 without
    coverage)."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else unsealed()
    runs = runs or (COVERAGE_RUNS if coverage else RUNS)
    models = [model_result(t, runs[t], n_boot) for t in (runs if coverage else MODELS)]
    prefix = prefix or ("x52_jread" if coverage else "x51_10")
    out = RESULTS / f"{prefix}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if coverage:
        batches = " / ".join(str(b) for b in sorted({COVERAGE_BATCH.get(t, 52) for t in runs}))
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", f"batch {batches} coverage, ")
    labels = {m["target"]: {w: {p: m["rules"][w][p]["label"] for p in ("P3", "P2")} for w in m["rules"]}
              for m in models if m["status"] == "tested"}  # fmt: skip
    slim = [{k: v for k, v in m.items() if k != "read"} for m in models]
    (out / "verdict.json").write_text(json.dumps({"dan": answer, "rule": RULE, "labels": labels, "models": slim},
                                                 indent=1, ensure_ascii=False) + "\n")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    for m in models:
        if m["status"] == "tested":
            figure(m, out / f"jread_{m['target']}.png")
    print("\n".join(lines))
    print(out)
    return out


# ---- view (CPU, sealed): the verify pack with the dumbest-ways checks ----------------------------------------------


def dumbest_lines(m: dict) -> list[str]:
    """The brief's four checks, per reader."""
    lines = ["### Dumbest ways to be wrong", "",
             "1. The probe's classes leak through the question text (identical in O and S: no) or the locker sentences' "
             "order: whole scenes are held out (a scene's O and S rows in one fold); O and S rows share the context's "
             "entities, so a context-only feature cannot tell O's label from S's. Per variant, at each reader's P3 and P2 "
             "read peak:", ""]  # fmt: skip
    for w in ("lookup", "recall"):
        for p in ("P3", "P2"):
            pk = m["rules"][w][p].get("peak")
            if pk is None:
                continue
            c = m["read"]["cells"][f"{w}|{p}|{pk}"]
            lines.append(f"   - {w} {p} L{pk}: " + "; ".join(f"{k} O {fmt(c[k]['lf_O'])} / S {fmt(c[k]['lf_S'])} (rows "
                                                             f"whose class is unseen in training: {c[k]['lf_class_unseen']} "
                                                             f"of {c[k]['n_lf']})" for k in INPUTS))  # fmt: skip
    lines += ["", "2. The lens readout at P3 in late layers is the digit, not the entity: the rule's ranks are among the "
              "letter tokens (his dictionary; digits are not in it); over the whole vocabulary, the share of P3 rows "
              "whose lens top token is a digit, by layer, against the answer layer:", ""]  # fmt: skip
    for w in ("lookup", "recall"):
        cur = [f"L{la} {fmt(m['read']['cells'][f'{w}|P3|{la}']['lens']['full_top_digit'])}" for la in m["layers"]]
        lines.append(f"   - {w} (answer L{m['answer'][w]['layer']}): " + ", ".join(cur))
    lines += ["", "3. His swap at P3 moves the digit rather than the entity: switched to S's answer vs changed to another "
              "digit, separately (all cached layers; the read peak marked *):", ""]  # fmt: skip
    for w in ("lookup", "recall"):
        sw = m["readers"][w]["switch"]
        for a in ("swap", "jpp1", "jpp2", "whole"):
            pk = m["rules"][w]["P3"].get("peak")
            lines.append(f"   - {w} {a}: " + ", ".join(
                f"L{la}{'*' if la == pk else ''} {sw[f'P3|{la}|{a}']['switch'][0]:.2f}/{sw[f'P3|{la}|{a}']['other_digit']:.2f}"
                for la in m["layers"]))  # fmt: skip
    lines += ["", "4. The whole-state patch at P3 at late layers switches trivially: the ratio is read at the read peak, "
              "not at the max:", ""]  # fmt: skip
    for w in ("lookup", "recall"):
        for p in ("P3", "P2"):
            r = m["rules"][w][p]
            if r.get("peak") is None:
                continue
            ratios = {a: v["ratio"] for a, v in r["at_peak"]["arms"].items()}
            best = {a: v["ratio"] for a, v in r["at_best"]["arms"].items()}
            lines.append(f"   - {w} {p}: at the read peak L{r['peak']} whole {r['at_peak']['whole']:.2f}, ratios "
                         f"{json.dumps(ratios)}; at the best layer L{r['best_layer']} ratios {json.dumps(best)}; the "
                         f"whole patch's max over layers {r['whole_max']:.2f}")  # fmt: skip
    return [*lines, ""]


def view_lines(
    m: dict, decode, k_prompts: int = N_PROMPTS, k_rows: int = N_ROWS, seed: int = X.EXAMPLES_SEED
) -> list[str]:
    src = RESULTS / m["run"]
    items = [it for it in X.read_jsonl(src / "cases.jsonl") if it["lf"]]
    by_scene = {it["scene"]: it for it in items}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    rem = X.read_jsonl(src / "removal.jsonl") if (src / "removal.jsonl").exists() else []
    lines = [f"## {m['target']}: {m['run']} ({len(items)} locker-first items)", "",
             f"### {min(k_prompts, len(items))} rendered prompts (seed {seed}); ⟦P1:…⟧ ⟦P2:…⟧ ⟦P3:…⟧ the positions", ""]  # fmt: skip
    for i in G.example_indices(len(items), k_prompts, seed):
        it = items[i]
        lines += [f"#### {it['scene']} ({it['domain']}): bridge {it['entity']} (O) → {it['cf_bridge']} (S)", ""]
        for w in X.READERS:
            for v in VARIANTS:
                lines += [f"{READER_NAME[w]}, {'O' if v == 'org' else 'S'} as read:", "", "```", as_read(decode, it, w, v),
                          "```", ""]  # fmt: skip
    lines += dumbest_lines(m)
    for arm_set, data, cols in ((WRITE_ARMS, rows, "pos | layer"), (REMOVE_ARMS, rem, "peak | band")):
        for a in arm_set:
            mine = [r for r in data if r["arm"] == a]
            pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
            lines += [f"### {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                      f"| scene | reader | {cols} | O's answer | S's answer | top token | switched | other digit |",
                      "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
            for j in pick:
                r = mine[j]
                rd = by_scene[r["scene"]]["readers"][r["reader"]]
                where = f"{r['pos']} | {r['layer']}" if "pos" in r else f"{r['peak']} | {r['band']}"
                lines.append(f"| {r['scene']} | {READER_NAME[r['reader']]} | {where} | {rd['answer']} | {rd['cf_answer']} "
                             f"| {decode([r['top']])!r} | {r['switched']} | {r['other_digit']} |")  # fmt: skip
            lines.append("")
    return lines


def stage_view(runs: dict[str, str] | None = None, decode_for=None, n_boot: int = X.N_BOOT) -> Path:
    from scripts import x47_atoms as A

    unsealed()
    runs = runs or RUNS
    out = RESULTS / f"x51_10-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.10 view (verify pack): prompts as the model reads them (the digit's space token appended), 10 random "
             "rows per arm, the dumbest-ways checks. UNVERIFIED.", ""]  # fmt: skip
    for t in MODELS:
        m = model_result(t, runs[t], n_boot)
        if m["status"] != "tested":
            lines += [f"## {t}: {runs[t]} {m['status']}", ""]
            continue
        lines += view_lines(m, (decode_for or A.default_decode)(t))
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "read", "verdict", "view"])
    ap.add_argument("--name", help="run / read: the run name (results/x51_jread/<name>/)")
    ap.add_argument("--why", default="batch 51, test 51.10 (jobs/c3/batch51.yaml addendum_2; Q51.10): read / write per "
                    "position; sealed")  # fmt: skip
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--runs", nargs=3, default=None, metavar=("9B", "27B", "MUSE"),
                    help=f"verdict / view: runs in place of the specs' {[RUNS[t] for t in MODELS]}")  # fmt: skip
    ap.add_argument("--coverage", action="store_true", help=f"verdict: the coverage runs ('{NO_PREDICTION}')")
    ap.add_argument("--prefix", default=None, help="verdict: the folder's prefix (default x52_jread with --coverage)")
    a = ap.parse_args()
    runs: dict[str, str] | None = {str(t): str(r) for t, r in zip(MODELS, a.runs, strict=True)} if a.runs else None
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "read":
        assert a.name, "read needs --name"
        stage_read(a.name, a.n_boot)
    elif a.stage == "view":
        stage_view(runs, n_boot=a.n_boot)
    else:
        stage_verdict(runs, n_boot=a.n_boot, coverage=a.coverage, prefix=a.prefix)


if __name__ == "__main__":
    main()
