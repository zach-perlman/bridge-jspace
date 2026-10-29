"""x47_depthmap (batch 47, amendment 3, the depth block: D1 and D2; jobs/c3/batch47.yaml, design and rules fixed in
advance; Q-depth in predictions/2026-10-28_dan.md). D1 replaces 47.4's arm list (scripts/x47_cumulative.py, whose items,
alignment checks and two cumulative arms this script reuses): a token x layer causal map.

Items: x47_cumulative's (each model's main-test X0 run at L, alt cf, its 200 scenes, the mixed ones in "all" only; and
its 45m clean-design run, alt fresh, the locker-first and locker-after scenes only: its mixed ones are left out, the
budget), the asserts as there (O and S the
same length, changed only at the bridge or the bridge and one token of the other person's pick; the asked pick sentence
at the same positions with the same ids but the bridge's; the readers' prompts equal through the last patched context
token). O = the original prompt, S = the changed one, each read with X0's chat read (the digit's space token appended;
switch = the top token is S's answer's first token). Both readers; their prompts differ from the question on, so S's
states are taken per reader (one unedited forward of S and of O per reader and item).

D1 cells: S's state placed into O at ONE token group and ONE layer l (the block's output set to S's there, exp04's
SetRows; the prompt O's tokens), l over the sampled layers (every 2nd on the 9B, every 4th on Muse and the 27B: 0, step,
..., and n_layers - 2). Token groups, positions by character overlap in the rendered prompt: bridge (the bridge word);
pick_rest (the asked pick sentence without the bridge and the person); person (the asked person's token(s)); per locker
sentence its item token(s) and its number token(s), the sentences named by role: lk_org (O's bridge's locker), lk_cf
(S's bridge's: the added one in the clean design, the other person's original pick's in the main test), lk_other1,
lk_other2 (the rest in context order); question (from the question's first token to the end of the prompt: the
template's closing tokens and 'Answer:' included); last (the read position, the appended space token). The bridge is
the only group whose token id differs between O and S; its map has one more cell, emb = O's prompt with S's token at the
bridge and no state placed (the input embedding swapped; block 0's input as a layer). Every other group's tokens are
identical in O and S, and S's state there still differs downstream of the bridge: a cell measures what those tokens
have read. In the main test the other person's changed pick is in no group (S's states at every group after it carry
it too; it is what (d)->100% measured in 47.4).
Margins (47.4's cumulative arms, the embedding swapped): b<l> = the bridge swapped at every layer <= l (blocks 0..l and
the embedding), one per sampled l; d = the whole pick sentence swapped at every layer. D2: w<l> = S's state set at the
bridge at every block output >= l (O's tokens; the complement of b), one per sampled l; l_R per reader = the first
sampled l at which the w curve is <= 0.1 (none: "not reached"). Beside them: none (O unedited), a (47.4's (a): h_S -
h_O added at the bridge at L) and S read on S. The run keeps 47.4's state check (under the bridge swap at blocks 0..L
the bridge's state after L is S's on items whose O and S agree before the bridge; a failure fails the job after its
files are written).

Readings (as computed; the specs' decision_rule carries the same): per model, design, reader and order group
(x45m's locker-first / locker-after; "all" = both), a cell = the switch rate over the group's items, 95% cluster-bootstrap
intervals over bridge items (10,000, seed 0). Rules, point estimates on the lookup unless said: D1 (a) locker-after: every
bridge cell (emb and every sampled layer) <= 0.25 and some locker-sentence cell (any lk_* item or number group, any layer)
>= 0.5; (b) locker-first: the last sampled layer with the lookup's bridge cell >= 0.3 is earlier than the recall's by >= 2
layers on the 9B, >= 4 on Muse (and the 27B); a reader with no such layer: "no layer", the rule does not hold; (c) the
recall's lk_cf item cell >= 0.3 at some layer in locker-first and < 0.3 at every layer in locker-after. D2: l_R(recall)
on all the design's items <= the start of Zach's late band (9B 26, 27B 52; Muse has no band: reported). Each rule is
scored on each design; the Q-depth answer per model reads the clean design (one token differs), the main test beside
it. Descriptive otherwise.

SEALED: the run writes per-item files only; verdict, view and figures refuse until "Dan:" under Q-depth in
predictions/2026-10-28_dan.md is non-empty at HEAD.

uv run python scripts/x47_depthmap.py plan                                              # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_depthmap.py run --name qwen35_9b_x47_depthmap   # GPU (sealed)
uv run python scripts/x47_depthmap.py verdict          # CPU, after Dan's Q-depth: rules, maps, l_R (the three runs)
uv run python scripts/x47_depthmap.py view             # CPU, after Dan's Q-depth: 10 items per design, seed 0
uv run python scripts/x47_depthmap.py figures --verdict results/x47_depthmap/depth-<UTC>
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x47_cumulative as C

EXP = "x47_depthmap"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = C.SPEC
PREDICTIONS = C.PREDICTIONS
QUESTION = "Q-depth"
RENDERING = C.RENDERING
DESIGNS = C.DESIGNS
GROUPS = ("locker-first", "locker-after", "all")  # order groups; "all" holds the main test's mixed scenes too
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_depthmap", "qwen3.6-27b": "x47_depthmap_27b",
        "muse-glimmer-30b": "muse30_x47_depthmap"}  # fmt: skip
STEP = {"qwen3.5-9b": 2, "qwen3.6-27b": 4, "muse-glimmer-30b": 4, "nemotron-3.5-lightning": 4}  # Lightning: as Muse
# batch 52 C coverage (amendment 3): Lightning's run, the main-test design only (--designs main: its clean one-pick
# design fails the gate, recall 0.751), read by verdict --coverage; RUNS and D1's own verdict unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_depthmap"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
LATE_BAND = {"qwen3.5-9b": 26, "qwen3.6-27b": 52}  # the start of Zach's late "question" band (D2's rule); Muse: none
LOCKER_ROLES = ("lk_org", "lk_cf", "lk_other1", "lk_other2")
TOKEN_GROUPS = ("bridge", "pick_rest", "person", *(f"{r}_{k}" for r in LOCKER_ROLES for k in ("item", "num")),
                "question", "last")  # fmt: skip
GROUP_TEXT = {"bridge": "the bridge word", "pick_rest": "the rest of the asked pick sentence",
              "person": "the asked person's token", "question": "the question tokens (to the end of the prompt)",
              "last": "the last token (the read position)",
              **{f"{r}_{k}": f"{what} token(s) of {who}'s locker sentence"
                 for r, who in (("lk_org", "O's bridge"), ("lk_cf", "S's bridge"), ("lk_other1", "the first other item"),
                                ("lk_other2", "the second other item"))
                 for k, what in (("item", "the item"), ("num", "the number"))}}  # fmt: skip
EMB = "emb"  # the bridge group's extra cell: the token swapped, no state placed
FIXED_ARMS = ("none", "a", "d", "S")
ARM_TEXT = {"none": "O unedited", "a": "(a) h_S - h_O added at the bridge word at L (47.4's (a), X0's whole arm)",
            "d": "the whole asked pick sentence swapped at every layer (47.4's (d); margin)",
            "S": "S read on S (unedited)", "b<l>": "the bridge swapped at every layer <= l (47.4's (b); margin)",
            "w<l>": "D2: S's state at the bridge at every block output >= l (the complement of b)",
            "g<group>@<l>": "D1 cell: S's state placed at the group's tokens at block output l",
            "gbridge@emb": "D1 cell: O's prompt with S's bridge token, no state placed"}  # fmt: skip
BRIDGE_MAX, LOCKER_MIN, HOT, W_FLOOR = 0.25, 0.5, 0.3, 0.1
LEAD = {
    "qwen3.5-9b": 2,
    "qwen3.6-27b": 4,
    "muse-glimmer-30b": 4,
}  # D1 (b): the lookup's bridge mass ends this many layers earlier
EPS = 1e-9
READER_NAME = C.READER_NAME


def sampled_layers(n_layers: int, step: int) -> list[int]:
    """0, step, 2 step, ... and n_layers - 2 (x45b_binding.q_sweep_layers: the last block's output at a position other
    than the read is read by nothing)."""
    return B.q_sweep_layers(n_layers, step)


def layer_grid(n_layers: int, step: int, layer: int) -> list[int]:
    """The sampled layers plus the layer fixed in advance: the margins b<L> and w<L> are read at L whether or not the
    step lands on it (Muse's L26 is between 24 and 28)."""
    return sorted(set(sampled_layers(n_layers, step)) | {layer})


# ---- token groups (tokenizer only) ----------------------------------------------------------------------------------


def locker_roles(context: str, bridge: str, cf_bridge: str) -> list[tuple[str, str]]:
    """Each locker sentence of the context in order with its role: lk_org (the bridge's), lk_cf (S's bridge's), then
    lk_other1, lk_other2, ... in context order."""
    out, k = [], 0
    for sent in B.locker_sentences(context):
        m = B.LOCKER_RE.match(sent)
        assert m, f"{sent!r} is not a locker sentence"
        item = m.group(1)
        if item == bridge:
            role = "lk_org"
        elif item == cf_bridge:
            role = "lk_cf"
        else:
            k += 1
            role = f"lk_other{k}"
        out.append((sent, role))
    roles = [r for _, r in out]
    assert {"lk_org", "lk_cf"} <= set(roles), f"the bridge's or S's bridge's locker sentence is missing: {roles}"
    assert set(roles) <= set(LOCKER_ROLES), f"more locker sentences than roles: {roles}"
    return out


def token_groups(tok, it: dict, reader: str) -> dict[str, list[int]]:
    """One reader's token groups (TOKEN_GROUPS, those the item has) as positions in its O prompt with the space token
    appended: the pick sentence's parts from the item record, the locker sentences' item and number tokens by character
    overlap, the question from its first character to the end of the prompt, the last token = the read position."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    rd = it["readers"][reader]
    text = rd["text"]["org"]
    enc = raw_encoding(tok, text, offsets=True)
    assert enc["input_ids"] == rd["ids"]["org"], f"{it['scene']} {reader}: the rendered prompt's ids differ"
    off = enc["offset_mapping"]
    pos, pick, person = it["pos"], it["pick"], it["person"]
    out = {"bridge": [pos], "pick_rest": [p for p in pick if p != pos and p not in person], "person": list(person)}
    base = text.index(it["context"])
    assert text.count(it["context"]) == 1
    for sent, role in locker_roles(it["context"], it["entity"], it["cf_bridge"]):
        m = B.LOCKER_RE.match(sent)
        assert m
        start = base + SP.find_sentence(it["context"], sent)
        for key, span in (("item", m.span(1)), ("num", m.span(2))):
            got = SP.tokens_in(off, start + span[0], start + span[1])
            assert got, f"{it['scene']}: no token overlaps the {key} of {sent!r}"
            out[f"{role}_{key}"] = got
    q0 = base + len(it["context"])
    i = text.index(rd["question"], q0)
    assert text.count(rd["question"], q0) == 1, f"{it['scene']} {reader}: the question is not once after the context"
    out["question"] = SP.tokens_in(off, i, len(text))
    out["last"] = [len(rd["ids"]["org"])]  # the appended space token
    assert all(out.values()), f"{it['scene']} {reader}: an empty group"
    flat = [p for g in out.values() for p in g]
    assert len(flat) == len(set(flat)), f"{it['scene']} {reader}: the groups overlap"
    assert max(flat) == out["last"][0], f"{it['scene']} {reader}: a group past the read position"
    return out


def select(tok, design: str, run: str, layer: int) -> tuple[list[dict], dict]:
    """x47_cumulative's items of the design (the main test's 200; the clean design's locker-first and locker-after
    scenes, its mixed ones left out) with each reader's token groups and the counts (x47_cumulative's, plus the groups
    per item)."""
    items, counts = C.select(tok, design, run, layer)
    kept = [it for it in items if design == "main" or it["group"] in GROUPS[:2]]
    for it in kept:
        it["token_groups"] = {w: token_groups(tok, it, w) for w in X.READERS}
        it["locker_roles"] = [r for _, r in locker_roles(it["context"], it["entity"], it["cf_bridge"])]
    counts |= {"items": len(kept), "mixed_left_out": len(items) - len(kept),
               "groups": dict(collections.Counter(it["group"] for it in kept)),
               "entities": len({it["entity"] for it in kept}),
               "token_groups": dict(collections.Counter(len(it["token_groups"][X.LOOKUP]) for it in kept)),
               "locker_roles": dict(collections.Counter(len(it["locker_roles"]) for it in kept))}  # fmt: skip
    return kept, counts


def arm_names(groups_present: list[str], layers: list[int]) -> list[str]:
    """Every arm of one read in order: the fixed arms, the D1 cells (group by group, emb first for the bridge), the b
    and w margins per layer."""
    cells = []
    for g in TOKEN_GROUPS:
        if g not in groups_present:
            continue
        if g == "bridge":
            cells.append(f"g{g}@{EMB}")
        cells += [f"g{g}@{la}" for la in layers]
    return [*FIXED_ARMS, *cells, *(f"b{la}" for la in layers), *(f"w{la}" for la in layers)]


def arm_of(name: str) -> tuple[str, str | None, int | str | None]:
    """(kind, token group, layer) of an arm name: fixed arms ('fixed', None, None); cells ('cell', group, layer | 'emb');
    margins ('b' / 'w', 'bridge', layer)."""
    if name in FIXED_ARMS:
        return "fixed", None, None
    if name.startswith("g"):
        g, la = name[1:].rsplit("@", 1)
        return "cell", g, (EMB if la == EMB else int(la))
    assert name[0] in "bw", name
    return name[0], "bridge", int(name[1:])


def stage_plan() -> dict:
    """Tokenizer only: per design the items, drops, groups, the reads per item (the GPU estimate's count) and one example
    (seed 0) with every token group marked on the lookup's prompt."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target, layer = pins.TARGET, X.PREDICTED[pins.TARGET]
    layers = layer_grid(pins.N_LAYERS, STEP[target], layer)
    out: dict[str, Any] = {"target": target, "layer": layer, "n_layers": pins.N_LAYERS, "layers": layers}
    for design in DESIGNS:
        items, counts = select(tok, design, C.SOURCES[design][target], layer)
        reads = [len(arm_names(list(it["token_groups"][w]), layers)) for it in items for w in X.READERS]
        counts["reads"] = {"per_reader_item": dict(collections.Counter(reads)), "total": sum(reads)}
        if items:
            it = items[C.example_indices(len(items), 1)[0]]
            counts["example"] = {"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}",
                                 "group": it["group"], "locker_roles": it["locker_roles"],
                                 "lookup_O_marked": item_marked(it, X.LOOKUP)}  # fmt: skip
        out[design] = counts
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def item_marked(it: dict, reader: str) -> str:
    """The reader's O prompt as the model reads it, every token group marked ⟦group:…⟧ (the read's space token last)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import x45m, x45p

    tok = x45m.tokenizer()
    text = it["readers"][reader]["text"]["org"] + it["read_suffix"]
    off = raw_encoding(tok, text, offsets=True)["offset_mapping"]
    spans = []
    for g, positions in it["token_groups"][reader].items():
        spans += [(a, b, g) for a, b in B.merged_spans(off, positions)]
    return x45p.marked(text, spans)


# ---- GPU ----------------------------------------------------------------------------------------------------------


def arm_edits(add_rows, set_rows, h_o: dict, h_s: dict, groups: dict[str, list[int]], pick: list[int], layer: int,
              layers: list[int], n_layers: int) -> dict[str, tuple[str, dict]]:  # fmt: skip
    """Each arm's (prompt, edit set) in arm_names order: the prompt 'org', 'swap' or 'alt' (x47_cumulative.prompts_of),
    an edit set {layer: SetRows / AddRows} on block outputs. h_o: O's block outputs at L; h_s: S's at every layer."""
    pos = groups["bridge"][0]

    def place(positions: list[int], las) -> dict:
        return {la: set_rows(h_s[la][list(positions)], list(positions)) for la in las}

    out: dict[str, tuple[str, dict]] = {
        "none": ("org", {}), "a": ("org", {layer: add_rows((h_s[layer][pos] - h_o[layer][pos])[None], [pos])}),
        "d": ("swap", place(pick, range(n_layers))), "S": ("alt", {})}  # fmt: skip
    for g in TOKEN_GROUPS:
        if g not in groups:
            continue
        if g == "bridge":
            out[f"g{g}@{EMB}"] = ("swap", {})
        for la in layers:
            out[f"g{g}@{la}"] = ("org", place(groups[g], [la]))
    for la in layers:
        out[f"b{la}"] = ("swap", place([pos], range(la + 1)))
    for la in layers:
        out[f"w{la}"] = ("org", place([pos], range(la, n_layers)))
    assert list(out) == arm_names(list(groups), layers)
    return out


def read_row(lg, rd: dict) -> list:
    """[switched, role, logit(alt) - logit(org)]: the decisive read as X0's (the top token is S's answer's first
    token), compact."""
    top = int(lg.argmax())
    role = "b" if top == rd["tok_b"] else "A" if top == rd["tok_A"] else "other"
    return [int(top == rd["tok_b"]), role, round(float(lg[rd["tok_b"]] - lg[rd["tok_A"]]), 3)]


GREEDY_ARMS = ("none", "a", "d", "S", f"g{'bridge'}@{EMB}")  # plus b<L> and w<L>: the view's greedy texts


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import suite_split as SUITE
    from scripts.exp04_brew_parts import AddRows, SetRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "D1 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in STEP, f"D1 runs on {sorted(STEP)}, not {target}"
    layer, n_layers = X.PREDICTED[target], pins.N_LAYERS
    layers = layer_grid(n_layers, STEP[target], layer)
    runs = {d: C.SOURCES[d][target] for d in DESIGNS}
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    srcs = [X.RESULTS / r for r in runs.values()]
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": "D1+D2 (batch 47, amendment 3)",
         "spec": "jobs/c3/batch47.yaml (D1, D2)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(s / f for s in srcs for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl")))},
         "sources": runs, "layer": layer, "n_layers": n_layers, "layers": layers, "step": STEP[target],
         "token_groups": GROUP_TEXT, "arms": ARM_TEXT, "late_band_start": LATE_BAND.get(target),
         "prompts": {"org": "O", "swap": "O with S's token at the bridge (its input embedding swapped)", "alt": "S"},
         "states": "set (SetRows) from one unedited forward of S per reader (every layer; the space token appended) and "
                   "of O (layer L); the readers' prompts differ from the question on",
         "items_rule": "x47_cumulative's items (main test: its 200, mixed scenes in 'all' only; clean design: the "
                       "locker-first and locker-after scenes, its mixed left out), its asserts; each reader's token "
                       "groups by character overlap (x47_depthmap.token_groups)",
         "groups": "x45m.group_of: locker-first (both locker sentences before the asked pick), locker-after, mixed",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = top token is S's answer",
         "state_check": f"47.4's: under b{layer} on O's tokens the bridge's state after L is S's on prefix-identical "
                        f"items (relative distance <= {C.STATE_TOL})",
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "fresh_draws": X.FRESH_SEED},
         "n_boot": X.N_BOOT, "order": {"items": "per design (main, clean), the source run's scene order",
                                       "reads": "per item and reader: the arms in arm_names order, batches of BJ_SUITE_BATCH",
                                       "batch": SUITE.BATCH},
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    m["designs"] = list(DESIGNS)
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {"question": NO_PREDICTION, "batch": 52, "sealed": "none (batch 52 coverage)"}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    assert len(model.layers) == n_layers, f"{len(model.layers)} blocks, pins say {n_layers}"
    items: list[dict] = []
    plan = {}
    for design in DESIGNS:
        got, counts = select(tok, design, runs[design], layer)
        items += got
        plan[design] = counts
        print(json.dumps(counts, ensure_ascii=False), flush=True)
    (out / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    assert items, "no items"
    examples = {d: set(C.example_indices(sum(it["design"] == d for it in items))) for d in DESIGNS}
    after = list(range(layer + 1, n_layers))
    greedy_arms = (*GREEDY_ARMS, f"b{layer}", f"w{layer}")
    rows, checks, greedy = [], [], []
    with torch.no_grad():
        for design in DESIGNS:
            mine = [it for it in items if it["design"] == design]
            for i, it in enumerate(progress(mine, f"D1+D2 {design} at L{layer}, {len(layers)} layers (item)")):
                C.assert_item(it)
                for w, rd in it["readers"].items():
                    prompts = {k: v + it["space"] for k, v in C.prompts_of(rd["ids"], it["pos"]).items()}
                    h_o = model.run(torch.tensor([prompts["org"]], device=model.device), record=(layer,))[1]
                    h_s = model.run(torch.tensor([prompts["alt"]], device=model.device), record=tuple(range(n_layers)))[
                        1
                    ]
                    groups = it["token_groups"][w]
                    arms = arm_edits(AddRows, SetRows, h_o, h_s, groups, it["pick"], layer, layers, n_layers)
                    if w == X.LOOKUP:
                        blocks = {la: e for la, e in arms[f"b{layer}"][1].items()}
                        gap = C.state_gap(model, prompts["org"], blocks, h_s, it["pos"], after)
                        worst = max(range(len(gap)), key=gap.__getitem__)
                        checks.append({"scene": it["scene"], "design": design, "group": it["group"],
                                       "upstream": it["upstream"], "prefix_same": it["prefix_same"],
                                       "gap_max": gap[worst], "gap_layer": after[worst]})  # fmt: skip
                    names = list(arms)
                    logits = C.read_rows(model, [prompts[arms[a][0]] for a in names], [arms[a][1] for a in names])
                    rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "design": design,
                                 "group": it["group"], "upstream": it["upstream"], "prefix_same": it["prefix_same"],
                                 "reader": w, "reads": {a: read_row(lg, rd) for a, lg in zip(names, logits, strict=True)},
                                 "top": {a: tok.decode([int(lg.argmax())]) for a, lg in zip(names, logits, strict=True)
                                         if a in greedy_arms}})  # fmt: skip
                    if i in examples[design]:
                        gen = torch.tensor([prompts[arms[a][0]] for a in greedy_arms], device=model.device)
                        texts = model.generate_batch(gen, X.GEN_TOKENS, [arms[a][1] for a in greedy_arms])
                        greedy += [{"scene": it["scene"], "design": design, "reader": w, "arm": a, "greedy": t}
                                   for a, t in zip(greedy_arms, texts, strict=True)]  # fmt: skip
                    del h_o, h_s, arms
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "checks.jsonl", checks)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    bad = C.state_flags(checks)
    print(
        f"wrote {out}: {sum(len(r['reads']) for r in rows)} reads of {len(items)} items (sealed: no verdict)",
        flush=True,
    )
    print(C.state_line(checks), flush=True)
    if bad:
        raise SystemExit(f"BUG (D1, stop and report): under the bridge swap at blocks 0..L the bridge's state after L is "
                         f"not S's on {len(bad)} items whose O and S agree before the bridge, e.g. {bad[:3]}")  # fmt: skip
    return out


# ---- verdict (CPU, sealed) ------------------------------------------------------------------------------------------


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer under **Q-depth** (its block's 'Dan:' line) in the predictions file at `rev`, '' if none."""
    import re
    import subprocess

    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0].split("\n## ", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def rates(rows: list[dict], arms: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict[str, list]:
    """Per arm [rate, lo, hi] over the rows (one reader's items): points from counts, X0's cluster bootstrap over the
    bridge entities, the same draws for every arm. An arm a row lacks counts as absent for that arm (the group is not in
    the item): its rate is over the rows that have it."""
    entities = [r["entity"] for r in rows]
    out = {}
    have_all = [a for a in arms if all(a in r["reads"] for r in rows)]
    if have_all:
        sw = {a: [r["reads"][a][0] for r in rows] for a in have_all}
        boot = X.resampled_rates(sw, entities, n_boot, seed)
        out |= {a: [sum(sw[a]) / len(rows), *X.interval(boot[a])] for a in have_all}
    for a in arms:
        if a in out:
            continue
        mine = [r for r in rows if a in r["reads"]]
        if not mine:
            continue
        sw = {a: [r["reads"][a][0] for r in mine]}
        boot = X.resampled_rates(sw, [r["entity"] for r in mine], n_boot, seed)
        out[a] = [sum(sw[a]) / len(mine), *X.interval(boot[a]), len(mine)]
    return out


def last_hot(cells: dict[str, list], layers: list[int], group: str, bar: float = HOT) -> int | None:
    """The last sampled layer at which the group's cell is >= bar (point estimate), None if none."""
    hot = [la for la in layers if f"g{group}@{la}" in cells and cells[f"g{group}@{la}"][0] >= bar - EPS]
    return max(hot) if hot else None


def l_r(cells: dict[str, list], layers: list[int], floor: float = W_FLOOR) -> int | None:
    """D2: the first sampled l at which the w curve is <= floor (point estimate), None if never."""
    return next((la for la in layers if cells[f"w{la}"][0] <= floor + EPS), None)


def rule_a(lookup: dict[str, list], layers: list[int], groups: list[str]) -> dict[str, Any]:
    """D1 (a), locker-after: every bridge cell <= 0.25 and some locker-sentence cell >= 0.5 (the lookup)."""
    bridge = [lookup[f"gbridge@{la}"][0] for la in (EMB, *layers) if f"gbridge@{la}" in lookup]
    lockers = {a: v[0] for a, v in lookup.items() if a.startswith("glk_")}
    best = max(lockers.items(), key=lambda kv: kv[1]) if lockers else ("-", math.nan)
    ok_b, ok_l = bool(bridge) and max(bridge) <= BRIDGE_MAX + EPS, bool(lockers) and best[1] >= LOCKER_MIN - EPS
    return {"holds": ok_b and ok_l, "bridge_max": max(bridge) if bridge else None, "bridge_ok": ok_b,
            "locker_best": {"arm": best[0], "rate": best[1]}, "locker_ok": ok_l, "groups": groups}  # fmt: skip


def rule_b(lookup: dict[str, list], recall: dict[str, list], layers: list[int], lead: int) -> dict[str, Any]:
    """D1 (b), locker-first: the last layer with the lookup's bridge cell >= 0.3 is earlier than the recall's by >= lead."""
    lk, rc = last_hot(lookup, layers, "bridge"), last_hot(recall, layers, "bridge")
    ok = lk is not None and rc is not None and rc - lk >= lead
    return {"holds": ok, "lookup_last": lk, "recall_last": rc, "lead_needed": lead,
            "lead": None if lk is None or rc is None else rc - lk}  # fmt: skip


def rule_c(first: dict[str, list] | None, after: dict[str, list] | None, layers: list[int]) -> dict[str, Any]:
    """D1 (c): the recall's lk_cf item cell >= 0.3 at some layer in locker-first and < 0.3 at every layer in
    locker-after."""
    peak = lambda cells: max((cells[f"glk_cf_item@{la}"][0] for la in layers if f"glk_cf_item@{la}" in cells),  # noqa: E731
                             default=None)  # fmt: skip
    pf, pa = (peak(first) if first else None), (peak(after) if after else None)
    ok = pf is not None and pf >= HOT - EPS and pa is not None and pa < HOT - EPS
    return {"holds": ok, "locker_first_peak": pf, "locker_after_peak": pa}


def rule_d2(l_recall: int | None, band: int | None) -> dict[str, Any]:
    """D2: l_R(recall) at or below the start of Zach's late band (no band: not scored)."""
    if band is None:
        return {"holds": None, "l_R_recall": l_recall, "band_start": None, "why": "no band on this model"}
    return {"holds": l_recall is not None and l_recall <= band, "l_R_recall": l_recall, "band_start": band}


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending, or per design and order group each reader's cells (every arm's rate), l_R, and the
    rules per design; the state check and the side checks beside."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no D1 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    target, layers = m["model"]["target"], m["layers"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    checks = X.read_jsonl(src / "checks.jsonl")
    arms = list(dict.fromkeys(a for r in rows for a in r["reads"]))
    cells: dict[str, dict[str, dict[str, Any]]] = {}
    rules: dict[str, dict[str, Any]] = {}
    for design in DESIGNS:
        cells[design] = {}
        for g in GROUPS:
            per_reader = {}
            for w in X.READERS:
                mine = [r for r in rows if r["design"] == design and r["reader"] == w and g in ("all", r["group"])]
                if mine:
                    per_reader[READER_NAME[w]] = {"n": len(mine), "entities": len({r["entity"] for r in mine}),
                                                  "cells": rates(mine, arms, n_boot)}  # fmt: skip
                    per_reader[READER_NAME[w]]["l_R"] = l_r(per_reader[READER_NAME[w]]["cells"], layers)
            cells[design][g] = per_reader
        lf, la_ = cells[design]["locker-first"], cells[design]["locker-after"]
        groups_present = sorted({a[1:].rsplit("@", 1)[0] for a in arms if a.startswith("g")})
        rules[design] = {
            "a": rule_a(la_["lookup"]["cells"], layers, groups_present) if "lookup" in la_ else {"holds": None, "why": "no locker-after items"},
            "b": rule_b(lf["lookup"]["cells"], lf["recall"]["cells"], layers, LEAD[target]) if "lookup" in lf else {"holds": None, "why": "no locker-first items"},
            "c": rule_c(lf.get("recall", {}).get("cells"), la_.get("recall", {}).get("cells"), layers),
            "d2": rule_d2(cells[design]["all"]["recall"]["l_R"] if "recall" in cells[design]["all"] else None, LATE_BAND.get(target)),
        }  # fmt: skip
    same = [c["gap_max"] for c in checks if c["prefix_same"]]
    state = {"n_prefix_same": len(same), "max": max(same, default=None), "flagged": C.state_flags(checks)}
    side = {}
    for design in DESIGNS:
        for w in X.READERS:
            mine = [r for r in rows if r["design"] == design and r["reader"] == w]
            side[f"{design} {READER_NAME[w]}"] = {
                "n": len(mine), "none_reads_O": sum(r["reads"]["none"][1] == "A" for r in mine),
                "S_reads_S": sum(r["reads"]["S"][0] for r in mine),
                "a_switches": sum(r["reads"]["a"][0] for r in mine),
                "clean_b_vs_S_disagree": sum(r["reads"][f"b{m['layer']}"][0] != r["reads"]["S"][0] for r in mine)
                if design == "clean" else None}  # fmt: skip
    return {"run": run, "target": target, "layer": m["layer"], "n_layers": m["n_layers"], "layers": layers,
            "sources": m["sources"], "status": "tested", "cells": cells, "rules": rules, "state": state, "checks": side,
            "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def yes(v) -> str:
    return "-" if v is None else "yes" if v else "no"


def fmt(v: list | None) -> str:
    return "-" if not v else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def map_lines(cells: dict[str, list], layers: list[int], groups: list[str]) -> list[str]:
    """One reader's map as a table: a row per token group (emb first for the bridge), the b and w margins, a column per
    sampled layer; the point estimate only (the json holds the intervals)."""
    head = "| group | " + " | ".join(["emb", *map(str, layers)]) + " |"
    lines = [head, "|---|" + "---|" * (len(layers) + 1)]
    for g in groups:
        emb = f"{cells[f'g{g}@{EMB}'][0]:.2f}" if f"g{g}@{EMB}" in cells else ""
        vals = [f"{cells[f'g{g}@{la}'][0]:.2f}" if f"g{g}@{la}" in cells else "" for la in layers]
        lines.append(f"| {g} | {emb} | " + " | ".join(vals) + " |")
    for k, label in (("b", "margin b: bridge at every layer <= l"), ("w", "D2 w: bridge at every layer >= l")):
        lines.append(f"| {label} | | " + " | ".join(f"{cells[f'{k}{la}'][0]:.2f}" for la in layers) + " |")
    lines.append(
        f"| margin d: pick sentence at every layer | {cells['d'][0]:.2f} | " + " | ".join("" for _ in layers) + " |"
    )
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """D1 + D2's verdict (sealed until Q-depth), or with coverage (batch 52) the same rules on the given runs only, no
    seal guard, "no prediction" in place of Dan's answer, written to x52_depthmap-<UTC>/."""
    answer = NO_PREDICTION if coverage else unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"}
               for t in RUNS if t not in targets and not coverage]  # fmt: skip
    tested = [m for m in models if m["status"] == "tested"]
    out = RESULTS / f"{'x52_depthmap' if coverage else 'depth'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    who = f"Batch 52 coverage ({answer}; designs {list(DESIGNS)})" if coverage else f"{QUESTION}, Dan: {answer}"
    lines = ["# D1 + D2 (batch 47, amendment 3): the token x layer causal map, and window patching", "",
             f"{who}. Cells = S's state placed into O at one token group and one layer; the switch "
             "rate over the order group's items (X0's chat read; switch = the top token is S's answer); cluster "
             f"bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}; intervals in depth.json). Rules scored per "
             "design, point estimates; the Q-depth answer reads the clean design, the main test beside it. UNVERIFIED.",
             ""]  # fmt: skip
    flags = [f"{m['target']}: the bridge's state after L is not S's on {len(m['state']['flagged'])} prefix-identical items"
             for m in tested if m["state"]["flagged"]]  # fmt: skip
    if flags:
        lines += ["## <<< BUG FLAG: STOP AND REPORT >>>", "", *[f"- **{f}**" for f in flags], ""]
    lines += ["## Rules", "", "| model | design | D1 (a) locker-after: bridge <= 0.25, a locker cell >= 0.5 | D1 (b) "
              "locker-first: lookup's bridge mass ends first | D1 (c) recall's lk_cf item hot in locker-first only | D2: "
              "l_R(recall) <= late band |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | | pending ({m['why']}) | | | |")
            continue
        for design in DESIGNS:
            r = m["rules"][design]
            a, b, c, d2 = r["a"], r["b"], r["c"], r["d2"]
            lines.append(
                f"| {m['target']} | {design} | {yes(a['holds'])} (bridge max {a.get('bridge_max')}, best locker "
                f"{a.get('locker_best')}) | {yes(b['holds'])} (lookup last {b.get('lookup_last')}, recall last "
                f"{b.get('recall_last')}, lead {b.get('lead')} of {b.get('lead_needed')}) | {yes(c['holds'])} (peaks "
                f"first {c['locker_first_peak']}, after {c['locker_after_peak']}) | {yes(d2['holds'])} (l_R recall "
                f"{d2['l_R_recall']}, band {d2['band_start']}) |")  # fmt: skip
    lines += ["", "## l_R per reader (D2: the first sampled layer where the w curve is <= 0.1)", "",
              "| model | design | order | lookup l_R | recall l_R | n |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for design in DESIGNS:
            for g in GROUPS:
                pr = m["cells"][design][g]
                if "lookup" in pr:
                    lines.append(f"| {m['target']} | {design} | {g} | {pr['lookup']['l_R']} | {pr['recall']['l_R']} | "
                                 f"{pr['lookup']['n']} |")  # fmt: skip
    for m in tested:
        lines += ["", f"## Maps: {m['target']} (L{m['layer']}, {m['n_layers']} layers; sampled {m['layers']})"]
        for design in DESIGNS:
            for g in GROUPS[:2]:
                pr = m["cells"][design][g]
                for w in ("lookup", "recall"):
                    if w not in pr:
                        continue
                    c = pr[w]["cells"]
                    groups = [x for x in TOKEN_GROUPS if any(a.startswith(f"g{x}@") for a in c)]
                    lines += ["", f"### {design}, {g}, {w} (n = {pr[w]['n']}, {pr[w]['entities']} bridge items; none "
                              f"{c['none'][0]:.2f}, a {fmt(c['a'])}, S {c['S'][0]:.2f}; l_R {pr[w]['l_R']})", "",
                              *map_lines(c, m["layers"], groups)]  # fmt: skip
    lines += ["", "## Checks", ""]
    for m in tested:
        s = m["state"]
        lines.append(f"- {m['target']}, states: the bridge after L under b{m['layer']} on O's tokens vs S's, max relative "
                     f"distance {s['max']} over {s['n_prefix_same']} prefix-identical items, flagged {len(s['flagged'])}")  # fmt: skip
        for key, c in m["checks"].items():
            lines.append(f"- {m['target']}, {key}: O unedited reads O's answer on {c['none_reads_O']} of {c['n']}; S reads "
                         f"S's on {c['S_reads_S']}; (a) switches {c['a_switches']}"
                         + (f"; b{m['layer']} vs S disagree on {c['clean_b_vs_S_disagree']} (S's own run)"
                            if c["clean_b_vs_S_disagree"] is not None else ""))  # fmt: skip
        for design, p in m["plan"].items():
            lines.append(f"- {m['target']}, {design} items: {p['items']} of {p['items_at_L']} at L from {p['source']} "
                         f"(dropped {p['dropped'] or 'none'}; mixed left out {p['mixed_left_out']}; groups {p['groups']}; "
                         f"{p['entities']} bridge items)")  # fmt: skip
    lines += ["", "Token groups: " + "; ".join(f"{g} = {t}" for g, t in GROUP_TEXT.items()) + ".",
              "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]  # fmt: skip
    (out / "depth.json").write_text(json.dumps({"runs": runs, "dan": answer, "flags": flags, "models": models}, indent=1)
                                    + "\n")  # fmt: skip
    (out / "depth.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> Path:
    """The verify-pack view: per design k random items (seed 0), each reader's O prompt with every token group marked,
    and the fixed arms', b<L>'s, w<L>'s and the emb cell's answers (the top token and the greedy text)."""
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# D1 + D2 verify-pack view: prompts exactly as the model reads them (the read appends the digit's space "
             "token); every token group marked ⟦group:…⟧. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        if not (src / "outcomes.jsonl").exists():
            continue
        m = json.loads((src / "manifest.json").read_text())
        cases = X.read_jsonl(src / "cases.jsonl")
        reads = {(r["design"], r["scene"], r["reader"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
        greedy = {(g["design"], g["scene"], g["reader"], g["arm"]): g["greedy"]
                  for g in X.read_jsonl(src / "examples_greedy.jsonl")}  # fmt: skip
        lines += [f"## {run} ({m['model']['target']}, L{m['layer']} of {m['n_layers']}; sampled {m['layers']})", ""]
        for design in DESIGNS:
            items = [c for c in cases if c["design"] == design]
            lines += [f"### {design}: {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
            for i in C.example_indices(len(items), k, seed):
                it = items[i]
                lines += [f"#### {it['scene']} ({it['domain']}, {it['group']}): bridge {it['entity']} → {it['cf_bridge']}; "
                          f"lockers {it['locker_roles']}", ""]  # fmt: skip
                for w, rd in it["readers"].items():
                    r = reads[(design, it["scene"], w)]
                    lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}",
                              "", "```", item_marked(it, w), "```", "", "| arm | top token | switched | greedy |",
                              "|---|---|---|---|"]  # fmt: skip
                    for a, top in r["top"].items():
                        lines.append(
                            f"| {a} | {top!r} | {r['reads'][a][0]} | {greedy.get((design, it['scene'], w, a))!r} |"
                        )
                    lines.append("")
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out / "view.md")
    return out


# ---- figures (story_style) ------------------------------------------------------------------------------------------


def heatmap(ax, cells: dict[str, list], layers: list[int], groups: list[str], label_rows: bool = True) -> Any:
    """One reader's map: rows = token groups then the two margins (b: bridge at every layer <= l; w: at every layer
    >= l), columns = emb then the sampled layers; a cell's colour = its switch rate; the d margin in the corner."""
    import numpy as np

    cols = [EMB, *layers]
    rows = [*groups, "b: bridge ≤ l", "w: bridge ≥ l"]
    grid = np.full((len(rows), len(cols)), np.nan)
    for i, g in enumerate(groups):
        for j, la in enumerate(cols):
            a = f"g{g}@{la}"
            if a in cells:
                grid[i, j] = cells[a][0]
    for i, k in ((len(groups), "b"), (len(groups) + 1, "w")):
        for j, la in enumerate(layers, start=1):
            grid[i, j] = cells[f"{k}{la}"][0]
    im = ax.imshow(grid, cmap="Purples", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(cols)), [str(c) for c in cols], fontsize=8)
    ax.set_yticks(range(len(rows)), rows if label_rows else [""] * len(rows), fontsize=9)
    ax.axhline(len(groups) - 0.5, color="white", lw=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return im


def stage_figures(verdict_dir: Path) -> list[Path]:
    """Per model and order group: two heatmaps (lookup, recall) per design, token group x layer, with the margins; the
    README's style (story_style), saved beside the verdict (never into figures/)."""
    unsealed()
    from scripts import story_style as S

    plt = S.setup()
    blob = json.loads((verdict_dir / "depth.json").read_text())
    folder = verdict_dir / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-figures"
    folder.mkdir()
    made = []
    for m in blob["models"]:
        if m["status"] != "tested":
            continue
        short = next((s for key, s, _ in S.MODELS if key == m["target"]), m["target"])
        for g in GROUPS[:2]:
            fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, 7.6), sharex=True)
            for i, design in enumerate(DESIGNS):
                for j, w in enumerate(("lookup", "recall")):
                    ax = axes[i][j]
                    pr = m["cells"][design][g].get(w)
                    if not pr:
                        S.empty(ax, "no items")
                        continue
                    c = pr["cells"]
                    groups = [x for x in TOKEN_GROUPS if any(a.startswith(f"g{x}@") for a in c)]
                    im = heatmap(ax, c, m["layers"], groups, label_rows=(j == 0))
                    ax.set_title(f"{design} design, {w}\nn = {pr['n']}; l_R = {pr['l_R']}; d = {c['d'][0]:.2f}",
                                 fontsize=9, color=S.COL[w])  # fmt: skip
            fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02, label="switch rate")
            S.title(fig, f"{short}, {g}: where and when each reader reads the change",
                    "rows: the group whose state is S's; margins b (bridge ≤ l), w (bridge ≥ l), d (pick sentence, "
                    "all layers)")  # fmt: skip
            fig.text(0.5, 0.015, "layer at which S's state is placed (emb = the token swapped, no state placed)",
                     ha="center", va="bottom", fontsize=S.FONT)  # fmt: skip
            fig.subplots_adjust(top=0.86, bottom=0.1, left=0.2, right=0.86, hspace=0.35, wspace=0.08)
            path = folder / f"depthmap_{short}_{g.replace('-', '_')}.png"
            fig.savefig(path, dpi=200, facecolor="white")
            plt.close(fig)
            made.append(path)
    print("\n".join(map(str, made)))
    return made


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view", "figures"])
    ap.add_argument("--name", help="run: the run name (results/x47_depthmap/<name>/)")
    ap.add_argument("--why", default="batch 47, amendment 3 (jobs/c3/batch47.yaml; D1 + D2, Q-depth, sealed)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the D1 runs")
    ap.add_argument("--verdict", type=Path, help="figures: the verdict folder (results/x47_depthmap/depth-<UTC>)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--designs", nargs="+", choices=list(C.DESIGNS), default=list(C.DESIGNS),
                    help="run / verdict: these designs only (batch 52: Lightning's main test; its clean design fails the gate)")  # fmt: skip
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    global DESIGNS
    DESIGNS = tuple(d for d in C.DESIGNS if d in a.designs)  # the order of C.DESIGNS
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, a.coverage)
    elif a.stage == "view":
        stage_view(a.runs)
    else:
        assert a.verdict, "figures needs --verdict"
        stage_figures(a.verdict)


if __name__ == "__main__":
    main()
