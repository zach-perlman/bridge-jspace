"""x47_cumulative (batch 47, test 47.4; jobs/c3/batch47.yaml, design and readings fixed in advance; Q47.4 in
predictions/2026-10-28_dan.md): why does not every answer switch? Cumulative patches at the bridge token.

O = the original prompt, S = the changed one. Two designs per model, each from the model's own X0 run at the layer fixed
in advance (chat): the main test (x0_necessity, alt cf: two people swap their picks, so S also changes the other
person's pick token) and the clean design (45m, x0_necessity --alt fresh: a locker item nobody picks becomes S's asked
pick; only the bridge token changes). Items: the scenes of the source run's chat outcomes at L, i.e. the items its
unedited run made eligible (org and alt said and read right by both readers); eligibility is never recounted under a
patch. The cases are rebuilt with X.build_cases on the target's tokenizer and must equal the run's (ids, bridge position).

Arms, each one forward of one prompt, read by both readers with X0's chat read (the prompt with a digit's space token
appended; switch = the top token over the vocabulary is S's answer's first token):
  none      O unedited
  a         h_S - h_O added at the bridge token at L (X0's whole arm: the existing cell)
  b         the bridge token swapped at every layer <= L: its state set to S's at the block outputs 0..L, and its input
            embedding swapped (O's prompt carries S's bridge token; the input of block 0 is a layer too)
  c         the same at every layer, block outputs 0..n_layers - 1: the bridge token fully swapped at all depths
  d         every token of the asked pick sentence swapped at every layer (each set to S's at every block output, and the
            embedding swapped: only the bridge's id differs inside the sentence)
  b_blocks  b on O's own tokens (block outputs 0..L only; descriptive: what later tokens read from the raw token at
            block 0, b - b_blocks)
  S         S read on S (unedited)
States are set, not added (exp04_brew_parts.SetRows): adding each layer's clean difference at layer after layer adds it
on top of the earlier ones and overshoots. They come from one unedited forward of S (every layer) and of O (layer L) on
the lookup's prompts; both readers' prompts agree through the last patched token (asserted), so the states serve both.

Asserted per item (an item failing one is dropped and counted in plan.json): O and S have the same length and differ
only at the bridge token (clean) or at the bridge token and one token of the other person's pick sentence (main); the
asked pick sentence covers the same positions in O and S, with the same ids but the bridge's (so its person token is the
same); both readers' prompts agree through the last patched token. The run asserts the same again on every kept item.

Readings (as computed; the job specs' decision_rule carries the same paragraph): per model, design, reader and order
group (x45m's grouping: locker-first = the bridge's and S's bridge's locker sentences both before the asked pick;
locker-after = both after; mixed scenes in "all" only), over the group's items: before L = S_b - S_a; propagation =
S_c - S_b; the pick sentence's other tokens = S_d - S_c; outside the pick sentence = 1 - S_d; they sum to the non-switch
1 - S_a. Points from counts; 95% intervals from a cluster bootstrap over bridge items (10,000, seed 0; every arm on the
same draws). Q47.4 reads the lookup in locker-first scenes: the largest of before L / other pick tokens / outside the
pick sentence (point estimates), per model and design. Descriptive; no bar. The main test's locker-first rows are also
split by whether the other changed pick comes before or after the asked one (descriptive).

The bug check (Dan: "(b)->(c) should be ~ 0 ... a non-zero difference is a bug, stop and report"), flagged at the top of
the verdict: on items whose O and S agree before the bridge (every clean item; main items whose other changed pick comes
after the asked one), (b) and (c) must give the same read; more than BUG_TOL of such items disagreeing in a (design,
reader) cell is a bug, not a result. The run checks the states too: under b_blocks the bridge token's state at every
layer after L must equal S's on those items (relative distance <= STATE_TOL); a failure is printed and fails the job
after its files are written. In the clean design (b), (c) and (d) are S's own run by construction (the bridge is the
only changed token, and with it swapped at every layer up to L everything after it is recomputed as S's), so there the
decomposition has one term, (a)->(b), and those arms must read S's answer wherever S read on S does (also flagged). In
main items whose other changed pick comes first, (b)->(c) is not expected to be 0 (the bridge's later states read that
pick in S): reported, not flagged.

SEALED (as batch 45): the run writes per-item files only; verdict, view and figures refuse until
predictions/2026-10-28_dan.md holds Dan's committed Q47.4 answer at HEAD.

uv run python scripts/x47_cumulative.py plan                                            # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_cumulative.py run --name qwen35_9b_x47_cumulative   # GPU (sealed)
uv run python scripts/x47_cumulative.py verdict    # CPU, after Dan's Q47.4: the table (default: the three runs)
uv run python scripts/x47_cumulative.py view       # CPU, after Dan's Q47.4: the verify-pack view, 10 items per design
uv run python scripts/x47_cumulative.py figures --verdict results/x47_cumulative/x47_4-<UTC>
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_strata as ST
from scripts import x45b_binding as B

EXP = "x47_cumulative"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.4"
RENDERING = "chat"
DESIGNS = ("main", "clean")
ALT = {"main": "cf", "clean": "fresh"}  # the x0_necessity alt each design's source run was made with
SOURCES = {"main": B.MAIN_RUN, "clean": B.FRESH_RUN}  # design -> target -> the source X0 run (main test / 45m)
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_cumulative", "qwen3.6-27b": "x47_cumulative_27b",
        "muse-glimmer-30b": "muse30_x47_cumulative"}  # fmt: skip
ARMS = ("none", "a", "b", "c", "d", "b_blocks", "S")
ARM_TEXT = {
    "none": "O unedited",
    "a": "(a) h_S - h_O added at the bridge token at L (X0's whole arm)",
    "b": "(b) the bridge token swapped at every layer <= L (block outputs 0..L, and its input embedding)",
    "c": "(c) the bridge token swapped at every layer (block outputs 0..n_layers - 1, and its input embedding)",
    "d": "(d) every token of the asked pick sentence swapped at every layer (and the bridge's input embedding)",
    "b_blocks": "(b) on O's own tokens: block outputs 0..L only, no embedding swap (descriptive)",
    "S": "S read on S (unedited)",
}
TERMS = {"before_L": ("a", "b"), "propagation": ("b", "c"), "pick_other": ("c", "d"), "outside": ("d", None)}
TERM_TEXT = {"before_L": "read before L at the bridge token, (a)->(b)",
             "propagation": "(b)->(c), should be ~0",
             "pick_other": "carried by the pick sentence's other tokens, (c)->(d)",
             "outside": "carried outside the pick sentence, (d)->100%"}  # fmt: skip
CANDIDATES = ("before_L", "pick_other", "outside")  # Q47.4's three terms
GROUPS = ("locker-first", "locker-after", "all")
SPLIT = ("locker-first, other change first", "locker-first, other change after")  # the main test only (descriptive)
GROUP_OF = {"locker-before": "locker-first", "locker-after": "locker-after", "mixed": "mixed"}  # x45m.group_of's names
BUG_TOL = 0.02  # the share of prefix-identical items on which (b) and (c) may disagree (batched-kernel rounding)
STATE_TOL = 0.05  # the bridge token's relative state distance to S's after L under b_blocks (prefix-identical items)
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


class Misaligned(ValueError):
    """O and S (or the readers' prompts) do not line up as the arms need."""


# ---- items (tokenizer only) ---------------------------------------------------------------------------------------


def changed_positions(ids_o: list[int], ids_s: list[int]) -> list[int]:
    """The positions where O and S hold different ids; raises Misaligned if their lengths differ."""
    if len(ids_o) != len(ids_s):
        raise Misaligned("O and S differ in length")
    return [i for i, (a, b) in enumerate(zip(ids_o, ids_s, strict=True)) if a != b]


def expected_changes(design: str, diff: list[int], pos: int) -> int | None:
    """The other changed token's position (main) or None (clean); raises Misaligned unless O and S differ exactly at
    the bridge token (clean), or at the bridge token and one other token (main)."""
    if design == "clean":
        if diff != [pos]:
            raise Misaligned("O and S differ beyond the bridge token")
        return None
    others = [p for p in diff if p != pos]
    if pos not in diff or len(others) != 1:
        raise Misaligned("O and S do not differ at exactly the bridge token and one other token")
    return others[0]


def sentence_start(text: str, context: str, sentence: str) -> int:
    """The sentence's first character in the rendered prompt (the context once in it, the sentence once in that)."""
    from scripts import statement_positions as SP

    assert text.count(context) == 1, "the context is not once in the prompt"
    return text.index(context) + SP.find_sentence(context, sentence)


def pick_sentence(item: dict, context: str, bridge: str) -> str:
    """The asked person's pick sentence ('<person> picked [the] <bridge>.') of a context (tasks_statements)."""
    from scripts import statement_positions as SP

    return SP.tasks_statements({**item, "context": context, "bridge": bridge})["bind_bridge"]


def pick_positions(
    texts: dict[str, str], offsets: dict[str, list[tuple[int, int]]], ids: dict[str, list[int]], sentences: dict[str, str],
    contexts: dict[str, str], pos: int,
) -> tuple[list[int], list[int]]:  # fmt: skip
    """The asked pick sentence's token positions (the same in O and S) and its person's token positions, by character
    overlap; raises Misaligned unless the sentence covers the same positions in both, holds the bridge token, and has
    the same ids in O and S everywhere but the bridge (so the person token is the same)."""
    from scripts import statement_positions as SP

    start = {v: sentence_start(texts[v], contexts[v], sentences[v]) for v in ("org", "alt")}
    pick = {v: SP.tokens_in(offsets[v], start[v], start[v] + len(sentences[v])) for v in ("org", "alt")}
    if pick["org"] != pick["alt"]:
        raise Misaligned("the asked pick sentence covers different positions in O and S")
    p = pick["org"]
    if pos not in p:
        raise Misaligned("the bridge token is not in the asked pick sentence")
    if any(ids["org"][q] != ids["alt"][q] for q in p if q != pos):
        raise Misaligned("the asked pick sentence differs in O and S beyond the bridge token")
    person = sentences["org"].split(" picked ", 1)[0]
    assert person == sentences["alt"].split(" picked ", 1)[0], "the asked pick sentence's person differs in O and S"
    who = SP.tokens_in(offsets["org"], start["org"], start["org"] + len(person))
    if not who or not set(who) <= set(p) or pos in who:
        raise Misaligned("the person's tokens are not apart from the bridge inside the pick sentence")
    return p, who


def item_record(tok, c: dict, src_item: dict[str, dict], design: str) -> dict:
    """One kept item (the arms' positions, both readers' prompts, the marks for the view) from a rebuilt X0 case and
    the readers' source items; raises Misaligned for an item the arms cannot use."""
    from bridge_jspace.tokens import raw_encoding

    pos, lk = c["pos"], X.LOOKUP
    contexts = {"org": c["context"], "alt": c["cf_context"]}
    texts: dict[tuple[str, str], str] = {}
    offsets: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for w in X.READERS:
        rd = c["readers"][w]
        for v, ctx in contexts.items():
            text = X.render(tok, src_item[w], RENDERING, ctx)
            enc = raw_encoding(tok, text, offsets=True)
            assert enc["input_ids"] == rd["ids"][v], f"{c['scene']} {w} {v}: the rendered prompt's ids differ"
            texts[(w, v)], offsets[(w, v)] = text, enc["offset_mapping"]
    ids = c["readers"][lk]["ids"]
    diff = changed_positions(ids["org"], ids["alt"])
    other = expected_changes(design, diff, pos)
    item = {**src_item[lk], "cf_bridge": c["cf_bridge"]}
    sentences = {"org": pick_sentence(item, c["context"], c["bridge"]),
                 "alt": pick_sentence(item, c["cf_context"], c["cf_bridge"])}  # fmt: skip
    pick, person = pick_positions({v: texts[(lk, v)] for v in contexts}, {v: offsets[(lk, v)] for v in contexts}, ids,
                                  sentences, contexts, pos)  # fmt: skip
    if other is not None and other in pick:
        raise Misaligned("the other changed token is inside the asked pick sentence")
    last = max(pick)
    for w in X.READERS:
        rd_ids = c["readers"][w]["ids"]
        if expected_changes(design, changed_positions(rd_ids["org"], rd_ids["alt"]), pos) != other:
            raise Misaligned("O and S change at other positions in the recall's prompt")
        if any(rd_ids[v][: last + 1] != ids[v][: last + 1] for v in contexts):
            raise Misaligned("the readers' prompts differ before the last patched token")
    upstream = min(diff) < pos
    assert upstream == bool(c["upstream"]), (
        f"{c['scene']}: upstream {c['upstream']} but the first change is at {min(diff)}"
    )
    o_off = offsets[(lk, "org")]
    marks = {"bridge": [list(o_off[pos])], "pick": [list(s) for s in B.merged_spans(o_off, [q for q in pick if q != pos])],
             "other": [list(o_off[other])] if other is not None else []}  # fmt: skip
    end = max(b for spans in marks.values() for _, b in spans)
    assert texts[(X.RECALL, "org")][:end] == texts[(lk, "org")][:end], f"{c['scene']}: the readers' texts differ"
    return {
        "scene": c["scene"], "design": design, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
        "upstream": upstream, "prefix_same": not upstream, "group": GROUP_OF[_group(c)], "features": ST.features(c),
        "pos": pos, "pick": pick, "person": person, "other": other, "sentences": sentences, "space": c["space"],
        "read_suffix": tok.decode(c["space"]), "context": c["context"], "cf_context": c["cf_context"], "marks": marks,
        "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b",
                                                         "ids")}, "text": {"org": texts[(w, "org")]}} for w in X.READERS},
        **({"fresh": c["fresh"]} if design == "clean" else {}),
    }  # fmt: skip


def _group(c: dict) -> str:
    from scripts import x45m

    return x45m.group_of(c)


def stored_whole(src: Path, layer: int) -> tuple[list[str], dict[str, dict[str, int]]]:
    """The source run's items at the layer (its chat outcomes' scenes, in order) and their stored whole-arm switch per
    reader (the check for arm a)."""
    scenes: dict[str, None] = {}
    whole: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] == RENDERING and r["layer"] == layer and r["arm"] == "whole":
            if r["reader"] == X.LOOKUP:
                scenes.setdefault(r["scene"])
            whole[r["scene"]][r["reader"]] = int(r["switched"])
    return list(scenes), {s: whole[s] for s in scenes}


def select(tok, design: str, run: str, layer: int) -> tuple[list[dict], dict]:
    """The design's items in the source run's scene order and the counts: the run's items at L, drops by reason, the
    groups, upstream / prefix-identical items, pick-sentence lengths, entities."""
    from scripts import tasks_v2 as T

    alt = ALT[design]
    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt", "cf") == alt, f"{run}: alt {m.get('alt', 'cf')!r}, not the {design} design's {alt!r}"
    assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    if alt == "fresh":
        assert m["fresh"]["seed"] == X.FRESH_SEED, f"{run}: fresh seed {m['fresh']['seed']}, not {X.FRESH_SEED}"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
    scenes, whole = stored_whole(src, layer)
    assert scenes, f"{run}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    with B.x0_alt(alt, (RENDERING,)):
        cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == RENDERING}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, dropped = [], collections.Counter()
    for scene in scenes:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        if alt == "fresh":
            assert c["fresh"] == old[scene]["fresh"], f"{scene}: the added locker sentence changed since {run}"
        try:
            rec = item_record(tok, c, {w: by_id[c["readers"][w]["id"]] for w in X.READERS}, design)
        except Misaligned as e:
            dropped[str(e)] += 1
            continue
        out.append({**rec, "stored": {"whole": whole[scene]}})
    counts = {"design": design, "source": run, "alt": alt, "layer": layer, "items_at_L": len(scenes),
              "dropped": dict(dropped), "items": len(out), "entities": len({it["entity"] for it in out}),
              "groups": dict(collections.Counter(it["group"] for it in out)),
              "upstream": dict(collections.Counter(str(it["upstream"]) for it in out)),
              "locker-first, prefix-identical": sum(it["group"] == "locker-first" and it["prefix_same"] for it in out),
              "pick_tokens": dict(collections.Counter(len(it["pick"]) for it in out))}  # fmt: skip
    return out, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    """The view's items: k random indices of n (seed 0), as X0 picks its examples."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def item_marked(it: dict, reader: str) -> str:
    """The reader's O prompt as the model reads it (the digit's space token appended): ⟦bridge:…⟧ the bridge token
    (arms a, b, c, b_blocks; d too), ⟦pick:…⟧ the pick sentence's other tokens (arm d), ⟦other:…⟧ the other changed
    pick token (main test; S changes it too, no arm patches it)."""
    from scripts import x45p

    spans = [(a, b, role) for role in ("bridge", "pick", "other") for a, b in it["marks"][role]]
    return x45p.marked(it["readers"][reader]["text"]["org"] + it["read_suffix"], spans)


def stage_plan() -> dict:
    """Tokenizer only: per design, the target's items, drops, groups and one example (seed 0) with the patches marked."""
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    out: dict[str, Any] = {"target": pins.TARGET, "layer": layer, "n_layers": pins.N_LAYERS, "arms": list(ARMS)}
    for design in DESIGNS:
        items, counts = select(tok, design, SOURCES[design][pins.TARGET], layer)
        counts["reads"] = len(items) * len(X.READERS) * len(ARMS)
        if items:
            it = items[example_indices(len(items), 1)[0]]
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            counts["example"] = {"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}",
                                 "group": it["group"], "upstream": it["upstream"],
                                 "pick_tokens": [tok.decode([ids[p]]) for p in it["pick"]],
                                 "person_tokens": [tok.decode([ids[p]]) for p in it["person"]],
                                 "other_token": None if it["other"] is None else [tok.decode([ids[it["other"]]]),
                                                                                  tok.decode([it["readers"][X.LOOKUP]["ids"]["alt"][it["other"]]])],
                                 "lookup_O_marked": item_marked(it, X.LOOKUP)}  # fmt: skip
        out[design] = counts
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# ---- GPU ----------------------------------------------------------------------------------------------------------


def prompts_of(ids: dict[str, list[int]], pos: int) -> dict[str, list[int]]:
    """A reader's prompts by arm prompt: O, O with S's token at the bridge ('swap'), S."""
    o, s = ids["org"], ids["alt"]
    assert len(o) == len(s), "O and S differ in length"
    swap = list(o)
    swap[pos] = s[pos]
    return {"org": list(o), "swap": swap, "alt": list(s)}


def arm_edits(add_rows, set_rows, h_o: dict, h_s: dict, pos: int, pick: list[int], layer: int,
              n_layers: int) -> dict[str, tuple[str, dict]]:  # fmt: skip
    """Each arm's (prompt, edit set) in ARMS order: the prompt is 'org', 'swap' or 'alt' (prompts_of); an edit set is
    {layer: edit} acting on that block's output. h_o / h_s: block outputs [seq, d] of O (layer L at least) and S (every
    layer), unedited."""

    def bridge(layers) -> dict:
        return {la: set_rows(h_s[la][[pos]], [pos]) for la in layers}

    upto, every = range(layer + 1), range(n_layers)
    out = {"none": ("org", {}),
           "a": ("org", {layer: add_rows((h_s[layer][pos] - h_o[layer][pos])[None], [pos])}),
           "b": ("swap", bridge(upto)), "c": ("swap", bridge(every)),
           "d": ("swap", {la: set_rows(h_s[la][list(pick)], list(pick)) for la in every}),
           "b_blocks": ("org", bridge(upto)), "S": ("alt", {})}  # fmt: skip
    assert tuple(out) == ARMS
    return out


def read_rows(model, prompts: list[list[int]], edits: list[dict]) -> Any:
    """X0's chat read of several prompts of one length (each with the digit's space token already appended), one edit
    set each: the first step's logits [rows, vocab], batched as X0 batches (BJ_SUITE_BATCH)."""
    import torch

    from scripts import suite_split as P

    assert len({len(p) for p in prompts}) == 1, "the prompts differ in length"
    return torch.cat([model.generate_batch(torch.tensor(prompts[s : s + P.BATCH], device=model.device), 1,
                                           edits[s : s + P.BATCH], first_logits=True)[1]
                      for s in range(0, len(edits), P.BATCH)])  # fmt: skip


def state_gap(model, ids_o: list[int], edits: dict, h_s: dict, pos: int, layers: list[int]) -> list[float]:
    """Under `edits` on O, the bridge token's relative distance to S's state at each of `layers`."""
    import torch

    _, st = model.run(torch.tensor([ids_o], device=model.device), edits=edits, record=tuple(layers))
    return [float((st[la][pos] - h_s[la][pos]).norm() / h_s[la][pos].norm().clamp_min(1e-30)) for la in layers]


def assert_item(it: dict) -> None:
    """The dumbest ways, checked again on every kept item before its forwards."""
    pos, pick = it["pos"], it["pick"]
    for w in X.READERS:
        ids = it["readers"][w]["ids"]
        diff = changed_positions(ids["org"], ids["alt"])
        assert expected_changes(it["design"], diff, pos) == it["other"], f"{it['scene']}: O and S changed elsewhere"
        assert all(ids["org"][q] == ids["alt"][q] for q in pick if q != pos), f"{it['scene']}: pick sentence differs"
        assert all(ids["org"][q] == ids["alt"][q] for q in it["person"]), f"{it['scene']}: the person token differs"
        lk = it["readers"][X.LOOKUP]["ids"]
        assert all(ids[v][: max(pick) + 1] == lk[v][: max(pick) + 1] for v in ("org", "alt")), (
            f"{it['scene']}: the readers differ before the last patched token"
        )


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import suite_split as SUITE
    from scripts.exp04_brew_parts import AddRows, SetRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.4 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert all(target in SOURCES[d] for d in DESIGNS), f"47.4 runs on {sorted(B.FRESH_RUN)}, not {target}"
    layer, n_layers = X.PREDICTED[target], pins.N_LAYERS
    runs = {d: SOURCES[d][target] for d in DESIGNS}
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    srcs = [X.RESULTS / r for r in runs.values()]
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": "47.4",
         "spec": "jobs/c3/batch47.yaml (47.4)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(s / f for s in srcs for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl")))},
         "sources": runs, "layer": layer, "n_layers": n_layers, "arms": ARM_TEXT,
         "prompts": {"org": "O", "swap": "O with S's token at the bridge (its input embedding swapped)", "alt": "S"},
         "states": "set (SetRows), from one unedited forward of S (every layer) and O (layer L) on the lookup's prompts",
         "items_rule": "each source run's scenes at L (chat), the items its unedited run made eligible; O and S the "
                       "same length, changed only at the bridge (clean) or the bridge and one other pick token (main); "
                       "the asked pick sentence at the same positions with the same ids but the bridge's; the readers' "
                       "prompts equal through the last patched token; else dropped and counted (plan.json)",
         "groups": "x45m.group_of: locker-first (both locker sentences before the asked pick), locker-after, mixed",
         "terms": TERM_TEXT, "bug_check": {"read": BUG_TOL, "state": STATE_TOL},
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = top token is S's answer",
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "fresh_draws": X.FRESH_SEED},
         "n_boot": X.N_BOOT, "order": {"items": "per design (main, clean), the source run's scene order",
                                       "reads": "per item and reader: the arms in ARMS order, one batch (BJ_SUITE_BATCH)",
                                       "batch": SUITE.BATCH},
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
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
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    examples = {d: set(example_indices(sum(it["design"] == d for it in items))) for d in DESIGNS}
    after = list(range(layer + 1, n_layers))
    rows, checks, greedy = [], [], []
    with torch.no_grad():
        for design in DESIGNS:
            mine = [it for it in items if it["design"] == design]
            for i, it in enumerate(progress(mine, f"47.4 {design} at L{layer} (item)")):
                assert_item(it)
                ids = it["readers"][X.LOOKUP]["ids"]
                h_o = model.run(torch.tensor([ids["org"]], device=model.device), record=(layer,))[1]
                h_s = model.run(torch.tensor([ids["alt"]], device=model.device), record=tuple(range(n_layers)))[1]
                arms = arm_edits(AddRows, SetRows, h_o, h_s, it["pos"], it["pick"], layer, n_layers)
                gap = state_gap(model, ids["org"], arms["b_blocks"][1], h_s, it["pos"], after)
                worst = max(range(len(gap)), key=gap.__getitem__)
                checks.append({"scene": it["scene"], "design": design, "group": it["group"], "upstream": it["upstream"],
                               "prefix_same": it["prefix_same"], "gap_max": gap[worst], "gap_layer": after[worst],
                               "gap": [round(g, 6) for g in gap]})  # fmt: skip
                for w, rd in it["readers"].items():
                    prompts = prompts_of(rd["ids"], it["pos"])
                    logits = read_rows(
                        model, [prompts[arms[a][0]] + it["space"] for a in ARMS], [arms[a][1] for a in ARMS]
                    )
                    base = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "design": design,
                            "group": it["group"], "upstream": it["upstream"], "prefix_same": it["prefix_same"],
                            "reader": w}  # fmt: skip
                    for arm, lg in zip(ARMS, logits, strict=True):
                        rows.append({**base, "arm": arm, "prompt": arms[arm][0], **X.read_row(lg, rd, digits),
                                     "top_text": tok.decode([int(lg.argmax())])})  # fmt: skip
                    if i in examples[design]:
                        gen = torch.tensor([prompts[arms[a][0]] for a in ARMS], device=model.device)
                        texts = model.generate_batch(gen, X.GEN_TOKENS, [arms[a][1] for a in ARMS])
                        greedy += [{"scene": it["scene"], "design": design, "reader": w, "arm": a, "greedy": t}
                                   for a, t in zip(ARMS, texts, strict=True)]  # fmt: skip
                del h_o, h_s, arms
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "checks.jsonl", checks)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    bad = state_flags(checks)
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    print(state_line(checks), flush=True)
    if bad:
        raise SystemExit(f"BUG (47.4, stop and report): under (b) on O's tokens the bridge token's state after L is not "
                         f"S's on {len(bad)} items whose O and S agree before the bridge, e.g. {bad[:3]}")  # fmt: skip
    return out


def state_flags(checks: list[dict]) -> list[str]:
    """The prefix-identical items whose bridge state after L under b_blocks is farther than STATE_TOL from S's."""
    return [f"{c['design']}/{c['scene']}" for c in checks if c["prefix_same"] and c["gap_max"] > STATE_TOL]


def state_line(checks: list[dict]) -> str:
    """The state check in one line (no switch is read: printed by the sealed run)."""
    same = [c["gap_max"] for c in checks if c["prefix_same"]]
    up = [c["gap_max"] for c in checks if not c["prefix_same"]]
    bad = state_flags(checks)
    return (f"state check (b_blocks: the bridge token after L vs S's; relative distance): items with O and S equal "
            f"before the bridge: n = {len(same)}, max {max(same, default=0):.2e}, flagged {len(bad)} (> {STATE_TOL}); "
            f"items whose other change comes first: n = {len(up)}, median {statistics.median(up) if up else 0:.2e} "
            f"(not expected to be 0)" + ("  <<< BUG FLAG >>>" if bad else ""))  # fmt: skip


# ---- verdict, view, figures (CPU, sealed) --------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.4 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def item_table(rows: list[dict], reader: str) -> tuple[list[str], list[str], dict[str, list[int]]]:
    """One reader's items (in row order), their bridge entities, and each arm's 0/1 switch per item; every item must
    have every arm."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["switched"])
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in ARMS if (s, a) not in by]
    assert not missing, f"{reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    return scenes, [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in ARMS}


def decomposition(switched: dict[str, list[int]], entities: list[str], n_boot: int = X.N_BOOT,
                  seed: int = X.BOOT_SEED) -> dict[str, Any]:  # fmt: skip
    """Each arm's switch rate and the terms (TERMS; 'outside' = 1 - S_d) over the items, with 95% percentile CIs from
    X0's cluster bootstrap over the bridge entities (the same draws for every arm: paired); the non-switch 1 - S_a,
    each term's share of it, and the largest of Q47.4's three terms (point estimates). Points from counts."""
    n = len(entities)
    hits = {a: int(sum(switched[a])) for a in ARMS}
    rate = {a: hits[a] / n for a in ARMS}
    boot = X.resampled_rates(switched, entities, n_boot, seed)
    terms = {}
    for t, (lo, hi) in TERMS.items():
        terms[t] = [(rate[hi] if hi else 1.0) - rate[lo], *X.interval((boot[hi] if hi else 1.0) - boot[lo])]
    non = [1.0 - rate["a"], *X.interval(1.0 - boot["a"])]
    share = {t: (terms[t][0] / non[0]) if non[0] > 0 else math.nan for t in TERMS}
    return {"n": n, "entities": len(set(entities)), "hits": hits,
            "rate": {a: [rate[a], *X.interval(boot[a])] for a in ARMS}, "terms": terms, "non_switch": non,
            "share_of_non_switch": share, "largest": max(CANDIDATES, key=lambda t: terms[t][0])}  # fmt: skip


def disagreements(switched: dict[str, list[int]], a: str, b: str) -> int:
    return sum(x != y for x, y in zip(switched[a], switched[b], strict=True))


def bug_checks(rows: list[dict], checks: list[dict]) -> dict[str, Any]:
    """The bug checks per design and reader: (b) vs (c) on the prefix-identical items (flagged above BUG_TOL); in the
    clean design (b), (c), (d) vs S read on S (flagged above BUG_TOL); the run's state check (flagged above STATE_TOL);
    and, reported, (b) vs (c) on main items whose other change comes first."""
    out: dict[str, Any] = {"read": {}, "state": {}, "flags": []}
    for design in DESIGNS:
        for w in X.READERS:
            key = f"{design} {READER_NAME[w]}"
            same = [r for r in rows if r["design"] == design and r["prefix_same"]]
            up = [r for r in rows if r["design"] == design and not r["prefix_same"]]
            cell: dict[str, Any] = {}
            if same:
                _, _, sw = item_table(same, w)
                n = len(sw["b"])
                k = disagreements(sw, "b", "c")
                cell["prefix_same"] = {"n": n, "b_vs_c_disagree": k, "S_b": sum(sw["b"]) / n, "S_c": sum(sw["c"]) / n}
                if k > BUG_TOL * n:
                    out["flags"].append(f"{key}: (b) and (c) disagree on {k} of {n} items whose O and S agree before "
                                        f"the bridge (> {BUG_TOL:.0%})")  # fmt: skip
                if design == "clean":
                    vs_s = {a: disagreements(sw, a, "S") for a in ("b", "c", "d")}
                    cell["clean_vs_S"] = vs_s
                    for a, k2 in vs_s.items():
                        if k2 > BUG_TOL * n:
                            out["flags"].append(f"{key}: ({a}) is S's own run in the clean design but disagrees with S "
                                                f"read on S on {k2} of {n} items (> {BUG_TOL:.0%})")  # fmt: skip
            if up:
                _, _, sw = item_table(up, w)
                n = len(sw["b"])
                cell["other_change_first"] = {"n": n, "b_vs_c_disagree": disagreements(sw, "b", "c"),
                                              "S_b": sum(sw["b"]) / n, "S_c": sum(sw["c"]) / n}  # fmt: skip
            out["read"][key] = cell
        mine = [c for c in checks if c["design"] == design]
        same = [c["gap_max"] for c in mine if c["prefix_same"]]
        out["state"][design] = {"n_prefix_same": len(same), "max": max(same, default=None),
                                "flagged": state_flags(mine),
                                "n_other_change_first": sum(not c["prefix_same"] for c in mine),
                                "median_other_change_first": statistics.median([c["gap_max"] for c in mine if not c["prefix_same"]])
                                if any(not c["prefix_same"] for c in mine) else None}  # fmt: skip
        if out["state"][design]["flagged"]:
            out["flags"].append(f"{design}: the bridge token's state after L under (b) is not S's on "
                                f"{len(out['state'][design]['flagged'])} prefix-identical items (> {STATE_TOL})")  # fmt: skip
    return out


def side_checks(rows: list[dict], cases: list[dict]) -> dict[str, Any]:
    """Descriptive: arm a against the source run's stored whole arm; O unedited reads O's answer; S read on S reads S's
    answer (per design and reader)."""
    stored = {(c["design"], c["scene"]): c["stored"]["whole"] for c in cases}
    out = {}
    for design in DESIGNS:
        for w in X.READERS:
            mine = [r for r in rows if r["design"] == design and r["reader"] == w]
            a = [(r["switched"], stored[(design, r["scene"])].get(w)) for r in mine if r["arm"] == "a"]
            none = [r for r in mine if r["arm"] == "none"]
            s = [r for r in mine if r["arm"] == "S"]
            out[f"{design} {READER_NAME[w]}"] = {
                "a_vs_stored_whole": {"n": len(a), "agree": sum(x == y for x, y in a), "rerun": sum(x for x, _ in a),
                                      "stored": sum(y or 0 for _, y in a)},
                "none_reads_O": sum(r["role"] == "A" for r in none), "S_reads_S": sum(r["switched"] for r in s),
                "n": len(none)}  # fmt: skip
    return out


def groups_of(design: str) -> tuple[str, ...]:
    """The design's order groups; the main test's locker-first scenes also split by where the other changed pick sits
    (descriptive: (b)->(c) and (c)->(d) are 0 by construction where it comes after the asked pick)."""
    return GROUPS + (SPLIT if design == "main" else ())


def in_group(r: dict, g: str) -> bool:
    if g == "all":
        return True
    if g in SPLIT:
        return r["group"] == "locker-first" and r["upstream"] == (g == SPLIT[0])
    return r["group"] == g


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending (not here), or per design, reader and group the decomposition, and the checks."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.4 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "the run has no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = X.read_jsonl(src / "cases.jsonl")
    checks = X.read_jsonl(src / "checks.jsonl")
    cells: dict[str, dict[str, dict[str, Any]]] = {d: {READER_NAME[w]: {} for w in X.READERS} for d in DESIGNS}
    for design in DESIGNS:
        for w in X.READERS:
            for g in groups_of(design):
                mine = [r for r in rows if r["design"] == design and r["reader"] == w and in_group(r, g)]
                if not mine:
                    cells[design][READER_NAME[w]][g] = {"n": 0}
                    continue
                _, entities, sw = item_table(mine, w)
                cells[design][READER_NAME[w]][g] = decomposition(sw, entities, n_boot)
    plan = json.loads((src / "plan.json").read_text())
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "n_layers": m["n_layers"],
            "sources": m["sources"], "status": "tested", "cells": cells, "bugs": bug_checks(rows, checks),
            "checks": side_checks(rows, cases), "plan": plan}  # fmt: skip


def fmt(v: list) -> str:
    return "-" if v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−"))  # fmt: skip


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"}
               for t in RUNS if t not in targets]  # fmt: skip
    tested = [m for m in models if m["status"] == "tested"]
    flags = [f"{m['target']}: {f}" for m in tested for f in m["bugs"]["flags"]]
    out = RESULTS / f"x47_4-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.4: why does not every answer switch? Cumulative patches at the bridge token", "",
             f"Batch 47, test 47.4 (jobs/c3/batch47.yaml; {QUESTION}, Dan: {answer}). Arms on O, read by X0's chat read "
             "(switch = the top token is S's answer). Terms are shares of all the group's items: before L = S_b − S_a; "
             "(b)->(c) = S_c − S_b; other pick tokens = S_d − S_c; outside the pick sentence = 1 − S_d; they sum to the "
             f"non-switch 1 − S_a. Cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). Descriptive, no "
             "bar. UNVERIFIED.", ""]  # fmt: skip
    if flags:
        lines += ["## <<< BUG FLAG: STOP AND REPORT >>>", "",
                  "(b)->(c) must be ~0 where O and S agree before the bridge (Dan: a non-zero difference is a bug). The "
                  "decomposition below is not to be read until this is explained:", "",
                  *[f"- **{f}**" for f in flags], ""]  # fmt: skip
    else:
        lines += ["Bug checks: none flagged ((b) and (c) agree on the prefix-identical items; the clean design's (b), "
                  "(c), (d) read as S does; the bridge token's states after L under (b) are S's).", ""]  # fmt: skip
    lines += ["## Q47.4: the largest term of the lookup's non-switch in locker-first scenes", "",
              "| model | design | n | S_a | non-switch | before L | other pick tokens | outside the pick sentence | (b)->(c) "
              "| largest |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | | pending ({m['why']}) | | | | | | | |")
            continue
        for design in DESIGNS:
            c = m["cells"][design]["lookup"]["locker-first"]
            if not c["n"]:
                lines.append(f"| {m['target']} | {design} | 0 | | | | | | | |")
                continue
            t = c["terms"]
            lines.append(f"| {m['target']} | {design} | {c['n']} | {fmt(c['rate']['a'])} | {fmt(c['non_switch'])} | "
                         f"{fmt(t['before_L'])} | {fmt(t['pick_other'])} | {fmt(t['outside'])} | "
                         f"{fmt(t['propagation'])} | {c['largest']} |")  # fmt: skip
    lines += ["", "In the clean design only the bridge token changes, so (b), (c) and (d) are S's own run by construction "
              "and the non-switch is (a)->(b) alone; the other terms are informative in the main test, where the other "
              "person's pick also changes (outside the asked pick sentence). In main items where that pick comes after "
              "the asked one, (b), (c) and (d) coincide by construction too; the main test's locker-first rows are "
              "split by it below (descriptive).", "", "## Decomposition", "",
              "| model | design | reader | group | n | S_none | S_a | S_b | S_c | S_d | S_b_blocks | S read on S | before L "
              "| (b)->(c) | other pick tokens | outside |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for design in DESIGNS:
            for w in ("lookup", "recall"):
                for g in groups_of(design):
                    c = m["cells"][design][w][g]
                    if not c["n"]:
                        lines.append(f"| {m['target']} | {design} | {w} | {g} | 0 | | | | | | | | | | | |")
                        continue
                    r, t = c["rate"], c["terms"]
                    lines.append(f"| {m['target']} | {design} | {w} | {g} | {c['n']} | {r['none'][0]:.2f} | "
                                 + " | ".join(fmt(r[a]) for a in ("a", "b", "c", "d", "b_blocks"))
                                 + f" | {r['S'][0]:.2f} | " + " | ".join(fmt(t[k]) for k in TERMS) + " |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "", "## Checks", ""]
    for m in tested:
        for key, cell in m["bugs"]["read"].items():
            parts = []
            if "prefix_same" in cell:
                p = cell["prefix_same"]
                parts.append(f"O and S equal before the bridge: (b) vs (c) disagree on {p['b_vs_c_disagree']} of {p['n']} "
                             f"(S_b {p['S_b']:.3f}, S_c {p['S_c']:.3f})")  # fmt: skip
            if "clean_vs_S" in cell:
                parts.append(
                    "vs S read on S, disagreements: " + ", ".join(f"({a}) {k}" for a, k in cell["clean_vs_S"].items())
                )
            if "other_change_first" in cell:
                p = cell["other_change_first"]
                parts.append(f"other change first (not expected to be 0): (b) vs (c) disagree on {p['b_vs_c_disagree']} "
                             f"of {p['n']} (S_b {p['S_b']:.3f}, S_c {p['S_c']:.3f})")  # fmt: skip
            lines.append(f"- {m['target']}, {key}: " + "; ".join(parts))
        for design, s in m["bugs"]["state"].items():
            lines.append(f"- {m['target']}, {design}, states: the bridge token after L under (b) on O's tokens vs S's, "
                         f"max relative distance {s['max']} over {s['n_prefix_same']} prefix-identical items, flagged "
                         f"{len(s['flagged'])}; other change first: n = {s['n_other_change_first']}, median "
                         f"{s['median_other_change_first']}")  # fmt: skip
        for key, s in m["checks"].items():
            a = s["a_vs_stored_whole"]
            lines.append(f"- {m['target']}, {key}: (a) vs the source run's whole arm: {a['agree']} of {a['n']} agree "
                         f"(rerun {a['rerun']}, stored {a['stored']}); O unedited reads O's answer on {s['none_reads_O']} "
                         f"of {s['n']}; S read on S reads S's on {s['S_reads_S']} of {s['n']}")  # fmt: skip
        for design, p in m["plan"].items():
            lines.append(f"- {m['target']}, {design} items: {p['items']} of {p['items_at_L']} at L from {p['source']} "
                         f"(dropped {p['dropped'] or 'none'}; groups {p['groups']}; other change first "
                         f"{p['upstream'].get('True', 0)}; {p['entities']} bridge items)")  # fmt: skip
    (out / "x47_4.json").write_text(json.dumps({"runs": runs, "dan": answer, "flags": flags, "models": models}, indent=1)
                                    + "\n")  # fmt: skip
    (out / "x47_4.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """Per design, k random items of the run (seed 0): each reader's O prompt as the model reads it with the patched
    positions marked, and each arm's answer (the top token read, and the greedy text)."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    cases = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["design"], r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["design"], g["scene"], g["reader"], g["arm"]): g["greedy"]
              for g in X.read_jsonl(src / "examples_greedy.jsonl")}  # fmt: skip
    lines = [f"## {run} ({m['model']['target']}, L{m['layer']} of {m['n_layers']} layers)", ""]
    for design in DESIGNS:
        items = [c for c in cases if c["design"] == design]
        lines += [f"### {design}: {min(k, len(items))} random items of {len(items)} (seed {seed}; from "
                  f"{m['sources'][design]})", ""]  # fmt: skip
        for i in example_indices(len(items), k, seed):
            it = items[i]
            lines += [f"#### {it['scene']} ({it['domain']}, {it['group']}, other change first: {it['upstream']}): "
                      f"bridge {it['entity']} → {it['cf_bridge']}; {len(it['pick'])} pick-sentence tokens", ""]  # fmt: skip
            for w, rd in it["readers"].items():
                lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}",
                          "", "```", item_marked(it, w), "```", "",
                          "| arm | what | prompt | top token | role | switched | greedy |", "|---|---|---|---|---|---|---|"]  # fmt: skip
                for arm in ARMS:
                    r = reads[(design, it["scene"], w, arm)]
                    lines.append(f"| {arm} | {ARM_TEXT[arm]} | {r['prompt']} | {r['top_text']!r} | {r['role']} | "
                                 f"{r['switched']} | {greedy.get((design, it['scene'], w, arm))!r} |")  # fmt: skip
                lines.append("")
    return lines


def stage_view(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> Path:
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.4 verify-pack view: prompts exactly as the model reads them (the read appends the digit's space token)",
             "", "⟦bridge:…⟧ the bridge token (arms a, b, c, b_blocks; d), ⟦pick:…⟧ the asked pick sentence's other "
             "tokens (arm d), ⟦other:…⟧ the other changed pick token (main test: S changes it too; no arm patches it). "
             "Prompt: org = O, swap = O with S's token at the bridge, alt = S. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        if (RESULTS / run / "outcomes.jsonl").exists():
            lines += view_lines(run, k, seed)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out / "view.md")
    return out


def stage_figures(verdict_dir: Path) -> Path:
    """The stacked figure: per design and model, the lookup's and the recall's items split into switched at (a), before
    L, (b)->(c), other pick tokens and outside the pick sentence, per order group; negative terms drawn at zero and
    printed."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    unsealed()
    blob = json.loads((verdict_dir / "x47_4.json").read_text())
    tested = [m for m in blob["models"] if m["status"] == "tested"]
    folder = verdict_dir / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-figures"
    folder.mkdir()
    parts = [("switched at (a)", F.LOOKUP), ("before L", "#b294c7"), ("(b)->(c)", "#d62728"),
             ("other pick tokens", F.CONTROL), ("outside the pick sentence", F.CHANCE)]  # fmt: skip
    fig, axes = plt.subplots(1, len(DESIGNS), figsize=(14, 6), sharex=True)
    for ax, design in zip(axes, DESIGNS, strict=True):
        labels, y = [], 0
        for m in tested:
            for w in ("lookup", "recall"):
                for g in ("locker-first", "locker-after"):
                    c = m["cells"][design][w][g]
                    if not c["n"]:
                        continue
                    vals = [c["rate"]["a"][0], *(c["terms"][t][0] for t in TERMS)]
                    left = 0.0
                    for (name, color), v in zip(parts, vals, strict=True):
                        ax.barh(y, max(v, 0.0), left=left, color=color, label=name if y == 0 else None)
                        if v < 0:
                            ax.text(left, y, f" {v:+.2f}", va="center", fontsize=7, color="#d62728")
                        left += max(v, 0.0)
                    labels.append(f"{m['target']} {w} {g} (n={c['n']})")
                    y += 1
        ax.set_yticks(range(len(labels)), labels, fontsize=8)
        ax.invert_yaxis()
        ax.set(xlim=(0, 1.05), xlabel="share of items", title=f"{design} design")
    axes[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(1.0, -0.1), ncol=len(parts), frameon=False)
    fig.suptitle("47.4: where the non-switch sits (cumulative patches at the bridge token; UNVERIFIED)", fontsize=11)
    fig.tight_layout()
    path = folder / "x47_4_stacked.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(path)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view", "figures"])
    ap.add_argument("--name", help="run: the run name (results/x47_cumulative/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.4 (jobs/c3/batch47.yaml; Q47.4, sealed)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the 47.4 runs")
    ap.add_argument("--verdict", type=Path, help="figures: the verdict folder (results/x47_cumulative/x47_4-<UTC>)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    elif a.stage == "view":
        stage_view(a.runs)
    else:
        assert a.verdict, "figures needs --verdict"
        stage_figures(a.verdict)


if __name__ == "__main__":
    main()
