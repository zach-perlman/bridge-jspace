"""x49_probe (batch 49, test 49.3; jobs/c3/batch49.yaml "49.3", design and rules fixed in advance; Q49.3 in
predictions/2026-10-28_dan.md): the locker-after link, a pooled probe over the locker sentence.

3b and 47.4 put the lookup's link in the locker sentences, made before L; 48.3 (scripts/x48_bind.py) found no "who
picked it" at the item or number token. Distributed over the sentence, or not a person mark at all?

Scenes: each model's clean-design run (x0_necessity --alt fresh, the 45m run 48.3 read beside the main test), its chat
scenes at the layer fixed in advance (X.PREDICTED), built by 48.3's scene_item (the generator's pickers, the asked
person, every locker sentence; a scene whose asked item's item or number is not one token is dropped and counted).
Groups by x45m.group_of as in 48.3: locker-after (the rule's scenes), locker-first ('before', the control), mixed
(training rows only). Only O (the original prompt, the lookup's) is read; one forward per scene.

States (run, GPU): at L and L // 2, at every token of every locker sentence that has a picker (the 45m added item has
none), and the sentence mean (every token whose characters overlap the sentence, its period included). Each token gets
a key by its role in 'The locker of [the] <item> is <number>.': 'item' / 'number' (the last token of the item / the
number; earlier ones 'item_pre' / 'number_pre'), else 'w:<its text>' ('w:The', 'w:locker', 'w:of', 'w:the', 'w:is',
'w:space' (the 9B's lone space before a digit), 'w:.'), so a key's probe reads the same word of every sentence.

Probes (verdict, CPU; 48.3's ridge: standardized features, the penalty by an inner CV, out-of-fold over 5 folds with
whole items held out, seed 0), each trained and scored within a stratum (48.3's: the sentence after / before its
picker's pick), per token key and on the sentence mean ('pooled'), at L and L // 2:
  (i)   the picker: which of the scene's three people picked the sentence's item (one-hot over the training rows'
        names, the prediction the best-scoring of the scene's three; chance 1/3). Rule cell: the bridge item's
        sentence in locker-after scenes; the other items' sentences of the stratum beside (control).
  (ii)  "this item was picked by the asked person" (binary: the bridge item's sentence vs the other items' ones),
        scored as balanced accuracy (chance 0.5) with the rule cell's rows as the positives and the stratum's other
        items' sentences as the negatives, its two class rates beside.
  (iii) the picked item's identity on the sentence mean (the scene's locker items as candidates, chance 1/4 on the
        clean design's four lockers;
        folds by the picker's name, so the person is held out): the pooled read's positive control.
Control: the same probes on locker-first scenes ('before' stratum; must be at chance for (i) and (ii)).

Rules (jobs/c3/batch49.yaml 49.3, verbatim): "Distributed person mark": pooled (i) >= 0.85 with every per-token (i)
<= 0.6. "A picked-flag, not a person": (ii) >= 0.85 pooled or at some token while (i) <= 0.5. "Neither at the
sentence": both at chance; the link is made elsewhere. As computed (fixed before any run): per layer on the rule
cells' point estimates (EPS 1e-9 at the bars); "every per-token" over the token keys present in >= half of the rule
cell's rows (the rest reported); "(i) <= 0.5" for every (i) cell, pooled and per token; "at chance" = every cell's
point <= chance + CHANCE_MARGIN; neither label: "in between". The locker-first control must be at chance (the same
definition) for (i) and (ii); where it is not, a 'distributed' or 'flag' label reads "not interpretable (control
above chance)", the raw label beside. A model's label: 'distributed' (or 'flag') if it holds at L or L // 2, 'neither'
if neither holds at both, else 'in between'; both layers reported. Cluster bootstrap over the sentence's item (the
bridge entity on the rule cells; 10,000, seed 0) beside every accuracy.

SEALED: the run writes states and rows only (no probe). The verdict stage refuses until predictions/2026-10-28_dan.md
holds Dan's Q49.3 answer at HEAD. Storage: tokens_L<l>.npz (every token's state, 50-150 MB) stays on the box and the
pull (not committed, as 48.2's states); means_L<l>.npz (the sentence means) is committed.

uv run python scripts/x49_probe.py plan --out results/x49_probe/plan-<UTC>                 # CPU, the tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x49_probe.py run --name qwen35_9b_x49_3          # GPU (sealed)
uv run python scripts/x49_probe.py verdict --runs qwen35_9b_x49_3 muse30_x49_3              # CPU, after Q49.3
uv run python scripts/x49_probe.py view --name qwen35_9b_x49_3                              # CPU: verify pack
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x45m
from scripts import x48_bind as W

EXP = "x49_probe"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch49.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION, TEST = "Q49.3", "49.3"
MODELS = ("qwen3.5-9b", "muse-glimmer-30b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x49_3", "muse-glimmer-30b": "muse30_x49_3"}
# batch 52 C coverage (amendment 2: the 27B fills every gap): run-stage targets beyond the design's; the
# verdict's own model list is unchanged (verdict --coverage reads these runs alone)
COVERAGE_RUNS = {"qwen3.6-27b": "x49_3_27b"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x49_probe/x49_3-20261028T154604Z"  # 49.3's rule first scored (the 9B and Muse)
SOURCE = "45m"  # the clean design: x0_necessity --alt fresh (B.FRESH_RUN)
RENDERING = "chat"
STRATA = ("after", "before")  # the sentence after / before its picker's pick; the rule's scenes / the control
POOLED = "mean"
PROBES = ("picker", "asked", "identity")
PROBE_TEXT = {"picker": "(i) the picker, of the scene's three people (chance 1/3)",
              "asked": "(ii) picked by the asked person, binary (balanced accuracy, chance 0.5)",
              "identity": "(iii) the picked item's identity, of the scene's locker items (chance 1/4)"}  # fmt: skip
CHANCE = {"picker": 1 / 3, "asked": 0.5}  # the rule's chance levels; (iii)'s from its candidates (descriptive)
DIST_POOL, DIST_TOKEN, FLAG, FLAG_PICKER = 0.85, 0.6, 0.85, 0.5
CHANCE_MARGIN = 0.10  # "at chance": the point <= chance + 0.10
KEY_SHARE = 0.5  # a token key is in "every per-token" if present in >= half of the rule cell's rows
EPS = 1e-9
FP16_MAX = 6e4
LABELS = {"distributed": "distributed person mark", "flag": "a picked-flag, not a person",
          "neither": "neither at the sentence", "between": "in between",
          "uninterpretable": "not interpretable (control above chance)", "pending": "pending"}  # fmt: skip
RULE = ('"Distributed person mark": pooled (i) >= 0.85 with every per-token (i) <= 0.6. "A picked-flag, not a person": '
        '(ii) >= 0.85 pooled or at some token while (i) <= 0.5. "Neither at the sentence": both at chance; the link is '
        "made elsewhere. Controls: locker-first scenes must be at chance for (i), (ii); the other items' locker "
        "sentences beside.")  # fmt: skip


# ---- scenes and token keys (tokenizer only) -----------------------------------------------------------------------


def layers_of(layer: int) -> tuple[int, int]:
    """The two layers read: L // 2 and L."""
    return (layer // 2, layer)


def token_keys(offsets: list, positions: list[int], start: int, sentence: str) -> list[str]:
    """Each position's key by its role in the locker sentence (characters [start, start + len(sentence)) of the
    prompt): 'item' / 'number' for the last token overlapping the item / the number, 'item_pre' / 'number_pre' for
    earlier ones, else 'w:' + the token's characters inside the sentence, stripped; a repeated key gets '#2'."""
    m = B.LOCKER_RE.match(sentence)
    assert m, f"{sentence!r} is not a locker sentence"
    roles = {"item": m.span(1), "number": m.span(2)}
    hits: dict[str, list[int]] = {r: [] for r in roles}
    keys: list[str | None] = []
    for j, p in enumerate(positions):
        a, b = offsets[p][0] - start, offsets[p][1] - start
        role = next((r for r, (x, y) in roles.items() if a < y and b > x), None)
        if role:
            hits[role].append(j)
            keys.append(None)
        else:
            keys.append("w:" + (sentence[max(a, 0) : min(b, len(sentence))].strip() or "space"))
    for role, js in hits.items():
        for n, j in enumerate(js):
            keys[j] = role if n == len(js) - 1 else f"{role}_pre"
    out, seen = [], collections.Counter()
    for k in keys:
        assert k is not None
        seen[k] += 1
        out.append(k if seen[k] == 1 else f"{k}#{seen[k]}")
    return out


def sentence_tokens(text: str, context: str, offsets: list, sents: list[dict]) -> list[dict]:
    """Per locker sentence of the prompt (context order): its token positions (every token overlapping the
    sentence's characters) and their keys."""
    from scripts import statement_positions as SP

    spans = B.locker_spans(text, context)
    out = []
    for s, (a, b) in zip(sents, spans, strict=True):
        assert text[a:b] == s["sentence"], f"{s['sentence']!r} is not at {a}"
        pos = SP.tokens_in(offsets, a, b)
        out.append({"positions": pos, "keys": token_keys(offsets, pos, a, s["sentence"])})
    return out


def scene_tokens(tok, it: dict) -> list[dict]:
    """sentence_tokens on the scene's lookup O prompt (its stored text and ids)."""
    from bridge_jspace.tokens import raw_encoding

    rd = it["readers"][X.LOOKUP]
    enc = raw_encoding(tok, rd["text"]["org"], offsets=True)
    assert list(enc["input_ids"]) == rd["ids"]["org"], f"{it['scene']}: the lookup's ids differ"
    return sentence_tokens(rd["text"]["org"], it["context"], enc["offset_mapping"], it["sentences"])


def select(tok, target: str, layer: int) -> tuple[list[dict], dict]:
    """The target's clean-design scenes at the layer (48.3's scene_item, in the run's scene order) with each locker
    sentence's tokens and keys, and the counts: scenes per group, drops, rows per stratum, keys."""
    from scripts import tasks_v2 as T

    run = B.FRESH_RUN[target]
    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    assert m.get("alt", "cf") == B.SOURCES[SOURCE], f"{run}: alt {m.get('alt')!r}, not {B.SOURCES[SOURCE]!r}"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
    scenes, _ = B.stored_reads(run, layer)
    assert scenes, f"{run}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    with B.x0_alt(B.SOURCES[SOURCE], (RENDERING,)):
        rebuilt = {c["scene"]: c for c in X.build_cases(tok, m["set"])[0]}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, dropped = [], collections.Counter()
    for scene in scenes:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        try:
            it = W.scene_item(tok, c, SOURCE, by_id)
        except W.Dropped as e:
            dropped[str(e)] += 1
            continue
        for s, t in zip(it["sentences"], scene_tokens(tok, it), strict=True):
            s["tokens"] = t
        out.append(it)
    return out, counts_of(out, {"run": run, "scenes_at_L": len(scenes), "dropped": dict(dropped)}, target, layer)


def counts_of(items: list[dict], head: dict, target: str, layer: int) -> dict:
    rows = probe_rows(items)
    keys = collections.Counter(k for it in items for s in it["sentences"] if s["picker"] for k in s["tokens"]["keys"])
    rule = [r for r in rows if r["asked"] and r["group"] == "after" and r["stratum"] == "after"]
    return {"target": target, "layers": list(layers_of(layer)), **head, "scenes": len(items),
            "entities": len({it["entity"] for it in items}),
            "groups": dict(collections.Counter(it["group"] for it in items)),
            "rows": len(rows), "rows_by_stratum": dict(collections.Counter(r["stratum"] for r in rows)),
            "rule_cell_rows": {"after (locker-after scenes)": len(rule),
                               "before (locker-first scenes)": sum(r["asked"] and r["group"] == "before"
                                                                   and r["stratum"] == "before" for r in rows)},
            "tokens": sum(len(s["tokens"]["positions"]) for it in items for s in it["sentences"] if s["picker"]),
            "keys": dict(keys.most_common()),
            "keys_in_rule": rule_keys(rows),
            "names": len({n for it in items for n in it["names"]})}  # fmt: skip


def probe_rows(items: list[dict]) -> list[dict]:
    """One row per locker sentence with a picker, in item order: the labels, the strata and the token keys."""
    return [{"item": i, "scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "group": it["group"],
             "k": s["k"], "locker_item": s["item"], "picker": s["picker"], "stratum": s["stratum"],
             "asked": s["asked"], "asked_person": it["asked"]["person"], "names": it["names"],
             "scene_items": [x["item"] for x in it["sentences"]], "keys": s["tokens"]["keys"]}
            for i, it in enumerate(items) for s in it["sentences"] if s["picker"]]  # fmt: skip


def rule_keys(rows: list[dict], share: float = KEY_SHARE) -> list[str]:
    """The token keys present in >= share of the rule cell's rows (the bridge sentence, locker-after scenes)."""
    rule = [r for r in rows if r["asked"] and r["group"] == "after" and r["stratum"] == "after"]
    c = collections.Counter(k for r in rule for k in r["keys"])
    return sorted(k for k, n in c.items() if rule and n >= share * len(rule) - EPS)


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def keyed_prompt(tok, it: dict) -> str:
    """The lookup's O prompt as the model reads it, the bridge item's locker sentence's tokens each marked with its
    key (⟦key:text⟧), the bridge word marked ⟦bridge:…⟧."""
    ids = it["readers"][X.LOOKUP]["ids"]["org"]
    mine = next(s for s in it["sentences"] if s["asked"])
    key_at = dict(zip(mine["tokens"]["positions"], mine["tokens"]["keys"], strict=True))
    out = []
    for p, t in enumerate(ids):
        piece = tok.decode([t]) if tok is not None else f"<{t}>"
        out.append(f"⟦{key_at[p]}:{piece}⟧" if p in key_at else f"⟦bridge:{piece}⟧" if p == it["pos"] else piece)
    return "".join(out)


def stage_plan(out: Path | None = None, k: int = 5) -> dict:
    """Tokenizer only: the scenes, drops, rows and keys, and k example scenes' prompts (seed 0) with the bridge
    sentence's tokens keyed. With `out`, written there as <target>_plan.json and <target>_prompts.md."""
    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = select(tok, pins.TARGET, layer)
    after = [it for it in items if it["group"] == "after"]
    lines = [f"# 49.3 plan: {pins.TARGET}, {min(k, len(after))} random locker-after scenes of {len(after)} (seed "
             f"{X.EXAMPLES_SEED}): the lookup's O prompt as the model reads it (ids decoded, the template included), "
             "the bridge item's locker sentence with each token's probe key ⟦key:token⟧, the bridge word "
             "⟦bridge:…⟧. UNVERIFIED.", ""]  # fmt: skip
    for i in example_indices(len(after), k):
        it = after[i]
        mine = next(s for s in it["sentences"] if s["asked"])
        lines += [f"### {it['scene']} ({it['domain']}): {it['asked']['person']} picked {it['entity']}; the scene's "
                  f"pickers {it['names']}; its locker sentence: {mine['sentence']!r} (slot {mine['k'] + 1})", "", "```",
                  keyed_prompt(tok, it), "```", ""]  # fmt: skip
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("\n".join(lines))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        tag = pins.RUN_PREFIX.rstrip("_") or "qwen36_27b"
        (out / f"{tag}_plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
        (out / f"{tag}_prompts.md").write_text("\n".join(lines) + "\n")
        print("wrote", out / f"{tag}_plan.json", out / f"{tag}_prompts.md")
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def half(h: np.ndarray) -> np.ndarray:
    return h.astype(np.float16) if np.abs(h).max() < FP16_MAX else h.astype(np.float32)


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.3 renders the runs' chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MODELS or target in COVERAGE_RUNS, f"49.3 runs on {[*MODELS, *COVERAGE_RUNS]}, not {target}"
    layer = X.PREDICTED[target]
    layers = layers_of(layer)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / B.FRESH_RUN[target]
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": TEST,
         "spec": f"jobs/c3/batch49.yaml ({TEST})", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(src / f for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl")))},
         "source": src.name, "layer": layer, "layers": list(layers), "rendering": RENDERING,
         "scenes": "the clean-design run's chat scenes at L (48.3's scene_item); groups by x45m.group_of",
         "states": "O (the lookup's prompt), every token of every locker sentence with a picker, and the sentence "
                   "mean (fp32 mean, stored fp16), at L // 2 and L",
         "probes": PROBE_TEXT, "rule": RULE, "chance_margin": CHANCE_MARGIN, "key_share": KEY_SHARE,
         "seeds": {"folds": W.SPLIT_SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no probe in the run; closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, target, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps({k: v for k, v in counts.items() if k != "keys"}, ensure_ascii=False), flush=True)
    assert items, "no scenes"
    rows = probe_rows(items)
    means: dict[int, list] = {la: [] for la in layers}
    toks: dict[int, list] = {la: [] for la in layers}
    tok_rows = []
    with torch.no_grad():
        for it in progress(items, f"{TEST} states at L{layers[0]}, L{layers[1]} (scene)"):
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            hs = model.run(torch.tensor([ids], device=model.device), record=layers)[1]
            hs = {la: hs[la].float().cpu() for la in layers}
            for s in it["sentences"]:
                if not s["picker"]:
                    continue
                pos = s["tokens"]["positions"]
                for la in layers:
                    means[la].append(hs[la][pos].mean(0).numpy())
                    toks[la].append(hs[la][pos].numpy())
                tok_rows += [{"row": len(means[layers[0]]) - 1, "key": key, "pos": p, "text": tok.decode([ids[p]])}
                             for key, p in zip(s["tokens"]["keys"], pos, strict=True)]  # fmt: skip
    assert len(means[layers[0]]) == len(rows), f"{len(means[layers[0]])} sentence states for {len(rows)} rows"
    for la in layers:
        np.savez_compressed(out / f"means_L{la}.npz", h=half(np.stack(means[la])))
        np.savez_compressed(out / f"tokens_L{la}.npz", h=half(np.concatenate(toks[la])))
    X.write_jsonl(out / "probe_rows.jsonl", rows)
    X.write_jsonl(out / "token_rows.jsonl", tok_rows)
    print("wrote", out, "(sealed: states and rows only, no probe)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q49.3 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def views(src: Path, layer: int, rows: list[dict]) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Per view (POOLED, then every token key), (the row indices that have it, their states [n, d] float64)."""
    out = {POOLED: (np.arange(len(rows)), np.load(src / f"means_L{layer}.npz")["h"].astype(np.float64))}
    tpath = src / f"tokens_L{layer}.npz"
    if not tpath.exists():  # the per-token states are not committed: pooled only
        return out
    th = np.load(tpath)["h"]
    trows = X.read_jsonl(src / "token_rows.jsonl")
    assert len(trows) == len(th), f"{tpath.name}: {len(th)} states for {len(trows)} token rows"
    by: dict[str, list] = collections.defaultdict(list)
    for j, t in enumerate(trows):
        by[t["key"]].append((t["row"], j))
    for key in sorted(by):
        rr = np.array([r for r, _ in by[key]])
        out[key] = (rr, th[[j for _, j in by[key]]].astype(np.float64))
    return out


def labels_of(rows: list[dict], probe: str) -> tuple[list[str], list[list[str]], list[str]]:
    """Per row: the label, the candidates and the fold group (the held-out unit) of one probe."""
    if probe == "picker":
        return [r["picker"] for r in rows], [r["names"] for r in rows], [r["locker_item"] for r in rows]
    if probe == "asked":
        return (
            ["yes" if r["asked"] else "no" for r in rows],
            [["no", "yes"]] * len(rows),
            [r["locker_item"] for r in rows],
        )
    assert probe == "identity", probe
    return [r["locker_item"] for r in rows], [r["scene_items"] for r in rows], [r["picker"] for r in rows]


def oof(h: np.ndarray, rows: list[dict], probe: str, stratum: str) -> list[str | None]:
    """Out-of-fold predictions of one probe on the stratum's rows (None elsewhere): 5 folds of whole groups (seed 0),
    48.3's ridge with its inner CV."""
    y, cands, groups = labels_of(rows, probe)
    idx = np.array([i for i, r in enumerate(rows) if r["stratum"] == stratum], dtype=int)
    pred: list[str | None] = [None] * len(rows)
    if len(idx) < 2:
        return pred
    folds = W.seeded_folds([groups[i] for i in idx])
    for f in range(W.K_FOLDS):
        tr, te = idx[folds != f], idx[folds == f]
        if not len(te) or len({y[i] for i in tr}) < 2:
            continue
        p, _ = W.fit_predict(h, y, cands, groups, tr, te)
        for i, v in zip(te, p, strict=True):
            pred[i] = v
    return pred


def accuracy(right: list[int], ents: list[str], n_boot: int) -> list[float]:
    if not right:
        return [math.nan, math.nan, math.nan]
    r = X.resampled_rates({"a": right}, ents, n_boot)["a"]
    return [float(np.mean(right)), *X.interval(r)]


def balanced(right: list[int], positive: list[bool], ents: list[str], n_boot: int) -> dict[str, Any]:
    """Balanced accuracy (the mean of the two classes' hit rates) with a cluster-bootstrap CI over ents (seed 0, the
    same draws as X.resampled_rates), and each class's rate."""
    if not right or all(positive) or not any(positive):
        return {"balanced": [math.nan] * 3, "pos": [math.nan] * 3, "neg": [math.nan] * 3, "n": len(right)}
    pos = np.asarray(positive)
    hit = np.asarray(right, dtype=float)
    keys = sorted(set(ents))
    index = {e: i for i, e in enumerate(keys)}
    ent = np.array([index[e] for e in ents])
    pick = np.random.default_rng(X.BOOT_SEED).integers(0, len(keys), size=(n_boot, len(keys)))
    rates = []
    for cls in (pos, ~pos):
        n_c = np.bincount(ent[cls], minlength=len(keys)).astype(float)
        s_c = np.bincount(ent[cls], weights=hit[cls], minlength=len(keys))
        with np.errstate(invalid="ignore", divide="ignore"):
            rates.append((s_c[pick].sum(1) / n_c[pick].sum(1), float(hit[cls].mean())))
    ba = (rates[0][0] + rates[1][0]) / 2
    point = (rates[0][1] + rates[1][1]) / 2
    return {"balanced": [point, *X.interval(ba)], "pos": [rates[0][1], *X.interval(rates[0][0])],
            "neg": [rates[1][1], *X.interval(rates[1][0])], "n": len(right), "n_pos": int(pos.sum())}  # fmt: skip


def probe_view(h: np.ndarray, rows: list[dict], probe: str, n_boot: int) -> dict[str, Any]:
    """One probe on one view (rows = the view's rows): per stratum, the out-of-fold score on the rule cell and on the
    stratum's other sentences. (i), (iii): accuracy on the bridge item's sentence in that stratum's own scenes
    (locker-after / locker-first), and on the other items' sentences; (ii): balanced accuracy, the rule cell's rows
    the positives, the stratum's other items' sentences the negatives."""
    y, cands, _ = labels_of(rows, probe)
    out: dict[str, Any] = {"chance": float(np.mean([1 / len(c) for c in cands])) if probe != "asked" else 0.5}
    for st in STRATA:
        pred = oof(h, rows, probe, st)
        mine = [i for i, r in enumerate(rows) if r["stratum"] == st and pred[i] is not None]
        if probe == "asked":
            sel = [i for i in mine if (rows[i]["asked"] and rows[i]["group"] == st) or not rows[i]["asked"]]
            b = balanced([int(pred[i] == y[i]) for i in sel], [rows[i]["asked"] for i in sel],
                         [rows[i]["locker_item"] for i in sel], n_boot)  # fmt: skip
            out[st] = {"accuracy": b["balanced"], "n": b["n"], "pos": b["pos"], "neg": b["neg"],
                       "n_pos": b.get("n_pos", 0)}  # fmt: skip
            continue
        cell = [i for i in mine if rows[i]["asked"] and rows[i]["group"] == st]
        others = [i for i in mine if not rows[i]["asked"]]
        for name, sel in ((st, cell), (f"{st}_others", others)):
            right = [int(pred[i] == y[i]) for i in sel]
            out[name] = {"accuracy": accuracy(right, [rows[i]["locker_item"] for i in sel], n_boot), "n": len(sel)}
    return out


def layer_result(src: Path, layer: int, rows: list[dict], n_boot: int) -> dict[str, Any]:
    """Every probe on every view at one layer ((iii) on the pooled view only)."""
    vs = views(src, layer, rows)
    out: dict[str, Any] = {"layer": layer, "views": list(vs), "probes": {}}
    for probe in PROBES:
        out["probes"][probe] = {}
        for view, (ri, h) in vs.items():
            if probe == "identity" and view != POOLED:
                continue
            out["probes"][probe][view] = probe_view(h, [rows[i] for i in ri], probe, n_boot)
    return out


def at_chance(v: float, probe: str) -> bool:
    return not (v > CHANCE[probe] + CHANCE_MARGIN + EPS)


def rule(res: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    """49.3's labels at one layer on the point estimates: the rule cells (stratum 'after') of (i) pooled and per token
    key (keys: the rule's keys), of (ii) pooled and per key; the locker-first control ('before') at chance."""
    pr = res["probes"]

    def pt(probe: str, view: str, st: str = "after") -> float | None:
        c = pr[probe].get(view, {}).get(st)
        return None if c is None or c["accuracy"][0] != c["accuracy"][0] else float(c["accuracy"][0])

    tok_keys = [k for k in keys if k in pr["picker"]]
    i_pool, ii_pool = pt("picker", POOLED), pt("asked", POOLED)
    i_tok = {k: pt("picker", k) for k in tok_keys}
    ii_tok = {k: pt("asked", k) for k in tok_keys}
    i_all = [v for v in (i_pool, *i_tok.values()) if v is not None]
    ii_all = [v for v in (ii_pool, *ii_tok.values()) if v is not None]
    if i_pool is None or ii_pool is None:
        return {"label": "pending", "why": "no pooled rule cell"}
    i_tok_max = max((v for v in i_tok.values() if v is not None), default=None)
    ii_best = max(ii_all)
    distributed = i_pool >= DIST_POOL - EPS and (i_tok_max is None or i_tok_max <= DIST_TOKEN + EPS) and bool(i_tok)
    flag = ii_best >= FLAG - EPS and max(i_all) <= FLAG_PICKER + EPS
    neither = all(at_chance(v, "picker") for v in i_all) and all(at_chance(v, "asked") for v in ii_all)
    ctrl = {p: [v for v in (pt(p, POOLED, "before"), *(pt(p, k, "before") for k in tok_keys)) if v is not None]
            for p in ("picker", "asked")}  # fmt: skip
    control_ok = all(at_chance(v, p) for p, vs in ctrl.items() for v in vs)
    raw = "distributed" if distributed else "flag" if flag else "neither" if neither else "between"
    label = "uninterpretable" if raw in ("distributed", "flag") and not control_ok else raw
    return {"label": label, "raw": raw, "control_ok": control_ok, "per_token": bool(i_tok),
            "i_pooled": i_pool, "i_token_max": i_tok_max, "ii_pooled": ii_pool,
            "ii_token_max": max((v for v in ii_tok.values() if v is not None), default=None),
            "control_max": {p: max(vs, default=None) for p, vs in ctrl.items()},
            "why": f"(i) pooled {i_pool:.2f}, per-token max {'-' if i_tok_max is None else f'{i_tok_max:.2f}'} over "
                   f"{len(i_tok)} keys; (ii) pooled {ii_pool:.2f}, best {ii_best:.2f}; locker-first control "
                   f"{'at chance' if control_ok else 'above chance'} (max (i) "
                   f"{max(ctrl['picker'], default=float('nan')):.2f}, (ii) {max(ctrl['asked'], default=float('nan')):.2f})"}  # fmt: skip


def model_label(by_layer: dict[str, dict]) -> str:
    labs = [r["label"] for r in by_layer.values()]
    for lab in ("distributed", "flag", "uninterpretable"):
        if lab in labs:
            return lab
    return "neither" if labs and all(lab == "neither" for lab in labs) else "between"


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "probe_rows.jsonl").exists():
        target = {r: t for t, r in {**RUNS, **COVERAGE_RUNS}.items()}.get(run)
        assert target, f"no 49.3 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "label": "pending", "why": "no rows here"}
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "probe_rows.jsonl")
    keys = rule_keys(rows)
    layers = {str(la): layer_result(src, la, rows, n_boot) for la in m["layers"]}
    rules = {la: rule(r, keys) for la, r in layers.items()}
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "layers": m["layers"], "status": "tested",
            "label": model_label(rules), "rules": rules, "results": layers, "rule_keys": keys,
            "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """49.3's verdict (sealed until Q49.3), or with coverage (batch 52 C) the same rule on the given coverage runs alone:
    no seal guard, "no prediction" in place of Dan's answer, no pending rows, written to x52_probe49-<UTC>/."""
    answer = f"{NO_PREDICTION}; rule first scored in {SCORED}" if coverage else dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [mm["target"] for mm in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    known = set(COVERAGE_RUNS) if coverage else set(MODELS)
    assert set(targets) <= known, f"49.3 runs on {sorted(known)}, not {sorted(set(targets) - known)}"
    if not coverage:
        models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "label": "pending", "why": "no run given"}
                   for t in MODELS if t not in targets]  # fmt: skip
    out = RESULTS / f"{'x52_probe49' if coverage else 'x49_3'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 49.3: the locker-after link, a pooled probe over the locker sentence", "",
             f"Batch 49, test {TEST} (jobs/c3/batch49.yaml; {QUESTION}, Dan: {answer}). Clean-design scenes (45m), the "
             "lookup's O prompt; states at every token of each locker sentence and the sentence mean, at L // 2 and L. "
             "Probes (48.3's ridge, 5 folds, the sentence's item held out, seed 0): " + "; ".join(PROBE_TEXT.values())
             + f". Cluster bootstrap over the sentence's item ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE} As computed: per layer on points (EPS 1e-9); 'every per-token' over the "
             f"keys in >= {KEY_SHARE} of the rule cell's rows; 'at chance' = point <= chance + {CHANCE_MARGIN}; a "
             "distributed / flag label with the locker-first control above chance reads 'not interpretable'; a model "
             "is distributed (flag) if it holds at L or L // 2, neither if neither at both, else in between.", "",
             "| model | run | label | layer | layer's label (raw) | control at chance | why |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            lines.append(f"| {mm['target']} | {mm['run']} | pending ({mm['why']}) | | | | |")
            continue
        for la, r in mm["rules"].items():
            lines.append(f"| {mm['target']} | {mm['run']} | {LABELS[mm['label']]} | L{la} | {LABELS[r['label']]} "
                         f"({r.get('raw', '-')}) | {r.get('control_ok', '-')} | {r['why']} |")  # fmt: skip
    for probe in PROBES:
        lines += ["", f"{PROBE_TEXT[probe]}: per view, locker-after (rule cell) / locker-first (control)"
                  + ("" if probe == "asked" else "; the other items' sentences beside") + ".", "",
                  "| model | layer | view | after | before | after, other sentences | before, other sentences |",
                  "|---|---|---|---|---|---|---|"]  # fmt: skip
        for mm in models:
            if mm["status"] != "tested":
                continue
            for la, res in mm["results"].items():
                for view, c in res["probes"][probe].items():
                    cells = [f"{fmt(c[k]['accuracy'])} (n {c[k]['n']})" if k in c else "" for k in
                             ("after", "before", "after_others", "before_others")]  # fmt: skip
                    lines.append(f"| {mm['target']} | L{la} | {view} | " + " | ".join(cells) + " |")
    lines += ["", "Scenes (descriptive):", ""]
    for mm in models:
        if mm["status"] == "tested":
            p = mm["plan"]
            lines.append(f"- {mm['target']} ({mm['run']}): {p['scenes']} scenes {p['groups']} (dropped "
                         f"{p['dropped'] or 'none'}); {p['rows']} sentence rows {p['rows_by_stratum']}; rule cells "
                         f"{p['rule_cell_rows']}; rule keys {mm['rule_keys']}; {p['names']} names.")  # fmt: skip
    if coverage:
        lines[2] = lines[2].replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ")
    (out / "x49_3.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1,
                                               default=str) + "\n")  # fmt: skip
    (out / "x49_3.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(name: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, tok=None) -> Path:
    """The verify-pack view: k random locker-after scenes of the run (seed 0), the prompt as the model reads it with
    the bridge sentence's tokens keyed, the scene's pickers and the probe labels of its sentences."""
    assert dan_answer(), f"sealed: {PREDICTIONS} has no committed answer to {QUESTION}"
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    if tok is None:
        from bridge_jspace.review import checks as RC

        tok = RC.tokenizer(m["model"]["target"])
    items = [it for it in X.read_jsonl(src / "cases.jsonl") if it["group"] == "after"]
    out = src / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# 49.3 view: {name}", "", f"Model {m['model']['target']}, layers {m['layers']}. {min(k, len(items))} "
             f"random locker-after scenes of {len(items)} (seed {seed}); the prompt as the model reads it, the bridge "
             "item's locker sentence's tokens with their probe keys. UNVERIFIED.", ""]  # fmt: skip
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"## {it['scene']} ({it['domain']}): {it['asked']['person']} picked {it['entity']}", "",
                  "| slot | sentence | picker | stratum | (i) label | (ii) label |", "|---|---|---|---|---|---|"]  # fmt: skip
        for s in it["sentences"]:
            lines.append(f"| {s['k'] + 1} | {s['sentence']} | {s['picker'] or '-'} | {s['stratum'] or '-'} | "
                         f"{s['picker'] or '-'} | {'yes' if s['asked'] else 'no'} |")  # fmt: skip
        lines += ["", "```", keyed_prompt(tok, it), "```", ""]
    (out / "examples.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run / view: the run name (results/x49_probe/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 49.3 runs (9B, Muse)")
    ap.add_argument("--why", default=f"batch 49, test {TEST} (jobs/c3/batch49.yaml; {QUESTION})")
    ap.add_argument("--out", type=Path, default=None, help="plan: write the counts and the prompts into this folder")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.out)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, a.coverage)
    else:
        assert a.name, "view needs --name"
        stage_view(a.name)


if __name__ == "__main__":
    main()
