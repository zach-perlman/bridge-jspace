"""x48_enrich (batch 48, test 48.2; jobs/c3/batch48.yaml, designs A and B, rules fixed in advance; Q48.2 in
predictions/2026-10-28_dan.md): why does the recall read J++? Attribute enrichment at the bridge token.

Items: each model's main-test X0 run (x0_necessity, chat, the 200 eligible scenes at the layer fixed in advance: 9B L12,
Muse L26), rebuilt with X.build_cases and checked against the run's stored ids. O = the original prompt, S = the changed
one (the generator's cf context: only the asked pick differs at the bridge token). The main test's arms at L on O, at the
bridge token: whole (h_S - h_O), no_jpp (the change minus its J++ part: signed OMP, k = 25, the J++ lens atoms at L as X0
takes them), no_rand (minus a random part of the same share: X0's random subspace, seed 888 + L).

Design A (probes). The recall attribute is the bridge item's number in its domain; the rule's domain is animals (legs,
the classes present: 2 / 4 / 6 / 8; 31-32 bridge entities over 4 classes, so an entity-held-out probe can read the
attribute). The other two domains (elements: the atomic number; greek: the alphabet position) have one entity per class
(6 and 7-8 entities), so a probe that holds the entity out never saw the held-out class and sits at 0 by construction:
their probes and readings are written and reported as descriptive, outside the rule. One probe per domain: one-hot
ridge on standardized states (x0_probe's probe, penalty by entity-held-out CV), trained on the unedited O prompts of
every chat scene of the set, bridge entities split into 5 folds (seed 0). Held-out accuracy = out-of-fold accuracy;
chance = 1 / the classes present in the domain. Probed at the bridge token and at the last token (the recall's read
position: the prompt with the digit's space token appended), layers L, L + 2, ..., and the last block. Readings on the
main items: the probe of the folds that hold out both the original's and the changed item's entity; m(h) =
score(changed item's class) - score(original item's class); the fraction of the way = (m(arm) - m(O)) / (m(S) - m(O)),
clipped to [0, 1], on items whose unedited gap m(S) - m(O) is positive (others counted, not read). Branch: the bridge
token if the animals probe's held-out accuracy reaches 2x chance at some probed layer there, else the last token (rule
A's fallback, run in the same job); the readings are written for both positions, the verdict reads the branch's.

Rule A (per model, the branch position, the animals items, point estimates, cluster-bootstrap CIs over the original
bridge entities, 10,000, seed 0): at every probed layer >= L + 4 where the probe reads the attribute (held-out accuracy
>= 2x chance), the mean fraction >= 0.6 under whole and under no_rand, <= 0.3 under no_jpp, and the paired CI of
no_rand - no_jpp excludes 0. "J++ keys the enrichment" on the batch if it holds on both models.

Design B (MLPs). Mean-ablate the MLP write of each block at one position: the block's MLP output as it enters the
residual (Qwen3.5: `mlp`; Muse: `post_feedforward_layernorm`, which scales `mlp` before the add) replaced by its
scene-mean over the unedited O prompts of the items at that role's position. Arms on O, both readers' chat read:
none; bridge_late = the bridge token, layers l > L; person_late = the asked person's token (the last token of the name
in the asked pick sentence), layers l > L (control 1, the same module count); bridge_early = the bridge token, layers l
<= L / 2 (control 2). Accuracy = the share of items whose top token is O's answer.

Rule B (per model, point estimates, CIs beside): the recall's accuracy falls >= 0.4 under bridge_late while the
lookup's stays within 0.1, and both controls stay within 0.1 for both readers. If the recall survives: the attribute is
fetched at the last token; reported.

SEALED: the runs write no verdict; `verdict` refuses until predictions/2026-10-28_dan.md holds Dan's Q48.2 answer.

uv run python scripts/x48_enrich.py plan                                                  # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_enrich.py run_a --name qwen35_9b_x48_2a   # GPU, then the probes (CPU)
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_enrich.py run_b --name qwen35_9b_x48_2b   # GPU
uv run python scripts/x48_enrich.py analyse_a --name qwen35_9b_x48_2a                    # CPU: refit the probes
uv run python scripts/x48_enrich.py verdict --runs-a qwen35_9b_x48_2a muse30_x48_2a --runs-b qwen35_9b_x48_2b muse30_x48_2b
"""

from __future__ import annotations

import argparse
import collections
import contextlib
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_probe as P

EXP = "x48_enrich"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch48.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q48.2"
MAIN_RUN = {"qwen3.5-9b": "qwen35_9b_x0_necessity", "muse-glimmer-30b": "muse30b_x0_necessity"}
RUNS_A = {"qwen3.5-9b": "qwen35_9b_x48_2a", "muse-glimmer-30b": "muse30_x48_2a"}
RUNS_B = {"qwen3.5-9b": "qwen35_9b_x48_2b", "muse-glimmer-30b": "muse30_x48_2b"}
RENDERING = "chat"
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
# design A
ARMS_A = ("none", "alt", "whole", "no_jpp", "no_rand")  # none = O unedited, alt = S unedited; the rest: edits at L on O
EDIT_ARMS = ("whole", "no_jpp", "no_rand")
ARM_TEXT_A = {"none": "O unedited", "alt": "S unedited (the changed prompt)",
              "whole": "the whole change h_S - h_O at the bridge token at L",
              "no_jpp": "the change minus its J++ part (signed OMP, k = 25) at the bridge token at L",
              "no_rand": "the change minus a random part of the J++ part's share at the bridge token at L"}  # fmt: skip
POSITIONS = ("bridge", "last")
RULE_DOMAIN = "animals"  # legs; the other domains have one entity per class (module docstring)
K_FOLDS, SPLIT_SEED = 5, 0
MOVE_MIN, STAY_MAX, READABLE_X, LAYER_FROM = 0.6, 0.3, 2.0, 4  # rule A: >= 0.6, <= 0.3, 2x chance, layers >= L + 4
# design B
ARMS_B = ("none", "bridge_late", "person_late", "bridge_early")
ARM_TEXT_B = {"none": "O unedited",
              "bridge_late": "MLP writes at the bridge token mean-ablated, layers l > L",
              "person_late": "MLP writes at the asked person's token mean-ablated, layers l > L (control 1)",
              "bridge_early": "MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2)"}  # fmt: skip
FALL_MIN, WITHIN = 0.4, 0.1
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULE_A = ("J++ keys the enrichment if, at every probed layer >= L + 4 where the legs probe (animals, entities held "
          "out) reads the attribute (held-out accuracy >= 2x chance), the probe moves >= 0.6 of the way under whole "
          "and under no_rand and <= 0.3 under no_jpp (the paired CI of no_rand - no_jpp excluding 0), on both models; "
          "if the probe reads the attribute at no layer at the bridge token, the same at the last token")  # fmt: skip
RULE_B = ("the recall's retrieval runs through the bridge token's late MLPs if recall accuracy falls >= 0.4 under "
          "bridge_late while lookup accuracy stays within 0.1, and both controls stay within 0.1 for both readers")  # fmt: skip


# ---- items (tokenizer only) ---------------------------------------------------------------------------------------


def probe_layers(layer: int, n_layers: int) -> list[int]:
    """L, L + 2, ..., and the last block (n_layers - 1) whether or not the step lands on it."""
    out = list(range(layer, n_layers, 2))
    return out if out[-1] == n_layers - 1 else [*out, n_layers - 1]


def main_scenes(src: Path, layer: int) -> dict[str, dict[str, dict[str, int]]]:
    """The main-test run's chat items at the layer (the scenes with a whole-arm read, in the run's order) with, per
    scene, reader and arm, its stored switch under the whole and no_part (J++ k = 25 signed) arms."""
    scenes: dict[str, dict[str, dict[str, int]]] = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] != RENDERING or r["layer"] != layer:
            continue
        if r["arm"] == "whole":
            scenes.setdefault(r["scene"], {"whole": {}, "no_jpp": {}})["whole"][r["reader"]] = r["switched"]
        elif r["arm"] == "no_part" and (r["dict"], r["k"], r["omp"]) == X.MAIN:
            scenes.setdefault(r["scene"], {"whole": {}, "no_jpp": {}})["no_jpp"][r["reader"]] = r["switched"]
    return scenes


def rebuild(tok, set_name: str) -> list[dict]:
    """Every chat scene of the set as X0 builds it (alt = the generator's cf); X0's module settings restored after."""
    old = X.ALT, X.RENDERINGS
    X.ALT, X.RENDERINGS = "cf", (RENDERING,)
    try:
        cases, _ = X.build_cases(tok, set_name)
    finally:
        X.ALT, X.RENDERINGS = old
    return cases


def person_of(case: dict) -> tuple[str, str]:
    """The asked person and their pick sentence in the context ('<person> picked the <item>.')."""
    from scripts import statement_positions as SP

    st = SP.tasks_statements({"id": case["scene"], "context": case["context"], "bridge": case["bridge"],
                              "cf_bridge": case["cf_bridge"], "question": case["readers"][X.LOOKUP]["question"]})  # fmt: skip
    return st["holder"], st["bind_bridge"]


def person_position(tok, text: str, context: str, case: dict, offsets: list) -> dict:
    """The asked person's token in the rendered O prompt: the last token overlapping the name in the asked pick sentence
    (the name's tokens listed beside it)."""
    from scripts import statement_positions as SP

    person, sent = person_of(case)
    assert text.count(context) == 1, "the context is not once in the prompt"
    w0 = text.index(context) + SP.find_sentence(context, sent)
    toks = SP.tokens_in(offsets, w0, w0 + len(person))
    assert toks, f"{case['scene']}: no token overlaps the person's name"
    assert max(toks) < case["pos"], f"{case['scene']}: the person's tokens {toks} are not before the bridge"
    return {"person": person, "sentence": sent, "tokens": toks, "pos": toks[-1], "span": [w0, w0 + len(person)]}


def select(tok, run: str, layer: int) -> tuple[list[dict], list[dict], dict]:
    """(the main items in the run's order, every chat scene of the set as training cases, counts). Each main item: the
    case, both readers' rendered O prompts, the bridge and person positions, the attribute labels (O's and S's recall
    answers) and the run's stored switches."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T

    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt", "cf") == "cf", f"{run}: alt {m.get('alt')!r}, not the main test's cf"
    assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
    stored = main_scenes(src, layer)
    assert stored, f"{run}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    cases = rebuild(tok, m["set"])
    by_scene = {c["scene"]: c for c in cases}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    for c in cases:
        c["label"] = c["readers"][X.RECALL]["answer"]  # the bridge item's number in its domain (animals: legs)
    out, n_person = [], collections.Counter()
    for scene in stored:
        c = by_scene[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {run}"
        texts, offsets = {}, {}
        for w in X.READERS:
            rd = c["readers"][w]
            texts[w] = X.render(tok, by_id[rd["id"]], RENDERING, c["context"])
            enc = raw_encoding(tok, texts[w], offsets=True)
            assert enc["input_ids"] == rd["ids"]["org"], f"{scene} {w}: the rendered prompt's ids differ"
            offsets[w] = enc["offset_mapping"]
        person = person_position(tok, texts[X.LOOKUP], c["context"], c, offsets[X.LOOKUP])
        n_person[len(person["tokens"])] += 1
        o_off = offsets[X.LOOKUP]
        out.append({
            "scene": scene, "entity": c["bridge"], "cf_entity": c["cf_bridge"], "domain": c["domain"],
            "upstream": c["upstream"], "pos": c["pos"], "space": c["space"], "read_suffix": tok.decode(c["space"]),
            "context": c["context"], "cf_context": c["cf_context"], "label": c["label"],
            "cf_label": c["readers"][X.RECALL]["cf_answer"], "person": person,
            "marks": {"bridge": [list(o_off[c["pos"]])], "person": [list(o_off[p]) for p in person["tokens"]]},
            "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b",
                                                             "ids")}, "text": {"org": texts[w]}} for w in X.READERS},
            "stored": {k: stored[scene][k] for k in ("whole", "no_jpp")},
        })  # fmt: skip
    counts = {"main_run": run, "set": m["set"], "layer": layer, "items": len(out),
              "entities": len({it["entity"] for it in out}),
              "domains": dict(collections.Counter(it["domain"] for it in out)),
              "person_tokens": {str(k): v for k, v in sorted(n_person.items())},
              "training_scenes": {d: {"scenes": sum(c["domain"] == d for c in cases),
                                      "entities": len({c["bridge"] for c in cases if c["domain"] == d}),
                                      "classes": sorted({c["label"] for c in cases if c["domain"] == d})}
                                  for d in sorted({c["domain"] for c in cases})}}  # fmt: skip
    return out, cases, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def marked(text: str, spans: list[tuple[int, int, str]]) -> str:
    """The text with ⟦label:…⟧ around each span (no overlaps); a span's leading whitespace stays outside."""
    out, last = [], 0
    for a, b, label in sorted(spans):
        while a < b and text[a].isspace():
            a += 1
        assert a >= last, f"span ({a}, {b}) overlaps the previous one"
        out += [text[last:a], f"⟦{label}:", text[a:b], "⟧"]
        last = b
    out.append(text[last:])
    return "".join(out)


def item_marked(it: dict, reader: str) -> str:
    spans = [(a, b, role) for role in ("bridge", "person") for a, b in it["marks"][role]]
    return marked(it["readers"][reader]["text"]["org"] + it["read_suffix"], spans)


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, _, counts = select(tok, MAIN_RUN[pins.TARGET], layer)
    counts.update(target=pins.TARGET, probe_layers=probe_layers(layer, pins.N_LAYERS),
                  b_layers={a: layers_b(a, layer, pins.N_LAYERS) for a in ARMS_B if a != "none"})  # fmt: skip
    it = items[example_indices(len(items), 1)[0]]
    counts["example"] = {"scene": it["scene"], "bridge": it["entity"], "changed": it["cf_entity"],
                         "labels": [it["label"], it["cf_label"]], "person": it["person"]["person"],
                         "recall_O_marked": item_marked(it, X.RECALL)}  # fmt: skip
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


# ---- manifests ----------------------------------------------------------------------------------------------------


def manifest(name: str, why: str, design: str, extra: dict) -> dict:
    from bridge_jspace.utils import git_state

    src = X.RESULTS / MAIN_RUN[pins.TARGET]
    return {"exp": EXP, "run": name, "why": why, "design": design, "test": "48.2",
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
            "switches": switches(), "code": git_state(), "lens": X.lens_record(), "spec": "jobs/c3/batch48.yaml (48.2)",
            "question": f"{QUESTION} ({PREDICTIONS})", "main_run": MAIN_RUN[pins.TARGET],
            "layer": X.PREDICTED[pins.TARGET], "n_layers": pins.N_LAYERS,
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                       for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")},
            "items_rule": "the main-test X0 run's chat items at L (every scene with a whole-arm read), rebuilt with "
                          "X.build_cases (alt = cf) and checked against the run's ids",
            "read": "X0's chat read: the prompt with a digit's space token appended; the top token",
            "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer",
            **extra}  # fmt: skip


# ---- design A: GPU ------------------------------------------------------------------------------------------------


def jpp_and_random(x, jdic, basis, k: int = X.K_MAIN):
    """The row's J++ part (signed OMP, k atoms; X.fit as X0) and a random part of the same share (X0's random
    subspace), and that share. x: [1, d]."""
    from scripts import statement_positions as SP

    x = x.float()
    part = X.fit(jdic, x, k, "signed").float()
    share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    return part, SP.random_subspace_part(x, share, basis).float(), share


def read_at(model, ids: list[int], edits: dict, layers: tuple[int, ...], pos: int):
    """One forward of ids (the read prompt) under `edits`: the final logits and, per recorded layer, the states at
    the bridge token and at the last token (fp32, CPU numpy)."""
    import torch

    logits, rec = model.run(torch.tensor([ids], device=model.device), edits, record=layers)
    return logits, {la: np.stack([rec[la][pos].float().cpu().numpy(), rec[la][-1].float().cpu().numpy()])
                    for la in layers}  # fmt: skip


def stage_run_a(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.2 renders the main test's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"48.2 runs on {sorted(MAIN_RUN)}, not {target}"
    layer, n_layers = X.PREDICTED[target], pins.N_LAYERS
    layers = tuple(probe_layers(layer, n_layers))
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, why, "A", {
        "probe_layers": list(layers), "positions": {"bridge": "the asked person's bridge token",
                                                    "last": "the recall's read position (the appended space token)"},
        "arms": ARM_TEXT_A, "k": X.K_MAIN, "omp": "signed",
        "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at the J++ part's share of ||Δ||^2",
        "states": "the recall reader's prompt (+ space) under each arm, at the probe layers, bridge and last token, fp16",
        "training": "every chat scene of the set, O unedited: the same states, labels = the bridge item's number "
                    "(animals: legs); one probe per domain; the rule's domain is animals (the others have one entity "
                    "per class: descriptive)", "rule_domain": RULE_DOMAIN,
        "probe": {"kind": "one-hot ridge on standardized states (x0_probe.ridge), penalty by entity-held-out CV",
                  "folds": K_FOLDS, "split_seed": SPLIT_SEED, "penalties": list(P.RELS)},
        "fraction": "(m(arm) - m(O)) / (m(S) - m(O)) clipped to [0, 1], m = score(changed class) - score(original "
                    "class) from the probe trained without the original's and the changed item's entity folds; items "
                    "with a non-positive unedited gap are not read",
        "branch": "bridge if the animals probe's held-out accuracy reaches 2x chance at some probed layer, else last",
        "rule": RULE_A, "seeds_more": {"random_subspace": f"{X.SUBSPACE_SEED} + layer", "split": SPLIT_SEED}})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, cases, counts = select(tok, MAIN_RUN[target], layer)
    counts["probe_layers"] = list(layers)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    X.write_jsonl(out / "training.jsonl", [{"scene": c["scene"], "entity": c["bridge"], "domain": c["domain"],
                                            "label": c["label"], "pos": c["pos"]} for c in cases])  # fmt: skip
    print(json.dumps({k: v for k, v in counts.items() if k != "training_scenes"}, ensure_ascii=False), flush=True)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    basis = None
    examples = set(example_indices(len(items)))
    # training states: every chat scene, O unedited, the recall's read prompt
    train = np.zeros((len(cases), len(layers), 2, jdic.shape[1]), dtype=np.float16)
    with torch.no_grad():
        for i, c in enumerate(progress(cases, f"48.2A training states at L{layer}.. (scene)")):
            _, st = read_at(model, c["readers"][X.RECALL]["ids"]["org"] + c["space"], {}, layers, c["pos"])
            for j, la in enumerate(layers):
                train[i, j] = st[la]
    np.savez_compressed(out / "states_train.npz", h=train, scene=np.array([c["scene"] for c in cases]),
                        layers=np.array(layers))  # fmt: skip
    del train
    # main items: O, S and the three edited arms; states from the recall's forward, reads from both readers
    main = np.zeros((len(items), len(ARMS_A), len(layers), 2, jdic.shape[1]), dtype=np.float16)
    rows, norms, greedy = [], [], []
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"48.2A arms at L{layer} (item)")):
            pos, space = it["pos"], it["space"]
            rc = it["readers"][X.RECALL]
            h = {v: model.run(torch.tensor([rc["ids"][v] + space], device=model.device), record=(layer,))[1][layer]
                 for v in ("org", "alt")}  # fmt: skip
            whole = (h["alt"][pos] - h["org"][pos]).float().to(jdic.device)[None]
            if basis is None:
                basis = SP.random_basis(whole.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer))
                basis = basis.to(jdic.device)
            part, rand, share = jpp_and_random(whole, jdic, basis)
            rshare = rand.norm(dim=-1) ** 2 / (whole.norm(dim=-1) ** 2).clamp_min(1e-30)
            norms.append({"scene": it["scene"], "whole_norm": round(float(whole.norm()), 4),
                          "jpp_share": round(float(share[0]), 5), "rand_share": round(float(rshare[0]), 5)})  # fmt: skip
            edits = {"none": {}, "alt": {}, "whole": {layer: AddRows(whole, [pos])},
                     "no_jpp": {layer: AddRows(whole - part, [pos])}, "no_rand": {layer: AddRows(whole - rand, [pos])}}  # fmt: skip
            assert tuple(edits) == ARMS_A
            for w, rd in it["readers"].items():
                for a, (arm, ed) in enumerate(edits.items()):
                    ids = rd["ids"]["alt" if arm == "alt" else "org"] + space
                    logits, st = read_at(model, ids, ed, layers, pos)
                    if w == X.RECALL:
                        for j, la in enumerate(layers):
                            main[i, a, j] = st[la]
                    top = int(logits.argmax())
                    rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                                 "arm": arm, **X.read_row(logits, rd, digits), "right": int(top == rd["tok_A"]),
                                 "top_text": tok.decode([top])})  # fmt: skip
                if i in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, [edits[a] for a in EDIT_ARMS])
                    greedy += [{"scene": it["scene"], "reader": w, "arm": arm, "greedy": t}
                               for arm, t in zip(EDIT_ARMS, texts, strict=True)]  # fmt: skip
    np.savez_compressed(out / "states_main.npz", h=main, scene=np.array([it["scene"] for it in items]),
                        arms=np.array(ARMS_A), layers=np.array(layers))  # fmt: skip
    X.write_jsonl(out / "reads.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote the states; fitting the probes (CPU)", flush=True)
    del model, jdic
    torch.cuda.empty_cache()
    analyse_a(name)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- design A: probes (CPU) ---------------------------------------------------------------------------------------


def entity_folds(entities: list[str], k: int = K_FOLDS, seed: int = SPLIT_SEED) -> dict[str, int]:
    """Fold per entity: the entities shuffled (seed), each dealt in that order to the fold with the fewest items so far
    (ties: the lowest fold); every item of an entity shares its fold."""
    count = collections.Counter(entities)
    order = sorted(count)
    random.Random(seed).shuffle(order)
    size = [0] * k
    out = {}
    for e in order:
        f = min(range(k), key=lambda i: (size[i], i))
        out[e] = f
        size[f] += count[e]
    return out


def ridge_scores(xtr: np.ndarray, ytr: list, xte: np.ndarray, rel: float) -> tuple[list, np.ndarray]:
    """x0_probe.ridge's one-hot ridge (standardized features, dual form) at one relative penalty: the classes and the
    test rows' class scores [n_te, classes] (the regression's estimate of each class indicator; argmax = P.ridge)."""
    classes = sorted(set(ytr), key=str)
    mu, sd = xtr.mean(0), xtr.std(0)
    sd[sd < 1e-6] = 1.0
    a, b = (xtr - mu) / sd, (xte - mu) / sd
    y = np.array([[v == c for c in classes] for v in ytr], dtype=float)
    ym = y.mean(0)
    s, u = np.linalg.eigh(a @ a.T)
    s = np.clip(s, 0.0, None)
    alpha = u @ ((u.T @ (y - ym)) / (s + rel * s.sum() / len(s))[:, None])
    return classes, (b @ a.T) @ alpha + ym


class Probe:
    """One domain's attribute probe at one layer and position: the penalty chosen by out-of-fold accuracy over the
    entity folds, its out-of-fold predictions, and fold-held-out models for reading other states."""

    def __init__(self, x: np.ndarray, y: list, fold: list[int]):
        self.x, self.y, self.fold = x, y, np.asarray(fold)
        self.classes = sorted(set(y), key=str)
        acc = np.zeros(len(P.RELS))
        for f in sorted(set(fold)):
            tr, te = np.flatnonzero(self.fold != f), np.flatnonzero(self.fold == f)
            for j, pred in enumerate(P.ridge(x[tr], [y[i] for i in tr], x[te], P.RELS)):
                acc[j] += sum(p == y[i] for p, i in zip(pred, te, strict=True))
        self.rel = P.RELS[max(range(len(P.RELS)), key=lambda j: (acc[j], j))]  # ties to the larger penalty
        self.oof: list = [None] * len(y)
        for f in sorted(set(fold)):
            tr, te = np.flatnonzero(self.fold != f), np.flatnonzero(self.fold == f)
            for i, p in zip(te, P.ridge(x[tr], [y[i] for i in tr], x[te], (self.rel,))[0], strict=True):
                self.oof[i] = p
        self.held_out = float(np.mean([p == t for p, t in zip(self.oof, y, strict=True)]))

    def scores(self, h: np.ndarray, without: frozenset) -> tuple[list, np.ndarray]:
        """Class scores of the rows of h from the model trained on the folds not in `without`."""
        tr = np.flatnonzero(~np.isin(self.fold, sorted(without)))
        assert len(tr), f"no training items outside folds {sorted(without)}"
        return ridge_scores(self.x[tr], [self.y[i] for i in tr], h, self.rel)


def margin(classes: list, scores: np.ndarray, changed: str, original: str) -> np.ndarray:
    """m(h) = score(changed class) - score(original class) per row; a class the probe never saw scores 0."""
    col = lambda c: scores[:, classes.index(c)] if c in classes else np.zeros(scores.shape[0])  # noqa: E731
    return col(changed) - col(original)


def fraction(m_arm: float, m_o: float, m_s: float) -> float | None:
    """The fraction of the way from O to S, clipped to [0, 1]; None when the unedited gap is not positive."""
    gap = m_s - m_o
    if gap <= 0:
        return None
    return float(min(1.0, max(0.0, (m_arm - m_o) / gap)))


def analyse_a(name: str) -> Path:
    """Fit the probes on the training states and read the main items: probe.json (held-out accuracies per domain,
    layer and position; pooled; the branch) and readings.jsonl (per item, position, layer and arm: m and the fraction)."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    layers = m["probe_layers"]
    zt, zm = np.load(src / "states_train.npz"), np.load(src / "states_main.npz")
    assert zt["layers"].tolist() == layers == zm["layers"].tolist()
    assert zm["arms"].tolist() == list(ARMS_A)
    train = X.read_jsonl(src / "training.jsonl")
    items = X.read_jsonl(src / "cases.jsonl")
    assert [t["scene"] for t in train] == [str(s) for s in zt["scene"]]
    assert [it["scene"] for it in items] == [str(s) for s in zm["scene"]]
    fold_of = entity_folds([t["entity"] for t in train])
    domains = sorted({t["domain"] for t in train})
    acc_rows, readings = [], []
    for pi, position in enumerate(POSITIONS):
        for li, la in enumerate(layers):
            for d in domains:
                idx = [i for i, t in enumerate(train) if t["domain"] == d]
                x = zt["h"][idx, li, pi].astype(np.float64)
                y = [train[i]["label"] for i in idx]
                probe = Probe(x, y, [fold_of[train[i]["entity"]] for i in idx])
                row_of = {
                    train[i]["scene"]: r for r, i in enumerate(idx)
                }  # the item's row in the domain's training set
                chance = 1 / len(probe.classes)
                ents = {train[i]["entity"] for i in idx}
                acc_rows.append({"position": position, "layer": la, "domain": d, "n": len(idx),
                                 "entities": len(ents), "classes": len(probe.classes),
                                 "one_entity_per_class": len(ents) == len(probe.classes),
                                 "chance": round(chance, 4), "held_out": round(probe.held_out, 4),
                                 "readable": probe.held_out >= READABLE_X * chance - EPS, "penalty": probe.rel})  # fmt: skip
                for k, it in enumerate(items):
                    if it["domain"] != d:
                        continue
                    assert it["scene"] in row_of, f"{it['scene']}: a main item outside the training scenes"
                    without = frozenset(fold_of[e] for e in (it["entity"], it["cf_entity"]) if e in fold_of)
                    classes, sc = probe.scores(zm["h"][k, :, li, pi].astype(np.float64), without)
                    ms = margin(classes, sc, it["cf_label"], it["label"])
                    m_by = dict(zip(ARMS_A, ms.tolist(), strict=True))
                    readings.append({"scene": it["scene"], "entity": it["entity"], "domain": d, "position": position,
                                     "layer": la, "held_out_folds": sorted(without),
                                     "oof_right": int(probe.oof[row_of[it["scene"]]] == it["label"]),
                                     "m": {a: round(v, 5) for a, v in m_by.items()},
                                     "gap": round(m_by["alt"] - m_by["none"], 5),
                                     "fraction": {a: fraction(m_by[a], m_by["none"], m_by["alt"]) for a in EDIT_ARMS}})  # fmt: skip
    readable = {p: [r["layer"] for r in acc_rows if r["position"] == p and r["domain"] == RULE_DOMAIN and r["readable"]]
                for p in POSITIONS}  # fmt: skip
    branch = "bridge" if readable["bridge"] else "last"
    blob = {"run": name, "layers": layers, "positions": list(POSITIONS), "rule_domain": RULE_DOMAIN, "folds": fold_of,
            "accuracy": acc_rows, "readable_layers": readable, "branch": branch,
            "branch_why": (f"the bridge token's {RULE_DOMAIN} probe reads the attribute (held-out >= 2x chance) at "
                           f"layers {readable['bridge']}" if branch == "bridge" else
                           f"the bridge token's {RULE_DOMAIN} probe is under 2x chance at every layer: rule A's "
                           "fallback, the last token")}  # fmt: skip
    (src / "probe.json").write_text(json.dumps(blob, indent=1) + "\n")
    X.write_jsonl(src / "readings.jsonl", readings)
    print(json.dumps({k: blob[k] for k in ("readable_layers", "branch", "branch_why")}), flush=True)
    return src


# ---- design B: GPU ------------------------------------------------------------------------------------------------


def layers_b(arm: str, layer: int, n_layers: int) -> list[int]:
    """The arm's ablated layers: l > L for the late arms, l <= L / 2 (floor) for bridge_early."""
    if arm in ("bridge_late", "person_late"):
        return list(range(layer + 1, n_layers))
    assert arm == "bridge_early", arm
    return list(range(0, layer // 2 + 1))


def mlp_write_module(block) -> tuple[str, Any]:
    """The module whose output is the block's MLP write to the residual: `post_feedforward_layernorm` where the block
    scales its MLP output before the add (Muse, Gemma-style), else `mlp` (Qwen3.5: full-attention and Gated DeltaNet
    blocks alike)."""
    assert hasattr(block, "mlp"), f"{type(block).__name__} has no mlp"
    name = "post_feedforward_layernorm" if hasattr(block, "post_feedforward_layernorm") else "mlp"
    return name, getattr(block, name)


def mlp_record(model) -> dict:
    """What the ablation hooks: per block the hooked module's name and class, and the block's kind."""
    from bridge_jspace import knockout as K

    blocks = list(model.layers)
    kinds = [K.layer_kind(b) for b in blocks]
    names = [mlp_write_module(b)[0] for b in blocks]
    return {"module": dict(collections.Counter(names)), "mlp_class": sorted({type(b.mlp).__name__ for b in blocks}),
            "hooked_class": sorted({type(mlp_write_module(b)[1]).__name__ for b in blocks}),
            "block_kinds": dict(collections.Counter(kinds)), "kinds": kinds}  # fmt: skip


@contextlib.contextmanager
def mlp_hooks(model, layers: list[int], fn):
    """Forward hooks on the MLP write modules of `layers`: fn(layer, out) -> a replacement for the module's output
    [B, S, d], or None to leave it."""
    handles = []
    for la in layers:
        _, mod = mlp_write_module(model.layers[la])
        handles.append(mod.register_forward_hook(lambda _m, _a, out, la=la: fn(la, out)))
    try:
        yield
    finally:
        for h in handles:
            h.remove()


def recorder(store: dict, positions: dict[str, int], prompt_len: int):
    """A hook fn that records each layer's MLP write at the roles' positions (fp32, CPU) on the prompt's forward."""

    def fn(la: int, out):
        if out.shape[1] != prompt_len:
            return None
        store[la] = {role: out[0, p].float().cpu() for role, p in positions.items()}
        return None

    return fn


def ablator(means: dict[int, Any], pos: int, prompt_len: int):
    """A hook fn that replaces each hooked layer's MLP write at `pos` by its scene-mean on the prompt's forward (decoding
    steps, shorter, pass through)."""

    def fn(la: int, out):
        if out.shape[1] != prompt_len:
            return None
        out = out.clone()
        out[:, pos] = means[la].to(out.device, out.dtype)
        return out

    return fn


def stage_run_b(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.2 renders the main test's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MAIN_RUN, f"48.2 runs on {sorted(MAIN_RUN)}, not {target}"
    layer, n_layers = X.PREDICTED[target], pins.N_LAYERS
    arm_layers = {a: layers_b(a, layer, n_layers) for a in ARMS_B if a != "none"}
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    model = load_model()
    rec = mlp_record(model)
    m = manifest(name, why, "B", {
        "arms": ARM_TEXT_B, "arm_layers": arm_layers, "module_counts": {a: len(v) for a, v in arm_layers.items()},
        "hooked": rec, "mean": "per layer and role, the mean MLP write over the items' unedited O prompts at the role's "
                               "position (bridge: the bridge token; person: the last token of the asked person's name "
                               "in the asked pick sentence)",
        "ablation": "a forward hook on the block's MLP write module replaces its output at the position by the mean, "
                    "on the prompt's forward only",
        "accuracy": "the share of items whose top token at the read is O's answer", "rule": RULE_B})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    tok = model.tokenizer
    items, _, counts = select(tok, MAIN_RUN[target], layer)
    counts.update(arm_layers=arm_layers, hooked=rec)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps({k: v for k, v in counts.items() if k not in ("training_scenes", "hooked")}), flush=True)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    every = list(range(n_layers))
    sums: dict[int, dict[str, Any]] = {}
    with torch.no_grad():
        for it in progress(items, "48.2B scene means of the MLP writes (item)"):
            ids = torch.tensor([it["readers"][X.LOOKUP]["ids"]["org"] + it["space"]], device=model.device)
            store: dict = {}
            with mlp_hooks(
                model, every, recorder(store, {"bridge": it["pos"], "person": it["person"]["pos"]}, ids.shape[1])
            ):
                model.run(ids)
            assert len(store) == n_layers, f"recorded {len(store)} of {n_layers} MLP writes"
            for la, by_role in store.items():
                for role, v in by_role.items():
                    sums.setdefault(la, {})[role] = sums.get(la, {}).get(role, 0) + v
    means = {la: {role: v / len(items) for role, v in by_role.items()} for la, by_role in sums.items()}
    torch.save({"means": means, "n": len(items), "layers": every}, out / "means.pt")
    role_of = {"bridge_late": "bridge", "person_late": "person", "bridge_early": "bridge"}
    examples = set(example_indices(len(items)))
    rows, greedy = [], []
    with torch.no_grad():
        for i, it in enumerate(progress(items, "48.2B reads under the ablations (item)")):
            for w, rd in it["readers"].items():
                ids = torch.tensor([rd["ids"]["org"] + it["space"]], device=model.device)
                for arm in ARMS_B:
                    if arm == "none":
                        ctx: Any = contextlib.nullcontext()
                    else:
                        role = role_of[arm]
                        pos = it["pos"] if role == "bridge" else it["person"]["pos"]
                        ctx = mlp_hooks(model, arm_layers[arm], ablator({la: means[la][role] for la in arm_layers[arm]},
                                                                         pos, ids.shape[1]))  # fmt: skip
                    with ctx:
                        logits, _ = model.run(ids)
                    if i in examples:
                        text = greedy_ablated(model, it, rd, arm, arm_layers.get(arm, []), means, role_of)
                        greedy.append({"scene": it["scene"], "reader": w, "arm": arm, "greedy": text})
                    top = int(logits.argmax())
                    rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                                 "arm": arm, **X.read_row(logits, rd, digits), "right": int(top == rd["tok_A"]),
                                 "top_text": tok.decode([top])})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


def greedy_ablated(model, it: dict, rd: dict, arm: str, layers: list[int], means: dict, role_of: dict) -> str:
    """The greedy continuation of the reader's O prompt (no space appended) under the arm's ablation (none: no hooks):
    the hooks act on the prompt's forward (its length) and pass the decoding steps through."""
    import torch

    ids = torch.tensor([rd["ids"]["org"]], device=model.device)
    if arm == "none":
        return model.generate_batch(ids, X.GEN_TOKENS, [{}])[0]
    role = role_of[arm]
    pos = it["pos"] if role == "bridge" else it["person"]["pos"]
    with mlp_hooks(model, layers, ablator({la: means[la][role] for la in layers}, pos, ids.shape[1])):
        return model.generate_batch(ids, X.GEN_TOKENS, [{}])[0]


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q48.2 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan:(.*)$", block, re.M)
    return m.group(1).strip() if m else ""


def interval(x: np.ndarray) -> list[float]:
    return [float(v) for v in X.interval(x)]


def layer_numbers(readings: list[dict], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict[str, Any]:
    """One position and layer's readings (one row per item): per edited arm the mean fraction over the items with a
    positive gap, no_rand - no_jpp, with cluster-bootstrap CIs over the original bridge entities (paired)."""
    read = [r for r in readings if r["gap"] > 0]
    out: dict[str, Any] = {"n": len(readings), "n_read": len(read), "entities": len({r["entity"] for r in read})}
    if not read:
        out.update({a: [None, None, None] for a in EDIT_ARMS}, diff=[None, None, None])
        return out
    vals = {a: [r["fraction"][a] for r in read] for a in EDIT_ARMS}
    ents = [r["entity"] for r in read]
    boot = X.resampled_rates(vals, ents, n_boot, seed)
    for a in EDIT_ARMS:
        out[a] = [float(np.mean(vals[a])), *interval(boot[a])]
    out["diff"] = [out["no_rand"][0] - out["no_jpp"][0], *interval(boot["no_rand"] - boot["no_jpp"])]
    return out


def rule_a_layer(num: dict[str, Any]) -> dict[str, Any]:
    """Rule A at one layer (point estimates; the paired CI of no_rand - no_jpp must exclude 0)."""
    if num["n_read"] == 0 or num["whole"][0] is None:
        return {"holds": False, "why": "no item with a positive unedited gap"}
    ok = {"whole >= 0.6": num["whole"][0] >= MOVE_MIN - EPS, "no_rand >= 0.6": num["no_rand"][0] >= MOVE_MIN - EPS,
          "no_jpp <= 0.3": num["no_jpp"][0] <= STAY_MAX + EPS, "CI(no_rand - no_jpp) > 0": num["diff"][1] > 0}  # fmt: skip
    return {"holds": all(ok.values()), "checks": ok}


def model_result_a(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "probe.json").exists():
        target = {r: t for t, r in RUNS_A.items()}.get(run)
        assert target, f"no 48.2A run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS_A.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False, "why": "no probe.json here"}
    m = json.loads((src / "manifest.json").read_text())
    probe = json.loads((src / "probe.json").read_text())
    readings = X.read_jsonl(src / "readings.jsonl")
    layer, branch = m["layer"], probe["branch"]
    tables: dict[str, Any] = {}
    for position in POSITIONS:
        readable = set(probe["readable_layers"][position])
        per_layer = {}
        for la in probe["layers"]:
            mine = [r for r in readings if r["position"] == position and r["layer"] == la]
            num = layer_numbers([r for r in mine if r["domain"] == RULE_DOMAIN], n_boot)
            per_layer[la] = {"readable": la in readable, "in_rule": la in readable and la >= layer + LAYER_FROM,
                             "rule_domain": num, "rule": rule_a_layer(num),
                             "by_domain": {d: layer_numbers([r for r in mine if r["domain"] == d], n_boot)
                                           for d in sorted({r["domain"] for r in mine}) if d != RULE_DOMAIN}}  # fmt: skip
        tables[position] = per_layer
    in_rule = [la for la, v in tables[branch].items() if v["in_rule"]]
    holds = bool(in_rule) and all(tables[branch][la]["rule"]["holds"] for la in in_rule)
    why = (f"the {branch} token; layers in the rule {in_rule}: "
           + "; ".join(f"L{la} " + ("holds" if tables[branch][la]["rule"]["holds"] else "fails") for la in in_rule)
           if in_rule else f"the {branch} token: no readable layer >= L + {LAYER_FROM}")  # fmt: skip
    label = ("J++ keys the enrichment at the bridge token" if holds and branch == "bridge" else
             "J++ keys the enrichment at the last token" if holds else
             "not readable" if not in_rule else f"does not hold at the {branch} token")  # fmt: skip
    return {"run": run, "target": m["model"]["target"], "layer": layer, "status": "tested", "branch": branch,
            "branch_why": probe["branch_why"], "holds": holds, "label": label,
            "why": why, "layers_in_rule": in_rule, "tables": tables, "accuracy": probe["accuracy"],
            "plan": json.loads((src / "plan.json").read_text()),
            "checks": agreement_a(X.read_jsonl(src / "cases.jsonl"), X.read_jsonl(src / "reads.jsonl"))}  # fmt: skip


def agreement_a(items: list[dict], rows: list[dict]) -> dict[str, Any]:
    """Descriptive: the rerun whole and no_jpp arms' switches against the main-test run's stored ones."""
    by = {(r["scene"], r["reader"], r["arm"]): int(r["switched"]) for r in rows}
    out = {}
    for w in X.READERS:
        for arm in ("whole", "no_jpp"):
            pairs = [(by[(it["scene"], w, arm)], it["stored"][arm][w]) for it in items if w in it["stored"][arm]]
            out[f"{READER_NAME[w]} {arm} vs the main run's stored"] = {
                "n": len(pairs), "agree": sum(a == b for a, b in pairs), "rerun": sum(a for a, _ in pairs),
                "stored": sum(b for _, b in pairs)}  # fmt: skip
    return out


def accuracy_table(rows: list[dict], reader: str) -> tuple[list[str], dict[str, list[int]]]:
    """One reader's items' entities and each arm's 0/1 right per item; every item must have every arm."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["right"])
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in ARMS_B if (s, a) not in by]
    assert not missing, f"{reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    return [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in ARMS_B}


def numbers_b(right: dict[str, list[int]], entities: list[str], n_boot: int = X.N_BOOT,
              seed: int = X.BOOT_SEED) -> dict[str, Any]:  # fmt: skip
    """Each arm's accuracy and its drop from none (none - arm), with paired cluster-bootstrap CIs over entities."""
    n = len(entities)
    hits = {a: int(sum(right[a])) for a in ARMS_B}
    boot = X.resampled_rates(right, entities, n_boot, seed)
    return {"n": n, "entities": len(set(entities)), "hits": hits,
            "accuracy": {a: [hits[a] / n, *interval(boot[a])] for a in ARMS_B},
            "drop": {a: [(hits["none"] - hits[a]) / n, *interval(boot["none"] - boot[a])] for a in ARMS_B[1:]}}  # fmt: skip


def rule_b(recall: dict[str, Any], lookup: dict[str, Any]) -> dict[str, Any]:
    """Rule B on one model (point estimates, EPS at the bars)."""
    d = lambda r, a: r["drop"][a][0]  # noqa: E731
    ok = {"recall falls >= 0.4 (bridge_late)": d(recall, "bridge_late") >= FALL_MIN - EPS,
          "lookup within 0.1 (bridge_late)": abs(d(lookup, "bridge_late")) <= WITHIN + EPS}  # fmt: skip
    for a in ("person_late", "bridge_early"):
        for w, r in (("recall", recall), ("lookup", lookup)):
            ok[f"{w} within 0.1 ({a})"] = abs(d(r, a)) <= WITHIN + EPS
    holds = all(ok.values())
    note = (
        ""
        if ok["recall falls >= 0.4 (bridge_late)"]
        else "; the recall survives: the attribute is fetched at the last token (design A at the last token covers it)"
    )
    return {
        "holds": holds,
        "checks": ok,
        "why": ", ".join(f"{k}: {'yes' if v else 'no'}" for k, v in ok.items()) + note,
    }


def model_result_b(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS_B.items()}.get(run)
        assert target, f"no 48.2B run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS_B.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False, "why": "no outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    readers = {}
    for w in X.READERS:
        entities, right = accuracy_table(rows, w)
        readers[READER_NAME[w]] = numbers_b(right, entities, n_boot)
    r = rule_b(readers["recall"], readers["lookup"])
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "status": "tested", **r,
            "readers": readers, "module_counts": m["module_counts"], "hooked": m["hooked"],
            "plan": {k: v for k, v in json.loads((src / "plan.json").read_text()).items() if k != "hooked"}}  # fmt: skip


def batch_label(models: list[dict]) -> str:
    """Holds once every model holds; does not hold once a tested model fails; else pending."""
    if models and all(m["status"] == "tested" and m["holds"] for m in models):
        return "holds"
    if any(m["status"] == "tested" and not m["holds"] for m in models):
        return "does not hold"
    return "pending"


def fmt(v: list) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def with_pending(models: list[dict], runs: dict[str, str], design: str) -> list[dict]:
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    assert set(targets) <= set(runs), f"48.2{design} runs on {sorted(runs)}, not {sorted(set(targets) - set(runs))}"
    return models + [{"run": f"({runs[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
                     for t in runs if t not in targets]  # fmt: skip


def example_lines_a(run: str, res: dict, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "reads.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    readings = collections.defaultdict(dict)
    for r in X.read_jsonl(src / "readings.jsonl"):
        readings[(r["scene"], r["position"])][r["layer"]] = r
    branch = res["branch"]
    lines = [
        f"## {run} (design A, the {branch} token): {min(k, len(items))} random items of {len(items)} (seed {seed})",
        "",
    ]
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} (attribute {it['label']}) → "
                  f"{it['cf_entity']} (attribute {it['cf_label']})", "", "```", item_marked(it, X.RECALL), "```", "",
                  "Reads (top token; switched = S's answer, right = O's):", "",
                  "| arm | recall top | switched | right | greedy | lookup top | switched | right |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for arm in ARMS_A:
            rc, lk = reads[(it["scene"], X.RECALL, arm)], reads[(it["scene"], X.LOOKUP, arm)]
            lines.append(f"| {arm} | {rc['top_text']!r} | {rc['switched']} | {rc['right']} | "
                         f"{greedy.get((it['scene'], X.RECALL, arm))!r} | {lk['top_text']!r} | {lk['switched']} | "
                         f"{lk['right']} |")  # fmt: skip
        lines += ["", f"Probe at the {branch} token, m = score(changed class) − score(original class), and the fraction "
                  "of the way (clipped; − when the unedited gap is not positive):", "",
                  "| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |", "|---|---|---|---|---|---|---|"]  # fmt: skip
        for la, r in sorted(readings[(it["scene"], branch)].items()):
            f_ = {a: "−" if r["fraction"][a] is None else f"{r['fraction'][a]:.2f}" for a in EDIT_ARMS}
            lines.append(f"| {la} | {r['m']['none']:.3f} | {r['m']['alt']:.3f} | {r['gap']:.3f} | {f_['whole']} | "
                         f"{f_['no_jpp']} | {f_['no_rand']} |")  # fmt: skip
        lines.append("")
    return lines


def example_lines_b(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {run} (design B): {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [
            f"### {it['scene']} ({it['domain']}): bridge {it['entity']}, asked person {it['person']['person']}",
            "",
        ]
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}", "", "```", item_marked(it, w),
                      "```", "", "| arm | what | top token | right | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            for arm in ARMS_B:
                r = reads[(it["scene"], w, arm)]
                lines.append(f"| {arm} | {ARM_TEXT_B[arm]} | {r['top_text']!r} | {r['right']} | "
                             f"{greedy.get((it['scene'], w, arm))!r} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs_a: list[str], runs_b: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    a = with_pending([model_result_a(r, n_boot) for r in runs_a], RUNS_A, "A")
    b = with_pending([model_result_b(r, n_boot) for r in runs_b], RUNS_B, "B")
    v = {"A": batch_label(a), "B": batch_label(b)}
    out = RESULTS / f"x48_2-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 48.2: why the recall reads J++ — attribute enrichment at the bridge token", "",
             f"Batch 48, test 48.2 (jobs/c3/batch48.yaml; {QUESTION}, Dan: {answer}). The main test's items and arms at "
             f"the layer fixed in advance; cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", f"Rule A (fixed in advance): {RULE_A}.", "", f"Rule B (fixed in advance): {RULE_B}.", "",
             f"**Verdict A: {v['A']}**; **Verdict B: {v['B']}**.", "", "## Design A (probes)", "",
             "| model | run | status | branch | layers in the rule | holds | label |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in a:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | |")
            continue
        lines.append(f"| {m['target']} | {m['run']} | tested | {m['branch']} | {m['layers_in_rule']} | "
                     f"{'yes' if m['holds'] else 'no'} | {m['label']} |")  # fmt: skip
    lines += ["", f"Per layer at the branch position, the rule's domain ({RULE_DOMAIN}: legs; entities held out): "
              "held-out accuracy vs chance, items read (positive unedited gap) and the mean fraction of the way per "
              "arm.", "",
              "| model | layer | in rule | held-out / chance | n read / n | whole | no_jpp | no_rand | no_rand − no_jpp | holds |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in a:
        if m["status"] == "pending":
            continue
        acc = {r["layer"]: r for r in m["accuracy"] if r["position"] == m["branch"] and r["domain"] == RULE_DOMAIN}
        for la, t in sorted(m["tables"][m["branch"]].items(), key=lambda kv: int(kv[0])):
            p = t["rule_domain"]
            lines.append(f"| {m['target']} | {la} | {'yes' if t['in_rule'] else 'no'} | {acc[int(la)]['held_out']:.2f} / "
                         f"{acc[int(la)]['chance']:.2f} | {p['n_read']} / {p['n']} | {fmt(p['whole'])} | "
                         f"{fmt(p['no_jpp'])} | {fmt(p['no_rand'])} | {fmt(p['diff'])} | "
                         f"{'yes' if t['rule']['holds'] else 'no'} |")  # fmt: skip
    lines += ["", "The other domains (descriptive: one entity per class, so an entity-held-out probe sits at 0 by "
              "construction; their readings use the probe's class scores all the same), at the branch position:", "",
              "| model | domain | layer | n read / n | whole | no_jpp | no_rand |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in a:
        if m["status"] == "pending":
            continue
        for la, t in sorted(m["tables"][m["branch"]].items(), key=lambda kv: int(kv[0])):
            for d, p in t["by_domain"].items():
                lines.append(f"| {m['target']} | {d} | {la} | {p['n_read']} / {p['n']} | {fmt(p['whole'])} | "
                             f"{fmt(p['no_jpp'])} | {fmt(p['no_rand'])} |")  # fmt: skip
    lines += ["", "Held-out probe accuracy per domain, position and layer (chance in brackets; * one entity per class):",
              "", "| model | position | domain | per layer: held-out (chance) |", "|---|---|---|---|"]  # fmt: skip
    for m in a:
        if m["status"] == "pending":
            continue
        for position in POSITIONS:
            for d in sorted({r["domain"] for r in m["accuracy"]}):
                rows_ = [r for r in m["accuracy"] if r["position"] == position and r["domain"] == d]
                cells = [f"L{r['layer']} {r['held_out']:.2f} ({r['chance']:.2f})" for r in rows_]
                star = "*" if rows_ and rows_[0]["one_entity_per_class"] else ""
                lines.append(f"| {m['target']} | {position} | {d}{star} | {'; '.join(cells)} |")
    lines += ["", "Checks (descriptive): the rerun whole / no_jpp switches against the main run's stored ones; the "
              "probe's split.", ""]  # fmt: skip
    for m in a:
        if m["status"] == "pending":
            continue
        p = m["plan"]
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): {p['items']} items, {p['entities']} entities, domains "
                     f"{p['domains']}; training scenes {p['training_scenes']}; branch: {m['branch_why']}; checks: "
                     + "; ".join(f"{k}: {c['agree']} of {c['n']} agree (rerun {c['rerun']}, stored {c['stored']})"
                                 for k, c in m["checks"].items()))  # fmt: skip
    lines += ["", "## Design B (MLPs)", "",
              "| model | run | status | n | recall: none | bridge_late drop | lookup: none | bridge_late drop | holds |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in b:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | | | |")
            continue
        rc, lk = m["readers"]["recall"], m["readers"]["lookup"]
        lines.append(f"| {m['target']} | {m['run']} | tested | {rc['n']} | {fmt(rc['accuracy']['none'])} | "
                     f"{fmt(rc['drop']['bridge_late'])} | {fmt(lk['accuracy']['none'])} | "
                     f"{fmt(lk['drop']['bridge_late'])} | {'yes' if m['holds'] else 'no'} |")  # fmt: skip
    lines += ["", "Per reader: accuracy per arm and the drop from none (none − arm).", "",
              "| model | reader | " + " | ".join(ARMS_B) + " | " + " | ".join(f"drop {a}" for a in ARMS_B[1:]) + " |",
              "|---|---|" + "---|" * (2 * len(ARMS_B) - 1)]  # fmt: skip
    for m in b:
        if m["status"] == "pending":
            continue
        for w in ("recall", "lookup"):
            r = m["readers"][w]
            lines.append(f"| {m['target']} | {w} | " + " | ".join(fmt(r["accuracy"][a]) for a in ARMS_B) + " | "
                         + " | ".join(fmt(r["drop"][a]) for a in ARMS_B[1:]) + " |")  # fmt: skip
        lines.append(f"| {m['target']} | | {m['why']} |" + " |" * (2 * len(ARMS_B) - 2))
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT_B.items()) + ".", ""]
    for m in b:
        if m["status"] != "pending":
            lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): modules ablated per arm {m['module_counts']}; "
                         f"hooked {m['hooked']['module']} (classes {m['hooked']['hooked_class']}, blocks "
                         f"{m['hooked']['block_kinds']}); person tokens {m['plan']['person_tokens']}.")  # fmt: skip
    (out / "x48_2.json").write_text(json.dumps({"runs_a": runs_a, "runs_b": runs_b, "dan": answer, "verdict": v,
                                                "A": a, "B": b}, indent=1) + "\n")  # fmt: skip
    (out / "x48_2.md").write_text("\n".join(lines) + "\n")
    ex = ["# 48.2 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, "
          "⟦person:…⟧ the asked person's token(s). UNVERIFIED.", ""]  # fmt: skip
    for m in a:
        if m["status"] != "pending":
            ex += example_lines_a(m["run"], m)
    for m in b:
        if m["status"] != "pending":
            ex += example_lines_b(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run_a", "run_b", "analyse_a", "verdict"])
    ap.add_argument("--name", help="run_a / run_b / analyse_a: the run name (results/x48_enrich/<name>/)")
    ap.add_argument("--runs-a", nargs="*", default=list(RUNS_A.values()), help="verdict: the design A runs")
    ap.add_argument("--runs-b", nargs="*", default=list(RUNS_B.values()), help="verdict: the design B runs")
    ap.add_argument("--why", default="batch 48, test 48.2 (jobs/c3/batch48.yaml; Q48.2)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run_a":
        assert a.name, "run_a needs --name"
        stage_run_a(a.name, a.why)
    elif a.stage == "run_b":
        assert a.name, "run_b needs --name"
        stage_run_b(a.name, a.why)
    elif a.stage == "analyse_a":
        assert a.name, "analyse_a needs --name"
        analyse_a(a.name)
    else:
        stage_verdict(a.runs_a, a.runs_b, a.n_boot)


if __name__ == "__main__":
    main()
