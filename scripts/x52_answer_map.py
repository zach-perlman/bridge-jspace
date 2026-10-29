"""x52_answer_map (batch 52, part B; jobs/c3/batch52.yaml `brief:` B, Dan 29 Oct 00:30; the rules are fixed in advance
by the brief; no prediction, per the addendum): where can the lens read the answer, and can it write it?

Datasets (each reader's O prompt as its source run reads it):
  main  our main test: every item of the model's X0 run at L (x51_jread.select: 51.10's / 51.12 e1's 200 items; X0's
        chat read, the digit's space token appended); readers lookup (PP) and recall (PM).
  z2    Zach's never-named passages: the stored x50 Z2 run's chosen passages (x51_answer.z2_items: rebuilt by
        x50_zach.encode, checked id by id, the source gate asserted); readers K (lookup) and M (recall); x50's read
        (the top token after the prompt, no prefill).

Token groups, per reader (B, E, Q, T):
  B  the bridge word. main: X0's bridge position (51.10's P1). z2: the description's last token in the question (his
     edit site; x50 Z2's patch token: the bridge is never named).
  E  the item's earlier mention: the last token of the bridge entity's last whole-word mention (case-insensitive)
     before the bridge word. main: its locker sentence ("The locker of iota is two"), on the items where it comes
     before the pick (in O the bridge is mentioned nowhere else); items without one have no E cell. z2: its name in the
     passage before the question (K: its fact sentence, M: the sentence that mentions it).
  Q  the question. main: the question's "pick" token (51.10's P2). z2: the question's closing "?" (the description,
     which names the bridge in the question, is B).
  T  the last token (the read position). main: the appended space token (51.10's P3). z2: the prompt's last token.

Layers: every second layer from L0 through the J++ lens's last source layer (9B L0-L30, 27B L0-L62, Muse L0-L50; the
run keeps those in lens.source_layers and records them).

Read (stage run, GPU: one forward per prompt, O and S, both readers): the block outputs at B / E / Q / T at every
cached layer (states.npz, fp16, gitignored); on O, per group and layer, the J++ readout over the full vocabulary
(JLens.readout): the rank (1 + tokens with a strictly higher lens logit) of (i) the bridge entity (its best first token
over the name's variants: x51_answer.variant_ids, 51.12's bridge rank) and (ii) the reader's answer word (its best
A-style token: x51_answer.word_ids, 51.12's readout check: main the number word's one-letter-token variants, "six" for
6; z2 the first token of the answer word and its variants); beside: S's answer word on O (a same-type distractor), the
answer token as read (main: the digit), the lens top token, and the plain logit lens's rank of the answer word. At T,
on O, the plain logit lens (model.unembed of the block output) at every layer: its top token and the answer's rank.
The answer layer ("the layer at which the plain logit lens first has the answer on top"): per item the first layer at
which the plain logit lens's top token at T is the answer as read (tok_A); per reader the lower median over the items
(items where it never is: counted, left out).

Write (stage write, GPU): per reader, at the group and layer where the answer is most readable (the largest share of
items with the answer word in the lens top-5 among cells before the answer layer; ties: the lower median rank, then
the earlier layer, then the order B, E, Q, T), on O, added at that position and layer (X0's AddRows), each read as the
source reads:
  ans1 / ans2    s x u and 2 s x u: u = the unit sum of the J++ lens directions (JLens.vectors(layer, ids), unit rows:
                 51.12's answer atoms) of S's answer word's tokens (the answer a real change would give); s = ||Δ|| at
                 that position and layer, Δ = h_S - h_O, the real change there (where Δ is ~0 because the position comes
                 before O and S differ: the bridge word's ||Δ|| at the same layer, flagged)
  rand1 / rand2  the same sizes along u turned by the layer's random rotation (X0's random basis, seed 888 + layer;
                 51.10's swap_rot): a random part of the same size
  freq1 / freq2  the same sizes along F's unit sum: per token of S's answer word one unrelated letter token with its BPE
                 id within a factor 2 and the closest J++ readout norm (x51_answer.freq_match, 51.12's control)
  whole          Δ (the whole state patched there; the upper bound, beside)
switch = the top token is S's answer's first token (the written answer); changed = the top token is not O's.

Rules (Dan, fixed in advance; per reader, per dataset, per model; point estimates decide, EPS 1e-9):
  readable  the answer word in the lens top-5 on >= 0.5 of items at some layer before the answer layer (any group)
  usable    writing its directions changes the answer on >= 0.3 of items with the random control <= 0.10 (at gain 1
            or 2: ans_g >= 0.3 with rand_g <= 0.10; "changes the answer" = switches to the written answer; "changed
            away from O's" and the frequency-matched part beside)
  the four combinations: readable and usable / readable, not usable / usable, not readable / neither.
Cluster-bootstrap CIs over the bridge entities (10,000, seed 0) beside. No prediction (addendum): the verdict writes
"rule fixed in advance in jobs/c3/batch52.yaml (B); no prediction". UNVERIFIED until hand-checked.

uv run python scripts/x52_answer_map.py plan                                                     # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x52_answer_map.py run --set main --name qwen35_9b_x52_read_main   # GPU
BJ_TARGET=qwen3.5-9b uv run python scripts/x52_answer_map.py write --set main --name qwen35_9b_x52_write_main \
    --read qwen35_9b_x52_read_main                                                               # GPU, after the read
uv run python scripts/x52_answer_map.py verdict                                                  # CPU: map, rules, figure, view
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import statistics
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x51_answer as A

EXP = "x52_answer_map"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch52.yaml"
NO_PREDICTION = "rule fixed in advance in jobs/c3/batch52.yaml (B); no prediction"
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
# batch 52 C coverage (amendment 3, extra c): Lightning, the main set only (Zach's Z2 never ran there); verdict
# --coverage reads it alone, the three models' verdict unchanged
COVERAGE_MODELS = ("nemotron-3.5-lightning",)
TAGS = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "nemotron-3.5-lightning": "lightning"}
NAMES = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B", "muse-glimmer-30b": "Muse-Glimmer-30B",
         "nemotron-3.5-lightning": "Nemotron-3.5-Lightning"}  # fmt: skip
SETS = ("main", "z2")
SET_TEXT = {"main": "our scenes (the main test)", "z2": "his passages (Z2, never-named bridge)"}
STAGES = ("read", "write")
GROUPS = ("B", "E", "Q", "T")
GROUP_NAME = {"B": "bridge word", "E": "earlier mention", "Q": "question", "T": "last token"}
GROUP_TEXT = {
    "main": {"B": "the bridge word (X0's position, 51.10's P1)",
             "E": "the bridge entity's last mention before the bridge word (its locker sentence), where there is one",
             "Q": "the question's 'pick' token (51.10's P2)", "T": "the appended space token (51.10's P3)"},
    "z2": {"B": "the description's last token in the question (his edit site)",
           "E": "the bridge entity's last mention in the passage before the question",
           "Q": "the question's closing '?'", "T": "the prompt's last token (no prefill)"},
}  # fmt: skip
VARIANTS = ("org", "alt")
READER_NAME = A.READER_NAME  # PP / K: lookup, PM / M: recall
WHO = ("lookup", "recall")
RANK_SETS = ("bridge", "ans", "ans_S", "tokA", "bridge_whole", "ans_whole")  # J++ ranks per cell; ans decides
RANK_TEXT = {"bridge": "the bridge entity (51.12's: the first token of each variant of its name)",
             "ans": "the reader's answer word (51.12's A-style tokens; decides)",
             "ans_S": "S's answer word on O (a same-type distractor; baseline)",
             "tokA": "the answer token as read (main: the digit)",
             "bridge_whole": "the bridge entity, whole-word variants only (no fragment such as 'I' for 'Iota')",
             "ans_whole": "the answer word, whole-word variants only (no fragment such as 'G' for 'Greece')"}  # fmt: skip
ARMS = ("whole", "ans1", "ans2", "rand1", "rand2", "freq1", "freq2")
GAINS = (1, 2)
ARM_TEXT = {
    "none": "O unedited",
    "whole": "Δ = h_S - h_O added at the cell (the whole state patched; the upper bound, beside)",
    "ans1": "s u: u the unit sum of the J++ lens directions of S's answer word's tokens, s = ||Δ|| at the cell",
    "ans2": "2 s u",
    "rand1": "s u R^T (R: X0's random basis at the layer, seed 888 + layer): a random part of the same size",
    "rand2": "2 s u R^T",
    "freq1": "s u_F: F per answer token one unrelated letter token, BPE id within a factor 2, closest J++ readout norm",
    "freq2": "2 s u_F",
}  # fmt: skip
TOP_K, TOP50 = 5, 50
READ_SHARE = 0.5  # readable: top-5 on >= 0.5 of items before the answer layer
USE_SWITCH, USE_RAND = 0.3, 0.10  # usable
EPS = 1e-9
SIZE_TOL = 1e-3  # ||Δ|| below this share of ||h_O||: the position comes before O and S differ
CHUNK = 256
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0
STATES_FILE, RANKS_FILE = "states.npz", "ranks.npz"
RULE = {
    "readable": "“Readable”: the answer word in the lens top-5 on ≥ 0.5 of items at some layer before "
                "the answer layer.",
    "usable": "“Usable”: writing its directions changes the answer on ≥ 0.3 of items with the random "
              "control ≤ 0.10.",
    "combinations": "Report the four combinations per reader, per dataset.",
}  # fmt: skip
COMBO = {(True, True): "readable and usable", (True, False): "readable, not usable",
         (False, True): "usable, not readable", (False, False): "neither"}  # fmt: skip


def run_name(stage: str, set_name: str, target: str) -> str:
    """Live prefixes: 9B qwen35_9b_x52_<stage>_<set>, 27B x52_<stage>_<set>_27b, Muse muse30_x52_<stage>_<set>."""
    prefix = pins.TARGETS[target]["run_prefix"]
    return f"{prefix}x52_{stage}_{set_name}" + ("" if prefix else f"_{TAGS[target]}")


def spec_id(stage: str, set_name: str, target: str) -> str:
    return f"x52_{stage}_{set_name}_{TAGS[target]}"


def layers_for(n_layers: int) -> tuple[int, ...]:
    """Every second layer from L0 through n_layers - 2 (the J++ lenses' last source layer)."""
    return tuple(range(0, n_layers - 1, 2))


# ---- positions and items (tokenizer only, CPU-testable) ------------------------------------------------------------


def earlier_mention(text: str, offsets: list, name: str, before: int) -> int | None:
    """The last token of the last whole-word, case-insensitive mention of `name` in text[:before]; None if none."""
    from scripts import statement_positions as SP

    hits = list(re.finditer(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text[:before], flags=re.IGNORECASE))
    if not hits:
        return None
    toks = SP.tokens_in([tuple(o) for o in offsets], hits[-1].start(), hits[-1].end())
    return toks[-1] if toks else None


def question_mark(text: str, offsets: list, question: str) -> int | None:
    """The token holding the question's closing '?' (the question's last occurrence in the text)."""
    from scripts import statement_positions as SP

    if question not in text or "?" not in question:
        return None
    at = text.rindex(question) + question.rindex("?")
    toks = SP.tokens_in([tuple(o) for o in offsets], at, at + 1)
    return toks[-1] if toks else None


def reader_tokens(tok, set_name: str, rd: dict, entity: str, cf_entity: str) -> dict[str, list[int]]:
    """The token sets ranked per cell: the reader's answer word and S's (51.12's A-style tokens: main the number word's
    one-letter-token variants, z2 the first token of the answer word's variants), the bridge entities' first tokens
    (51.12's bridge rank), the answer token as read; beside, the whole-word variants alone (one token each)."""
    num = set_name == "main"
    word = A.number_word if num else str
    return {"ans": A.word_ids(tok, [word(rd["answer"])], num), "ans_S": A.word_ids(tok, [word(rd["cf_answer"])], num),
            "bridge": A.variant_ids(tok, [entity]), "bridge_S": A.variant_ids(tok, [cf_entity]),
            "tokA": [int(rd["tok_A"])], "bridge_whole": A.word_ids(tok, [entity], True),
            "ans_whole": A.word_ids(tok, [word(rd["answer"])], True)}  # fmt: skip


def main_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    """main: 51.10's items (x51_jread.select: every item of the X0 run at L, with P1 / P2 / P3 in O and S) with E."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import x49_gain as G
    from scripts import x51_jread as J

    items, counts = J.select(tok, target)
    out, why = [], collections.Counter()
    for it in items:
        readers = {}
        for w in X.READERS:
            rd = it["readers"][w]
            text = rd["text"]["org"]
            enc = raw_encoding(tok, text, offsets=True)
            assert list(enc["input_ids"]) == rd["ids"]["org"], f"{it['scene']} {w}: the rendered prompt's ids differ"
            jp = it["jpos"][w]
            p1 = jp["P1"]["org"]
            e = earlier_mention(text, enc["offset_mapping"], it["entity"], enc["offset_mapping"][p1][0])
            ids = rd["ids"]
            e_alt = e if e is not None and len(ids["alt"]) > e and ids["alt"][e] == ids["org"][e] else None
            if w == X.LOOKUP:  # E is the same for both readers (their prompts agree through the bridge word)
                why[f"E {'found' if e is not None else 'none before the bridge word'}"] += 1
            pos ={"org": {"B": p1, "E": e, "Q": jp["P2"]["org"], "T": jp["P3"]["org"]},
                   "alt": {"B": jp["P1"]["alt"], "E": e_alt, "Q": jp["P2"]["alt"], "T": jp["P3"]["alt"]}}  # fmt: skip
            readers[w] = {"ids": ids, "suffix": it["space"], "pos": pos, "question": rd["question"],
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")},
                          "toks": reader_tokens(tok, "main", rd, it["entity"], it["cf_bridge"])}  # fmt: skip
        out.append({"set": "main", "key": it["scene"], "scene": it["scene"], "entity": it["entity"],
                    "cf_entity": it["cf_bridge"], "domain": it["domain"], "lf": it["lf"], "readers": readers})  # fmt: skip
    gate = G.source_gate(G.SOURCES[target])
    g = {"pass": bool(G.gate_passes(gate)), "source": G.SOURCES[target], "gate": gate}
    return out, g, {**counts, "earlier_mention": dict(why)}


def z2_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    """z2: 51.12's items (x51_answer.z2_items: the stored Z2 run's chosen passages, rebuilt and checked id by id) with
    each reader's O prompt re-rendered for E and Q (checked against the stored ids)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import x50_zach as Z

    items, gate, counts = A.z2_items(tok, target)
    passages: dict[tuple[str, str], dict] = {}
    for s in sorted({it["key"].split("|", 1)[0] for it in items}):
        ps, _ = Z.load_pairs(s, "z2")
        passages.update({(s, p[Z.LOOKUP]["scene"]): p for p in ps})
    out, why = [], collections.Counter()
    for it in items:
        p = passages[tuple(it["key"].split("|", 1))]  # type: ignore[index]
        readers = {}
        for w in Z.READERS:
            rd, src = it["readers"][w], p[w]
            text = Z.render(tok, src, src["context"], src["question"])
            enc = raw_encoding(tok, text, offsets=True)
            ids = rd["ids"]
            assert list(enc["input_ids"]) == ids["org"], f"{it['key']} {w}: the rendered prompt's ids differ"
            assert len(ids["org"]) == len(ids["alt"]), f"{it['key']} {w}: O and S differ in length"
            q0 = text.rindex(src["question"])
            e = earlier_mention(text, enc["offset_mapping"], it["entity"], q0)
            q = question_mark(text, enc["offset_mapping"], src["question"])
            if q is not None and q <= rd["pos"]:
                q = None
            why[f"{w}: E {'found' if e is not None else 'none'}"] += 1
            why[f"{w}: Q {'found' if q is not None else 'none'}"] += 1
            org = {"B": rd["pos"], "E": e, "Q": q, "T": len(ids["org"]) - 1}
            readers[w] = {"ids": ids, "suffix": [], "pos": {"org": org, "alt": dict(org)},
                          "question": src["question"], "cf_question": rd["cf_question"], "tok_lure": rd["tok_lure"],
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")},
                          "toks": reader_tokens(tok, "z2", rd, it["entity"], it["cf_entity"])}  # fmt: skip
        out.append({"set": "z2", "key": it["key"], "scene": it["scene"], "entity": it["entity"],
                    "cf_entity": it["cf_entity"], "source_set": it["source_set"], "lf": None, "readers": readers})  # fmt: skip
    return out, gate, {**counts, "positions": dict(why)}


BUILD = {"main": main_items, "z2": z2_items}


def readers_of(items: list[dict]) -> tuple[str, str]:
    """The set's reader keys in (lookup, recall) order."""
    ks = tuple(items[0]["readers"])
    return tuple(sorted(ks, key=lambda w: WHO.index(READER_NAME[w])))  # type: ignore[return-value]


def marked(decode, ids: list[int], marks: dict[int, str]) -> str:
    out = []
    for i, t in enumerate(ids):
        out.append(f"⟦{marks[i]}:{decode([t])}⟧" if i in marks else decode([t]))
    return "".join(out)


def as_read(decode, it: dict, w: str, v: str = "org") -> str:
    rd = it["readers"][w]
    ids = rd["ids"][v] + rd["suffix"]
    marks: dict[int, str] = {}
    for g in GROUPS:
        q = rd["pos"][v][g]
        if q is not None:
            marks[q] = "+".join(x for x in (marks.get(q), g) if x)
    return marked(decode, ids, marks)


def stage_plan(plan_dir: str | None = None, k_prompts: int = N_PROMPTS) -> Path:
    """Tokenizer and stored runs only: per set the items after every filter, the source gate, the positions found,
    the token sets' sizes, the layers, forwards and reads, k rendered prompts (seed 0) with B / E / Q / T marked."""
    from bridge_jspace.utils import git_state
    from scripts import x45m

    target = pins.TARGET
    assert target in MODELS, f"x52 runs on {MODELS}, not {target}"
    tok = x45m.tokenizer()
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    n_layers = pins.TARGETS[target]["n_layers"]
    for s in SETS:
        items, gate, counts = BUILD[s](tok, target)
        rds = readers_of(items)
        present = {f"{READER_NAME[w]}|{g}": sum(it["readers"][w]["pos"]["org"][g] is not None for it in items)
                   for w in rds for g in GROUPS}  # fmt: skip
        sizes = {f"{READER_NAME[w]}|{k}": A.size_summary([len(it["readers"][w]["toks"][k]) for it in items])
                 for w in rds for k in ("ans", "ans_S", "bridge", "ans_whole", "bridge_whole")}  # fmt: skip
        e_tokens = collections.Counter(decode([it["readers"][w]["ids"]["org"][it["readers"][w]["pos"]["org"]["E"]]])
                                       for it in items for w in rds if it["readers"][w]["pos"]["org"]["E"] is not None)  # fmt: skip
        q_tokens = collections.Counter(decode([it["readers"][w]["ids"]["org"][it["readers"][w]["pos"]["org"]["Q"]]])
                                       for it in items for w in rds if it["readers"][w]["pos"]["org"]["Q"] is not None)  # fmt: skip
        e_alt_missing = sum(it["readers"][w]["pos"]["org"]["E"] is not None and it["readers"][w]["pos"]["alt"]["E"] is None
                            for it in items for w in rds)  # fmt: skip
        order_ok = sum(all(p[a] < p[b] for a, b in (("E", "B"), ("B", "Q"), ("Q", "T")) if p[a] is not None and p[b] is not None)
                       for it in items for w in rds for p in [it["readers"][w]["pos"]["org"]])  # fmt: skip
        chosen = sorted(random.Random(VIEW_SEED).sample(range(len(items)), min(k_prompts, len(items))))
        layers = layers_for(n_layers)
        blob = {"set": s, "target": target, "read_run": run_name("read", s, target), "write_run": run_name("write", s, target),
                "read_spec": spec_id("read", s, target), "write_spec": spec_id("write", s, target), "code": git_state(),
                "source_gate": gate, "counts": counts, "items": len(items), "entities": len({it["entity"] for it in items}),
                "readers": [READER_NAME[w] for w in rds], "positions_present": present,
                "positions_in_order": [order_ok, len(items) * 2], "E_tokens": e_tokens.most_common(20),
                "Q_tokens": q_tokens.most_common(10), "E_found_in_O_not_in_S": e_alt_missing,
                "token_set_sizes": sizes, "items_without_an_answer_word_token": sum(
                    not it["readers"][w]["toks"][k] for it in items for w in rds for k in ("ans", "ans_S")),
                "layers_candidate": list(layers), "n_layers_model": n_layers,
                "forwards_read": len(items) * 2 * 2, "lens_cells": len(items) * 2 * len(GROUPS) * len(layers),
                "reads_write": len(items) * 2 * (1 + len(ARMS)), "locker_first": sum(bool(it["lf"]) for it in items),
                "prompts": [{"key": items[i]["key"], "bridge": f"{items[i]['entity']} -> {items[i]['cf_entity']}",
                             **{f"{READER_NAME[w]}_{v}": as_read(decode, items[i], w, v) for w in rds for v in VARIANTS},
                             "answer_words": {READER_NAME[w]: {k: [decode([t]) for t in items[i]["readers"][w]["toks"][k]]
                                                               for k in ("ans", "ans_S", "bridge")} for w in rds}}
                            for i in chosen]}  # fmt: skip
        stem = f"plan-{s}-{TAGS[target]}"
        (out / f"{stem}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
        lines = [f"# {EXP} plan: {SET_TEXT[s]} on {target} (tokenizer and stored runs only; UNVERIFIED)", "",
                 f"Items {len(items)} ({blob['entities']} bridge entities), source gate pass {gate['pass']}; positions "
                 f"present {present}; in order E < B < Q < T: {order_ok} of {len(items) * 2}; layers {list(layers)}.", "",
                 "Groups: " + "; ".join(f"{g} = {GROUP_TEXT[s][g]}" for g in GROUPS) + ".", ""]  # fmt: skip
        for p in blob["prompts"]:
            lines += [f"## {p['key']}: {p['bridge']}; tokens {json.dumps(p['answer_words'], ensure_ascii=False)}", ""]
            for k, v in p.items():
                if k.endswith(VARIANTS):
                    lines += [f"{k}:", "", "```", v, "```", ""]
        (out / f"{stem}.md").write_text("\n".join(lines) + "\n")
        print(json.dumps({k: v for k, v in blob.items() if k not in ("prompts", "code")}, indent=1, ensure_ascii=False))
    print("wrote", out, flush=True)
    return out


# ---- ranks and the write's vectors (CPU-testable) -------------------------------------------------------------------


def pad(sets: list[list[int]]):
    """[m, k] long tensor of the sets, -1 padding (k >= 1)."""
    import torch

    k = max([1, *(len(s) for s in sets)])
    out = torch.full((len(sets), k), -1, dtype=torch.long)
    for i, s in enumerate(sets):
        if s:
            out[i, : len(s)] = torch.tensor(s, dtype=torch.long)
    return out


def best_rank(logits, ids):
    """Per row of logits [m, V], the rank (1 + tokens with a strictly higher logit) of the row's best token in ids
    [m, k] (-1 padding): the rank of its highest-logit member; -1 for an empty set."""
    import torch

    ids = ids.to(logits.device)
    has = ids >= 0
    vals = logits.gather(1, ids.clamp(min=0)).masked_fill(~has, float("-inf"))
    m = vals.max(1).values
    r = (logits > m[:, None]).sum(1) + 1
    return torch.where(has.any(1), r, torch.full_like(r, -1))


def unit_sum(vecs):
    """The unit vector along the sum of the rows of vecs [m, d] (unit rows: each token weighs the same)."""
    import torch

    return torch.nn.functional.normalize(vecs.float().sum(0), dim=0)


def write_size(h_o, h_s, b_o, b_s) -> tuple[float, bool]:
    """s = ||Δ|| at the cell (Δ = h_S - h_O); where Δ is below SIZE_TOL of ||h_O|| (or S has no such position: h_s None)
    the position comes before O and S differ: the bridge word's ||Δ|| at the same layer, flagged."""
    if h_s is not None:
        d = float((h_s.float() - h_o.float()).norm())
        if d > SIZE_TOL * float(h_o.float().norm()):
            return d, False
    return float((b_s.float() - b_o.float()).norm()), True


def write_vectors(u, u_f, basis, s: float, delta) -> dict[str, Any]:
    """The arms' vectors at one cell: the whole change, the answer directions at s and 2s, their random turn and the
    frequency-matched directions at the same sizes."""
    rot = u @ basis.T
    out = {"whole": delta}
    for g in GAINS:
        out[f"ans{g}"] = g * s * u
        out[f"rand{g}"] = g * s * rot
        out[f"freq{g}"] = g * s * u_f
    return {a: out[a] for a in ARMS}


# ---- the rules and the map's numbers (CPU) --------------------------------------------------------------------------


def first_top(tops, tok: int) -> int | None:
    """The first layer at which the plain logit lens's top token is tok."""
    hit = np.flatnonzero(np.asarray(tops) == tok)
    return int(hit[0]) if hit.size else None


def answer_layer(ll_top: np.ndarray, tok_a: list[int]) -> dict:
    """Per item the first layer with the answer on top at T; the reader's answer layer = their lower median (items
    where it never is: counted, left out); 51.10's settle layer (on top from there through the last layer) beside."""
    from scripts import x51_jread as J

    first = [first_top(t, a) for t, a in zip(ll_top, tok_a, strict=True)]
    settle = [J.settle_layer(list(map(int, t)), a) for t, a in zip(ll_top, tok_a, strict=True)]
    ok, oks = [f for f in first if f is not None], [s for s in settle if s is not None]
    return {"layer": statistics.median_low(ok) if ok else None, "n": len(first), "never": len(first) - len(ok),
            "quartiles": [float(np.percentile(ok, q)) for q in (25, 50, 75)] if ok else None,
            "settle_layer": statistics.median_low(oks) if oks else None, "per_item": first}  # fmt: skip


def readable(top5: Mapping[tuple[str, int], float | None], ans: int | None) -> dict:
    """The rule: some cell (any group) before the answer layer with the answer word in the top-5 on >= 0.5 of items."""
    if ans is None:
        return {"holds": None, "why": "the plain logit lens never has the answer on top", "cells": []}
    cells = sorted(((g, la) for (g, la), v in top5.items() if v is not None and la < ans and v >= READ_SHARE - EPS),
                   key=lambda c: (c[1], GROUPS.index(c[0])))  # fmt: skip
    best = max(((v, g, la) for (g, la), v in top5.items() if v is not None and la < ans), default=None)
    return {"holds": bool(cells), "cells": [list(c) for c in cells], "first": list(cells[0]) if cells else None,
            "best_before": None if best is None else {"group": best[1], "layer": best[2], "top5": best[0]}}  # fmt: skip


def select_cell(top5: Mapping[tuple[str, int], float | None], med: Mapping[tuple[str, int], float | None],
                ans: int | None) -> tuple[str, int] | None:  # fmt: skip
    """Where the answer is most readable before the answer layer: the largest top-5 share; ties: the lower median rank,
    the earlier layer, the order B, E, Q, T. (No answer layer at all: every layer.)"""
    cands = [(g, la) for (g, la), v in top5.items() if v is not None and (ans is None or la < ans)]
    if not cands:
        return None

    def key(c: tuple[str, int]) -> tuple[float, float, int, int]:
        m = med.get(c)
        return -(top5[c] or 0.0), float("inf") if m is None else m, c[1], GROUPS.index(c[0])

    return min(cands, key=key)


def usable(sw: dict[str, float]) -> dict:
    """The rule on point estimates: at gain 1 or 2 the answer directions switch >= 0.3 of items with that gain's random
    control <= 0.10."""
    per = {g: {"ans": sw[f"ans{g}"], "rand": sw[f"rand{g}"],
               "ok": sw[f"ans{g}"] >= USE_SWITCH - EPS and sw[f"rand{g}"] <= USE_RAND + EPS} for g in GAINS}  # fmt: skip
    return {"holds": any(v["ok"] for v in per.values()), "per_gain": per}


def combination(read: bool | None, use: bool | None) -> str | None:
    return None if read is None or use is None else COMBO[(bool(read), bool(use))]


def boot_shares(vals: np.ndarray, ents: list[str], n_boot: int, seed: int = X.BOOT_SEED) -> np.ndarray:
    """Cluster-bootstrap shares [cells, n_boot] of vals [cells, n] (0/1, nan = no such cell for the item): whole
    entities drawn with replacement (X0's draws: the same rng and order as x0_necessity.resampled_rates), each cell's
    share over its present items in the draw."""
    keys = sorted(set(ents))
    index = {e: i for i, e in enumerate(keys)}
    onehot = np.zeros((len(ents), len(keys)))
    onehot[np.arange(len(ents)), [index[e] for e in ents]] = 1.0
    present = ~np.isnan(vals)
    sx, sn = np.nan_to_num(vals) @ onehot, present.astype(float) @ onehot  # [cells, K]
    pick = np.random.default_rng(seed).integers(0, len(keys), size=(n_boot, len(keys)))
    counts = np.zeros((n_boot, len(keys)))
    np.add.at(counts, (np.repeat(np.arange(n_boot), len(keys)), pick.ravel()), 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return ((counts @ sx.T) / (counts @ sn.T)).T


def share_ci(vals: np.ndarray, ents: list[str], n_boot: int) -> list[list[float]]:
    """Per row of vals [cells, n]: [share over present items, 2.5 %, 97.5 %] (nan where no item has the cell)."""
    out = []
    boot = boot_shares(vals, ents, n_boot) if n_boot > 0 else None
    for c in range(vals.shape[0]):
        row = vals[c][~np.isnan(vals[c])]
        if not row.size:
            out.append([math.nan] * 3)
            continue
        lo, hi = X.interval(boot[c]) if boot is not None else (math.nan, math.nan)
        out.append([float(row.mean()), lo, hi])
    return out


def load_run(run: str) -> dict:
    src = RESULTS / run
    z = np.load(src / RANKS_FILE)
    return {"dir": src, "manifest": json.loads((src / "manifest.json").read_text()), "items": X.read_jsonl(src / "cases.jsonl"),
            "ranks": {k: z[k] for k in z.files}, "layers": [int(x) for x in z["layers"]]}  # fmt: skip


def map_numbers(run: dict, n_boot: int) -> dict:
    """One read run's map: per reader the answer layer, and per rank set, group and layer the top-5 / top-50 shares
    (CIs over the bridge entities) and the median rank over the items with that position; the rules' inputs."""
    items, z, layers = run["items"], run["ranks"], run["layers"]
    rds = readers_of(items)
    ents = [it["entity"] for it in items]
    out: dict[str, Any] = {"layers": layers, "n": len(items), "entities": len(set(ents)), "readers": {}}
    for r, w in enumerate(rds):
        name = READER_NAME[w]
        al = answer_layer(z["ll_top"][:, r], [it["readers"][w]["tok_A"] for it in items])
        cells = [(k, g, li) for k in RANK_SETS for g in range(len(GROUPS)) for li in range(len(layers))]
        ranks = np.stack([z[f"lens_{k}"][:, r, g, li] for k, g, li in cells]).astype(float)  # [cells, n]
        ranks[ranks <= 0] = np.nan
        top5 = share_ci(np.where(np.isnan(ranks), np.nan, (ranks <= TOP_K).astype(float)), ents, n_boot)
        top50 = share_ci(np.where(np.isnan(ranks), np.nan, (ranks <= TOP50).astype(float)), ents, n_boot)
        per: dict[str, Any] = {}
        for c, (k, g, li) in enumerate(cells):
            row = ranks[c][~np.isnan(ranks[c])]
            per[f"{k}|{GROUPS[g]}|{layers[li]}"] = {"n": int(row.size), "top5": top5[c], "top50": top50[c],
                                                     "median_rank": float(np.median(row)) if row.size else None}  # fmt: skip
        t5 = {k: {(g, la): per[f"{k}|{g}|{la}"]["top5"][0] if per[f"{k}|{g}|{la}"]["n"] else None
                  for g in GROUPS for la in layers} for k in ("ans", "ans_whole", "ans_S")}  # fmt: skip
        med = {(g, la): per[f"ans|{g}|{la}"]["median_rank"] for g in GROUPS for la in layers}
        cell = select_cell(t5["ans"], med, al["layer"])
        out["readers"][name] = {"answer": {k: v for k, v in al.items() if k != "per_item"}, "cells": per,
                                "readable": readable(t5["ans"], al["layer"]),
                                "readable_whole_words": readable(t5["ans_whole"], al["layer"]),
                                "readable_distractor": readable(t5["ans_S"], al["layer"]),
                                "write_cell": list(cell) if cell else None}  # fmt: skip
    return out


# ---- GPU: the read ---------------------------------------------------------------------------------------------------


def cache_states(model, items: list[dict], layers: tuple[int, ...], n_layers: int) -> dict[str, Any]:
    """Per item, reader and variant one forward of the prompt as read; the block outputs at B / E / Q / T at the cached
    layers [n, 2, 2, 4, L, d] (fp32, CPU) and which positions exist; on O the plain logit lens at T at every layer."""
    import torch

    from bridge_jspace.utils import progress

    dev = model.device
    rds = readers_of(items)
    n, nl = len(items), len(layers)
    hst: Any = None
    mask = np.zeros((n, 2, 2, len(GROUPS)), dtype=bool)
    ll_top = np.zeros((n, 2, n_layers), dtype=np.int64)
    ll_rank = np.zeros((n, 2, n_layers), dtype=np.int64)
    for i, it in enumerate(progress(items, "x52 read: forwards (item: 2 readers x O / S)")):
        for r, w in enumerate(rds):
            rd = it["readers"][w]
            for v, variant in enumerate(VARIANTS):
                rec_at = tuple(range(n_layers)) if variant == "org" else layers
                _, rec = model.run(torch.tensor([rd["ids"][variant] + rd["suffix"]], device=dev), record=rec_at)
                if hst is None:
                    hst = torch.zeros(n, 2, 2, len(GROUPS), nl, rec[layers[0]].shape[-1])
                for gi, g in enumerate(GROUPS):
                    q = rd["pos"][variant][g]
                    if q is None:
                        continue
                    mask[i, r, v, gi] = True
                    for li, la in enumerate(layers):
                        hst[i, r, v, gi, li] = rec[la][q].cpu()  # a copy, not a view (memory lesson 2)
                if variant == "org":
                    t = rd["pos"]["org"]["T"]
                    lg = model.unembed(torch.stack([rec[la][t] for la in range(n_layers)]))
                    a = int(rd["tok_A"])
                    ll_top[i, r] = lg.argmax(1).cpu().numpy()
                    ll_rank[i, r] = ((lg > lg[:, a : a + 1]).sum(1) + 1).cpu().numpy()
                    del lg
                del rec
    return {"h": hst, "mask": mask, "ll_top": ll_top, "ll_rankA": ll_rank}


def lens_ranks(model, lens, items: list[dict], cache: dict, layers: tuple[int, ...]) -> dict[str, np.ndarray]:
    """On O, per group and cached layer: the J++ readout's ranks of each token set (best member), its top token, and
    the plain logit lens's rank of the answer word and top token; -1 where the item has no such position."""
    import torch

    from bridge_jspace.utils import progress

    dev = model.device
    rds = readers_of(items)
    n, ng, nl = len(items), len(GROUPS), len(layers)
    h = cache["h"]
    d = h.shape[-1]
    meta = [(i, r, g) for i in range(n) for r in range(2) for g in range(ng)]
    sets = {k: pad([items[i]["readers"][rds[r]]["toks"][k] for i, r, _ in meta]) for k in RANK_SETS}
    present = torch.tensor([bool(cache["mask"][i, r, 0, g]) for i, r, g in meta])
    keys = [*(f"lens_{k}" for k in RANK_SETS), "lens_top", "logit_ans", "logit_top"]
    out = {k: np.full((n * 2 * ng, nl), -1, dtype=np.int64) for k in keys}
    for li, la in enumerate(progress(layers, "x52 read: J++ ranks (layer)")):
        flat = h[:, :, 0, :, li].reshape(-1, d)
        for s in range(0, flat.shape[0], CHUNK):
            sl = slice(s, s + CHUNK)
            ok = present[sl]
            if not ok.any():
                continue
            x = flat[sl].to(dev)
            full = lens.readout(x, la)
            for k in RANK_SETS:
                out[f"lens_{k}"][sl, li] = best_rank(full, sets[k][sl]).cpu().numpy()
            out["lens_top"][sl, li] = full.argmax(1).cpu().numpy()
            del full
            plain = model.unembed(x)
            out["logit_ans"][sl, li] = best_rank(plain, sets["ans"][sl]).cpu().numpy()
            out["logit_top"][sl, li] = plain.argmax(1).cpu().numpy()
            del plain
            for k in keys:
                out[k][sl, li][~ok.numpy()] = -1
    shaped = {k: v.reshape(n, 2, ng, nl) for k, v in out.items()}
    return {**shaped, "ll_top": cache["ll_top"], "ll_rankA": cache["ll_rankA"], "mask": cache["mask"][:, :, 0],
            "layers": np.array(layers)}  # fmt: skip


def manifest(name: str, stage: str, set_name: str, target: str, extra: dict) -> dict:
    from bridge_jspace.utils import git_state

    return {"exp": EXP, "run": name, "stage": stage, "set": set_name, "set_text": SET_TEXT[set_name],
            "spec": f"jobs/c3/batch52.yaml (brief B); jobs/c3/{spec_id(stage, set_name, target)}.yaml",
            "prediction": NO_PREDICTION, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "groups": GROUP_TEXT[set_name], "rank_sets": RANK_TEXT, "rule": RULE, "arms": ARM_TEXT,
            "seeds": {"random_rotation": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                      "view": VIEW_SEED}, **extra}  # fmt: skip


def rel(p: Path) -> str:
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


def source_files(set_name: str, target: str) -> list[Path]:
    from scripts import x49_gain as G

    src = A.source_of("z2", target) if set_name == "z2" else X.RESULTS / G.SOURCES[target]
    return [SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl"))]


def stage_run(name: str, set_name: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "x52 reads the sources' chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MODELS + COVERAGE_MODELS, f"x52 runs on {MODELS + COVERAGE_MODELS}, not {target}"
    assert target in MODELS or set_name == "main", f"{target}: the main set only (Zach's Z2 never ran there)"
    n_layers = pins.TARGETS[target]["n_layers"]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, "read", set_name, target, {
        "inputs": {rel(p): X.sha256_of(p) for p in source_files(set_name, target) if p.exists()},
        "layers_candidate": list(layers_for(n_layers)), "n_layers": n_layers,
        "storage": f"{STATES_FILE}: fp16 block outputs at B / E / Q / T, O and S, the cached layers (gitignored); "
                   f"{RANKS_FILE}: the ranks (committed)"})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    layers = tuple(la for la in layers_for(n_layers) if la in lens.source_layers)
    assert layers, "the J++ lens has no map at any candidate layer"
    items, gate, counts = BUILD[set_name](model.tokenizer, target)
    tested = bool(gate["pass"]) and bool(items)
    (out / "plan.json").write_text(json.dumps(counts, indent=1, ensure_ascii=False) + "\n")
    (out / "gate.json").write_text(json.dumps({"gate": gate, "tested": tested, "order": [it["key"] for it in items],
                                              "layers": list(layers), "hub_kernels": loaded_hub_kernels()}, indent=1)
                                   + "\n")  # fmt: skip
    X.write_jsonl(out / "cases.jsonl", items)
    if not tested:
        print("not tested: the source run's gate failed or no items; see gate.json", flush=True)
        return out
    with torch.no_grad():  # memory lesson 1
        cache = cache_states(model, items, layers, n_layers)
        ranks = lens_ranks(model, lens, items, cache, layers)
    small: dict[str, Any] = {k: v.astype(np.int32) if v.dtype == np.int64 else v for k, v in ranks.items()}
    np.savez(out / RANKS_FILE, **small)
    h16 = cache["h"].numpy().astype(np.float16)
    assert np.isfinite(h16).all(), "fp16 overflow in the cached states"
    np.savez(out / STATES_FILE, h=h16, mask=cache["mask"], layers=np.array(layers))
    m["layers"] = list(layers)
    m["items"] = len(items)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(
        f"wrote {out}: {len(items)} items x 2 readers, {len(layers)} layers (no label: the verdict reads it)",
        flush=True,
    )
    return out


# ---- GPU: the write --------------------------------------------------------------------------------------------------


def related_keys(tok, items: list[dict]) -> set[str]:
    """51.12's related keys (x51_answer.related_keys) over this set: every answer word and its tokens (O and S, both
    readers), the bridge entities' names and tokens, the bridge word's token in O and S."""
    adapt_items, adapt_toks = [], []
    for it in items:
        rds = it["readers"].values()
        adapt_items.append({"readers": {w: {"ids": rd["ids"], "pos": rd["pos"]["org"]["B"]} for w, rd in it["readers"].items()},
                            "entity": it["entity"], "cf_entity": it["cf_entity"]})  # fmt: skip
        words = [
            A.number_word(x) if it["set"] == "main" else str(x) for rd in rds for x in (rd["answer"], rd["cf_answer"])
        ]
        adapt_toks.append({"A": sorted({t for rd in rds for k in ("ans", "ans_S") for t in rd["toks"][k]}),
                           "A_words": list(dict.fromkeys(words)),
                           "bridge": {"org": next(iter(rds))["toks"]["bridge"], "alt": next(iter(rds))["toks"]["bridge_S"]}})  # fmt: skip
    return A.related_keys(tok, adapt_items, adapt_toks)


def stage_write(name: str, set_name: str, read: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "x52 reads the sources' chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    src = RESULTS / read
    rm = json.loads((src / "manifest.json").read_text())
    assert rm["model"]["target"] == target, f"{read} is a {rm['model']['target']} run, not {target}'s"
    assert rm["set"] == set_name, f"{read} reads {rm['set']}, not {set_name}"
    assert rm["stage"] == "read", f"{read} is not a read run"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, "write", set_name, target, {
        "read_run": read, "inputs": {rel(p): X.sha256_of(p)
                                     for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / RANKS_FILE)},
        "cell_rule": "per reader the (group, layer) before the answer layer with the largest share of items whose answer "
                     "word is in the J++ top-5 (ties: lower median rank, earlier layer, B < E < Q < T), point estimates",
        "size": f"s = ||h_S - h_O|| at the cell; below {SIZE_TOL} x ||h_O|| (the position precedes the change): the "
                "bridge word's ||Δ|| at that layer (flagged)"})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    run = load_run(read)
    numbers = map_numbers(run, n_boot=0)
    items, layers = run["items"], run["layers"]
    rds = readers_of(items)
    cells = {READER_NAME[w]: numbers["readers"][READER_NAME[w]]["write_cell"] for w in rds}
    st = np.load(src / STATES_FILE)
    h, smask = st["h"], st["mask"]

    model = load_model()
    tok, dev = model.tokenizer, model.device
    lens = JLens(model, "jpp")
    letters = model.letter_token_ids()
    lid = letters.cpu().numpy().astype(np.int64)
    keys = [A.key_of(tok.decode([int(t)])) for t in lid]
    banned = A.related_mask(keys, related_keys(tok, items))
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    rows, norms = [], []
    with torch.no_grad():
        for r, w in enumerate(rds):
            cell = cells[READER_NAME[w]]
            if cell is None:
                continue
            g, la = cell
            gi, li = GROUPS.index(g), layers.index(la)
            rn = torch.cat([lens.vectors(la, letters[s : s + A.NORM_CHUNK], unit=False).norm(dim=-1).cpu()
                            for s in range(0, len(letters), A.NORM_CHUNK)])  # fmt: skip
            log_norm = np.log(rn.double().numpy().clip(1e-30))
            basis = SP.random_basis(h.shape[-1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            for i, it in enumerate(progress(items, f"x52 write: {READER_NAME[w]} at {g} L{la} (item)")):
                rd = it["readers"][w]
                a_ids = rd["toks"]["ans_S"]
                if not smask[i, r, 0, gi] or not a_ids:
                    norms.append({"key": it["key"], "reader": w, "skipped": "no such position" if a_ids else
                                  "S's answer word has no letter token"})  # fmt: skip
                    continue
                ho = torch.from_numpy(h[i, r, 0, gi, li].astype(np.float32))
                hs = torch.from_numpy(h[i, r, 1, gi, li].astype(np.float32)) if smask[i, r, 1, gi] else None
                b = GROUPS.index("B")
                s, flagged = write_size(ho, hs, torch.from_numpy(h[i, r, 0, b, li].astype(np.float32)),
                                        torch.from_numpy(h[i, r, 1, b, li].astype(np.float32)))  # fmt: skip
                fm = A.freq_match(a_ids, lid, log_norm, banned)
                u = unit_sum(lens.vectors(la, torch.tensor(a_ids, dtype=torch.long, device=dev)))
                uf = unit_sum(lens.vectors(la, torch.tensor([x["f"] for x in fm], dtype=torch.long, device=dev)))
                delta = (hs - ho).to(dev) if hs is not None else torch.zeros_like(u)
                vecs = write_vectors(u.to(dev), uf.to(dev), basis, s, delta)
                q = rd["pos"]["org"][g]
                edits = [{}] + [{la: AddRows(vecs[a][None].float(), [q])} for a in ARMS]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
                if set_name == "z2":
                    cands = torch.tensor(sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}),
                                         device=dev)  # fmt: skip
                else:
                    cands = digits
                for a, lg in zip(("none", *ARMS), logits, strict=True):
                    x = X.read_row(lg, rd, cands)
                    rows.append({"key": it["key"], "entity": it["entity"], "reader": w, "group": g, "layer": la, "arm": a,
                                 **x, "changed": int(x["top"] != rd["tok_A"])})  # fmt: skip
                norms.append({"key": it["key"], "reader": w, "group": g, "layer": la, "s": round(s, 4),
                              "size_from_bridge_word": flagged, "norm_delta": round(float(delta.norm()), 4),
                              "norm_h": round(float(ho.norm()), 4), "A_ids": a_ids, "F": fm,
                              "cos_u_delta": round(float(u.to(dev) @ delta.float() / delta.norm().clamp_min(1e-12)), 5)})  # fmt: skip
            del basis
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    (out / "cells.json").write_text(json.dumps({"cells": cells, "from": read, "answer": {
        k: v["answer"] for k, v in numbers["readers"].items()}}, indent=1) + "\n")  # fmt: skip
    print(f"wrote {out}: {len(rows)} reads (no label: the verdict reads it)", flush=True)
    return out


# ---- verdict (CPU) ---------------------------------------------------------------------------------------------------


def write_numbers(run_dir: Path, n_boot: int) -> dict:
    """Per reader: the cell, n, every arm's switch and changed shares (cluster-bootstrap CIs, paired), the rule."""
    rows = X.read_jsonl(run_dir / "outcomes.jsonl")
    cells = json.loads((run_dir / "cells.json").read_text())["cells"]
    norms = X.read_jsonl(run_dir / "norms.jsonl")
    out = {}
    for w in dict.fromkeys(r["reader"] for r in rows):
        mine = [r for r in rows if r["reader"] == w]
        by = {(r["key"], r["arm"]): r for r in mine}
        keys = list(dict.fromkeys(r["key"] for r in mine))
        ents = [by[(k, "none")]["entity"] for k in keys]
        arms = ("none", *ARMS)
        sw = {a: [int(by[(k, a)]["switched"]) for k in keys] for a in arms}
        ch = {a: [int(by[(k, a)]["changed"]) for k in keys] for a in arms}
        bs, bc = X.resampled_rates(sw, ents, n_boot), X.resampled_rates(ch, ents, n_boot)
        nm = [n for n in norms if n["reader"] == w and "s" in n]
        out[READER_NAME[w]] = {
            "cell": cells.get(READER_NAME[w]), "n": len(keys), "entities": len(set(ents)),
            "switch": {a: [float(np.mean(v)), *X.interval(bs[a])] for a, v in sw.items()},
            "changed": {a: [float(np.mean(v)), *X.interval(bc[a])] for a, v in ch.items()},
            "rule": usable({a: float(np.mean(v)) for a, v in sw.items()}),
            "size_from_bridge_word": sum(n["size_from_bridge_word"] for n in nm),
            "s_median": float(np.median([n["s"] for n in nm])) if nm else None,
            "skipped": sum("skipped" in n for n in norms if n["reader"] == w)}  # fmt: skip
    return out


def check_51_12(numbers: dict, target: str, set_name: str) -> dict | None:
    """The bridge word at X0's L against 51.12's stored readout check (same items, state and token sets): the answer
    word's top-50 share on O, ours vs 51.12's (r2 runs' readout.jsonl, the reader's own answer word on O)."""
    from scripts import x50_zach as Z

    L = Z.LAYERS[target][0] if set_name == "z2" else X.PREDICTED[target]
    run = A.runs_of("z2" if set_name == "z2" else "e1").get(target)  # 51.12's runs and batch 52's coverage runs
    path = A.RESULTS / run / "readout.jsonl" if run else None
    if path is None or not path.exists() or L not in numbers["layers"]:
        return None
    rows = X.read_jsonl(path)
    out = {"L": L, "run": run}
    for w in READER_NAME:
        name = READER_NAME[w]
        if name not in numbers["readers"] or (set_name == "z2") != (w in ("K", "M")):
            continue
        src = w if set_name == "z2" else X.LOOKUP
        rk = [r["answer_word_rank"].get(w) for r in rows if r["source"] == src and r["variant"] == "org"]
        rk = [x for x in rk if x is not None]
        ours = numbers["readers"][name]["cells"][f"ans|B|{L}"]
        out[name] = {"ours_top50": ours["top50"][0], "x51_12_top50": float(np.mean([x <= TOP50 for x in rk])) if rk else None,
                     "ours_median": ours["median_rank"], "x51_12_median": float(np.median(rk)) if rk else None,
                     "n_ours": ours["n"], "n_x51_12": len(rk)}  # fmt: skip
    return out


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, (int, float)):
        return "-" if v != v else f"{v:.2f}"
    return "-" if v[0] is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(target: str, maps: dict[str, dict | None], writes: dict[str, dict | None], path: Path) -> None:
    """Rows: the token groups; columns: the cached layers; per reader (rows of panels) our scenes and his passages side
    by side, each with a bridge-entity and an answer-word panel. Colour = the median J++ rank (log scale, dark = read
    at the top), a dot where >= 0.5 of items have it in the top-5, a dashed line at the plain logit lens's answer
    layer, a box at the write's cell."""
    import matplotlib.colors as mcolors
    from matplotlib.patches import Rectangle

    from scripts import story_style as S

    plt = S.setup()
    cmap = plt.get_cmap("Blues_r").with_extremes(bad="#e6e6e6")
    norm = mcolors.Normalize(vmin=0.0, vmax=4.0)
    panels = [(s, k) for s in SETS for k in ("bridge", "ans")]
    fig, axes = plt.subplots(2, 4, figsize=(S.WIDTH * 2.0, 7.0), squeeze=False)
    fig.subplots_adjust(hspace=0.6, wspace=0.12, top=0.80)
    im = None
    for row, who in enumerate(WHO):
        for col, (s, k) in enumerate(panels):
            ax = axes[row, col]
            mp = maps.get(s)
            if mp is None or who not in mp["readers"]:
                ax.text(0.5, 0.5, f"{SET_TEXT[s].split(' (')[0]}: pending", ha="center", va="center",
                        transform=ax.transAxes, color="#777777")  # fmt: skip
                ax.axis("off")
                continue
            layers, rr = mp["layers"], mp["readers"][who]
            med = np.array(
                [[rr["cells"][f"{k}|{g}|{la}"]["median_rank"] or np.nan for la in layers] for g in GROUPS], float
            )
            t5 = np.array([[rr["cells"][f"{k}|{g}|{la}"]["top5"][0] for la in layers] for g in GROUPS], float)
            im = ax.imshow(np.ma.masked_invalid(np.log10(np.clip(med, 1, 1e4))), cmap=cmap, norm=norm, aspect="auto")
            ys, xs = np.nonzero(np.nan_to_num(t5) >= READ_SHARE - EPS)
            ax.scatter(xs, ys, s=10, c="white", edgecolors="none", zorder=3)
            ans = rr["answer"]["layer"]
            if ans is not None:
                ax.axvline(float(np.interp(ans, layers, range(len(layers)))), color="#d62728", ls="--", lw=1.3)
            wc = rr.get("write_cell")
            if k == "ans" and wc:
                ax.add_patch(Rectangle((layers.index(wc[1]) - 0.5, GROUPS.index(wc[0]) - 0.5), 1, 1, fill=False,
                                           ec="#e08a1e", lw=1.8, zorder=4))  # fmt: skip
            step = max(1, len(layers) // 8)
            ax.set_xticks(range(0, len(layers), step), [str(la) for la in layers[::step]], fontsize=8)
            ax.set_yticks(range(len(GROUPS)), [GROUP_NAME[g] for g in GROUPS] if col == 0 else [""] * len(GROUPS),
                          fontsize=9)  # fmt: skip
            wr = (writes.get(s) or {}).get(who)
            sub = "the bridge entity" if k == "bridge" else "the answer word"
            if k == "ans":
                sw = (wr or {}).get("switch")
                sub += (f"\nwrite: answer {sw['ans1'][0]:.2f} / {sw['ans2'][0]:.2f}, random {sw['rand1'][0]:.2f} / "
                        f"{sw['rand2'][0]:.2f} (1x / 2x)" if sw else "\nwrite: pending")  # fmt: skip
            ax.set_title(sub, fontsize=9)
            if row == 1:
                ax.set_xlabel("layer", fontsize=9)
            if row == 0 and k == "bridge":
                ax.annotate(f"{SET_TEXT[s]}, n = {mp['n']}", xy=(1.1, 1.32), xycoords="axes fraction", ha="center",
                            fontsize=10, fontweight="bold")  # fmt: skip
        axes[row, 0].set_ylabel(who, fontsize=11, fontweight="bold")
    if im is not None:
        cb = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.7, pad=0.01)
        cb.set_ticks([0, 1, 2, 3, 4], labels=["1", "10", "100", "1000", "≥10⁴"])
        cb.set_label("median J++ lens rank (dark: read at the top)")
    fig.suptitle(f"x52 {NAMES[target]}: where the J++ lens reads the bridge entity and the answer word. Dot: top-5 on "
                 "≥ 0.5 of items; dashed: the plain logit lens's answer layer; box: the write's cell. UNVERIFIED.",
                 x=0.01, ha="left", fontsize=10)  # fmt: skip
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def cell_line(rr: dict, layers: list[int], k: str = "ans") -> list[str]:
    """Per group the top-5 share by layer (one markdown row each)."""
    out = []
    for g in GROUPS:
        vals = [rr["cells"][f"{k}|{g}|{la}"] for la in layers]
        out.append(f"| {GROUP_NAME[g]} | n {max(v['n'] for v in vals)} | "
                   + " | ".join("-" if not v["n"] else f"{v['top5'][0]:.2f}" for v in vals) + " |")  # fmt: skip
    return out


def pair(w: dict | None, a: str, b: str) -> str:
    return f"{fmt(w['switch'][a])} / {fmt(w['switch'][b])}" if w else "pending"


def combinations(results: list[dict]) -> dict[str, dict]:
    """Per model, dataset and reader: readable, usable (None while the write is pending) and the combination."""
    out = {}
    for r in results:
        for s in SETS:
            mp = r["maps"].get(s)
            if mp is None:
                continue
            for who, rr in mp["readers"].items():
                w = (r["writes"].get(s) or {}).get(who)
                read, use = rr["readable"]["holds"], (w["rule"]["holds"] if w else None)
                out[f"{r['target']}|{s}|{who}"] = {
                    "readable": read,
                    "usable": use,
                    "combination": combination(read, use),
                }
    return out


def verdict_lines(results: list[dict], n_boot: int) -> list[str]:
    lines = ["# x52 (batch 52 B): where can the lens read the answer, and can it write it? (UNVERIFIED)", "",
             f"Prediction: {NO_PREDICTION}. Cluster bootstrap over the bridge entities ({n_boot}, seed {X.BOOT_SEED}).", "",
             "Rules (Dan, jobs/c3/batch52.yaml brief B, verbatim):", "", *[f"- {v}" for v in RULE.values()], "",
             "As computed: the answer word = 51.12's (x51_answer: main the number word's one-letter-token variants, "
             "z2 the first token of the answer word's variants), its rank = 1 + tokens with a strictly higher J++ lens "
             "logit over the full vocabulary (best variant), on O; the answer layer = per item the first layer at which "
             "the plain logit lens's top token at the last token is the answer as read, the reader's lower median; "
             "'before' = cached layers strictly below it; any token group counts; the write at the readable-most cell "
             "before the answer layer, 'changes the answer' = the top token becomes S's answer (the written word), at "
             "gain 1 or 2 with that gain's random control <= 0.10; point estimates decide (EPS 1e-9).", "",
             "| model | dataset | reader | n | answer layer | readable (first cell; best before) | write cell | ans1 / ans2 "
             "| rand1 / rand2 | freq1 / freq2 | whole | usable | combination |", "|" + "---|" * 13]  # fmt: skip
    for res in results:
        for s in SETS:
            mp, wr = res["maps"].get(s), res["writes"].get(s)
            if mp is None:
                lines.append(f"| {res['target']} | {s} | - | - | read pending | | | | | | | | |")
                continue
            for who, rr in mp["readers"].items():
                rd, w = rr["readable"], (wr or {}).get(who)
                best = rd.get("best_before") or {}
                use = w["rule"]["holds"] if w else None
                lines.append(f"| {res['target']} | {s} | {who} | {mp['n']} | L{rr['answer']['layer']} (never "
                             f"{rr['answer']['never']}) | **{rd['holds']}** ({rd.get('first')}; best "
                             f"{best.get('group')} L{best.get('layer')} {fmt(best.get('top5'))}) | {rr['write_cell']} | "
                             f"{pair(w, 'ans1', 'ans2')} | {pair(w, 'rand1', 'rand2')} | {pair(w, 'freq1', 'freq2')} | "
                             f"{fmt(w['switch']['whole']) if w else '-'} | **{use}** | "
                             f"**{combination(rd['holds'], use)}** |")  # fmt: skip
    for res in results:
        for s in SETS:
            mp = res["maps"].get(s)
            if mp is None:
                continue
            lines += ["", f"## {res['target']}, {SET_TEXT[s]}: answer word in the J++ top-5 (share of items)", "",
                      f"Read run {res['runs'][s]['read']}; groups: " + "; ".join(f"{g} = {GROUP_TEXT[s][g]}" for g in GROUPS)
                      + ".", ""]  # fmt: skip
            for who, rr in mp["readers"].items():
                a = rr["answer"]
                lines += [f"### {who}: answer layer L{a['layer']} (quartiles {a['quartiles']}; never {a['never']} of "
                          f"{a['n']}; 51.10's settle layer L{a['settle_layer']})", "",
                          "| group | n | " + " | ".join(f"L{la}" for la in mp["layers"]) + " |",
                          "|" + "---|" * (2 + len(mp["layers"]))]  # fmt: skip
                lines += cell_line(rr, mp["layers"])
                lines += ["", "Bridge entity in the top-5:", "", "| group | n | " + " | ".join(f"L{la}" for la in mp["layers"])
                          + " |", "|" + "---|" * (2 + len(mp["layers"]))]  # fmt: skip
                lines += cell_line(rr, mp["layers"], "bridge")
                lines += ["", "S's answer word on O in the top-5 (a same-type distractor; baseline):", "",
                          "| group | n | " + " | ".join(f"L{la}" for la in mp["layers"]) + " |",
                          "|" + "---|" * (2 + len(mp["layers"]))]  # fmt: skip
                lines += cell_line(rr, mp["layers"], "ans_S")
                lines += ["", "The answer word, whole-word variants only, in the top-5:", "",
                          "| group | n | " + " | ".join(f"L{la}" for la in mp["layers"]) + " |",
                          "|" + "---|" * (2 + len(mp["layers"]))]  # fmt: skip
                lines += cell_line(rr, mp["layers"], "ans_whole")
                rw, rdis = rr["readable_whole_words"], rr["readable_distractor"]
                lines += ["", f"- the rule on the whole-word variants alone: {rw['holds']} (first {rw.get('first')}); "
                          f"on S's answer word (the distractor, not the answer): {rdis['holds']} (first "
                          f"{rdis.get('first')})", ""]  # fmt: skip
            chk = res["checks"].get(s)
            if chk:
                lines.append(f"Check against 51.12 at the bridge word, L{chk['L']} ({chk['run']}): " + "; ".join(
                    f"{w}: top-50 ours {fmt(v['ours_top50'])} vs 51.12 {fmt(v['x51_12_top50'])}, median rank "
                    f"{fmt(v['ours_median'])} vs {fmt(v['x51_12_median'])} (n {v['n_ours']} / {v['n_x51_12']})"
                    for w, v in chk.items() if isinstance(v, dict)))  # fmt: skip
            wr = res["writes"].get(s)
            if wr:
                lines += ["", "Write (switch to the written answer; changed away from O's answer):", "",
                          "| reader | cell | n | " + " | ".join(("none", *ARMS)) + " | s median | size from B |",
                          "|" + "---|" * (6 + len(ARMS))]  # fmt: skip
                for who, w in wr.items():
                    lines.append(f"| {who} | {w['cell']} | {w['n']} | " + " | ".join(
                        f"{fmt(w['switch'][a])}; {w['changed'][a][0]:.2f}" for a in ("none", *ARMS))
                        + f" | {fmt(w['s_median'])} | {w['size_from_bridge_word']} |")  # fmt: skip
            lines.append(f"\n![{res['target']}](map_{TAGS[res['target']]}.png)\n")
    lines += ["Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def view_lines(res: dict, decode, k_prompts: int = N_PROMPTS, k_rows: int = N_ROWS, seed: int = VIEW_SEED) -> list[str]:
    """The verify pack: k rendered prompts per dataset (seed 0) with the groups marked, the answer word's and the
    bridge's tokens; k random write rows per arm."""
    lines = [f"## {res['target']}", ""]
    for s in SETS:
        if res["maps"].get(s) is None:
            continue
        run = res["runs"][s]
        items = X.read_jsonl(RESULTS / run["read"] / "cases.jsonl")
        lines += [
            f"### {SET_TEXT[s]}: {min(k_prompts, len(items))} prompts of {len(items)} (random.Random({seed}))",
            "",
        ]
        for i in sorted(random.Random(seed).sample(range(len(items)), min(k_prompts, len(items)))):
            it = items[i]
            lines += [f"#### {it['key']}: {it['entity']} -> {it['cf_entity']}", ""]
            for w, rd in it["readers"].items():
                toks = {k: [decode([t]) for t in rd["toks"][k]] for k in ("ans", "ans_S", "bridge")}
                lines += [f"{READER_NAME[w]} (answer {rd['answer']}, S's {rd['cf_answer']}; tokens "
                          f"{json.dumps(toks, ensure_ascii=False)}), O as read:", "", "```", as_read(decode, it, w), "```", ""]  # fmt: skip
        wdir = RESULTS / run["write"]
        if (wdir / "outcomes.jsonl").exists():
            rows = X.read_jsonl(wdir / "outcomes.jsonl")
            for a in ("none", *ARMS):
                mine = [r for r in rows if r["arm"] == a]
                pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
                lines += [f"#### {s} {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                          "| key | reader | cell | top token | switched | changed |", "|---|---|---|---|---|---|"]  # fmt: skip
                for j in pick:
                    r = mine[j]
                    lines.append(f"| {r['key']} | {READER_NAME[r['reader']]} | {r['group']} L{r['layer']} | "
                                 f"{decode([r['top']])!r} | {r['switched']} | {r['changed']} |")  # fmt: skip
                lines.append("")
    return lines


def model_results(target: str, runs: dict | None, n_boot: int) -> dict:
    runs = runs or {s: {st: run_name(st, s, target) for st in STAGES} for s in SETS}
    res: dict[str, Any] = {"target": target, "runs": runs, "maps": {}, "writes": {}, "checks": {}}
    for s in SETS:
        rd = RESULTS / runs[s]["read"]
        if not (rd / RANKS_FILE).exists():
            res["maps"][s] = None
            continue
        run = load_run(runs[s]["read"])
        assert run["manifest"]["model"]["target"] == target, f"{rd.name} is not {target}'s"
        res["maps"][s] = map_numbers(run, n_boot)
        res["checks"][s] = check_51_12(res["maps"][s], target, s)
        wd = RESULTS / runs[s]["write"]
        if (wd / "outcomes.jsonl").exists():
            res["writes"][s] = write_numbers(wd, n_boot)
            for who, w in res["writes"][s].items():
                assert w["cell"] == res["maps"][s]["readers"][who]["write_cell"], f"{wd.name}: {who}'s cell differs"
    return res


def stage_verdict(n_boot: int = X.N_BOOT, decode_for=None, coverage: bool = False) -> Path:
    """The three models' verdict, or with coverage (batch 52 C) the same readings on COVERAGE_MODELS' runs alone
    (x52cov-<UTC>/)."""
    from scripts import x47_atoms as AT

    out = RESULTS / f"{'x52cov' if coverage else 'x52'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    results = [model_results(t, None, n_boot) for t in (COVERAGE_MODELS if coverage else MODELS)]
    lines = verdict_lines(results, n_boot)
    combos = combinations(results)
    (out / "verdict.json").write_text(json.dumps({"prediction": NO_PREDICTION, "rule": RULE, "combinations": combos,
                                                 "models": results}, indent=1, ensure_ascii=False) + "\n")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    view = ["# x52 view (verify pack): prompts as read with ⟦B⟧ ⟦E⟧ ⟦Q⟧ ⟦T⟧ marked, random write rows. UNVERIFIED.", ""]
    for r in results:
        if any(r["maps"].values()):
            figure(r["target"], r["maps"], r["writes"], out / f"map_{TAGS[r['target']]}.png")
            view += view_lines(r, (decode_for or AT.default_decode)(r["target"]))
    (out / "view.md").write_text("\n".join(view) + "\n")
    print("\n".join(lines[:40]))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "write", "verdict"])
    ap.add_argument("--set", choices=SETS)
    ap.add_argument("--name", help="run / write: the run name (results/x52_answer_map/<name>/)")
    ap.add_argument("--read", help="write: the read run whose ranks and states it uses")
    ap.add_argument("--plan-dir", default=None)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help="verdict: batch 52 C's coverage models (Lightning) alone")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.plan_dir)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        assert a.set, "run needs --set"
        stage_run(a.name, a.set)
    elif a.stage == "write":
        assert a.name, "write needs --name"
        assert a.set, "write needs --set"
        assert a.read, "write needs --read (the read run)"
        stage_write(a.name, a.set, a.read)
    else:
        stage_verdict(a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
