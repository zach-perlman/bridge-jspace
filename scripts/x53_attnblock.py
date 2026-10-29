"""x53_attnblock (test 53.4; Dan 29 Oct ~10:05, jobs/c3/batch52.yaml `lightning_attn_block`, kept unchanged as 53.4 in
jobs/c3/batch53.yaml; the rule fixed then, no prediction): does Lightning's lookup read the bridge word through
attention blocks 19 and 26?

Items: Lightning's conflict run (x0_necessity nem35l_x52_conflict: X0's main test, two people swap picks, chat; the 60
dev scenes already kept out by that run), its items at L = the committed layer (14, BJ_PREDICTED_LAYER), in its order,
rebuilt and checked id by id. The whole change Δ = h_alt - h_org at the bridge word (one token; X0's position) at block
L's output, one forward per prompt (X0's). Reads: X0's chat read on the org prompt (a digit's space token appended; the
top token over the vocabulary), lookup and recall, with Δ added at the bridge word at L ("whole") or nothing ("clean").
Switch = the top token is the alt answer's first token (X0's).

Blocking (bridge_jspace.knockout.knock_out, 47.6's mechanics through x47_edges.forward: uncached forwards, mode value):
in the listed attention blocks, every position after the source cannot attend to it: those query -> key logits are -inf
in every head, so each such query's softmax renormalises over the keys it still reads; every other pair and every other
block as is (Lightning's Mamba-2 and MoE blocks untouched). Arms (rows of one batched forward per item and reader, each
arm clean and whole; equal-length rows):
  none     no block (the whole change's switches: S_whole)
  b19      (i)   block 19 only, source = the bridge word
  b26      (ii)  block 26 only, source = the bridge word
  both     (iii) blocks 19 and 26, source = the bridge word
  after    (iv)  every softmax-attention block after L (Lightning at L14: 19 / 26 / 33 / 42; from the config, asserted
                 to hold 19 and 26), source = the bridge word
  control  (v)   blocks 19 and 26, source = a random non-bridge token of the bridge's sentence (X0's bind_bridge
                 statement: the asked pick sentence; tokens overlapping the sentence, the bridge word's excluded), one per
                 scene (random.Random keyed by CONTROL_SEED and the scene); destinations every position after it
Edges per row (destinations x blocks) are stored; the control's differ from (iii)'s by the gap between the two sources.

Rule (verbatim, RULE) and how it is computed (AS_COMPUTED). The recall's numbers are reported beside (no label). The
clean rows give each arm's collateral damage (the clean answer lost). Cluster-bootstrap CIs over the bridge entities
(10,000, seed 0; paired across arms) beside the points. Every result UNVERIFIED.

BJ_TARGET=nemotron-3.5-lightning BJ_PREDICTED_LAYER=14 uv run python scripts/x53_attnblock.py plan          # CPU
BJ_TARGET=nemotron-3.5-lightning BJ_PREDICTED_LAYER=14 uv run python scripts/x53_attnblock.py run --name nem35l_x53_attnblock
uv run python scripts/x53_attnblock.py verdict --name nem35l_x53_attnblock                                   # CPU
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.knockout import FULL
from scripts import x0_necessity as X

EXP = "x53_attnblock"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch52.yaml"  # the rule's text (lightning_attn_block)
BATCH = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"  # 53.4: "the spec sent at 09:20, unchanged"
TARGET = "nemotron-3.5-lightning"
RUN = "nem35l_x53_attnblock"
BLOCKS = (19, 26)  # Dan's two blocks
ARMS = ("none", "b19", "b26", "both", "after", "control")
PATCHES = ("clean", "whole")
RULE_ARM = {"i": "b19", "ii": "b26", "iii": "both", "iv": "after", "v": "control"}
ARM_TEXT = {"none": "no block", "b19": "(i) block 19 only", "b26": "(ii) block 26 only", "both": "(iii) blocks 19 and 26",
            "after": "(iv) every attention block after L", "control": "(v) blocks 19 and 26, a random non-bridge token "
            "of the bridge's sentence as the source"}  # fmt: skip
CONTROL_SEED = 5346
TWO, CONTROL_MAX, ONE, NOT_ATTN = 0.6, 0.15, 0.6, 0.3
EPS = 1e-9  # a value exactly at a bar counts as at the bar
NO_PREDICTION = "no prediction (Dan, 29 Oct ~10:05: the rule fixed then, before any run)"
LABELS = ("read through two blocks", "one block", "not through attention at the bridge", "in between")
RULE = (
    "\"read through two blocks\" if (iii) cuts the lookup's switches by >= 0.6 of the whole change's and (v) by <= "
    '0.15; "one block" if (i) or (ii) alone cuts >= 0.6; "not through attention at the bridge" if (iv) cuts < 0.3 (the '
    "Mamba state carries it); else in between."
)
# 53.4 follow-up (Dan 11:10, jobs/c3/batch53.yaml next_1110 item 4; spec jobs/c3/x53_4b_lightning_attnspan.yaml): the
# span from the bridge word to the scene's last token as the keys, vs a control span of the same length
RUN_SPAN = "nem35l_x53_attnspan"
SPAN_ARMS = ("none", "both", "span", "span_ctrl")
SPAN_TEXT = {"none": "no block", "both": "(iii) of 53.4, rerun here: blocks 19 and 26, source = the bridge word",
             "span": "blocks 19 and 26: every position after the scene's last token cannot attend to any position from "
                     "the bridge word through the scene's last token",
             "span_ctrl": "the control: blocks 19 and 26, the same destinations, a source span of the same length inside "
                          "the scene before the bridge word (seeded start)"}  # fmt: skip
SPAN_SEED = 5348
SPAN_CUT, SPAN_CONTROL_MAX = 0.6, 0.15
SPAN_LABEL = "the pointer is read by attention after the Mamba state spreads it"
RULE_SPAN = (
    '"the pointer is read by attention after the Mamba state spreads it" if the span cuts the lookup\'s switches by '
    ">= 0.6 and the control by <= 0.15; else as 53.4."
)
SPAN_CONTROL = (
    "the control span: as many tokens as the bridge-to-scene-end span, inside the scene before the bridge word (from the "
    "scene's first token to the token before the bridge word; never the bridge-to-end span, never the question, never "
    "position 0), its start drawn per scene among the starts that fit (random.Random('x53_attnspan|5348|<scene>')); a "
    "scene where no such span fits is dropped from the rule and counted (its span arm read beside); the destinations are the span arm's (every position after the "
    "scene's last token: the question and the read), so the two arms differ only in the keys blocked"
)
AS_COMPUTED_SPAN = (
    "cut(x) = 1 - S_x / S_whole on the lookup (53.4's), S_x = the share of the scenes kept whose lookup switches under "
    "the whole change with arm x's block, S_whole = the same with no block, all in this run's forwards; point estimates "
    f'decide, EPS {EPS} at the bars. "else as 53.4": 53.4\'s labels applied to the span arm: its (iv) clause "not '
    'through attention at the bridge" if the span cuts < 0.3 (the Mamba state carries it), else "in between" (the '
    "per-block clauses (i) / (ii) have no span arm). The span's destinations are every position after the scene's last "
    "token (knock_out needs disjoint sources and destinations, so attention inside the span is as is), the same for the "
    f"control. {SPAN_CONTROL}. S_whole = 0: not tested; X0's validity reported, not a gate. 53.4's (iii) and (v) from "
    "its committed verdict beside, and (iii) rerun here"
)
AS_COMPUTED = (
    "cut(x) = 1 - S_x / S_whole on the lookup, S_x = the share of items whose lookup switches under the whole change "
    "with arm x's block, S_whole = the same with no block (arm none), all in this run's forwards; point estimates "
    f"decide, EPS {EPS} at the bars ('< 0.3' strict). The clauses are checked in the rule's order and the first that "
    "holds is the label; any other clause that also holds is listed beside it (flagged for Dan: the rule does not say "
    "which wins). S_whole = 0: not tested. X0's validity (S_whole >= 0.30 and >= 30 items switched) is reported, not a "
    "gate (the rule has none)."
)


# ---- pure (CPU) ---------------------------------------------------------------------------------------------------


def arm_layers(kinds: list[str], layer: int) -> dict[str, list[int]]:
    """Each blocking arm's blocks: Dan's two, both, and every softmax-attention block after `layer` (both of his
    asserted among them)."""
    after = [la for la, k in enumerate(kinds) if k == FULL and la > layer]
    assert set(BLOCKS) <= set(after), f"blocks {BLOCKS} are not all softmax attention after L{layer}: {after}"
    a, b = BLOCKS
    return {"b19": [a], "b26": [b], "both": [a, b], "after": after, "control": [a, b]}


def control_position(scene: str, candidates: list[int], seed: int = CONTROL_SEED) -> int:
    """The control's source: one of the sentence's non-bridge positions, drawn per scene."""
    assert candidates, f"{scene}: no non-bridge token in the bridge's sentence"
    return random.Random(f"x53_attnblock|{seed}|{scene}").choice(sorted(candidates))


def knock_of(arm: str, sets: dict[str, list[int]], pos: int, control: int, length: int) -> tuple | None:
    """x47_edges.forward's knock entry (blocks, sources, destinations) of one arm on a prompt of `length` tokens:
    every position after the source is a destination."""
    if arm == "none":
        return None
    src = control if arm == "control" else pos
    assert 0 < src < length - 1, f"source {src} in a prompt of {length}"
    return sets[arm], [src], list(range(src + 1, length))


def cut(s_arm: float, s_whole: float) -> float:
    return 1.0 - s_arm / s_whole if s_whole > 0 else math.nan


def label(cuts: dict[str, float]) -> dict[str, Any]:
    """The rule on the lookup's cuts per rule arm (i .. v): every clause, the label (first clause holding, in the
    rule's order) and the other clauses that hold."""
    if any(math.isnan(cuts[k]) for k in RULE_ARM):
        return {"label": "not tested (nothing switched under the whole change)", "clauses": {}, "also": []}
    clauses = {
        LABELS[0]: cuts["iii"] >= TWO - EPS and cuts["v"] <= CONTROL_MAX + EPS,
        LABELS[1]: cuts["i"] >= ONE - EPS or cuts["ii"] >= ONE - EPS,
        LABELS[2]: cuts["iv"] < NOT_ATTN - EPS,
    }
    held = [k for k, v in clauses.items() if v]
    return {"label": held[0] if held else LABELS[3], "clauses": clauses, "also": held[1:]}


def span_positions(pos: int, scene: tuple[int, int], question: list[int]) -> dict[str, Any] | None:
    """The 53.4 follow-up's sources for one scene: the span from the bridge word `pos` through the scene's last token,
    and the control span of the same length inside the scene before the bridge word (the starts that fit; the draw is
    control_span's). None if no control span fits."""
    first, last = scene
    assert first <= pos <= last, f"the bridge word {pos} is not inside the scene {scene}"
    span = list(range(pos, last + 1))
    n = len(span)
    lo = max(first, 1)  # position 0 is never a source (knock_out)
    starts = [s for s in range(lo, pos - n + 1) if not set(range(s, s + n)) & (set(span) | set(question))]
    return {"span": span, "starts": starts} if starts else None


def control_span(scene_id: str, starts: list[int], n: int, seed: int = SPAN_SEED) -> list[int]:
    """The control span: n tokens from a start drawn per scene among those that fit."""
    s = random.Random(f"x53_attnspan|{seed}|{scene_id}").choice(sorted(starts))
    return list(range(s, s + n))


def span_knock(arm: str, sets: dict[str, list[int]], it: dict, length: int) -> tuple | None:
    """x47_edges.forward's knock entry of a follow-up arm on a prompt of `length` tokens: the span arms block, in blocks
    19 and 26, every position after the scene's last token (the question and the read) from their source span; (iii)
    as 53.4."""
    if arm == "none":
        return None
    if arm == "both":
        return knock_of("both", sets, it["pos"], it["control"], length)
    src = it["span"] if arm == "span" else it["span_control"]
    dst = list(range(it["scene_end"] + 1, length))
    assert dst, f"{it['scene']}: no destination after the scene"
    assert not set(src) & set(dst), f"{it['scene']}: the {arm} sources reach the destinations"
    assert 0 not in src, f"{it['scene']}: position 0 in the {arm} sources"
    return sets["both"], src, dst


def label_span(cut_span: float, cut_control: float) -> str:
    """The follow-up's rule on the lookup's cuts (point estimates, EPS); "else as 53.4": its labels on the span arm."""
    if math.isnan(cut_span) or math.isnan(cut_control):
        return "not tested (nothing switched under the whole change)"
    if cut_span >= SPAN_CUT - EPS and cut_control <= SPAN_CONTROL_MAX + EPS:
        return SPAN_LABEL
    if cut_span < NOT_ATTN - EPS:
        return LABELS[2]
    return LABELS[3]


# ---- items (tokenizer and the stored run) ---------------------------------------------------------------------------


def sentence_tokens(tok, item: dict) -> tuple[list[int], list[int], list[int]]:
    """The org chat prompt's ids, the token positions of the bridge's sentence (X0's bind_bridge statement) and of the
    bridge word in it, found as x0_necessity.encode_bridge finds the word."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    context = item["context"]
    text = X.render(tok, item, "chat", context)
    enc = raw_encoding(tok, text, offsets=True)
    sentence = SP.tasks_statements(item)["bind_bridge"]
    s0 = text.index(context) + SP.find_sentence(context, sentence)
    w0 = s0 + sentence.rindex(item["bridge"])
    offs = enc["offset_mapping"]
    return (
        list(enc["input_ids"]),
        SP.tokens_in(offs, s0, s0 + len(sentence)),
        SP.tokens_in(offs, w0, w0 + len(item["bridge"])),
    )


def build_items(tok, target: str = TARGET) -> tuple[list[dict], dict]:
    """The conflict run's items at L in its order (rebuilt; ids and position asserted equal to its cases), each with
    its bridge sentence's positions, the control's source and the stored whole-change switch per reader."""
    from scripts import tasks_v2 as T
    from scripts import x45b_binding as B
    from scripts import x47_cumulative as C

    src = X.RESULTS / B.MAIN_RUN[target]
    layer = X.PREDICTED[target]
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["predicted"] == layer, f"{src.name}: layer {m['predicted']}, not {layer} (BJ_PREDICTED_LAYER)"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {src.name}"
    scenes, stored = C.stored_whole(src, layer)
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    with B.x0_alt(m.get("alt") or "cf", ("chat",)):
        cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, multi = [], 0
    for s in scenes:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the bridge position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        ids, sent, word = sentence_tokens(tok, by_id[c["readers"][X.LOOKUP]["id"]])
        assert ids == c["readers"][X.LOOKUP]["ids"]["org"], f"{s}: the rebuilt prompt differs from the run's"
        assert word == [c["pos"]], f"{s}: the bridge word is not at the run's position"
        end = max(sent) + 1
        for w in X.READERS:
            assert c["readers"][w]["ids"]["org"][:end] == ids[:end], f"{s}: {w}'s prompt differs in the bridge sentence"
        cands = [p for p in sent if p not in word and p > 0]
        multi += len(word) > 1
        out.append({**c, "sentence": sent, "control": control_position(s, cands), "candidates": len(cands),
                    "stored_whole": stored[s]})  # fmt: skip
    counts = {"source": src.name, "set": m["set"], "layer": layer, "items": len(out),
              "entities": len({it["bridge"] for it in out}), "control_before_bridge": sum(it["control"] < it["pos"] for it in out),
              "sentence_tokens": [min(len(it["sentence"]) for it in out), max(len(it["sentence"]) for it in out)] if out else None}  # fmt: skip
    return out, counts


def scene_tokens(tok, item: dict) -> tuple[list[int], tuple[int, int], list[int]]:
    """The org chat prompt's ids, the scene's first and last token (the tokens overlapping the context) and the
    question's tokens."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    context = item["context"]
    text = X.render(tok, item, "chat", context)
    enc = raw_encoding(tok, text, offsets=True)
    offs = enc["offset_mapping"]
    c0 = text.index(context)
    scene = SP.tokens_in(offs, c0, c0 + len(context))
    q0 = text.index(item["question"], c0 + len(context))
    question = SP.tokens_in(offs, q0, q0 + len(item["question"]))
    assert scene, f"{item['id']}: no scene token"
    assert question, f"{item['id']}: no question token"
    assert max(scene) < min(question), f"{item['id']}: the scene does not precede the question"
    return list(enc["input_ids"]), (min(scene), max(scene)), question


def build_span_items(tok, target: str = TARGET) -> tuple[list[dict], dict]:
    """53.4's items (build_items, its order) with the follow-up's spans: the bridge-to-scene-end span and the control
    span (span_positions / control_span); where no control fits, span_control is None: the scene is dropped from the
    rule (counted) and its span arm read beside. Both readers' prompts are asserted identical through the scene's last
    token (so one mask serves both)."""
    from scripts import tasks_v2 as T
    from scripts import x45b_binding as B

    its, counts = build_items(tok, target)
    m = json.loads((X.RESULTS / B.MAIN_RUN[target] / "manifest.json").read_text())
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, dropped = [], 0
    for it in its:
        ids, scene, question = scene_tokens(tok, by_id[it["readers"][X.LOOKUP]["id"]])
        assert ids == it["readers"][X.LOOKUP]["ids"]["org"], f"{it['scene']}: the rebuilt prompt differs"
        for w in X.READERS:
            assert it["readers"][w]["ids"]["org"][: scene[1] + 1] == ids[: scene[1] + 1], f"{it['scene']}: {w} differs"
        sp = span_positions(it["pos"], scene, question)
        span = list(range(it["pos"], scene[1] + 1))
        dropped += sp is None
        out.append({**it, "scene_first": scene[0], "scene_end": scene[1], "question_tokens": [min(question), max(question)],
                    "span": span, "span_control": None if sp is None else control_span(it["scene"], sp["starts"], len(span)),
                    "control_starts": 0 if sp is None else len(sp["starts"])})  # fmt: skip
    kept = [it for it in out if it["span_control"] is not None]
    lengths = [len(it["span"]) for it in kept]
    counts = {**counts, "span_items_in_rule": len(kept), "span_dropped_no_control_fits": dropped,
              "span_entities_in_rule": len({it["bridge"] for it in kept}),
              "span_tokens_in_rule": [min(lengths), int(np.median(lengths)), max(lengths)] if lengths else None,
              "span_tokens_all": [min(len(it["span"]) for it in out), int(np.median([len(it["span"]) for it in out])),
                                  max(len(it["span"]) for it in out)] if out else None}  # fmt: skip
    return out, counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def manifest(name: str, why: str, sets: dict[str, list[int]], counts: dict) -> dict:
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state

    src = X.RESULTS / counts["source"]
    return {"exp": EXP, "run": name, "why": why, "test": "53.4", "spec": "jobs/c3/batch52.yaml (lightning_attn_block); "
            "jobs/c3/batch53.yaml (53.4); jobs/c3/x53_4_lightning_attnblock.yaml",
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(),
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): pins.sha256_file(p)
                       for p in (SPEC, BATCH, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")
                       if p.exists()},
            "items": counts, "layer": counts["layer"], "arms": list(ARMS), "arm_text": ARM_TEXT, "arm_layers": sets,
            "patches": {"clean": "nothing added", "whole": "Δ added at the bridge word at L (AddRows' arithmetic)"},
            "blocking": "knockout.knock_out (mode value) via x47_edges.forward: in the arm's blocks, every position after "
                        "the source has its logits to the source at -inf in every head; uncached forwards",
            "read": "X0's chat read (the org prompt with a digit's space token appended; top token over the vocabulary; "
                    "switch = the alt answer's first token)",
            "seeds": {"control": f"random.Random('x53_attnblock|{CONTROL_SEED}|<scene>')", "bootstrap": X.BOOT_SEED},
            "order": {"items": "the conflict run's item order",
                      "rows": "per item and reader one forward of len(ARMS) x 2 rows: arm-major, clean then whole"},
            "rule": RULE, "as_computed": AS_COMPUTED, "prediction": NO_PREDICTION}  # fmt: skip


def stage_plan() -> dict:
    """CPU: the items, the control sources and the arms' blocks from the target's config, counts printed."""
    from bridge_jspace.knockout import config_layer_kinds
    from scripts import x45m

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    tok = x45m.tokenizer()
    its, counts = build_items(tok)
    sets = arm_layers(config_layer_kinds(_config()), X.PREDICTED[TARGET])
    out = {"counts": counts, "arm_layers": sets}
    print(json.dumps(out, indent=1))
    for it in its[:3]:
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        print(it["scene"], "bridge", repr(tok.decode([ids[it["pos"]]])), "control", repr(tok.decode([ids[it["control"]]])),
              "sentence", repr(tok.decode([ids[p] for p in it["sentence"]])))  # fmt: skip
    return out


def _config():
    from huggingface_hub import try_to_load_from_cache
    from transformers import AutoConfig

    t = pins.TARGETS[TARGET]
    path = try_to_load_from_cache(t["repo"], "config.json", revision=t["revision"])
    assert isinstance(path, str), f"{t['repo']}: config not cached"
    return AutoConfig.from_pretrained(str(Path(path).parent))


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.knockout import layer_kinds
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import x47_edges as E

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    model = load_model()
    tok = model.tokenizer
    layer = X.PREDICTED[TARGET]
    sets = arm_layers(layer_kinds(model), layer)
    its, counts = build_items(tok)
    (out / "manifest.json").write_text(json.dumps(manifest(name, why, sets, counts), indent=1) + "\n")
    print(json.dumps({"items": counts, "arm_layers": sets}), flush=True)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    specs = [(a, p) for a in ARMS for p in PATCHES]
    with (out / "items.jsonl").open("w") as f:
        for it in its:
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "pos": it["pos"], "control": it["control"],
                                "sentence": it["sentence"], "candidates": it["candidates"],
                                "bridge_token": tok.decode([ids[it["pos"]]]), "control_token": tok.decode([ids[it["control"]]]),
                                "sentence_text": tok.decode([ids[p] for p in it["sentence"]]),
                                "stored_whole": it["stored_whole"]}) + "\n")  # fmt: skip
    t0 = time.time()
    with torch.no_grad(), (out / "outcomes.jsonl").open("w") as f:
        for it in progress(its, "attention blocks (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][it["pos"]]
                 for v in ("org", "alt")}  # fmt: skip
            delta = h["alt"] - h["org"]
            for w, rd in it["readers"].items():
                prompt = rd["ids"]["org"] + it["space"]
                n = len(prompt)
                adds = [[(layer, it["pos"], delta)] if p == "whole" else None for _, p in specs]
                knock = [knock_of(a, sets, it["pos"], it["control"], n) for a, _ in specs]
                logits, _ = E.forward(model, [prompt] * len(specs), adds, knock)
                assert logits is not None
                for (a, p), k, lg in zip(specs, knock, logits, strict=True):
                    row = X.read_row(lg, rd, digits)
                    f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "reader": w, "arm": a, "patch": p,
                                        **row, "top_text": tok.decode([row["top"]]),
                                        "edges": len(k[0]) * len(k[2]) if k else 0}) + "\n")  # fmt: skip
    print(f"{len(its)} items in {time.time() - t0:.0f} s -> {out}", flush=True)
    return out


# ---- verdict (CPU) --------------------------------------------------------------------------------------------------


def reader_numbers(rows: list[dict], reader: str, n_boot: int = X.N_BOOT, arms: tuple[str, ...] = ARMS,
                   scenes: list[str] | None = None) -> dict:  # fmt: skip
    """One reader: per arm the switched share under the whole change and the clean answer kept (top = org answer's
    first token) without it; the cut of each blocking arm vs none with a paired cluster-bootstrap CI. `arms` (none
    first) and `scenes` (default: every scene read) restrict the table (the 53.4 follow-up)."""
    by = {(r["scene"], r["arm"], r["patch"]): r for r in rows if r["reader"] == reader}
    if scenes is None:
        scenes = list(dict.fromkeys(r["scene"] for r in rows if r["reader"] == reader))
    ents = [by[(s, "none", "whole")]["entity"] for s in scenes]
    sw = {a: [int(by[(s, a, "whole")]["switched"]) for s in scenes] for a in arms}
    kept = {a: [int(by[(s, a, "clean")]["role"] == "A") for s in scenes] for a in arms}
    r = X.resampled_rates(sw, ents, n_boot)
    s = {a: float(np.mean(v)) for a, v in sw.items()}
    cuts, cis = {}, {}
    for a in arms[1:]:
        cuts[a] = cut(s[a], s["none"])
        cis[a] = (
            [round(x, 3) for x in X.interval(1.0 - r[a] / np.where(r["none"] > 0, r["none"], np.nan))]
            if s["none"] > 0
            else None
        )
    edges = {a: [by[(sc, a, "whole")]["edges"] for sc in scenes] for a in arms[1:]}
    return {"n": len(scenes), "entities": len(set(ents)), "switched": {a: int(sum(v)) for a, v in sw.items()},
            "S": {a: round(v, 4) for a, v in s.items()}, "cut": {a: round(v, 4) for a, v in cuts.items()},
            "cut_ci": cis, "clean_kept": {a: round(float(np.mean(v)), 4) for a, v in kept.items()},
            "x0_valid": bool(s["none"] >= X.VALID_S and sum(sw["none"]) >= X.VALID_N),
            "edges_median": {a: float(np.median(v)) for a, v in edges.items()}}  # fmt: skip


def agreement(rows: list[dict], items: list[dict]) -> dict:
    """This run's whole-change switch (no block) vs the conflict run's stored one, per reader (Lightning's numerics
    depend on batch composition: descriptive)."""
    stored = {it["scene"]: it["stored_whole"] for it in items}
    out = {}
    for w in X.READERS:
        pairs = [(int(r["switched"]), stored[r["scene"]][w]) for r in rows
                 if r["reader"] == w and r["arm"] == "none" and r["patch"] == "whole"]  # fmt: skip
        out[w] = {"agree": round(float(np.mean([a == b for a, b in pairs])), 4), "this_run": sum(a for a, _ in pairs),
                  "stored": sum(b for _, b in pairs), "n": len(pairs)}  # fmt: skip
    return out


def fmt(x: float, ci: list | None = None) -> str:
    return (
        "nan"
        if x is None or (isinstance(x, float) and math.isnan(x))
        else f"{x:.3f}" + (f" [{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "")
    )


def example_lines(rows: list[dict], items: list[dict], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items (fixed seed): bridge and control tokens, the lookup's top token under the whole change per arm."""
    idx = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    by = {(r["scene"], r["arm"]): r for r in rows if r["reader"] == X.LOOKUP and r["patch"] == "whole"}
    out = [f"Examples ({len(idx)} random items, seed {seed}; the lookup's top token under the whole change, '*' = "
           "switched):"]  # fmt: skip
    for i in idx:
        it = items[i]
        tops = ", ".join(f"{a} {by[(it['scene'], a)]['top_text']!r}{'*' if by[(it['scene'], a)]['switched'] else ''}"
                         for a in ARMS)  # fmt: skip
        out.append(f"- {it['scene']}: sentence {it['sentence_text']!r}, bridge {it['bridge_token']!r}, control "
                   f"{it['control_token']!r}; {tops}")  # fmt: skip
    return out


def stage_verdict(name: str = RUN, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "items.jsonl")
    nums = {w: reader_numbers(rows, w, n_boot) for w in X.READERS}
    lk = nums[X.LOOKUP]
    res = label({k: lk["cut"][a] for k, a in RULE_ARM.items()})
    out = RESULTS / f"{EXP}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    agree = agreement(rows, items)
    lines = [f"x53_attnblock (Lightning, L{m['layer']}; run {name}); {NO_PREDICTION}; UNVERIFIED", "",
             f"Rule (verbatim): {RULE}", f"As computed: {AS_COMPUTED}", "",
             f"Label (lookup): {res['label']}" + (f"; also holds: {', '.join(res['also'])}" if res["also"] else ""),
             f"Clauses: {json.dumps(res['clauses'])}", "",
             f"Blocks: {json.dumps(m['arm_layers'])}; items {m['items']['items']} ({m['items']['entities']} bridge "
             f"entities), the control's source before the bridge in {m['items']['control_before_bridge']}", ""]  # fmt: skip
    for w in X.READERS:
        r = nums[w]
        lines.append(f"{'lookup' if w == X.LOOKUP else 'recall (beside)'}: n {r['n']}, S_whole {fmt(r['S']['none'])} "
                     f"({r['switched']['none']} switched; X0-valid {r['x0_valid']}), clean answer kept with no block "
                     f"{fmt(r['clean_kept']['none'])}")  # fmt: skip
        for a in ARMS[1:]:
            lines.append(f"  {ARM_TEXT[a]}: S {fmt(r['S'][a])}, cut {fmt(r['cut'][a], r['cut_ci'][a])}, clean kept "
                         f"{fmt(r['clean_kept'][a])}, edges (median) {r['edges_median'][a]:.0f}")  # fmt: skip
    lines += ["", f"Whole change vs the conflict run's stored switch (descriptive): {json.dumps(agree)}", "",
              *example_lines(rows, items)]  # fmt: skip
    blob = {"prediction": NO_PREDICTION, "rule": RULE, "as_computed": AS_COMPUTED, "run": name, "layer": m["layer"],
            "arm_layers": m["arm_layers"], "label": res, "readers": {("lookup" if w == X.LOOKUP else "recall"): v
            for w, v in nums.items()}, "agreement": agree, "status": "UNVERIFIED"}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- the 53.4 follow-up: the bridge-to-scene-end span (Dan 11:10) ---------------------------------------------------


def stage_plan_span() -> dict:
    from scripts import x45m

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    tok = x45m.tokenizer()
    its, counts = build_span_items(tok)
    print(json.dumps(counts, indent=1))
    for it in [x for x in its if x["span_control"] is not None][:3]:
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        print(it["scene"], "span", repr(tok.decode([ids[p] for p in it["span"]])), "control",
              repr(tok.decode([ids[p] for p in it["span_control"]])))  # fmt: skip
    return counts


def stage_run_span(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.knockout import layer_kinds
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state, progress
    from scripts import x47_edges as E

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    model = load_model()
    tok = model.tokenizer
    layer = X.PREDICTED[TARGET]
    sets = arm_layers(layer_kinds(model), layer)
    its, counts = build_span_items(tok)
    m = {**manifest(name, why, sets, counts), "test": "53.4 follow-up (Dan 11:10)",
         "spec": "jobs/c3/batch53.yaml (next_1110, item 4); jobs/c3/x53_4b_lightning_attnspan.yaml",
         "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "switches": switches(), "code": git_state(),
         "arms": list(SPAN_ARMS), "arm_text": SPAN_TEXT, "control": SPAN_CONTROL, "rule": RULE_SPAN,
         "as_computed": AS_COMPUTED_SPAN, "rule_53_4": RULE,
         "seeds": {"span_control": f"random.Random('x53_attnspan|{SPAN_SEED}|<scene>')", "bootstrap": X.BOOT_SEED},
         "order": {"items": "the conflict run's item order (53.4's)",
                   "rows": "per item and reader one forward: arm-major (none, both, span, span_ctrl where a control "
                           "fits), clean then whole"}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=1) + "\n")
    print(json.dumps({"items": counts, "arm_layers": sets}), flush=True)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    with (out / "items.jsonl").open("w") as f:
        for it in its:
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "pos": it["pos"], "scene_first": it["scene_first"],
                                "scene_end": it["scene_end"], "span": it["span"], "span_control": it["span_control"],
                                "control_starts": it["control_starts"], "in_rule": it["span_control"] is not None,
                                "span_text": tok.decode([ids[p] for p in it["span"]]),
                                "control_text": None if it["span_control"] is None else tok.decode([ids[p] for p in it["span_control"]]),
                                "stored_whole": it["stored_whole"]}) + "\n")  # fmt: skip
    t0 = time.time()
    with torch.no_grad(), (out / "outcomes.jsonl").open("w") as f:
        for it in progress(its, "attention blocks over the span (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][it["pos"]]
                 for v in ("org", "alt")}  # fmt: skip
            delta = h["alt"] - h["org"]
            arms = [a for a in SPAN_ARMS if a != "span_ctrl" or it["span_control"] is not None]
            specs = [(a, p) for a in arms for p in PATCHES]
            for w, rd in it["readers"].items():
                prompt = rd["ids"]["org"] + it["space"]
                n = len(prompt)
                adds = [[(layer, it["pos"], delta)] if p == "whole" else None for _, p in specs]
                knock = [span_knock(a, sets, it, n) for a, _ in specs]
                logits, _ = E.forward(model, [prompt] * len(specs), adds, knock)
                assert logits is not None
                for (a, p), k, lg in zip(specs, knock, logits, strict=True):
                    row = X.read_row(lg, rd, digits)
                    f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "reader": w, "arm": a, "patch": p,
                                        "in_rule": it["span_control"] is not None, **row, "top_text": tok.decode([row["top"]]),
                                        "edges": len(k[0]) * len(k[1]) * len(k[2]) if k else 0}) + "\n")  # fmt: skip
    print(f"{len(its)} items in {time.time() - t0:.0f} s -> {out}", flush=True)
    return out


def committed_53_4() -> dict | None:
    """53.4's committed verdict (the newest x53_attnblock-*/verdict.json): its lookup's (iii) and (v)."""
    found = sorted(RESULTS.glob(f"{EXP}-*/verdict.json"))
    if not found:
        return None
    v = json.loads(found[-1].read_text())
    lk = v["readers"]["lookup"]
    return {"verdict": str(found[-1].parent.relative_to(pins.REPO_ROOT)), "label": v["label"]["label"], "n": lk["n"],
            "S_whole": lk["S"]["none"], **{k: {"cut": lk["cut"][a], "cut_ci": lk["cut_ci"][a], "clean_kept": lk["clean_kept"][a]}
                                           for k, a in (("iii", "both"), ("v", "control"))}}  # fmt: skip


def stage_verdict_span(name: str = RUN_SPAN, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "items.jsonl")
    in_rule = [it["scene"] for it in items if it["in_rule"]]
    rest = [it["scene"] for it in items if not it["in_rule"]]
    nums = {w: reader_numbers(rows, w, n_boot, SPAN_ARMS, in_rule) for w in X.READERS}
    beside_all = {w: reader_numbers(rows, w, n_boot, SPAN_ARMS[:3], [it["scene"] for it in items]) for w in X.READERS}
    beside_rest = {w: reader_numbers(rows, w, n_boot, SPAN_ARMS[:3], rest) for w in X.READERS} if rest else None
    lk = nums[X.LOOKUP]
    lab = label_span(lk["cut"]["span"], lk["cut"]["span_ctrl"])
    prior = committed_53_4()
    out = RESULTS / f"x53_attnspan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    c = m["items"]
    lines = [f"x53_attnspan: the 53.4 follow-up on Lightning (L{m['layer']}; run {name}); Batch 53, 53.4 follow-up (Dan "
             f"11:10); {NO_PREDICTION}; UNVERIFIED", "", f"Rule (verbatim): {RULE_SPAN}", f"53.4's rule (for \"else as "
             f"53.4\"): {RULE}", f"As computed: {AS_COMPUTED_SPAN}", "", f"Label (lookup): {lab}", "",
             f"Scenes: {c['items']} (53.4's); in the rule (a control span fits) {c['span_items_in_rule']} "
             f"({c['span_entities_in_rule']} bridge entities); dropped from the rule, no control fits: "
             f"{c['span_dropped_no_control_fits']}; span length (tokens, min / median / max) in the rule "
             f"{c['span_tokens_in_rule']}, all {c['span_tokens_all']}", ""]  # fmt: skip
    for w in X.READERS:
        r = nums[w]
        lines.append(f"{'lookup' if w == X.LOOKUP else 'recall (beside)'} (the rule's scenes): n {r['n']}, S_whole "
                     f"{fmt(r['S']['none'])} ({r['switched']['none']} switched; X0-valid {r['x0_valid']}), clean kept "
                     f"with no block {fmt(r['clean_kept']['none'])}")  # fmt: skip
        for a in SPAN_ARMS[1:]:
            lines.append(f"  {SPAN_TEXT[a]}: S {fmt(r['S'][a])}, cut {fmt(r['cut'][a], r['cut_ci'][a])}, clean kept "
                         f"{fmt(r['clean_kept'][a])} (collateral), edges (median) {r['edges_median'][a]:.0f}")  # fmt: skip
    lines += ["", "Beside, the span and (iii) on every scene, and on the scenes without a control:"]
    for tag, block in (("all", beside_all), ("no control fits", beside_rest)):
        if block is None:
            continue
        for w in X.READERS:
            r = block[w]
            lines.append(f"  {tag}, {'lookup' if w == X.LOOKUP else 'recall'}: n {r['n']}, S_whole {fmt(r['S']['none'])}; "
                         f"span cut {fmt(r['cut']['span'], r['cut_ci']['span'])}, clean kept {fmt(r['clean_kept']['span'])}; "
                         f"(iii) cut {fmt(r['cut']['both'], r['cut_ci']['both'])}")  # fmt: skip
    if prior:
        lines += ["", f"Beside, 53.4's committed verdict ({prior['verdict']}; label {prior['label']}; n {prior['n']}, S_whole "
                  f"{fmt(prior['S_whole'])}): (iii) cut {fmt(prior['iii']['cut'], prior['iii']['cut_ci'])}, clean kept "
                  f"{fmt(prior['iii']['clean_kept'])}; (v) cut {fmt(prior['v']['cut'], prior['v']['cut_ci'])}, clean kept "
                  f"{fmt(prior['v']['clean_kept'])}"]  # fmt: skip
    ex_items = [it for it in items if it["in_rule"]]
    idx = sorted(random.Random(X.EXAMPLES_SEED).sample(range(len(ex_items)), min(X.K_EXAMPLES, len(ex_items))))
    by = {(r["scene"], r["arm"]): r for r in rows if r["reader"] == X.LOOKUP and r["patch"] == "whole"}
    lines += ["", f"Examples ({len(idx)} random scenes of the rule, seed {X.EXAMPLES_SEED}; the lookup's top token under "
              "the whole change, '*' = switched):"]  # fmt: skip
    for i in idx:
        it = ex_items[i]
        tops = ", ".join(f"{a} {by[(it['scene'], a)]['top_text']!r}{'*' if by[(it['scene'], a)]['switched'] else ''}"
                         for a in SPAN_ARMS)  # fmt: skip
        lines.append(f"- {it['scene']}: span {it['span_text']!r}; control {it['control_text']!r}; {tops}")
    blob = {"prediction": NO_PREDICTION, "rule": RULE_SPAN, "rule_53_4": RULE, "as_computed": AS_COMPUTED_SPAN,
            "control": SPAN_CONTROL, "run": name, "layer": m["layer"], "arm_layers": m["arm_layers"], "label": lab,
            "items": c, "readers": {("lookup" if w == X.LOOKUP else "recall"): v for w, v in nums.items()},
            "beside_all": {("lookup" if w == X.LOOKUP else "recall"): v for w, v in beside_all.items()},
            "beside_no_control": None if beside_rest is None else {("lookup" if w == X.LOOKUP else "recall"): v
                                                                  for w, v in beside_rest.items()},
            "x53_4": prior, "status": "UNVERIFIED"}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "plan-span", "run-span", "verdict-span"])
    ap.add_argument("--name", default=None, help=f"the run (default {RUN}; the span stages {RUN_SPAN})")
    ap.add_argument("--why", default="53.4, Dan 29 Oct ~10:05 (lightning_attn_block): does the lookup read the "
                    "bridge word through attention blocks 19 and 26? Rule fixed then, no prediction")  # fmt: skip
    a = ap.parse_args()
    span = a.stage.endswith("-span")
    name = a.name or (RUN_SPAN if span else RUN)
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        stage_run(name, a.why)
    elif a.stage == "verdict":
        stage_verdict(name)
    elif a.stage == "plan-span":
        stage_plan_span()
    elif a.stage == "run-span":
        stage_run_span(name, a.why)
    else:
        stage_verdict_span(name)


if __name__ == "__main__":
    main()
