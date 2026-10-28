"""Batch 47, test 47.13 (jobs/c3/batch47.yaml, amendment 4; Q47.13, SEALED): does the address probe predict the
lookup's errors?

Data (Dan): unedited scenes where the lookup answers wrong, excluded by the gate. The source Dan named, x0_probe_power
(results/x0_probe/*_x0_probe_v4, d1_topics_v4), holds the bridge-word state of every scene but no read of the lookup:
x0_probe records states only. On the sibling set d1_topics_v5 (x0_replicate, the same code and models) the unedited
lookup is wrong on 0 of 528 (9B), 0 of 528 (27B) and 3 of 463 (Muse) scenes, so the d1 sets hold almost no lookup
errors. The one local source with a stored read AND a stored bridge-word state at the layer fixed in advance for
EVERY scene, wrong ones included, is the varied-scene run (x0b_generalize/<model>_x0b_v2: 7 domains, levels 0-2,
prose / json / table, 3-9 locker statements): the lookup is wrong on 100 of 2,258 (9B), 5 of 2,258 (27B), 32 of 2,535
(Muse). `count` runs on it now (the agent's substitution of the data source, stated in the manifest; Dan may
override); `gpu` (one small job per model, jobs/c3/x47_13_<model>.yaml) adds the lens's top item at the bridge word on
every scene of that run, and the lookup's read on every d1_topics_v4 scene so Dan's named source can be counted too.

Read (per model): the slot probe's predicted slot (probe (b): one-hot ridge on the bridge-word states of the scenes the
lookup gets right, per format and locker order as x0b's own probe (b), the wrong item's bridge entity held out of its
training set, the penalty by entity-held-out CV on the training scenes) against the slot of the model's wrong answer
(the locker statement that states the answered digit; none if no statement does); beside it the majority slot of the
training scenes (Dan's "predict the most common slot"), the layout-conditioned majority (given how many locker
statements precede the asked pick, of how many) and the pick-ordinal-conditioned one; and the lens's top item at the
bridge word among the scene's locker items (J++ readout, as the digit check's; from `gpu`).

Rule (verbatim, batch47.yaml 47.13): "The address predicts the error" if they match in >= 0.5 of wrong items (chance ~
0.33 with three lockers; report the layout baseline too), and the lens's top item at the bridge word is still the right
item in >= 0.8 of those (the identity was right; the address was wrong). As computed (fixed by the agent before any
count; Dan may override): the denominator is every wrong item of the run (a wrong answer that no locker statement
states, or a group too small for a probe, counts as no match); "of those" = the matched wrong items (the lens's rate on
all wrong items beside); a model with fewer than N_MIN = 30 wrong items is "not tested"; cluster bootstrap over bridge
items (10,000, seed 0); a value at a bar is at the bar (EPS). The verdict refuses until Dan's "Dan:" line under Q47.13
in predictions/2026-10-28_dan.md is non-empty at HEAD; `count` writes per-item rows and counts only, no match rate.

uv run python scripts/x47_errors.py count --name <run>              # CPU (BJ_TARGET picks the model); sealed rows
uv run python scripts/x47_errors.py gpu --name <run>                # GPU: lens top items (x0b and v4), v4 lookup reads
uv run python scripts/x47_errors.py verdict --runs <run> ...        # CPU, refuses until Q47.13 is answered
Writes results/x47_errors/<run>-<UTC>/{manifest.json, plan.json, rows.jsonl, groups.json}, <run>-gpu-<UTC>/{lens.jsonl,
v4_reads.jsonl}, x47_13-<UTC>/{x47_errors.json, x47_errors.md}. UNVERIFIED.
"""

from __future__ import annotations

import argparse
import collections
import json
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
from scripts import x0b_generalize as B

EXP = "x47_errors"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.13"
# the scenes with a stored read and a stored bridge-word state for every scene (x0b_generalize's run per model)
SOURCES = {"qwen3.5-9b": "qwen35_9b_x0b_v2", "qwen3.6-27b": "x0b_v2_27b", "muse-glimmer-30b": "muse30b_x0b_v2"}
# the source Dan named: states for every scene, no read (x0_probe records states only); `gpu` reads the lookup there
NAMED = {
    "qwen3.5-9b": "qwen35_9b_x0_probe_v4",
    "qwen3.6-27b": "x0_probe_v4_27b",
    "muse-glimmer-30b": "muse30b_x0_probe_v4",
}
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_errors", "qwen3.6-27b": "x47_errors_27b", "muse-glimmer-30b": "muse30_x47_errors"}
MATCH_BAR, LENS_BAR, N_MIN = 0.5, 0.8, 30
EPS = 1e-9
RULE = ('"The address predicts the error" if the probe\'s slot matches the wrong answer\'s slot in >= 0.5 of wrong items '
        "(chance ~ 0.33 with three lockers; the layout baseline beside), and the lens's top item at the bridge word is "
        "still the right item in >= 0.8 of those")  # fmt: skip
BASELINES = ("majority", "layout", "structure")


def stamp() -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


# ---- the items ----------------------------------------------------------------------------------------------------


def lookup_reads(src: Path) -> dict[str, dict]:
    """Per scene, the unedited lookup's chat read: what it said, whether that was right, and whether the decisive read
    (the top token) was right too. Wrong = said wrong; a scene said right but read wrong is dropped (it is excluded by
    the gate, but its answer is not wrong: its said digit would match the gold slot)."""
    out = {}
    for r in X.read_jsonl(src / "competence.jsonl"):
        if r["rendering"] == "chat" and r["reader"] == X.LOOKUP and r["variant"] == "org":
            out[r["scene"]] = {"said": r["said"], "right": bool(r["right"]), "read_right": bool(r["read_right"])}
    return out


def locker_ordinals(case: dict) -> dict[str, int]:
    """Each locker item's statement ordinal among the scene's locker statements (context order), as x0b's probe (b)."""
    f, ctx = case["facts"], case["context"]
    start = {t: ctx.index(B.statements(case, f["person"], t)[1]) for t in f["locker"]}
    order = sorted(start.values())
    return {t: order.index(s) for t, s in start.items()}


def slot_of(case: dict, said: Any) -> int | None:
    """The ordinal of the locker statement stating the answered digit; None if the answer is not a digit, no statement
    states it, or more than one does."""
    if said is None or not str(said).isdigit():
        return None
    things = [t for t, n in case["facts"]["locker"].items() if int(n) == int(said)]
    return locker_ordinals(case)[things[0]] if len(things) == 1 else None


def item_rows(cases: list[dict], reads: dict[str, dict]) -> list[dict]:
    """One row per scene with a stored read: the scene's features, the gold slot, the lookup's answer and, when wrong,
    the slot of its answer."""
    rows = []
    for c in cases:
        if c["scene"] not in reads:
            continue
        rd = reads[c["scene"]]
        if rd["right"] and not rd["read_right"]:
            continue
        o = B.ordinals(c)
        rows.append({"scene": c["scene"], "entity": c["bridge"], "format": c["format"], "order": c["order"],
                     "domain": c["domain"], "level": c["level"], "numbers": c["numbers"],
                     "n_lockers": len(c["facts"]["locker"]), "gold": c["readers"][X.LOOKUP]["answer"],
                     "locker_index": o["locker_index"], "pick_index": o["pick_index"], "layout": o["layout"],
                     "said": rd["said"], "right": rd["right"],
                     "wrong_slot": None if rd["right"] else slot_of(c, rd["said"])})  # fmt: skip
    return rows


# ---- the probe on the wrong items ---------------------------------------------------------------------------------


def group_key(it: dict) -> tuple[str, str]:
    return it["format"], it["order"]


def predict_wrong(h: np.ndarray, items: list[dict]) -> tuple[list[dict], list[dict]]:
    """For every wrong item: the slot probe's prediction with the item's entity held out of the training scenes (the
    right scenes of its format and locker order), the majority, layout and structure baselines from the same training
    scenes, and the penalty used; per group, the probe's entity-held-out CV accuracy on the right scenes (descriptive).
    A group with fewer than 2 * K_OUTER right scenes or K_OUTER entities gets no probe (prediction None)."""
    groups = sorted({group_key(it) for it in items if not it["right"]})
    preds, summary = [], []
    for g in groups:
        pool = [i for i, it in enumerate(items) if it["right"] and group_key(it) == g]
        wrong = [i for i, it in enumerate(items) if not it["right"] and group_key(it) == g]
        y_pool = [items[i]["locker_index"] for i in pool]
        ents = [items[i]["entity"] for i in pool]
        usable = len(pool) >= 2 * P.K_OUTER and len(set(ents)) >= P.K_OUTER and len(set(y_pool)) >= 2
        info: dict[str, Any] = {"format": g[0], "order": g[1], "right_scenes": len(pool), "entities": len(set(ents)),
                                "wrong_items": len(wrong), "probe": usable}  # fmt: skip
        if usable:
            rel = P.select_penalty(h[pool], y_pool, ents)
            cv, _, _ = P.cv_predict(h[pool], y_pool, ents, True)
            info |= {"penalty": rel, "cv_accuracy_right": float(np.mean([p == t for p, t in zip(cv, y_pool, strict=True)])),
                     "classes": len(set(y_pool)), "majority_share": max(collections.Counter(y_pool).values()) / len(y_pool)}  # fmt: skip
        summary.append(info)
        for i in wrong:
            row = {"scene": items[i]["scene"], "probe_slot": None, "penalty": None}
            tr = [j for j in pool if items[j]["entity"] != items[i]["entity"]]
            ytr = [items[j]["locker_index"] for j in tr]
            if tr:
                row["majority_slot"] = P.mode(ytr)
                for b, key in (("layout", "layout"), ("structure", "pick_index")):
                    same = [items[j]["locker_index"] for j in tr if items[j][key] == items[i][key]]
                    row[f"{b}_slot"] = P.mode(same) if same else row["majority_slot"]
            else:
                row |= {f"{b}_slot": None for b in BASELINES}
            if usable and len(tr) >= P.K_OUTER and len(set(ytr)) >= 2:
                row["probe_slot"] = P.ridge(h[tr], ytr, h[[i]], (info["penalty"],))[0][0]
                row["penalty"] = info["penalty"]
            preds.append(row)
    return preds, summary


def stage_count(name: str, source: str | None = None) -> Path:
    pins.check_run_name(name)
    run = source or SOURCES[pins.TARGET]
    src = pins.RESULTS_DIR / "x0b_generalize" / run
    out = RESULTS / f"{name}-{stamp()}"
    out.mkdir(parents=True, exist_ok=False)
    sm = json.loads((src / "manifest.json").read_text())
    m = {"exp": EXP, "stage": "count", "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "why": f"batch 47, test 47.13 ({SPEC.relative_to(pins.REPO_ROOT)}; {QUESTION}, sealed)",
         "source": {"run": f"x0b_generalize/{run}", "set": sm.get("set"), "layer": sm.get("predicted"),
                    "model": sm.get("model"), "code": sm.get("code")},
         "named_source": {"run": f"x0_probe/{NAMED.get(pins.TARGET)}", "why_not": "x0_probe stores the states of every "
                          "scene but no read of the lookup; `gpu` reads it there (v4_reads.jsonl)"},
         "substitution": "the data source is the varied-scene run (x0b_v2), the one local source with a stored read and "
                         "a stored bridge-word state for every scene, wrong ones included; the agent's choice, stated "
                         "before any count; Dan may override",
         "model": pins.model_pin(), "switches": switches(), "code": pins.git_state(), "position": "the asked person's bridge word, org run, chat",
         "probe": {"target": "the bridge's locker statement ordinal (x0b probe (b))", "groups": "format x locker order",
                   "training": "the scenes the lookup reads right, the wrong item's bridge entity held out",
                   "penalty": "entity-held-out CV on the training scenes (x0_probe.select_penalty)",
                   "folds": {"outer": P.K_OUTER, "inner": P.K_INNER, "penalties": list(P.RELS)}},
         "rule": RULE, "bars": {"match": MATCH_BAR, "lens": LENS_BAR, "n_min": N_MIN},
         "seeds": {"bootstrap": X.BOOT_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"per-item rows and counts only; no match rate until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    cases = [c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"]
    z = np.load(src / "states.npz")
    h_by = {str(s): i for i, s in enumerate(z["scene"])}
    reads = lookup_reads(src)
    items = [r for r in item_rows(cases, reads) if r["scene"] in h_by]
    h = z["h"].astype(np.float64)[[h_by[r["scene"]] for r in items]]
    preds, groups = predict_wrong(h, items)
    pred_by = {p["scene"]: p for p in preds}
    rows = [{**it, **{k: v for k, v in pred_by.get(it["scene"], {}).items() if k != "scene"}}
            for it in items if not it["right"]]  # fmt: skip
    X.write_jsonl(out / "rows.jsonl", rows)
    (out / "groups.json").write_text(json.dumps(groups, indent=1) + "\n")
    plan = {"scenes": len(items), "right": sum(r["right"] for r in items), "wrong": len(rows),
            "said_right_read_wrong_dropped": sum(r["right"] and not r["read_right"] for r in reads.values()),
            "wrong_with_a_slot": sum(r["wrong_slot"] is not None for r in rows),
            "wrong_with_a_probe": sum(r.get("probe_slot") is not None for r in rows),
            "wrong_entities": len({r["entity"] for r in rows}),
            "wrong_by_format": dict(collections.Counter(r["format"] for r in rows)),
            "wrong_by_order": dict(collections.Counter(r["order"] for r in rows)),
            "wrong_by_lockers": {str(k): v for k, v in sorted(collections.Counter(r["n_lockers"] for r in rows).items())},
            "tested": len(rows) >= N_MIN}  # fmt: skip
    (out / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
    print(json.dumps(plan), flush=True)
    print(f"wrote {out} (sealed: rows and counts, no match rate)", flush=True)
    return out


# ---- the GPU stage: the lens's top item, and the named source's reads ---------------------------------------------


def item_token(tok, ids: list[int], pos: int, thing: str) -> int:
    """The first token of `thing` where the bridge word sits: as the continuation of the prompt up to pos."""
    from bridge_jspace.readout import continuation_first_token

    return continuation_first_token(tok, tok.decode(ids[:pos]), thing)


def lens_rows(model, lens, layer: int, cases: list[dict], h: np.ndarray, scenes: list[str]) -> list[dict]:
    """Per scene: the J++ readout's order of the scene's locker items at the bridge word (the item tokens' lens vectors
    against the stored state, as the digit check ranks the digits), the top item and the bridge's rank. A scene whose
    bridge token is not reproduced by item_token is dropped (counted by the caller)."""
    import torch

    by = {s: i for i, s in enumerate(scenes)}
    rows = []
    for c in cases:
        if c["scene"] not in by:
            continue
        ids, pos = c["readers"][X.LOOKUP]["ids"]["org"], c["pos"]
        things = list(c["facts"]["locker"]) if "facts" in c else [c["bridge"]]
        toks = {t: item_token(model.tokenizer, ids, pos, t) for t in things}
        if toks[c["bridge"]] != ids[pos]:
            rows.append({"scene": c["scene"], "dropped": "the bridge token is not reproduced"})
            continue
        vec = lens.vectors(layer, torch.tensor([toks[t] for t in things], device="cuda"), unit=False)
        scores = (vec @ torch.tensor(h[by[c["scene"]]], dtype=torch.float32, device="cuda")).tolist()
        order = [t for _, t in sorted(zip(scores, things, strict=True), key=lambda x: -x[0])]
        rows.append({"scene": c["scene"], "bridge": c["bridge"], "items": things, "order": order, "top": order[0],
                     "bridge_rank": order.index(c["bridge"]) + 1, "top_is_bridge": order[0] == c["bridge"]})  # fmt: skip
    return rows


def stage_gpu(name: str) -> Path:
    """The lens's top item at the bridge word on every scene of the x0b source and of the named source (from their
    stored states), and the lookup's unedited read on every scene of the named source (d1_topics_v4), which x0_probe
    never took. Sealed: no rate is printed."""
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    pins.check_run_name(name)
    out = RESULTS / f"{name}-gpu-{stamp()}"
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "stage": "gpu", "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "why": f"batch 47, test 47.13 ({SPEC.relative_to(pins.REPO_ROOT)}; {QUESTION}, sealed): the lens's top item",
         "model": pins.model_pin(), "switches": switches(), "code": pins.git_state(), "lens": "jpp",
         "sources": {"x0b": f"x0b_generalize/{SOURCES[pins.TARGET]}", "named": f"x0_probe/{NAMED[pins.TARGET]}"}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, "jpp")
    src = pins.RESULTS_DIR / "x0b_generalize" / SOURCES[pins.TARGET]
    layer = json.loads((src / "manifest.json").read_text())["predicted"]
    z = np.load(src / "states.npz")
    cases = [c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"]
    rows = [{"source": "x0b", **r} for r in lens_rows(model, lens, layer, cases, z["h"], [str(s) for s in z["scene"]])]
    named = pins.RESULTS_DIR / "x0_probe" / NAMED[pins.TARGET]
    nm = json.loads((named / "manifest.json").read_text())
    v4, _ = X.build_cases(model.tokenizer, nm["set"])
    v4 = [c for c in v4 if c["rendering"] == "chat"]
    z4 = np.load(named / "states.npz")
    rows += [
        {"source": "v4", **r} for r in lens_rows(model, lens, nm["layer"], v4, z4["h"], [str(s) for s in z4["scene"]])
    ]
    X.write_jsonl(out / "lens.jsonl", rows)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(model.tokenizer), device="cuda")
    reads = []
    with torch.no_grad():
        for c in progress(v4, "the lookup's unedited read (v4 scene)"):
            rd = c["readers"][X.LOOKUP]
            ids = torch.tensor([rd["ids"]["org"]], device="cuda")
            text = model.generate_batch(ids, X.GEN_TOKENS, [{}])[0]
            logits, _ = X.read_logits(model, rd["ids"]["org"], [{}], "chat", c["space"], ws)
            said = S.said(text, "digit")
            reads.append({"scene": c["scene"], "rendering": "chat", "reader": X.LOOKUP, "variant": "org", "greedy": text,
                          "said": said, "right": said == rd["answer"], "read_right": int(logits[0].argmax()) == rd["tok_A"],
                          "cand_right": X.first_among(logits[0], rd["tok_A"], digits)})  # fmt: skip
    X.write_jsonl(out / "v4_reads.jsonl", reads)
    dropped = sum("dropped" in r for r in rows)
    print(
        f"wrote {out}: {len(rows)} lens rows ({dropped} dropped), {len(reads)} v4 reads, "
        f"{sum(not r['right'] for r in reads)} wrong (sealed: no rate)",
        flush=True,
    )
    return out


# ---- verdict (CPU, sealed) ----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.13 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
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


def rate(hits: list[int], entities: list[str], n_boot: int) -> list[float] | None:
    """[point, lo, hi] of a share over items, cluster bootstrap over bridge entities; None without items."""
    if not hits:
        return None
    r = X.resampled_rates({"x": hits}, entities, n_boot)["x"]
    return [float(np.mean(hits)), *X.interval(r)]


def rates(rows: list[dict], lens: dict[str, dict] | None, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """The rule's numbers on one model's wrong items: the probe's and each baseline's match with the wrong answer's
    slot (over every wrong item: no slot or no probe = no match; over the items with a slot beside), the probe's match
    with the gold slot, and the lens's top item being the bridge (on the matched items, the rule's 'of those', and on
    every wrong item with a lens row)."""
    ents = [r["entity"] for r in rows]
    out: dict[str, Any] = {"n": len(rows), "n_slot": sum(r["wrong_slot"] is not None for r in rows),
                           "n_probe": sum(r.get("probe_slot") is not None for r in rows),
                           "entities": len(set(ents)), "chance": None, "match": {}, "match_with_slot": {}}  # fmt: skip
    if rows:
        out["chance"] = float(np.mean([1 / r["n_lockers"] for r in rows]))
    with_slot = [i for i, r in enumerate(rows) if r["wrong_slot"] is not None]
    for k in ("probe", *BASELINES):
        hit = [int(r.get(f"{k}_slot") is not None and r.get(f"{k}_slot") == r["wrong_slot"]) for r in rows]
        out["match"][k] = rate(hit, ents, n_boot)
        out["match_with_slot"][k] = rate([hit[i] for i in with_slot], [ents[i] for i in with_slot], n_boot)
    out["probe_gold"] = rate([int(r.get("probe_slot") == r["locker_index"]) for r in rows], ents, n_boot)
    matched = [i for i, r in enumerate(rows) if r.get("probe_slot") is not None and r["probe_slot"] == r["wrong_slot"]]
    out["n_matched"] = len(matched)
    if lens is None:
        out["lens"] = None
    else:
        have = [i for i, r in enumerate(rows) if r["scene"] in lens and "top" in lens[r["scene"]]]
        hit = {i: int(lens[rows[i]["scene"]]["top_is_bridge"]) for i in have}
        out["lens"] = {"n": len(have), "right_all": rate([hit[i] for i in have], [ents[i] for i in have], n_boot),
                       "right_matched": rate([hit[i] for i in matched if i in hit],
                                             [ents[i] for i in matched if i in hit], n_boot),
                       "n_matched_with_lens": sum(i in hit for i in matched)}  # fmt: skip
    return out


def rule(r: dict[str, Any]) -> dict[str, Any]:
    """The rule on one model's rates: not tested below N_MIN wrong items; pending without the lens stage; else holds
    iff the probe's match >= MATCH_BAR and the lens is right on >= LENS_BAR of the matched items (points, EPS)."""
    if r["n"] < N_MIN:
        return {"status": "not tested", "holds": False, "why": f"{r['n']} wrong items, fewer than {N_MIN}"}
    match = r["match"]["probe"][0] >= MATCH_BAR - EPS
    if r["lens"] is None or r["lens"]["right_matched"] is None:
        return {"status": "pending", "holds": False, "match_holds": match,
                "why": "no lens row (the gpu stage has not landed, or no matched item has one)"}  # fmt: skip
    lens = r["lens"]["right_matched"][0] >= LENS_BAR - EPS
    return {"status": "scored", "holds": bool(match and lens), "match_holds": match, "lens_holds": lens}


def latest(pattern: str) -> Path | None:
    found = sorted(RESULTS.glob(pattern), key=lambda p: p.name[-16:])
    return found[-1] if found else None


def rel(path: Path) -> str:
    return str(path.relative_to(pins.REPO_ROOT)) if path.is_relative_to(pins.REPO_ROOT) else str(path)


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """The newest count folder of `run` (and its newest gpu folder, if any): the rates, the rule and the split by
    format (descriptive)."""
    count = latest(f"{run}-2*")
    assert count is not None, f"no count folder results/x47_errors/{run}-<UTC>/"
    m = json.loads((count / "manifest.json").read_text())
    rows = X.read_jsonl(count / "rows.jsonl")
    gpu = latest(f"{run}-gpu-*")
    lens = None
    if gpu is not None:
        lens = {r["scene"]: r for r in X.read_jsonl(gpu / "lens.jsonl") if r["source"] == "x0b"}
    r = rates(rows, lens, n_boot)
    by_format = {
        f: rates([x for x in rows if x["format"] == f], lens, n_boot) for f in sorted({x["format"] for x in rows})
    }
    by_order = {
        o: rates([x for x in rows if x["order"] == o], lens, n_boot) for o in sorted({x["order"] for x in rows})
    }
    return {"run": run, "count": rel(count), "gpu": rel(gpu) if gpu else None, "target": m["model"]["target"],
            "source": m["source"], "layer": m["source"].get("layer"), "plan": json.loads((count / "plan.json").read_text()),
            "groups": json.loads((count / "groups.json").read_text()), "rates": r, "rule": rule(r),
            "by_format": by_format, "by_order": by_order}  # fmt: skip


def fmt(v: list[float] | None) -> str:
    return "-" if v is None else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    out = RESULTS / f"x47_13-{stamp()}"
    out.mkdir(parents=True)
    lines = ["# 47.13: does the address probe predict the lookup's errors?", "",
             f"Batch 47, test 47.13 (jobs/c3/batch47.yaml, amendment 4; {QUESTION}, Dan: {answer}). Unedited scenes "
             "where the lookup answers wrong, from the varied-scene runs (x0b_v2; the d1 sets hold almost no lookup "
             "errors, see the script's docstring); the slot probe trained on the scenes the lookup gets right (per "
             "format and locker order, the wrong item's entity held out) against the slot of the wrong answer; the "
             f"lens's top item at the bridge word from the gpu stage. Cluster bootstrap over bridge items ({n_boot}, "
             f"seed {X.BOOT_SEED}). UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             "| model | run | status | wrong items (with a slot / with a probe; entities) | chance | probe matches the "
             "wrong slot | majority | layout | structure | probe = gold slot | lens top item right: matched / all | holds |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        r, v = m["rates"], m["rule"]
        lens = "-" if r["lens"] is None else f"{fmt(r['lens']['right_matched'])} / {fmt(r['lens']['right_all'])}"
        lines.append(f"| {m['target']} | {m['run']} | {v['status']} | {r['n']} ({r['n_slot']} / {r['n_probe']}; "
                     f"{r['entities']}) | {r['chance'] if r['chance'] is None else f'{r['chance']:.2f}'} | "
                     f"{fmt(r['match']['probe'])} | {fmt(r['match']['majority'])} | {fmt(r['match']['layout'])} | "
                     f"{fmt(r['match']['structure'])} | {fmt(r['probe_gold'])} | {lens} | "
                     f"{'yes' if v['holds'] else 'no'} ({v.get('why', '')}) |")  # fmt: skip
    lines += ["", "Over the wrong items that have a slot (a locker statement states the answered digit):", "",
              "| model | n | probe | majority | layout | structure |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        r = m["rates"]
        lines.append(
            f"| {m['target']} | {r['n_slot']} | "
            + " | ".join(fmt(r["match_with_slot"][k]) for k in ("probe", *BASELINES))
            + " |"
        )
    lines += ["", "By format and by locker order (descriptive):", "",
              "| model | split | n | probe matches the wrong slot | majority | layout | probe = gold slot |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        for name, r in (*m["by_format"].items(), *m["by_order"].items()):
            lines.append(f"| {m['target']} | {name} | {r['n']} | {fmt(r['match']['probe'])} | {fmt(r['match']['majority'])} "
                         f"| {fmt(r['match']['layout'])} | {fmt(r['probe_gold'])} |")  # fmt: skip
    lines += ["", "The probe on the right scenes (entity-held-out CV accuracy per group; descriptive):", "",
              "| model | format | order | right scenes | entities | wrong items | probe | CV accuracy | majority share |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        for g in m["groups"]:
            acc = f"{g['cv_accuracy_right']:.2f}" if g.get("probe") else "-"
            maj = f"{g['majority_share']:.2f}" if g.get("probe") else "-"
            lines.append(f"| {m['target']} | {g['format']} | {g['order']} | {g['right_scenes']} | {g['entities']} | "
                         f"{g['wrong_items']} | {'yes' if g['probe'] else 'no'} | {acc} | {maj} |")  # fmt: skip
    (out / "x47_errors.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "x47_errors.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["count", "gpu", "verdict"])
    ap.add_argument("--name", help="count / gpu: the run name (results/x47_errors/<name>-<UTC>/)")
    ap.add_argument("--source", default=None, help="count: an x0b_generalize run instead of SOURCES[target]")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the runs (9B, 27B, Muse)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "count":
        assert a.name, "count needs --name"
        stage_count(a.name, a.source)
    elif a.stage == "gpu":
        assert a.name, "gpu needs --name"
        stage_gpu(a.name)
    else:
        stage_verdict(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
