"""x48_bind (batch 48, test 48.3; jobs/c3/batch48.yaml, design and rule fixed in advance; Q48.3 in
predictions/2026-10-28_dan.md): why locker-after lookups ignore the bridge word: forward binding at the locker sentence.

Scenes: each model's main-test run (x0_necessity, two picks swap) and its 45m run (--alt fresh, the clean design), the
scenes of their chat outcomes at the layer fixed in advance (X.PREDICTED), grouped by the asked item's locker sentence
against the asked pick: main test by x0_strata's 'org locker vs asked pick' (after / before); 45m by x45m.group_of
(locker-after / locker-before; mixed scenes feed the descriptive cells only). Only O (the original prompt) is read.

Probe (verdict, CPU): at the locker sentence's item token and at its number token, which person picked this item: a
ridge probe (x0_probe's ridge, standardized features, the penalty by an inner CV) over the scene's three pickers' names
(one-hot over every name in the training rows; the prediction is the best-scoring of the scene's three names, so chance
is 1 / 3), out-of-fold with the sentence's item held out (5 folds, entities shuffled by seed 0). Trained and scored
within each stratum: 'after' sentences (the sentence follows its picker's pick) and 'before' (it precedes it: the
control by construction). The rule's cells are the asked item's sentence in locker-after scenes and in locker-first
scenes; every locker sentence with a picker (the 45m added item has none) is reported beside, and the after-trained
probe read on the before states ('transfer').

Contrast and lens share (run, GPU): mu_name per token = the mean state over the after sentences of the fit half (the
bridge entities split in two by seed 0, balanced on locker-after scenes) whose picker is that name; the contrast for a
write is mu_Iris - mu_Jack (Iris the asked person, Jack the picker of the written item); its J++ share = ||P Delta||^2 /
||Delta||^2 with P the signed OMP fit of k = 25 atoms of the J++ lens at L (X.fit, as X0); beside it the same share of
N_RANDOM_DIRS Gaussian directions (seed RAND_SEED + L).

The write (run): on locker-after scenes of the test half, the written sentence = the first locker sentence in context
order whose item another person picked and which comes after both that person's pick and the asked pick (item and
number one token each, decoding exactly to their text). Arms at L on O: none; the contrast added at the item token
and at the number token (each token its own contrast), s * (mu_Iris - mu_Jack) for s in S_LIST (unit = the contrast's
own norm); a Gaussian vector of the same norm per token (seed RAND_SEED, one draw per scene, s and token). Reads: X0's
chat read, both readers. The lookup's top token classified target (the written item's locker digit) / original (O's
answer) / other; the recall's: target (the written item's attribute number) / original / other, and 'same' where the
written item's attribute equals the bridge's (the move is unreadable there; left out of the move rate).

Rule (fixed in advance, 48.3): "forward binding at the locker sentence, outside the lens" if probe >= 0.85 in
locker-after and <= 0.5 in locker-first; lens share of the person contrast <= 2x the random direction's; the write
sends >= 0.3 of lookups to the written item's locker (random <= 0.05); on both models. As computed: the probe and lens
clauses per token (item, number); a model passes them if they hold at at least one token (both reported); the lens
share = the median over the written contrasts, the random = the mean over the Gaussian directions; the write clause at
some s in S_LIST with its random control at the same s; the batch holds if both models hold. "Does the write move the
recall too": the same bars on the recall's target rate (>= 0.3 at some s, random <= 0.05). Cluster bootstrap over
bridge entities (10,000, seed 0) beside every rate.

SEALED: the run writes per-item outputs only (no probe, no rates). The verdict stage refuses until
predictions/2026-10-28_dan.md holds Dan's Q48.3 answer at HEAD.

uv run python scripts/x48_bind.py plan                                                   # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_bind.py run --name qwen35_9b_x48_bind     # GPU (sealed)
uv run python scripts/x48_bind.py verdict --runs qwen35_9b_x48_bind muse30_x48_bind      # CPU, after Dan's Q48.3
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

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_probe as PR
from scripts import x0_strata as ST
from scripts import x45b_binding as B
from scripts import x45m
from scripts import x45p as P

EXP = "x48_bind"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch48.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q48.3"
MODELS = ("qwen3.5-9b", "muse-glimmer-30b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x48_bind", "muse-glimmer-30b": "muse30_x48_bind"}
# batch 52 C coverage (amendment 2: the 27B fills every gap): run-stage targets beyond the design's; the
# verdict's own model list is unchanged (verdict --coverage reads these runs alone)
COVERAGE_RUNS = {"qwen3.6-27b": "x48_bind_27b"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x48_bind/x48_bind-20261028T113120Z"  # 48.3's rule first scored (the 9B and Muse)
SOURCES = {"main": B.MAIN_RUN, "45m": B.FRESH_RUN}  # item source -> the x0_necessity run per target
RENDERING = "chat"
TOKENS = ("item", "number")
S_LIST = (1.0, 2.0)
ARMS = ("none", "w1", "w2", "r1", "r2")  # the write at s = 1, 2; a random vector of the same norm at s = 1, 2
ARM_TEXT = {"none": "O unedited", "w1": "s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens",
            "w2": "s = 2 (mu_Iris - mu_Jack)", "r1": "a random vector of the s = 1 write's norm, per token",
            "r2": "a random vector of the s = 2 write's norm, per token"}  # fmt: skip
LOOKUP_CLASSES = ("target", "original", "other")
RECALL_CLASSES = ("target", "original", "other", "same")
K_FOLDS, SPLIT_SEED, MIN_FIT = 5, 0, 3  # the probe's folds and the halves (seed 0); a name's mean needs MIN_FIT states
N_RANDOM_DIRS, RAND_SEED = 20, 4803
PROBE_AFTER, PROBE_BEFORE, LENS_FACTOR, WRITE_MIN, RANDOM_MAX = 0.85, 0.5, 2.0, 0.3, 0.05
EPS = 1e-9
RULE = ("forward binding at the locker sentence, outside the lens: probe >= 0.85 in locker-after and <= 0.5 in "
        "locker-first; the person contrast's J++ share (k = 25) <= 2x a random direction's; the write sends >= 0.3 of "
        "lookups to the written item's locker (random <= 0.05); on both models")  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
ASKED_RE = re.compile(r"([A-Z][a-z]+)'s pick")


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def sentences(context: str) -> list[str]:
    """The context's sentences as x0_strata splits them."""
    return [s if s.endswith(".") else s + "." for s in context.split(". ")]


def picks_of(context: str) -> list[dict]:
    """The pick sentences in context order: {person, item, index (among the sentences)}."""
    out = []
    for i, s in enumerate(sentences(context)):
        m = ST.PICK.search(s)
        if m:
            out.append({"person": m.group(1), "item": m.group(2), "index": i})
    return out


def lockers_of(context: str) -> list[dict]:
    """The locker sentences in context order: {k, index, sentence, item, number}."""
    out = []
    for i, s in enumerate(sentences(context)):
        if s.startswith(B.LOCKER_PREFIX):
            m = B.LOCKER_RE.match(s)
            assert m, f"{s!r} is not a locker sentence"
            out.append({"k": len(out), "index": i, "sentence": s, "item": m.group(1), "number": m.group(2)})
    return out


def token_spans(text: str, context: str, lockers: list[dict]) -> list[dict[str, list[int]]]:
    """Per locker sentence, the character spans of its item and of its number in the rendered prompt."""
    spans = B.locker_spans(text, context)
    out = []
    for lk, (a, _) in zip(lockers, spans, strict=True):
        m = B.LOCKER_RE.match(lk["sentence"])
        assert m
        out.append({t: [a + m.span(g)[0], a + m.span(g)[1]] for t, g in (("item", 1), ("number", 2))})
    return out


def group_of(c: dict, source: str) -> str:
    """after / before / mixed: the asked item's locker sentence against the asked pick (main: x0_strata's org locker;
    45m: x45m's grouping, which also needs the added item's sentence on the same side)."""
    if source == "main":
        return ST.features(c)["org locker vs asked pick"]
    return {"locker-before": "before", "locker-after": "after"}.get(x45m.group_of(c), "mixed")


class Dropped(ValueError):
    """A scene left out, with the reason."""


def scene_item(tok, c: dict, source: str, by_id: dict[str, dict]) -> dict:
    """One scene's record: the pickers (the generator's), the asked person, every locker sentence's positions and
    stratum, the write candidate; raises Dropped with the reason."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T

    lk = X.LOOKUP
    item = by_id[c["readers"][lk]["id"]]
    facts = item["scene_facts"]
    ctx = c["context"]
    picks = picks_of(ctx)
    assert {p["person"]: p["item"] for p in picks} == facts["pick"], (
        f"{c['scene']}: the pick sentences are not the generator's picks"
    )
    pick_index = {p["person"]: p["index"] for p in picks}
    picker = {p["item"]: p["person"] for p in picks}
    asked = ASKED_RE.search(c["readers"][lk]["question"]).group(1)  # type: ignore[union-attr]
    assert asked in pick_index, f"{c['scene']}: the question's {asked} has no pick sentence"
    assert facts["pick"][asked] == c["bridge"], f"{c['scene']}: {asked} did not pick {c['bridge']}"
    texts, offsets = {}, {}
    for w in X.READERS:
        rd = c["readers"][w]
        texts[w] = X.render(tok, by_id[rd["id"]], RENDERING, ctx)
        enc = raw_encoding(tok, texts[w], offsets=True)
        assert enc["input_ids"] == rd["ids"]["org"], f"{c['scene']} {w}: the rendered prompt's ids differ"
        offsets[w] = enc["offset_mapping"]
    ids = c["readers"][lk]["ids"]["org"]
    lockers = lockers_of(ctx)
    spans = token_spans(texts[lk], ctx, lockers)
    dom = T.DOMAINS[c["domain"]]
    sents = []
    for lo, sp in zip(lockers, spans, strict=True):
        who = picker.get(lo["item"])
        rec = {**lo, "picker": who, "asked": lo["item"] == c["bridge"], "positions": {}, "exact": {}, "span": sp,
               "stratum": None if who is None else ("after" if lo["index"] > pick_index[who] else "before"),
               "after_asked_pick": lo["index"] > pick_index[asked]}  # fmt: skip
        for t in TOKENS:
            pos = P.token_positions(offsets[lk], sp[t])
            rec["positions"][t] = pos
            rec["exact"][t] = len(pos) == 1 and P.exact(tok, ids, pos, lo[t])
        sents.append(rec)
    mine = [s for s in sents if s["asked"]]
    assert len(mine) == 1, f"{c['scene']}: the asked item has {len(mine)} locker sentences"
    if not all(mine[0]["exact"].values()):
        raise Dropped("the asked item's sentence tokens are not exactly its item and number")
    last = max(p for s in sents for t in TOKENS for p in s["positions"][t])
    if c["readers"][X.RECALL]["ids"]["org"][: last + 1] != ids[: last + 1]:
        raise Dropped("the readers' prompts differ before the last locker token")
    group = group_of(c, source)
    write, why = None, None
    if group == "after":
        cands = [s for s in sents if s["picker"] not in (None, asked) and s["stratum"] == "after"
                 and s["after_asked_pick"]]  # fmt: skip
        ok = [s for s in cands if all(s["exact"].values())]
        if not cands:
            why = "no other person's locker sentence after both picks"
        elif not ok:
            why = "the candidate sentence's tokens are not one token each"
        else:
            s = ok[0]
            write = {"k": s["k"], "item": s["item"], "person": s["picker"], "digit": str(facts["locker"][s["item"]]),
                     "attribute": str(dom.values[s["item"]]), "positions": s["positions"],
                     "same_attribute": str(dom.values[s["item"]]) == c["readers"][X.RECALL]["answer"]}  # fmt: skip
    o_off = offsets[lk]
    marks = {"bridge": [list(o_off[c["pos"]])]}
    if write:
        marks["write"] = [list(sp) for t in TOKENS for sp in B.merged_spans(o_off, write["positions"][t])]
    return {"scene": c["scene"], "source": source, "entity": c["bridge"], "domain": c["domain"], "group": group,
            "numbers": item["numbers"], "asked": {"person": asked, "pick_index": pick_index[asked]},
            "names": [p["person"] for p in picks], "pos": c["pos"], "space": c["space"],
            "read_suffix": tok.decode(c["space"]), "context": ctx, "sentences": sents, "write": write,
            "write_dropped": why, "marks": marks,
            "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "tok_A")},
                            "ids": {"org": c["readers"][w]["ids"]["org"]}, "text": {"org": texts[w]}}
                        for w in X.READERS}}  # fmt: skip


def halves(items: list[dict], seed: int = SPLIT_SEED) -> dict[str, str]:
    """Each bridge entity's half ('A' fits the contrast, 'B' is written on): entities in seeded random order, each to
    the half with fewer locker-after scenes so far (ties to A)."""
    count = collections.Counter(it["entity"] for it in items if it["group"] == "after")
    ents = sorted({it["entity"] for it in items})
    random.Random(seed).shuffle(ents)
    size, out = {"A": 0, "B": 0}, {}
    for e in ents:
        h = "A" if size["A"] <= size["B"] else "B"
        out[e] = h
        size[h] += count.get(e, 0)
    return out


def select(tok, target: str, layer: int) -> tuple[list[dict], dict]:
    """The target's scenes from both sources at the layer, in each run's scene order (main first), with the halves
    and the counts: scenes per source and group, drops, write candidates, names, strata."""
    from scripts import tasks_v2 as T

    out, counts = [], {"target": target, "layer": layer, "runs": {}, "dropped": collections.Counter()}
    for source, runs in SOURCES.items():
        run = runs[target]
        src = X.RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
        assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
        assert m.get("alt", "cf") == B.SOURCES[source], f"{run}: alt {m.get('alt')!r}, not {B.SOURCES[source]!r}"
        items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
        rel = str(items_file.relative_to(pins.REPO_ROOT))
        assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
        scenes, _ = B.stored_reads(run, layer)
        assert scenes, f"{run}: no chat outcomes at layer {layer}"
        old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
        with B.x0_alt(B.SOURCES[source], (RENDERING,)):
            rebuilt = {c["scene"]: c for c in X.build_cases(tok, m["set"])[0]}
        by_id = {it["id"]: it for it in T.load(m["set"])}
        groups: collections.Counter = collections.Counter()
        for scene in scenes:
            c = rebuilt[scene]
            assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
            for w in X.READERS:
                assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
            try:
                it = scene_item(tok, c, source, by_id)
            except Dropped as e:
                counts["dropped"][f"{source}: {e}"] += 1
                continue
            groups[it["group"]] += 1
            out.append(it)
        counts["runs"][source] = {"run": run, "scenes_at_L": len(scenes), "groups": dict(groups)}
    half = halves(out)
    for it in out:
        it["half"] = half[it["entity"]]
    after = [it for it in out if it["group"] == "after"]
    counts.update({
        "dropped": dict(counts["dropped"]), "scenes": len(out), "entities": len(half),
        "halves": {h: sorted(e for e, hh in half.items() if hh == h) for h in ("A", "B")},
        "locker_after": {"scenes": len(after), "A": sum(it["half"] == "A" for it in after),
                         "B": sum(it["half"] == "B" for it in after)},
        "write_candidates_B": sum(it["half"] == "B" and it["write"] is not None for it in after),
        "write_dropped": dict(collections.Counter(it["write_dropped"] for it in after if it["write"] is None)),
        "names": len({n for it in out for n in it["names"]}),
        "strata": dict(collections.Counter(s["stratum"] for it in out for s in it["sentences"] if s["picker"])),
        "numbers": dict(collections.Counter(it["numbers"] for it in out)),
        "exact": dict(collections.Counter(f"{t}: {'one token' if s['exact'][t] else 'not one token'}"
                                          for it in out for s in it["sentences"] for t in TOKENS)),
    })  # fmt: skip
    return out, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def write_items(items: list[dict]) -> list[int]:
    """The indices of the scenes written on: locker-after, half B, with a write candidate (in item order)."""
    return [i for i, it in enumerate(items) if it["group"] == "after" and it["half"] == "B" and it["write"]]


def item_marked(it: dict, reader: str) -> str:
    spans = [(a, b, role) for role in ("bridge", "write") for a, b in it["marks"].get(role, [])]
    return P.marked(it["readers"][reader]["text"]["org"] + it["read_suffix"], spans)


def stage_plan() -> dict:
    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = select(tok, pins.TARGET, layer)
    writes = write_items(items)
    if writes:
        it = items[writes[example_indices(len(writes), 1)[0]]]
        counts["example"] = {"scene": it["scene"], "source": it["source"], "asked": it["asked"], "names": it["names"],
                             "write": it["write"], "lookup_O_marked": item_marked(it, X.LOOKUP)}  # fmt: skip
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def probe_rows(items: list[dict]) -> list[dict]:
    """One row per locker sentence with a picker: what the probe and the means need, in item order."""
    return [{"item": i, "scene": it["scene"], "source": it["source"], "entity": it["entity"], "domain": it["domain"],
             "group": it["group"], "half": it["half"], "k": s["k"], "locker_item": s["item"], "picker": s["picker"],
             "stratum": s["stratum"], "asked": s["asked"], "names": it["names"]}
            for i, it in enumerate(items) for s in it["sentences"] if s["picker"]]  # fmt: skip


def class_means(
    h: np.ndarray, rows: list[dict], min_fit: int = MIN_FIT
) -> tuple[dict[str, np.ndarray], dict[str, int]]:
    """Per picker name, the mean state over the after rows of half A (h in row order), and each name's count; names
    with fewer than min_fit states get no mean."""
    idx = collections.defaultdict(list)
    for j, r in enumerate(rows):
        if r["stratum"] == "after" and r["half"] == "A":
            idx[r["picker"]].append(j)
    return ({n: h[j].mean(0) for n, j in idx.items() if len(j) >= min_fit}, {n: len(j) for n, j in idx.items()})


def omp_share(jdic, x, k: int = X.K_MAIN) -> list[float]:
    """Per row of x [n, d] (on jdic's device): the share of its squared norm in its k-atom signed OMP fit."""
    part = X.fit(jdic, x.float(), k, "signed").float()
    return (part.norm(dim=-1) ** 2 / (x.float().norm(dim=-1) ** 2).clamp_min(1e-30)).tolist()


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import suite_v1 as S
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.3 renders the runs' chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MODELS or target in COVERAGE_RUNS, f"48.3 runs on {[*MODELS, *COVERAGE_RUNS]}, not {target}"
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    runs = {src: X.RESULTS / r[target] for src, r in SOURCES.items()}
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "48.3",
         "spec": "jobs/c3/batch48.yaml (48.3)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(d / f for d in runs.values() for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl")))},
         "sources": {src: d.name for src, d in runs.items()}, "layer": layer, "arms": ARM_TEXT, "s": list(S_LIST),
         "tokens": list(TOKENS), "k": X.K_MAIN, "omp": "signed", "random_dirs": N_RANDOM_DIRS,
         "items_rule": "the scenes of both runs' chat outcomes at L; groups: main by x0_strata's org locker vs asked "
                       "pick, 45m by x45m.group_of; the write on locker-after scenes of half B with a candidate",
         "means": "per picker name and token, the mean state over the after sentences of half A (MIN_FIT states)",
         "write": "at the written sentence's item and number tokens, s * (mu_asked - mu_picker) per token; random: a "
                  "Gaussian vector of the same norm per token (seed RAND_SEED, drawn in item order)",
         "read": "X0's chat read: the prompt with a digit's space token appended; the top token classified",
         "rule": RULE,
         "seeds": {"split": SPLIT_SEED, "random": RAND_SEED, "random_dirs": f"{RAND_SEED} + layer", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED, "fresh_draws": X.FRESH_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no probe, rates or verdict in the run; closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, target, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps({k: v for k, v in counts.items() if k != "halves"}, ensure_ascii=False), flush=True)
    assert items, "no scenes"
    rows_p = probe_rows(items)
    ws = X.whitespace_mask(model)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    dev = jdic.device
    # 1. states at every locker sentence's item and number tokens (one forward per scene; the last token of a
    #    multi-token item or number)
    states: dict[str, list] = {t: [] for t in TOKENS}
    with torch.no_grad():
        for it in progress(items, f"48.3 states at L{layer} (scene)"):
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            h = model.run(torch.tensor([ids], device=model.device), record=(layer,))[1][layer].float().cpu()
            for s in it["sentences"]:
                if s["picker"]:
                    for t in TOKENS:
                        states[t].append(h[s["positions"][t][-1]].numpy())
    h_np = {t: np.stack(states[t]) for t in TOKENS}
    np.savez_compressed(out / "states.npz", h_item=h_np["item"].astype(np.float16),
                        h_number=h_np["number"].astype(np.float16))  # fmt: skip
    X.write_jsonl(out / "probe_rows.jsonl", rows_p)
    # 2. the means (half A, after) and the written contrasts' J++ shares beside random directions'
    means, fit_counts = {}, {}
    for t in TOKENS:
        means[t], fit_counts[t] = class_means(h_np[t].astype(np.float64), rows_p)
    gen_dirs = torch.Generator().manual_seed(RAND_SEED + layer)
    dirs = torch.randn(N_RANDOM_DIRS, jdic.shape[1], generator=gen_dirs).to(dev)
    rand_share = dict.fromkeys(TOKENS, omp_share(jdic, dirs))  # a direction's share does not depend on the token
    writes, no_mean = [], collections.Counter()
    for i in write_items(items):
        it = items[i]
        a, j = it["asked"]["person"], it["write"]["person"]
        if any(n not in means[t] for t in TOKENS for n in (a, j)):
            no_mean[
                f"{'the asked' if a not in means[TOKENS[0]] else 'the written'} person has fewer than {MIN_FIT} fit states"
            ] += 1
            it["write_dropped"] = "no mean"
            continue
        writes.append(i)
    deltas = {t: torch.tensor(np.stack([means[t][items[i]["asked"]["person"]] - means[t][items[i]["write"]["person"]]
                                        for i in writes]), dtype=torch.float32, device=dev) for t in TOKENS} if writes else {}  # fmt: skip
    shares = {t: omp_share(jdic, deltas[t]) for t in TOKENS} if writes else {t: [] for t in TOKENS}
    contrasts = {"fit_counts": fit_counts, "names_with_means": {t: sorted(means[t]) for t in TOKENS},
                 "writes": len(writes), "no_mean": dict(no_mean), "random_dirs_share": rand_share,
                 "per_write": [{"item": i, "scene": items[i]["scene"], "entity": items[i]["entity"],
                                "asked": items[i]["asked"]["person"], "written": items[i]["write"]["person"],
                                **{f"norm_{t}": round(float(deltas[t][w].norm()), 4) for t in TOKENS},
                                **{f"share_{t}": round(shares[t][w], 5) for t in TOKENS}}
                               for w, i in enumerate(writes)]}  # fmt: skip
    (out / "contrasts.json").write_text(json.dumps(contrasts, indent=1) + "\n")
    # 3. the writes, both readers
    gen = torch.Generator().manual_seed(RAND_SEED)
    examples = {writes[e] for e in example_indices(len(writes))}
    rows, greedy = [], []
    with torch.no_grad():
        for w, i in enumerate(progress(writes, f"48.3 writes at L{layer} (scene)")):
            it = items[i]
            wr = it["write"]
            vec = {t: deltas[t][w] for t in TOKENS}
            vectors: dict[str, dict] = {}  # arm -> token -> the row added
            for s in S_LIST:
                tag = str(int(s))
                vectors[f"w{tag}"] = {t: s * vec[t] for t in TOKENS}
                vectors[f"r{tag}"] = {}
                for t in TOKENS:
                    r = torch.randn(vec[t].shape[0], generator=gen).to(dev)
                    vectors[f"r{tag}"][t] = r / r.norm() * vectors[f"w{tag}"][t].norm()
            positions = [wr["positions"][t][0] for t in TOKENS]
            arms: dict[str, dict] = {"none": {}}
            arms.update(
                {a: {layer: AddRows(torch.stack([vectors[a][t] for t in TOKENS]), positions)} for a in ARMS[1:]}
            )
            assert tuple(arms) == ARMS
            tokens = {
                "lookup": {"target": S.answer_token(tok, wr["digit"], "digit")},
                "recall": {"target": S.answer_token(tok, wr["attribute"], "digit")},
            }
            for rw, rd in it["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(arms.values()), RENDERING, it["space"], ws)
                for arm, lg in zip(arms, logits, strict=True):
                    top = int(lg.argmax())
                    p = torch.softmax(lg.float(), -1)
                    tgt = tokens[READER_NAME[rw]]["target"]
                    cls = "target" if top == tgt else "original" if top == rd["tok_A"] else "other"
                    if rw == X.RECALL and wr["same_attribute"]:
                        cls = "same"
                    rows.append({"scene": it["scene"], "source": it["source"], "entity": it["entity"],
                                 "domain": it["domain"], "reader": rw, "arm": arm, "top": top,
                                 "top_text": tok.decode([top]), "class": cls, "right": int(top == rd["tok_A"]),
                                 "p_org": round(float(p[rd["tok_A"]]), 4), "p_target": round(float(p[tgt]), 4),
                                 "ld": round(float(lg[tgt] - lg[rd["tok_A"]]), 3)})  # fmt: skip
                if i in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, list(arms.values()))
                    greedy += [{"scene": it["scene"], "reader": rw, "arm": arm, "greedy": t}
                               for arm, t in zip(arms, texts, strict=True)]  # fmt: skip
    X.write_jsonl(out / "cases.jsonl", items)  # with 'no mean' drops recorded
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, "(sealed: no probe, rates or verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q48.3 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def seeded_folds(groups: list[str], k: int = K_FOLDS, seed: int = SPLIT_SEED) -> np.ndarray:
    """Fold per row, whole groups (entities) per fold: entities by count (largest first, ties in a seeded random
    order), each to the smallest fold so far."""
    count = collections.Counter(groups)
    order = sorted(count)
    random.Random(seed).shuffle(order)
    rank = {g: i for i, g in enumerate(order)}
    out, size = np.empty(len(groups), dtype=int), [0] * k
    for g in sorted(count, key=lambda g: (-count[g], rank[g])):
        f = min(range(k), key=lambda i: (size[i], i))
        out[[i for i, x in enumerate(groups) if x == g]] = f
        size[f] += count[g]
    return out


def ridge_scores(
    xtr: np.ndarray, ytr: list[str], xte: np.ndarray, rels: tuple[float, ...]
) -> tuple[list[str], list[np.ndarray]]:
    """x0_probe's one-hot ridge (standardized features, dual form): the classes and, per relative penalty, the test
    rows' scores [n_te, classes]."""
    classes = sorted(set(ytr))
    mu, sd = xtr.mean(0), xtr.std(0)
    sd[sd < 1e-6] = 1.0
    a, b = (xtr - mu) / sd, (xte - mu) / sd
    y = np.array([[v == c for c in classes] for v in ytr], dtype=float)
    ym = y.mean(0)
    s, u = np.linalg.eigh(a @ a.T)
    s = np.clip(s, 0.0, None)
    proj, kt = u.T @ (y - ym), b @ a.T
    return classes, [kt @ (u @ (proj / (s + r * s.sum() / len(s))[:, None])) + ym for r in rels]


def predict_names(scores: np.ndarray, classes: list[str], cands: list[list[str]]) -> list[str | None]:
    """Per test row, the best-scoring of the row's candidate names (None when no candidate is a training class)."""
    col = {c: j for j, c in enumerate(classes)}
    out = []
    for sc, names in zip(scores, cands, strict=True):
        known = [n for n in names if n in col]
        out.append(max(known, key=lambda n: sc[col[n]]) if known else None)
    return out


def fit_predict(x: np.ndarray, y: list[str], cands: list[list[str]], groups: list[str], tr: np.ndarray,
                te: np.ndarray, rels: tuple[float, ...] = PR.RELS) -> tuple[list[str | None], float]:  # fmt: skip
    """Train on rows tr, predict rows te; the penalty by an inner K_INNER-fold CV over tr with whole groups (the
    sentence's item) per fold (x0_probe's RELS; ties to the larger). Returns the predictions and the penalty."""
    ytr = [y[i] for i in tr]
    inner = seeded_folds([groups[i] for i in tr], PR.K_INNER)
    acc = np.zeros(len(rels))
    for g in range(PR.K_INNER):
        itr, ite = tr[inner != g], tr[inner == g]
        if not len(ite):
            continue
        classes, scores = ridge_scores(x[itr], [y[i] for i in itr], x[ite], rels)
        for j, sc in enumerate(scores):
            pred = predict_names(sc, classes, [cands[i] for i in ite])
            acc[j] += sum(p == y[i] for p, i in zip(pred, ite, strict=True))
    best = max(range(len(rels)), key=lambda j: (acc[j], j))
    classes, scores = ridge_scores(x[tr], ytr, x[te], (rels[best],))
    return predict_names(scores[0], classes, [cands[i] for i in te]), rels[best]


def probe_cells(h: np.ndarray, rows: list[dict], n_boot: int) -> dict[str, Any]:
    """One token's probes: per stratum the out-of-fold accuracy (folds by the sentence's item, seed 0) on the rule's
    cell (the asked item's sentence in that group's scenes) and on every sentence of the stratum, the after-trained
    probe on the before rows (transfer), chance 1 / 3; cluster-bootstrap CIs over the sentence's item."""
    y = [r["picker"] for r in rows]
    cands = [r["names"] for r in rows]
    ents = [r["locker_item"] for r in rows]
    folds = seeded_folds(ents)
    idx = {st: np.array([i for i, r in enumerate(rows) if r["stratum"] == st], dtype=int) for st in ("after", "before")}
    pred: dict[str, list] = {"after": [None] * len(rows), "before": [None] * len(rows), "transfer": [None] * len(rows)}
    pens: dict[str, list] = collections.defaultdict(list)
    for f in range(K_FOLDS):
        for st in ("after", "before"):
            tr, te = idx[st][folds[idx[st]] != f], idx[st][folds[idx[st]] == f]
            if not len(te) or not len(tr):
                continue
            p, pen = fit_predict(h, y, cands, ents, tr, te)
            pens[st].append(pen)
            for i, v in zip(te, p, strict=True):
                pred[st][i] = v
            if st == "after":
                te_b = idx["before"][folds[idx["before"]] == f]
                if len(te_b):
                    p, _ = fit_predict(h, y, cands, ents, tr, te_b)
                    for i, v in zip(te_b, p, strict=True):
                        pred["transfer"][i] = v
    out: dict[str, Any] = {"penalties": dict(pens), "chance": round(1 / 3, 4)}
    cells = {"after": ("after", "after", True), "before": ("before", "before", True),
             "after_all": ("after", "after", False), "before_all": ("before", "before", False),
             "transfer": ("transfer", "before", True), "transfer_all": ("transfer", "before", False)}  # fmt: skip
    for cell, (which, st, asked_only) in cells.items():
        sel = [i for i in idx[st] if (not asked_only or (rows[i]["asked"] and rows[i]["group"] == st))
               and pred[which][i] is not None]  # fmt: skip
        if not sel:
            out[cell] = {"n": 0, "accuracy": [math.nan, math.nan, math.nan]}
            continue
        right = [int(pred[which][i] == y[i]) for i in sel]
        r = X.resampled_rates({"probe": right}, [ents[i] for i in sel], n_boot)["probe"]
        out[cell] = {"n": len(sel), "entities": len({ents[i] for i in sel}), "names": len({y[i] for i in sel}),
                     "accuracy": [float(np.mean(right)), *X.interval(r)]}  # fmt: skip
    return out


def rate_table(rows: list[dict], reader: str, classes: tuple[str, ...], n_boot: int) -> dict[str, Any]:
    """Per arm, each class's share over the written scenes (the recall's over the scenes whose attribute differs),
    with cluster-bootstrap CIs over bridge entities; the write's target minus its random control's, paired."""
    mine = [r for r in rows if r["reader"] == reader]
    scenes = list(dict.fromkeys(r["scene"] for r in mine))
    got = {(r["scene"], r["arm"]): r for r in mine}
    same = {s for s in scenes if got[(s, "none")]["class"] == "same"}
    keep = [s for s in scenes if s not in same]
    ents = [got[(s, "none")]["entity"] for s in keep]
    out: dict[str, Any] = {"n": len(keep), "same_attribute": len(same), "entities": len(set(ents)), "arms": {}}
    if not keep:
        return out
    sw = {f"{a}|{c}": [int(got[(s, a)]["class"] == c) for s in keep] for a in ARMS for c in classes if c != "same"}
    sw.update({f"{a}|right": [got[(s, a)]["right"] for s in keep] for a in ARMS})
    r = X.resampled_rates(sw, ents, n_boot)
    for a in ARMS:
        out["arms"][a] = {k: [float(np.mean(sw[f"{a}|{k}"])), *X.interval(r[f"{a}|{k}"])]
                          for k in (*(c for c in classes if c != "same"), "right")}  # fmt: skip
    out["write_minus_random"] = {str(int(s)): [out["arms"][f"w{int(s)}"]["target"][0] - out["arms"][f"r{int(s)}"]["target"][0],
                                               *X.interval(r[f"w{int(s)}|target"] - r[f"r{int(s)}|target"])] for s in S_LIST}  # fmt: skip
    return out


def clause_write(rates: dict[str, Any]) -> dict[str, Any]:
    """The write clause on one reader's rates: at some s the target rate >= WRITE_MIN with its random control's
    <= RANDOM_MAX (point estimates, EPS)."""
    by_s = {}
    for s in S_LIST:
        tag = str(int(s))
        if not rates.get("arms"):
            by_s[tag] = {"holds": False, "why": "no written scenes"}
            continue
        w, rnd = rates["arms"][f"w{tag}"]["target"][0], rates["arms"][f"r{tag}"]["target"][0]
        ok = w >= WRITE_MIN - EPS and rnd <= RANDOM_MAX + EPS
        by_s[tag] = {"holds": ok, "write": w, "random": rnd,
                     "why": f"s = {tag}: target {w:.3f} {'>=' if w >= WRITE_MIN - EPS else '<'} {WRITE_MIN}, random "
                            f"{rnd:.3f} {'<=' if rnd <= RANDOM_MAX + EPS else '>'} {RANDOM_MAX}"}  # fmt: skip
    return {"holds": any(v["holds"] for v in by_s.values()), "by_s": by_s}


def clause_token(probe: dict[str, Any], share: float | None, random_share: float) -> dict[str, Any]:
    """One token's probe and lens clauses."""
    after, before = probe["after"]["accuracy"][0], probe["before"]["accuracy"][0]
    ok_probe = after >= PROBE_AFTER - EPS and before <= PROBE_BEFORE + EPS
    ok_lens = share is not None and share <= LENS_FACTOR * random_share + EPS
    return {"probe": ok_probe, "lens": ok_lens, "holds": ok_probe and ok_lens, "after": after, "before": before,
            "share": share, "random_share": random_share,
            "why": f"probe after {after:.3f} {'>=' if after >= PROBE_AFTER - EPS else '<'} {PROBE_AFTER}, before "
                   f"{before:.3f} {'<=' if before <= PROBE_BEFORE + EPS else '>'} {PROBE_BEFORE}; share "
                   f"{'-' if share is None else f'{share:.4f}'} {'<=' if ok_lens else '>'} {LENS_FACTOR} x {random_share:.4f}"}  # fmt: skip


def rule(tokens: dict[str, dict], lookup: dict[str, Any], recall: dict[str, Any]) -> dict[str, Any]:
    """48.3 on one model: the probe and lens clauses at at least one token, and the write clause on the lookup; the
    recall's move beside it (the same bars), not in the rule."""
    tok_ok = [t for t, c in tokens.items() if c["holds"]]
    return {"holds": bool(tok_ok) and lookup["holds"], "tokens_holding": tok_ok, "write": lookup["holds"],
            "recall_moves": recall["holds"],
            "why": "; ".join([*(f"{t}: {c['why']}" for t, c in tokens.items()),
                              "lookup " + "; ".join(v["why"] for v in lookup["by_s"].values()),
                              "recall " + "; ".join(v["why"] for v in recall["by_s"].values())])}  # fmt: skip


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in {**RUNS, **COVERAGE_RUNS}.items()}.get(run)
        assert target, f"no 48.3 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {
            "run": run,
            "target": target,
            "status": "pending",
            "holds": False,
            "why": "no manifest or outcomes here",
        }
    m = json.loads((src / "manifest.json").read_text())
    rows_p = X.read_jsonl(src / "probe_rows.jsonl")
    z = np.load(src / "states.npz")
    contrasts = json.loads((src / "contrasts.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    probes, tokens = {}, {}
    for t in TOKENS:
        h = z[f"h_{t}"].astype(np.float64)
        assert len(h) == len(rows_p), f"{run}: {len(h)} states for {len(rows_p)} probe rows"
        probes[t] = probe_cells(h, rows_p, n_boot)
        shares = [w[f"share_{t}"] for w in contrasts["per_write"]]
        tokens[t] = clause_token(probes[t], statistics.median(shares) if shares else None,
                                 float(np.mean(contrasts["random_dirs_share"][t])))  # fmt: skip
    lookup = rate_table(rows, X.LOOKUP, LOOKUP_CLASSES, n_boot)
    recall = rate_table(rows, X.RECALL, RECALL_CLASSES, n_boot)
    cl_lookup, cl_recall = clause_write(lookup), clause_write(recall)
    r = rule(tokens, cl_lookup, cl_recall)
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "status": "tested", **r,
            "clauses": {"tokens": tokens, "lookup": cl_lookup, "recall": cl_recall}, "probes": probes,
            "rates": {"lookup": lookup, "recall": recall}, "contrasts": {k: v for k, v in contrasts.items() if k != "per_write"},
            "norms_median": {t: statistics.median([w[f"norm_{t}"] for w in contrasts["per_write"]]) if contrasts["per_write"] else None
                             for t in TOKENS}, "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def batch_verdict(models: list[dict]) -> dict[str, Any]:
    """The rule over the models: holds iff both hold; does not hold once one tested model fails; else pending."""
    n_hold = sum(bool(m["holds"]) for m in models)
    failed = [m["run"] for m in models if m["status"] == "tested" and not m["holds"]]
    pending = [m["run"] for m in models if m["status"] == "pending"]
    label = "holds" if n_hold == len(MODELS) else "does not hold" if failed else "pending"
    moves = {m["target"]: m.get("recall_moves") for m in models if m["status"] == "tested"}
    return {"label": label, QUESTION: {"holds": "yes", "does not hold": "no"}.get(label, "pending"),
            "recall_moves": {"by_model": moves,
                             "answer": "pending" if pending else ("yes" if all(moves.values()) else "no")},
            "models_holding": n_hold, "models": len(models), "failed": failed, "pending": pending}  # fmt: skip


def fmt(v: list) -> str:
    return "-" if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−"))  # fmt: skip


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random written scenes of the run (seed 0): each reader's O prompt with the bridge word and the written
    tokens marked, each arm's top token, class and greedy text."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    written = [it for it in items if (it["scene"], X.LOOKUP, "none") in reads]
    lines = [f"## {run}: {min(k, len(written))} random written scenes of {len(written)} (seed {seed})", ""]
    for i in example_indices(len(written), k, seed):
        it = written[i]
        wr = it["write"]
        lines += [f"### {it['scene']} ({it['source']}, {it['domain']}): bridge {it['entity']} picked by "
                  f"{it['asked']['person']}; written: {wr['item']} (picked by {wr['person']}; locker {wr['digit']}, "
                  f"attribute {wr['attribute']})", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, the written item's "
                      f"{wr['digit'] if w == X.LOOKUP else wr['attribute']}", "", "```", item_marked(it, w), "```", "",
                      "| arm | what | top token | class | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            for arm in ARMS:
                r = reads[(it["scene"], w, arm)]
                lines.append(f"| {arm} | {ARM_TEXT[arm]} | {r['top_text']!r} | {r['class']} | "
                             f"{greedy.get((it['scene'], w, arm))!r} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """48.3's verdict (sealed until Q48.3), or with coverage (batch 52 C) the same rule on the given coverage runs alone:
    no seal guard, "no prediction" in place of Dan's answer, no pending rows, written to x52_bind-<UTC>/."""
    answer = (f"{NO_PREDICTION}; rule first scored in {SCORED}; the all-models count covers the given runs only, "
              "not re-scored") if coverage else dan_answer()  # fmt: skip
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    known = set(COVERAGE_RUNS) if coverage else set(MODELS)
    assert set(targets) <= known, f"48.3 runs on {sorted(known)}, not {sorted(set(targets) - known)}"
    if not coverage:
        models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
                   for t in MODELS if t not in targets]  # fmt: skip
    v = batch_verdict(models)
    out = RESULTS / f"{'x52_bind' if coverage else 'x48_bind'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 48.3: forward binding at the locker sentence, outside the lens?", "",
             f"Batch 48, test 48.3 (jobs/c3/batch48.yaml; {QUESTION}, Dan: {answer}). Probe = which of the scene's three "
             "people picked the item, read at the locker sentence's item / number token (ridge, the sentence's item held "
             "out, 5 folds seed 0; chance 0.33); lens share = the written contrast's J++ k = 25 share (median) against "
             f"{N_RANDOM_DIRS} Gaussian directions' (mean); the write = s (mu_asked - mu_picker) at both tokens, read by "
             f"both readers. Cluster bootstrap over bridge entities ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}. As computed: the probe and lens clauses hold on a model at at least one "
             "token; the write clause at some s with its random control at that s; the recall's move with the same bars "
             "(reported, Q48.3's second question).", "",
             f"**Verdict: {v['label']}** ({QUESTION} {v[QUESTION]}; the write moves the recall too: "
             f"{v['recall_moves']['answer']}, by model {v['recall_moves']['by_model']}): {v['models_holding']} of "
             f"{v['models']} models hold" + (f"; failed: {', '.join(v['failed'])}" if v["failed"] else "")
             + (f"; pending: {', '.join(v['pending'])}" if v["pending"] else "") + ".", "",
             "| model | run | status | holds | tokens holding | write (lookup) | recall moves | why |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | | |")
            continue
        lines.append(f"| {m['target']} | {m['run']} | tested | {'yes' if m['holds'] else 'no'} | "
                     f"{m['tokens_holding'] or 'none'} | {'yes' if m['write'] else 'no'} | "
                     f"{'yes' if m['recall_moves'] else 'no'} | {m['why']} |")  # fmt: skip
    lines += ["", "Probes (accuracy, chance 0.33): the rule's cells (the asked item's sentence in locker-after / "
              "locker-first scenes), every sentence of the stratum beside, and the after-trained probe on the before "
              "states (transfer).", "",
              "| model | token | after (rule) | before (rule) | after, all sentences | before, all | transfer (rule cell) "
              "| transfer, all |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for t in TOKENS:
            p = m["probes"][t]
            cells = [f"{fmt(p[c]['accuracy'])} (n {p[c]['n']})"
                     for c in ("after", "before", "after_all", "before_all", "transfer", "transfer_all")]  # fmt: skip
            lines.append(f"| {m['target']} | {t} | " + " | ".join(cells) + " |")
    lines += ["", "Lens share of the written person contrast (J++ k = 25 signed OMP; median over the written scenes) "
              "against random directions' (mean), and the contrast's norm (median).", "",
              "| model | token | contrast share | random share | 2x random | norm | written scenes |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for t in TOKENS:
            c = m["clauses"]["tokens"][t]
            lines.append(f"| {m['target']} | {t} | {'-' if c['share'] is None else f'{c['share']:.4f}'} | "
                         f"{c['random_share']:.4f} | {LENS_FACTOR * c['random_share']:.4f} | {m['norms_median'][t]} | "
                         f"{m['contrasts']['writes']} |")  # fmt: skip
    lines += ["", "The write (locker-after scenes of half B): per arm the lookup's answer class (target = the written "
              "item's locker, original = O's answer) and the recall's (target = the written item's attribute; scenes "
              "whose attribute equals the bridge's are left out), and the share still right (O's answer).", "",
              "| model | reader | n (same attribute) | arm | target | original | other | right |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for w in ("lookup", "recall"):
            r = m["rates"][w]
            for a in ARMS:
                if a not in r.get("arms", {}):
                    continue
                c = r["arms"][a]
                lines.append(f"| {m['target']} | {w} | {r['n']} ({r['same_attribute']}) | {a} | {fmt(c['target'])} | "
                             f"{fmt(c['original'])} | {fmt(c['other'])} | {fmt(c['right'])} |")  # fmt: skip
    lines += ["", "Write minus random (target rate, paired): " + "; ".join(
        f"{m['target']} {w} s = {s}: {fmt(v)}" for m in models if m["status"] == "tested" for w in ("lookup", "recall")
        for s, v in m["rates"][w].get("write_minus_random", {}).items()) + ".", "",
        "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "", "Scenes and fit (descriptive):", ""]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        p, c = m["plan"], m["contrasts"]
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): {p['scenes']} scenes ({p['runs']}; dropped "
                     f"{p['dropped'] or 'none'}); {p['entities']} bridge entities in halves A / B; locker-after "
                     f"{p['locker_after']}; write candidates in B {p['write_candidates_B']} (dropped {p['write_dropped'] or 'none'}; "
                     f"no mean {c['no_mean'] or 'none'}); written {c['writes']}; {p['names']} names, names with means "
                     f"{ {t: len(v) for t, v in c['names_with_means'].items()} }; strata {p['strata']}; numbers {p['numbers']}.")  # fmt: skip
    if coverage:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ")
    (out / "x48_bind.json").write_text(json.dumps({"runs": runs, "dan": answer, "verdict": v, "models": models}, indent=1,
                                                  default=str) + "\n")  # fmt: skip
    (out / "x48_bind.md").write_text("\n".join(lines) + "\n")
    ex = ["# 48.3 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, "
          "⟦write:…⟧ the written sentence's item and number tokens. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x48_bind/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 48.3 runs (9B, Muse)")
    ap.add_argument("--why", default="batch 48, test 48.3 (jobs/c3/batch48.yaml; Q48.3)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        stage_verdict(a.runs, a.n_boot, a.coverage)


if __name__ == "__main__":
    main()
