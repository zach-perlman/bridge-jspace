"""x45b_binding (batch 45, test 45b; jobs/c3/batch45.yaml, design and rule fixed in advance): where is the binding made
when the locker comes after the pick?

Items: the main test's items (X0: two people swap their picks; chat rendering; the scenes of the run's outcomes at L, its
eligible items) whose original bridge's locker sentence comes after the asked pick (x0_strata's "org locker vs asked
pick" = after). The cases are rebuilt with X.build_cases on the run's set (chat) and must equal the run's cases.jsonl
(ids and bridge position). 9B: L = 12 (qwen35_9b_x0_necessity); 27B: L = 32 (x0_necessity_27b_chat).

O = the original prompt, S = the swapped one (X0's alt). Arms, one forward of O each with one edit at one layer, read at
O's answer position as X0 reads (chat: the prompt with a digit's space token appended; the top token over the vocabulary):
  a          h_S - h_O added at the bridge word at L (X0's whole arm, rerun on these items)
  b_half     the same at L // 2
  b_quarter  the same at L // 4
  c          S patched into O at every token of the locker sentences at L (h_S - h_O added at each: O's state there
             becomes S's)
  d          the same as c at L // 2
  none       O unedited (sanity: reads O's answer)
and S read on S, unedited ("S switches"). Switch = the top token is S's answer's first token (X0). The lookup decides;
the recall is read on the identical patches (descriptive). The locker sentences: every "The locker of <thing> is <n>."
sentence of the context (a sentence before the first change has h_S = h_O there, a no-op). They must align token for
token between O and S (the same positions, the same ids); otherwise by sentence (the k-th locker sentence of each, the
same token count, positions paired in order); an item where that fails is dropped and counted.

Rule (stage verdict; batch 45, point estimates on the lookup): the reading-order explanation holds if (c) or (d) switches
at least half of the lookups that S itself switches (among the items S switches, the share c, or d, switches >= 0.5),
while (a) stays at or below 0.25 (a's switch rate over all items). Rates with cluster-bootstrap CIs over bridge items
(10,000 resamples, seed 0) and the n. Results stay closed until docs/predictions_batch45.md holds Dan's Q45.5 commit.

uv run python scripts/x45b_binding.py plan                                                    # tokenizer only
BJ_TARGET=qwen3.5-9b uv run python scripts/x45b_binding.py run --name qwen35_9b_x45b_binding  # GPU
uv run python scripts/x45b_binding.py run --name x45b_binding_27b                             # GPU (the 27B)
uv run python scripts/x45b_binding.py examples --name x45b_binding_27b                        # CPU, after run
uv run python scripts/x45b_binding.py verdict --name x45b_binding_27b                         # CPU, after Dan's commit
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x45b_binding"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch45.yaml"
MAIN_RUN = {
    "qwen3.5-9b": "qwen35_9b_x0_necessity",
    "qwen3.6-27b": "x0_necessity_27b_chat",
    "muse-glimmer-30b": "muse30b_x0_necessity",
}  # Muse: Dan ~22:35, 45b on Muse after the sweep
RENDERING = "chat"
LOCKER_PREFIX = "The locker of "
BRIDGE_ARMS = ("a", "b_half", "b_quarter")
LOCKER_ARMS = ("c", "d")
O_ARMS = ("none", *BRIDGE_ARMS, *LOCKER_ARMS)  # read on O
S_ARM = "S"  # S read on S
ARMS = (*O_ARMS, S_ARM)
HALF, A_MAX = 0.5, 0.25
RULE = (
    "the reading-order explanation holds if (c) or (d) switches at least half of the lookups that S itself switches, "
    "while (a) stays at or below 0.25."
)
MARK_OPEN, MARK_CLOSE = "⟦", "⟧"
ARM_TEXT = {
    "none": "O unedited",
    "a": "the bridge-word change at L",
    "b_half": "the bridge-word change at L/2",
    "b_quarter": "the bridge-word change at L/4",
    "c": "S patched into O at every locker-sentence token, at L",
    "d": "S patched into O at every locker-sentence token, at L/2",
    "S": "S read on S (unedited)",
}


def arm_layers(layer: int) -> dict[str, int]:
    """Each edited arm's layer: a and c at L, b_half and d at L // 2, b_quarter at L // 4 (integer division)."""
    return {"a": layer, "b_half": layer // 2, "b_quarter": layer // 4, "c": layer, "d": layer // 2}


# ---- locker sentences (tokenizer only) ----------------------------------------------------------------------------


class Misaligned(ValueError):
    """The locker sentences of O and S do not align, token for token or by sentence."""


def locker_sentences(context: str) -> list[str]:
    """The context's locker sentences in order, split as tasks_v2's level-0 prose (and x0_strata) splits it."""
    sents = [s if s.endswith(".") else s + "." for s in context.split(". ")]
    return [s for s in sents if s.startswith(LOCKER_PREFIX)]


def locker_spans(text: str, context: str) -> list[tuple[int, int]]:
    """Each locker sentence's character span [start, end) in the rendered prompt, in context order."""
    from scripts import statement_positions as SP

    assert text.count(context) == 1, "the context is not once in the prompt"
    base = text.index(context)
    spans = []
    for s in locker_sentences(context):
        i = base + SP.find_sentence(context, s)
        spans.append((i, i + len(s)))
    return spans


def locker_positions(offsets: list[tuple[int, int]], spans: list[tuple[int, int]]) -> list[list[int]]:
    """Per locker sentence, the token positions whose characters overlap it (statement_positions.tokens_in)."""
    from scripts import statement_positions as SP

    out = [SP.tokens_in(offsets, a, b) for a, b in spans]
    assert all(out), "a locker sentence has no token"
    return out


def align(
    pos_o: list[list[int]], pos_s: list[list[int]], ids_o: list[int], ids_s: list[int]
) -> tuple[list[int], list[int], str]:
    """O's patched positions, the S positions their states come from, and how they were aligned: "token" when every
    locker sentence sits at the same positions with the same ids in O and S; else "sentence" when the k-th locker
    sentence of each has the same token count (positions paired in order). Raises Misaligned otherwise."""
    if len(pos_o) != len(pos_s):
        raise Misaligned(f"{len(pos_o)} locker sentences in O, {len(pos_s)} in S")
    flat_o = [p for sent in pos_o for p in sent]
    flat_s = [p for sent in pos_s for p in sent]
    if pos_o == pos_s and all(ids_o[p] == ids_s[p] for p in flat_o):
        return flat_o, flat_s, "token"
    for k, (a, b) in enumerate(zip(pos_o, pos_s, strict=True)):
        if len(a) != len(b):
            raise Misaligned(f"locker sentence {k}: {len(a)} tokens in O, {len(b)} in S")
    return flat_o, flat_s, "sentence"


def merged_spans(offsets: list[tuple[int, int]], positions: list[int]) -> list[tuple[int, int]]:
    """The character spans of the tokens at `positions`, adjacent ones merged."""
    from scripts import statement_positions as SP

    return SP.merged_spans(offsets, positions)


# ---- items (tokenizer only) ---------------------------------------------------------------------------------------


def stored_reads(main_run: str, layer: int) -> tuple[list[str], dict[str, dict]]:
    """The main run's items at the layer (the scenes of its chat outcomes, in order) and, per scene, its stored reads:
    the whole arm's switch at every layer it ran, per reader, and the unedited S read (competence.jsonl, read_right)."""
    src = X.RESULTS / main_run
    scenes: dict[str, None] = {}  # ordered: the scenes at the layer, in the run's order
    stored: dict[str, dict] = collections.defaultdict(lambda: {"whole": {}, "S_read": {}})
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] != RENDERING or r["arm"] != "whole":
            continue
        if r["layer"] == layer and r["reader"] == X.LOOKUP:
            scenes.setdefault(r["scene"])
        stored[r["scene"]]["whole"].setdefault(str(r["layer"]), {})[r["reader"]] = r["switched"]
    for r in X.read_jsonl(src / "competence.jsonl"):
        if r["rendering"] == RENDERING and r["variant"] == "alt" and r["scene"] in scenes:
            stored[r["scene"]]["S_read"][r["reader"]] = int(r["read_right"])
    return list(scenes), {s: stored[s] for s in scenes}


def select(tok, main_run: str, layer: int) -> tuple[list[dict], dict]:
    """The 45b items in the main run's scene order (locker after the asked pick, locker sentences aligned) and the
    counts: the main run's items, the locker-after ones, drops by reason, alignment modes, entities."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T

    src = X.RESULTS / main_run
    m = json.loads((src / "manifest.json").read_text())
    assert m["predicted"] == layer, f"{main_run}: predicted layer {m['predicted']}, not {layer}"
    assert m.get("alt", "cf") == "cf", f"{main_run}: not the main test's alt (two picks swap)"
    assert X.ALT == "cf", "45b rebuilds the main test's alt (two picks swap): x0_necessity.ALT must be 'cf'"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {main_run}"
    scenes, stored = stored_reads(main_run, layer)
    assert scenes, f"{main_run}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == RENDERING}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    read_suffix = tok.decode(next(iter(rebuilt.values()))["space"])
    out, dropped, modes = [], collections.Counter(), collections.Counter()
    after = 0
    for scene in scenes:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {main_run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        feats = ST.features(c)
        if feats["org locker vs asked pick"] != "after":
            continue
        after += 1
        texts: dict[tuple[str, str], str] = {}
        offsets: dict[tuple[str, str], list[tuple[int, int]]] = {}
        for w in X.READERS:
            rd = c["readers"][w]
            for v, ctx in (("org", c["context"]), ("alt", c["cf_context"])):
                text = X.render(tok, by_id[rd["id"]], RENDERING, ctx)
                enc = raw_encoding(tok, text, offsets=True)
                assert enc["input_ids"] == rd["ids"][v], f"{scene} {w} {v}: the rendered prompt's ids differ"
                texts[(w, v)], offsets[(w, v)] = text, enc["offset_mapping"]
        lk = X.LOOKUP
        ids = c["readers"][lk]["ids"]
        pos_o = locker_positions(offsets[(lk, "org")], locker_spans(texts[(lk, "org")], c["context"]))
        pos_s = locker_positions(offsets[(lk, "alt")], locker_spans(texts[(lk, "alt")], c["cf_context"]))
        try:
            patched, source, mode = align(pos_o, pos_s, ids["org"], ids["alt"])
        except Misaligned as e:
            dropped[f"the locker sentences do not align: {e}"] += 1
            continue
        if any(
            c["readers"][X.RECALL]["ids"][v][: last + 1] != ids[v][: last + 1]
            for v, last in (("org", max(patched)), ("alt", max(source)))
        ):
            dropped["the readers' prompts differ before the last locker token"] += 1
            continue
        modes[mode] += 1
        o_off = offsets[(lk, "org")]
        marks = {"bridge": [list(o_off[c["pos"]])],
                 "lockers": [list(s) for sent in pos_o for s in merged_spans(o_off, sent)]}  # fmt: skip
        end = max(b for spans in marks.values() for _, b in spans)
        assert texts[(X.RECALL, "org")][:end] == texts[(lk, "org")][:end], f"{scene}: the readers' texts differ"
        out.append({
            "scene": scene, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
            "upstream": c["upstream"], "features": feats, "pos": c["pos"], "space": c["space"],
            "read_suffix": read_suffix, "context": c["context"], "cf_context": c["cf_context"],
            "lockers": {"sentences": locker_sentences(c["context"]), "org": pos_o, "alt": pos_s, "align": mode},
            "patched": patched, "source": source, "marks": marks,
            "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b",
                                                             "ids")},
                            "text": {v: texts[(w, v)] for v in ("org", "alt")}} for w in X.READERS},
            "stored": stored[scene],
        })  # fmt: skip
    counts = {"main_run": main_run, "layer": layer, "main_items": len(scenes), "locker_after": after,
              "dropped": dict(dropped), "align": dict(modes), "items": len(out),
              "entities": len({it["entity"] for it in out})}  # fmt: skip
    return out, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    """The example items: k random indices of n (seed 0), as X0 picks its examples."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def stage_plan() -> dict:
    """Tokenizer only: the items, drops and alignment for the target, and whether each prompt decodes to its text."""
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = select(tok, MAIN_RUN[pins.TARGET], layer)
    counts["arm_layers"] = arm_layers(layer)
    counts["patched_tokens_median"] = statistics.median(len(it["patched"]) for it in items) if items else None
    counts["decodes_to_text"] = sum(
        tok.decode(it["readers"][w]["ids"][v]) == it["readers"][w]["text"][v]
        for it in items
        for w in X.READERS
        for v in ("org", "alt")
    )
    counts["prompts"] = 4 * len(items)
    print(json.dumps(counts, indent=2))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "45b renders the main test's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"45b runs on {sorted(MAIN_RUN)}, not {target}"
    main_run, layer = MAIN_RUN[target], X.PREDICTED[target]
    layers = arm_layers(layer)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / main_run
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "spec": "jobs/c3/batch45.yaml (45b)",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl",
                              src / "competence.jsonl")},
         "main_run": main_run, "layer": layer, "arm_layers": layers, "arms": {a: ARM_TEXT[a] for a in ARMS},
         "items_rule": "the main run's items at L (chat) whose org bridge's locker sentence comes after the asked pick "
                       "(x0_strata); locker sentences aligned token for token, else by sentence; else dropped",
         "locker_sentences": "every 'The locker of <thing> is <n>.' sentence of the context",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = top token is S's answer",
         "rule": RULE, "decisive_reader": X.LOOKUP,
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "note": "batch 45 (Dan 26 Oct ~18:30); results closed until docs/predictions_batch45.md holds Dan's Q45.5"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, main_run, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    record = tuple(sorted(set(layers.values())))
    examples = set(example_indices(len(items)))
    rows, norms, greedy = [], [], []
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"45b at L{layer} (item)")):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=record)[1] for v in ("org", "alt")}
            pos, patched, source = it["pos"], it["patched"], it["source"]
            edits: dict[str, dict] = {"none": {}}
            for arm in BRIDGE_ARMS:
                la = layers[arm]
                delta = (h["alt"][la][pos] - h["org"][la][pos])[None]
                edits[arm] = {la: AddRows(delta, [pos])}
                norms.append({"scene": it["scene"], "arm": arm, "layer": la, "positions": 1,
                              "delta_norm": round(float(delta.norm()), 4),
                              "org_norm": round(float(h["org"][la][pos].norm()), 4)})  # fmt: skip
            for arm in LOCKER_ARMS:
                la = layers[arm]
                delta = h["alt"][la][source] - h["org"][la][patched]
                edits[arm] = {la: AddRows(delta, patched)}
                row_norms = delta.norm(dim=-1)
                norms.append({"scene": it["scene"], "arm": arm, "layer": la, "positions": len(patched),
                              "changed_positions": int((row_norms > 0).sum()),
                              "delta_norm": round(float(delta.norm()), 4),
                              "org_norm": round(float(h["org"][la][patched].norm()), 4)})  # fmt: skip
            assert list(edits) == list(O_ARMS)
            for w, rd in it["readers"].items():
                base = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w}
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(edits.values()), RENDERING, it["space"], ws)
                s_logits, _ = X.read_logits(model, rd["ids"]["alt"], [{}], RENDERING, it["space"], ws)
                for arm, lg in zip((*O_ARMS, S_ARM), [*logits, s_logits[0]], strict=True):
                    top = int(lg.argmax())
                    rows.append({**base, "arm": arm, "prompt": "S" if arm == S_ARM else "O",
                                 "layer": layers.get(arm), "site": site(arm), **X.read_row(lg, rd, digits),
                                 "top": top, "top_text": tok.decode([top])})  # fmt: skip
                if i in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, list(edits.values()))
                    s_ids = torch.tensor([rd["ids"]["alt"]], device=model.device)
                    texts += model.generate_batch(s_ids, X.GEN_TOKENS, [{}])
                    greedy += [{"scene": it["scene"], "reader": w, "arm": arm, "greedy": t}
                               for arm, t in zip((*O_ARMS, S_ARM), texts, strict=True)]  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, flush=True)
    return out


SWEEP_STEP = 2  # the layer sweep (Dan 26 Oct ~21:20; descriptive, after the data): every 2 layers from L/2 to L
# the sweep's arms per layer: the bridge word, every locker-sentence token, and (Dan ~22:00) only the item, only the
# value (the digit or number word) or only the sentence-final token of every locker sentence
SWEEP_ARMS = {"bw": "the bridge-word change", "ls": "S patched into O at every locker-sentence token",
              "li": "only the item's tokens inside the locker sentences", "lv": "only the value token(s)",
              "lf": "only the sentence-final token"}  # fmt: skip
ROLE_ARM = {"item": "li", "value": "lv", "final": "lf"}
LOCKER_RE = re.compile(r"^The locker of (?:the )?(.+) is (.+?)\.$")


def sweep_layers(layer: int) -> list[int]:
    """The sweep's layers: L // 2 to L every SWEEP_STEP layers, L always included."""
    return sorted(set(range(layer // 2, layer + 1, SWEEP_STEP)) | {layer})


def role_positions(tok, it: dict) -> dict[str, tuple[list[int], list[int]]]:
    """Per role (item / value / final), O's positions and the paired S positions inside every locker sentence: the
    tokens whose characters overlap the item's name, the value, or the final '.' ('The locker of [the] <item> is
    <value>.'), found by decoding the sentence's tokens one by one. O and S hold the same locker sentences, paired in
    order (select's alignment), so the k-th token plays the same role in both."""
    ids = it["readers"][X.LOOKUP]["ids"]["org"]
    out: dict[str, tuple[list[int], list[int]]] = {r: ([], []) for r in ROLE_ARM}
    for sent, po, ps in zip(it["lockers"]["sentences"], it["lockers"]["org"], it["lockers"]["alt"], strict=True):
        pieces = [tok.decode([ids[p]]) for p in po]
        start = "".join(pieces).find(sent)
        m = LOCKER_RE.match(sent)
        assert start >= 0, f"{it['scene']}: {sent!r} is not in its tokens' text"
        assert m, f"{it['scene']}: {sent!r} is not a locker sentence"
        spans = {"item": m.span(1), "value": m.span(2), "final": (len(sent) - 1, len(sent))}
        at = -start
        for k, piece in enumerate(pieces):
            a, b = at, at + len(piece)
            at = b
            for role, (x, y) in spans.items():
                if a < y and b > x:
                    out[role][0].append(po[k])
                    out[role][1].append(ps[k])
    assert all(o for o, _ in out.values()), f"{it['scene']}: a role has no token"
    return out


def stage_sweep(name: str, why: str) -> Path:
    """45b's layer sweep (descriptive, after the data): on the same locker-after items, at each sweep layer, the
    bridge-word change (arm bw<l>, as a) and S patched into O at every locker-sentence token (arm ls<l>, as c); none and
    S as in the run. Reads as stage_run."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "45b renders the main test's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"45b runs on {sorted(MAIN_RUN)}, not {target}"
    main_run, layer = MAIN_RUN[target], X.PREDICTED[target]
    layers = sweep_layers(layer)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "main_run": main_run, "layer": layer, "sweep_layers": layers,
         "arms": {**{f"{k}<l>": f"{v}, at layer l" for k, v in SWEEP_ARMS.items()}, "none": ARM_TEXT["none"],
                  "S": ARM_TEXT["S"]},
         "roles": "item / value / final tokens of every locker sentence by character overlap (role_positions)",
         "items_rule": "as the 45b run (x45b_binding.select)", "read": "as the 45b run",
         "descriptive": "after the data (Dan 26 Oct ~21:20): no rule", "seeds": {"bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, main_run, layer)
    for it in items:
        it["roles"] = {r: {"org": o, "alt": s} for r, (o, s) in role_positions(tok, it).items()}
    (out / "plan.json").write_text(json.dumps(counts, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    rows = []
    with torch.no_grad():
        for it in progress(items, f"45b sweep L{layers[0]}-L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=tuple(layers))[1]
                 for v in ("org", "alt")}  # fmt: skip
            pos, patched, source = it["pos"], it["patched"], it["source"]
            edits: dict[str, dict] = {"none": {}}
            for la in layers:
                edits[f"bw{la}"] = {la: AddRows((h["alt"][la][pos] - h["org"][la][pos])[None], [pos])}
                edits[f"ls{la}"] = {la: AddRows(h["alt"][la][source] - h["org"][la][patched], patched)}
                for role, arm in ROLE_ARM.items():
                    o, s = it["roles"][role]["org"], it["roles"][role]["alt"]
                    edits[f"{arm}{la}"] = {la: AddRows(h["alt"][la][s] - h["org"][la][o], o)}
            for w, rd in it["readers"].items():
                base = {"scene": it["scene"], "entity": it["entity"], "reader": w}
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(edits.values()), RENDERING, it["space"], ws)
                s_logits, _ = X.read_logits(model, rd["ids"]["alt"], [{}], RENDERING, it["space"], ws)
                for arm, lg in zip((*edits, S_ARM), [*logits, s_logits[0]], strict=True):
                    la = int(arm[2:]) if arm[:2] in SWEEP_ARMS else None
                    rows.append({**base, "arm": arm, "layer": la, **X.read_row(lg, rd, digits)})
    X.write_jsonl(out / "outcomes.jsonl", rows)
    print("wrote", out, flush=True)
    return out


def sweep_cells(rows: list[dict], n_boot: int = X.N_BOOT) -> dict[str, list[dict]]:
    """Per reader and sweep layer: each sweep arm's switch rate over the items (the arms the run has), and each
    locker-sentence arm's share of S's switches (among the items S switches), with cluster-bootstrap CIs over bridge
    entities."""
    out: dict[str, list[dict]] = {}
    for w in X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        entity = {r["scene"]: r["entity"] for r in mine}
        scenes = list(entity)
        by = {(r["scene"], r["arm"]): int(r["switched"]) for r in mine}
        arms = sorted({r["arm"] for r in mine})
        cols = {a: [by[(s, a)] for s in scenes] for a in arms}
        layers = sorted({r["layer"] for r in mine if r["layer"] is not None})
        kinds = [k for k in SWEEP_ARMS if f"{k}{layers[0]}" in cols]
        for la in layers:
            for k in kinds[1:]:  # every locker-sentence arm (not the bridge word)
                cols[f"{k}{la}_and_S"] = [x & y for x, y in zip(cols[f"{k}{la}"], cols[S_ARM], strict=True)]
        boot = X.resampled_rates(cols, [entity[s] for s in scenes], n_boot)
        n, n_s = len(scenes), sum(cols[S_ARM])
        cells = []
        for la in layers:
            cell: dict[str, Any] = {"layer": la, "n": n, "S_switched": n_s}
            for k in kinds:
                cell[k] = [sum(cols[f"{k}{la}"]) / n, *X.interval(boot[f"{k}{la}"])]
                if k != "bw":
                    with np.errstate(divide="ignore", invalid="ignore"):
                        ratio = boot[f"{k}{la}_and_S"] / np.where(boot[S_ARM] > 0, boot[S_ARM], np.nan)
                    cell[f"{k}_of_S"] = [sum(cols[f"{k}{la}_and_S"]) / n_s if n_s else None, *X.interval(ratio)]
            cells.append(cell)
        out[w] = cells
    return out


def stage_sweep_table(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    keep, sanity = sane(X.read_jsonl(src / "cases.jsonl"))  # Dan ~22:35: only the items passing the sanity check
    cells = sweep_cells([r for r in X.read_jsonl(src / "outcomes.jsonl") if r["scene"] in keep], n_boot)
    out = src / f"sweep-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# 45b layer sweep (descriptive, after the data): {name}", "",
             f"Model {m['model']['target']}, L = {m['layer']}; the 45b items (locker after the pick) that pass the sanity "
             f"check (O and S the same length and the same ids after the bridge word): {sanity['pass']} of "
             f"{sanity['items']}, {sanity['dropped']} dropped. Switch = the top token is S's answer. Cluster bootstrap "
             f"over bridge entities ({n_boot} resamples). UNVERIFIED.", ""]  # fmt: skip
    for w, rows_ in cells.items():
        kinds = [k for k in SWEEP_ARMS if k in rows_[0]]
        lines += [f"## {'lookup' if w == X.LOOKUP else 'recall'} (n = {rows_[0]['n']}, S switches {rows_[0]['S_switched']}): "
                  "switch rate over the items", "", "| layer | " + " | ".join(SWEEP_ARMS[k] for k in kinds) + " |",
                  "|---" * (len(kinds) + 1) + "|"]  # fmt: skip
        lines += [f"| {c['layer']} | " + " | ".join(fmt(c[k]) for k in kinds) + " |" for c in rows_]
        lines.append("")
    (out / "sweep.json").write_text(json.dumps({"run": name, "sanity": sanity, "cells": cells}, indent=1) + "\n")
    (out / "sweep.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


# 45n (Dan ~22:35, fixed in advance, jobs/c3/batch45.yaml): is the link the locker sentences carry outside the lens?
LINK_ARMS = {"c": "S patched into O at every locker-sentence token, at L (45b's c)",
             "c_nojpp": "the same copy without each token's J++ part (signed OMP, k = 25)",
             "c_norand": "the same copy without a random part of each token's J++ share"}  # fmt: skip
LINK_SHARE, LINK_SLACK = 0.8, 0.1  # without J++ >= 0.8 x the full copy, and >= without the random part - 0.1
LINK_MODELS = ("qwen3.5-9b", "qwen3.6-27b")  # the rule reads these two; Muse is reported, not counted
EPS = 1e-9


def link_parts(delta, jdic, basis, k: int = X.K_MAIN):
    """Per locker token (row of delta [n, d]): its J++ part (signed OMP, k atoms of jdic) and a random part of the same
    share of the row's squared norm (X0's random subspace); rows with no change keep zero parts."""
    import torch

    from scripts import statement_positions as SP

    part = torch.zeros_like(delta)
    live = delta.norm(dim=-1) > 0
    if bool(live.any()):
        part[live] = X.fit(jdic, delta[live], k, "signed").to(delta.dtype)
    share = part.norm(dim=-1) ** 2 / (delta.norm(dim=-1) ** 2).clamp_min(1e-30)
    return part, SP.random_subspace_part(delta, share, basis).to(delta.dtype), share


def stage_link(name: str, why: str) -> Path:
    """45n's run (GPU): the 45b items at L; arms none, c, c_nojpp, c_norand, read on O, and S read on S."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "45n renders the main test's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"45n runs on {sorted(MAIN_RUN)}, not {target}"
    main_run, layer = MAIN_RUN[target], X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "main_run": main_run, "layer": layer, "test": "45n",
         "arms": {**LINK_ARMS, "none": ARM_TEXT["none"], "S": ARM_TEXT["S"]}, "k": X.K_MAIN, "omp": "signed",
         "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at each token's J++ share",
         "items_rule": "as the 45b run (x45b_binding.select); the verdict keeps the items passing same_after_bridge",
         "spec": "jobs/c3/batch45.yaml (45n)", "seeds": {"bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, main_run, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    rows, norms, basis = [], [], None
    with torch.no_grad():
        for it in progress(items, f"45n at L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer]
                 for v in ("org", "alt")}  # fmt: skip
            patched, source = it["patched"], it["source"]
            delta = (h["alt"][source] - h["org"][patched]).float().to(jdic.device)
            if basis is None:
                basis = SP.random_basis(delta.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer))
                basis = basis.to(delta.device)
            part, rand, share = link_parts(delta, jdic, basis)
            dt = h["org"].dtype
            edits = {"none": {}, "c": {layer: AddRows(delta.to(dt), patched)},
                     "c_nojpp": {layer: AddRows((delta - part).to(dt), patched)},
                     "c_norand": {layer: AddRows((delta - rand).to(dt), patched)}}  # fmt: skip
            live = delta.norm(dim=-1) > 0
            norms.append({"scene": it["scene"], "positions": len(patched), "changed_positions": int(live.sum()),
                          "median_jpp_share": round(float(share[live].median()), 5) if bool(live.any()) else None})  # fmt: skip
            for w, rd in it["readers"].items():
                base = {"scene": it["scene"], "entity": it["entity"], "reader": w}
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(edits.values()), RENDERING, it["space"], ws)
                s_logits, _ = X.read_logits(model, rd["ids"]["alt"], [{}], RENDERING, it["space"], ws)
                for arm, lg in zip((*edits, S_ARM), [*logits, s_logits[0]], strict=True):
                    rows.append({**base, "arm": arm, **X.read_row(lg, rd, digits)})
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    print("wrote", out, flush=True)
    return out


def link_rule(rate: dict[str, float]) -> bool:
    """45n on one model's lookup switch rates (point estimates)."""
    return (rate["c_nojpp"] >= LINK_SHARE * rate["c"] - EPS
            and rate["c_nojpp"] >= rate["c_norand"] - LINK_SLACK - EPS)  # fmt: skip


def stage_link_verdict(names: list[str], n_boot: int = X.N_BOOT) -> Path:
    """45n's verdict over its runs: per model, the items passing the sanity check, each arm's switch rate per reader
    with its CI, the rule per model and over the 9B and the 27B."""
    out = RESULTS / f"x45n-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob: dict[str, Any] = {"rule": f"without J++ >= {LINK_SHARE} x the full copy and >= without the random part - "
                                    f"{LINK_SLACK}, lookup, point estimates; both of {list(LINK_MODELS)}", "runs": {}}  # fmt: skip
    lines = ["# 45n: is the link the locker sentences carry outside the lens? (jobs/c3/batch45.yaml, fixed in advance)",
             "", "Lookup switch rate over the items passing the sanity check (O and S the same length and the same ids "
             "after the bridge word); recall descriptive. UNVERIFIED.", "",
             "| run | model | items (pass / all) | reader | " + " | ".join(("none", *LINK_ARMS, S_ARM)) + " | holds |",
             "|---|---|---|---|" + "---|" * (len(LINK_ARMS) + 3)]  # fmt: skip
    arms = ("none", *LINK_ARMS, S_ARM)
    for name in names:
        src = RESULTS / name
        m = json.loads((src / "manifest.json").read_text())
        keep, sanity = sane(X.read_jsonl(src / "cases.jsonl"))
        rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["scene"] in keep]
        res: dict[str, Any] = {"model": m["model"]["target"], "sanity": sanity, "readers": {}}
        for w in X.READERS:
            mine = [r for r in rows if r["reader"] == w]
            ent = {r["scene"]: r["entity"] for r in mine}
            scenes = list(ent)
            by = {(r["scene"], r["arm"]): int(r["switched"]) for r in mine}
            cols = {a: [by[(s, a)] for s in scenes] for a in arms}
            boot = X.resampled_rates(cols, [ent[s] for s in scenes], n_boot)
            res["readers"][w] = {a: [sum(cols[a]) / len(scenes), *X.interval(boot[a])] for a in arms}
        rate = {a: v[0] for a, v in res["readers"][X.LOOKUP].items()}
        res["holds"] = link_rule(rate)
        blob["runs"][name] = res
        for w in X.READERS:
            cells = " | ".join(fmt(res["readers"][w][a]) for a in arms)
            mark = ("yes" if res["holds"] else "no") if w == X.LOOKUP else ""
            lines.append(f"| {name} | {res['model']} | {sanity['pass']} / {sanity['items']} | "
                         f"{'lookup' if w == X.LOOKUP else 'recall'} | {cells} | {mark} |")  # fmt: skip
    counted = {r["model"]: r["holds"] for r in blob["runs"].values() if r["model"] in LINK_MODELS}
    blob["outlink"] = all(counted.get(t, False) for t in LINK_MODELS)
    blob["missing"] = [t for t in LINK_MODELS if t not in counted]
    verdict = ("the copied link is outside the lens" if blob["outlink"] else
               "pending" if blob["missing"] else "not outside the lens")  # fmt: skip
    blob["verdict"] = verdict
    lines += [
        "",
        f"Verdict (both 9B and 27B): **{verdict}**" + (f" (missing: {blob['missing']})" if blob["missing"] else ""),
    ]
    (out / "x45n.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "x45n.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def site(arm: str) -> str:
    return "bridge word" if arm in BRIDGE_ARMS else "locker sentences" if arm in LOCKER_ARMS else "-"


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


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


def numbers(
    switched: dict[str, list[int]], entities: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED
) -> dict[str, Any]:
    """Each arm's switch rate over the items, and for c and d the share of S's switches they switch (among the items S
    switches), with 95% percentile CIs from X0's cluster bootstrap over bridge entities (paired across arms)."""
    s = switched[S_ARM]
    cols = dict(switched)
    for arm in LOCKER_ARMS:
        cols[f"{arm}_and_S"] = [x & y for x, y in zip(switched[arm], s, strict=True)]
    boot = X.resampled_rates(cols, entities, n_boot, seed)
    n, n_s = len(entities), sum(s)
    out: dict[str, Any] = {"n": n, "entities": len(set(entities)), "S_switched": n_s,
                           "hits": {a: sum(switched[a]) for a in ARMS}, "rate": {}, "hits_of_S": {}, "of_S": {}}  # fmt: skip
    for arm in ARMS:
        out["rate"][arm] = [out["hits"][arm] / n, *X.interval(boot[arm])]
    for arm in LOCKER_ARMS:
        hits = sum(cols[f"{arm}_and_S"])
        out["hits_of_S"][arm] = hits
        if not n_s:
            out["of_S"][arm] = [None, None, None]
            continue
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = boot[f"{arm}_and_S"] / np.where(boot[S_ARM] > 0, boot[S_ARM], np.nan)
        out["of_S"][arm] = [hits / n_s, *X.interval(ratio)]
    return out


def rule(nums: dict[str, Any]) -> dict[str, Any]:
    """The 45b rule on one reader's counts (point estimates): (c) or (d) switches at least half of the items S switches,
    and (a) switches at most 0.25 of all items. Compared as counts (exact at the thresholds); can't tell if S switches
    none."""
    n, n_s = nums["n"], nums["S_switched"]
    a_ok = nums["hits"]["a"] <= A_MAX * n
    half = {arm: n_s > 0 and nums["hits_of_S"][arm] >= HALF * n_s for arm in LOCKER_ARMS}
    if not n_s:
        verdict = "can't tell (S switches no lookup)"
    else:
        verdict = "holds" if (half["c"] or half["d"]) and a_ok else "does not hold"
    return {"verdict": verdict, "holds": verdict == "holds", "c_at_least_half_of_S": half["c"],
            "d_at_least_half_of_S": half["d"], "a_at_most_0.25": a_ok}  # fmt: skip


def agreement(items: list[dict], rows: list[dict], layers: dict[str, int]) -> dict[str, Any]:
    """Descriptive checks against the main run: the rerun bridge-word arms against its stored whole arm at the same
    layer (where it ran), and the recomputed S read against its stored one (competence.jsonl)."""
    by = {(r["scene"], r["reader"], r["arm"]): int(r["switched"]) for r in rows}
    out: dict[str, Any] = {}
    for w in X.READERS:
        for arm in BRIDGE_ARMS:
            pairs = [(by[(it["scene"], w, arm)], it["stored"]["whole"][str(layers[arm])][w]) for it in items
                     if str(layers[arm]) in it["stored"]["whole"]]  # fmt: skip
            if pairs:
                out[f"{w} {arm} vs stored whole at L{layers[arm]}"] = agree(pairs)
        pairs = [
            (by[(it["scene"], w, S_ARM)], it["stored"]["S_read"][w]) for it in items if w in it["stored"]["S_read"]
        ]
        if pairs:
            out[f"{w} S vs stored S read"] = agree(pairs)
    return out


def agree(pairs: list[tuple[int, int]]) -> dict[str, Any]:
    return {"n": len(pairs), "agree": sum(a == b for a, b in pairs), "rerun": sum(a for a, _ in pairs),
            "stored": sum(b for _, b in pairs)}  # fmt: skip


def fmt(v: list) -> str:
    return "-" if v[0] is None else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def same_after_bridge(it: dict) -> bool:
    """Dan's sanity check (26 Oct ~22:35): O and S have the same token count and every position after the bridge word
    holds the same token id in both, for both readers' prompts (else S also differs after the bridge, e.g. the other
    swapped pick comes later)."""
    for rd in it["readers"].values():
        o, s = rd["ids"]["org"], rd["ids"]["alt"]
        if len(o) != len(s) or o[it["pos"] + 1 :] != s[it["pos"] + 1 :]:
            return False
    return True


def sane(items: list[dict]) -> tuple[set[str], dict[str, int]]:
    """The scenes that pass same_after_bridge, and the counts (pass / dropped)."""
    keep = {it["scene"] for it in items if same_after_bridge(it)}
    return keep, {"items": len(items), "pass": len(keep), "dropped": len(items) - len(keep)}


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "cases.jsonl")
    plan = json.loads((src / "plan.json").read_text())
    layers = m["arm_layers"]
    per_reader = {}
    for w in X.READERS:
        _, entities, switched = item_table(rows, w)
        per_reader[w] = numbers(switched, entities, n_boot)
    r = rule(per_reader[X.LOOKUP])
    norms = X.read_jsonl(src / "norms.jsonl")
    med_norm = {arm: statistics.median(x["delta_norm"] for x in norms if x["arm"] == arm)
                for arm in (*BRIDGE_ARMS, *LOCKER_ARMS)}  # fmt: skip
    checks = agreement(items, rows, layers)
    keep, sanity = sane(items)  # Dan ~22:35: the rule again on the items that pass the sanity check
    sane_lk = None
    if keep:
        _, ents, sw = item_table([x for x in rows if x["scene"] in keep], X.LOOKUP)
        sane_lk = numbers(sw, ents, n_boot)
    sanity["rule"] = rule(sane_lk) if sane_lk else None
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": name, "model": m["model"], "main_run": m["main_run"], "layer": m["layer"], "arm_layers": layers,
            "rule_text": RULE, "rule": r, "readers": per_reader, "plan": plan, "checks": checks,
            "median_delta_norm": med_norm, "n_boot": n_boot, "seed": X.BOOT_SEED, "sanity": sanity,
            "sanity_lookup": sane_lk}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=2) + "\n")
    lk = per_reader[X.LOOKUP]
    lines = [f"# 45b, where the binding is made when the locker comes after the pick: {name}", "",
             f"Model {m['model']['target']}, L = {m['layer']} (L/2 = {layers['d']}, L/4 = {layers['b_quarter']}); items: "
             f"{m['main_run']}'s items whose org locker sentence comes after the asked pick, n = {lk['n']} "
             f"({lk['entities']} bridge entities; {plan['locker_after']} locker-after, dropped {plan['dropped'] or 'none'}; "
             f"aligned {plan['align']}). Read on O at its answer position as X0 reads; switch = the top token is S's "
             f"answer. Cluster bootstrap over bridge entities ({n_boot} resamples, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"## Rule (lookup, point estimates): {r['verdict'].upper()}", "", f"Rule (batch 45, fixed in advance): {RULE}",
             f"(c) switches {lk['hits_of_S']['c']} of the {lk['S_switched']} lookups S switches "
             f"({fmt(lk['of_S']['c'])}); (d) {lk['hits_of_S']['d']} of {lk['S_switched']} ({fmt(lk['of_S']['d'])}); "
             f"(a) switches {lk['hits']['a']} of {lk['n']} ({fmt(lk['rate']['a'])}).", "",
             "| arm | what | layer | lookup switch rate | lookup switched | recall switch rate (descriptive) | "
             "median ‖h_S − h_O‖ |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    rc = per_reader[X.RECALL]
    for arm in ARMS:
        la = layers.get(arm, "-")
        nrm = f"{med_norm[arm]:.1f}" if arm in med_norm else "-"
        lines.append(f"| {arm} | {ARM_TEXT[arm]} | {la} | {fmt(lk['rate'][arm])} | {lk['hits'][arm]} / {lk['n']} | "
                     f"{fmt(rc['rate'][arm])} | {nrm} |")  # fmt: skip
    lines += ["", "Among the items S itself switches:", "", "| arm | lookup: share of S's switches | recall (descriptive) |",
              "|---|---|---|"]  # fmt: skip
    lines += [f"| {arm} | {fmt(lk['of_S'][arm])} ({lk['hits_of_S'][arm]} / {lk['S_switched']}) | "
              f"{fmt(rc['of_S'][arm])} ({rc['hits_of_S'][arm]} / {rc['S_switched']}) |" for arm in LOCKER_ARMS]  # fmt: skip
    lines += ["", "Checks against the main run (descriptive): " + "; ".join(
        f"{k}: {v['agree']} of {v['n']} agree (rerun {v['rerun']}, stored {v['stored']})" for k, v in checks.items())]  # fmt: skip
    lines += ["", f"Sanity check (Dan ~22:35: O and S the same length, the same token ids after the bridge word, both "
              f"readers): {sanity['pass']} of {sanity['items']} items pass, {sanity['dropped']} dropped."]  # fmt: skip
    if sane_lk:
        lines.append(f"The rule on the passing items: {sanity['rule']['verdict']}; (c) {sane_lk['hits_of_S']['c']} of "
                     f"{sane_lk['S_switched']} S switches ({fmt(sane_lk['of_S']['c'])}), (d) {sane_lk['hits_of_S']['d']} "
                     f"({fmt(sane_lk['of_S']['d'])}), (a) {sane_lk['hits']['a']} of {sane_lk['n']} ({fmt(sane_lk['rate']['a'])}).")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


# ---- examples (CPU) -----------------------------------------------------------------------------------------------


def marked(text: str, spans: list[tuple[int, int]]) -> str:
    """The text with ⟦ ⟧ around each span (spans must not overlap); a span's leading whitespace stays outside."""
    out, last = [], 0
    for a, b in sorted(spans):
        while a < b and text[a].isspace():
            a += 1
        assert a >= last, f"span ({a}, {b}) overlaps the previous one"
        out += [text[last:a], MARK_OPEN, text[a:b], MARK_CLOSE]
        last = b
    out.append(text[last:])
    return "".join(out)


def stage_examples(name: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> Path:
    """examples.json (job pages) and examples.md: k random items (seed, as the run's greedy examples), each reader's
    O prompt exactly as the model reads it (the digit's space token appended), the bridge word and every patched
    locker-sentence token span marked, and each arm's answer (the top token read, and 8 greedy tokens)."""
    src = RESULTS / name
    path = src / "examples.json"
    assert not path.exists(), f"{path} exists; examples are written once"
    m = json.loads((src / "manifest.json").read_text())
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    layers = m["arm_layers"]
    groups = [{"key": w, "title": "lookup" if w == X.LOOKUP else "recall (descriptive)",
               "definition": "the O prompt as the model reads it; ⟦…⟧ / underlined: the bridge word (arms a, b) and "
                             "the patched locker-sentence tokens (arms c, d)", "n_total": len(items)}
              for w in X.READERS]  # fmt: skip
    examples, md = [], [f"# 45b examples: {name}", "",
                        f"{min(k, len(items))} random items of {len(items)} (seed {seed}); model {m['model']['target']}, "
                        f"L = {m['layer']}. Prompts exactly as the model reads them (the read appends the digit's space "
                        f"token); ⟦…⟧ marks the bridge word (arms a, b) and each patched locker-sentence token span "
                        f"(arms c, d; a token's leading space shown outside). Answer = the top token at the read step; "
                        f"greedy = 8 greedy tokens of the edited prompt (no space appended). UNVERIFIED.", ""]  # fmt: skip
    for i in example_indices(len(items), k, seed):
        it = items[i]
        spans = [(a, b) for a, b in it["marks"]["bridge"] + it["marks"]["lockers"]]
        md += [f"## {it['scene']} ({it['domain']}): bridge {it['entity']} → {it['cf_bridge']}; aligned "
               f"{it['lockers']['align']}; {len(it['patched'])} locker tokens patched", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            prompt = rd["text"]["org"] + it["read_suffix"]
            answers = {}
            for arm in ARMS:
                r = reads[(it["scene"], w, arm)]
                where = f"L{layers[arm]}" if arm in layers else ""
                answers[arm] = {"top": r["top_text"], "role": r["role"], "switched": r["switched"], "layer": where,
                                "greedy": greedy.get((it["scene"], w, arm))}  # fmt: skip
            examples.append({
                "group": w, "family": w, "item_id": rd["id"], "prompt": prompt, "prompt_marked": marked(prompt, spans),
                "spans": [{"start": a, "end": b, "role": "bridge_word"} for a, b in it["marks"]["bridge"]]
                + [{"start": a, "end": b, "role": "patched_locker"} for a, b in it["marks"]["lockers"]],
                "condition": f"{rd['question']} O's answer {rd['answer']}, S's answer {rd['cf_answer']}",
                "answers": {"clean": answers["none"]["top"].strip(), "edited": answers["c"]["top"].strip(),
                            "expected": {"switches (S's answer)": rd["cf_answer"], "stays (O's answer)": rd["answer"]}},
                "numbers": {f"{arm} {ARM_TEXT[arm]}": f"top {a['top']!r} ({a['role']}); greedy {a['greedy']!r}"
                            for arm, a in answers.items()},
                "why": "edited = arm c (S patched into O at the locker sentences, at L); every arm under numbers",
            })  # fmt: skip
            md += [f"**{'lookup' if w == X.LOOKUP else 'recall'}** ({rd['id']}): O's answer {rd['answer']}, S's "
                   f"answer {rd['cf_answer']}", "", "```", marked(prompt, spans), "```", "",
                   "| arm | what | answer (top token) | switched | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            md += [f"| {arm} {a['layer']} | {ARM_TEXT[arm]} | {a['top']!r} ({a['role']}) | {a['switched']} | "
                   f"{a['greedy']!r} |" for arm, a in answers.items()]  # fmt: skip
            md.append("")
    blob = {"exp": EXP, "run": name, "k": k, "seed": seed, "groups": groups, "examples": examples}
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (src / "examples.md").write_text("\n".join(md) + "\n")
    print("wrote", path, src / "examples.md")
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "examples", "sweep", "sweep-table", "link",
                                      "link-verdict"])  # fmt: skip
    ap.add_argument("--name", help="run name (results/x45b_binding/<name>/); not for plan")
    ap.add_argument("--names", nargs="+", default=[], help="link-verdict: the 45n runs (9B, 27B, Muse if run)")
    ap.add_argument("--why", default="batch 45, test 45b (jobs/c3/batch45.yaml)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
        return
    if a.stage == "link-verdict":
        stage_link_verdict(a.names, a.n_boot)
        return
    assert a.name, f"{a.stage} needs --name"
    if a.stage == "run":
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.name, a.n_boot)
    elif a.stage == "sweep":
        stage_sweep(a.name, a.why)
    elif a.stage == "sweep-table":
        stage_sweep_table(a.name, a.n_boot)
    elif a.stage == "link":
        stage_link(a.name, a.why)
    else:
        stage_examples(a.name)


if __name__ == "__main__":
    main()
