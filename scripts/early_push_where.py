"""early_push_where (D4 v2, 2026-10-22): can the lens write a STATED bridge where it sits?

Background (UNVERIFIED; README slide 6): at layer 20 on Qwen3.6-27B, a lens push v_X - v_I (8x) on the question's
subject phrase switches bridges the model recalls (memory -> prompt 73%, memory -> memory 84%) but not bridges stated in
the prompt (prompt -> prompt 1%, prompt -> memory 2%). The stated bridge was pushed at the question, but it sits at its
own sentence ("Clara's pet is a cow.") until layer ~24 and over the whole context until ~44 (statement_positions
d1_map_n80_v1). The null for stated bridges may only mean that the push missed the bridge.

Design. Animal suite (wording A), the four families on the same scenes (suite_split map_A8_v1's cases, the first n per
family), Qwen3.6-27B, J++. Push positions of the unedited prompt:
  b  the question's subject phrase ("Clara's pet", "the animal known for mooing"): slide 6's own (replication anchor)
  s  the bridge's owner sentence ("Clara's pet is a cow."): where a stated bridge sits early
  w  the bridge's word in that sentence ("cow")
  c  the whole context (every sentence), layers 28-44 only: where a stated bridge sits later
At each layer of L (12-44, every 4) and scale of S (1, 2, 4, 8), each pushed position gets scale x the scene's reference
norm (early_push's: the RMS of C's copy delta over suite_split's question group, pooled over the scene's families), along
  lens      v_X - v_I (unit J++ vectors at that layer; X = the bridge of the C prompt)
  random    a random direction at the same per-position norms (one generator per item)
  offscene  v_Y - v_I, Y an animal not in the scene whose leg count differs from I's and X's (one Y per scene, seeded)
Text edits as early_push (E-name, E-insert, E-head, E-cue, E-unrelated); E-cue is the C prompt, which for prompt -> *
rebinds the stated sentence to X: the input-edit limit at s. Read: suite_split's (the top token after 'Answer:' and a
space): A (unchanged), b (X's answer), y (Y's legs; recall families only), oc (another in-context answer), other.
Families: prompt -> memory (BR) is the positive control (a stated bridge, a recalled answer: D1 found that the
lens-readable part of a stated bridge's change does the work there, 66%); prompt -> prompt (BL) is the test; memory ->
prompt and memory -> memory (RL, RR) are off the path at s and w (their bridge comes from the cue) and the replication
anchor at b. Only items the model answers right unedited count.

Decision rule (fixed 2026-10-22 before the run; the controls agreed with Dan):
  select   on BR rows only: cells (subset s or w, layer, scale) where the lens push switches BR to X's answer in >= 30%
           with Wilson lower bound >= 0.20, and the random push switches <= 5%. Primary cell: the selected cell with the
           highest BR rate (ties: smaller scale, earlier layer, w before s). No selected cell: the lens does not write a
           stated bridge at its sentence even for recall, and BL is not interpretable there (reported).
  valid    at the primary cell, the lens push changes <= 10% of RL and of RR answers (off the path), and the random
           push switches <= 5% of BL.
  verdict  H-where (the stated null of slide 6 was a location artefact): BL switched >= 30% with lower bound >= 0.20.
           H-around (consistent with D1: the lookup does not use the lens-writable form of a stated bridge): BL switched
           <= 10% and the scene-paired bootstrap of BR - BL has its 2.5th percentile >= 0.20. Otherwise inconclusive.
  reported, not decisive: every cell; c; b at layer 20, 8x against slide 6 (RL 73%, RR 84%, BL 1%, BR 2%); offscene
           (BR to Y's legs, BL changed); the edits.

Rule v2 (fixed 2026-10-22 evening, after d4_where_27b and before the fresh-scene run; config "rule": "v2"). In
d4_where_27b the primary cell (w, layer 28, 8x) changed 25% of RR, so the verdict was "not valid" while other cells
passed. v2 moves the validity conditions into the selection: a cell is selected iff it passes v1's selection AND, at
that cell, the lens push changes <= 10% of RL and of RR and the random push switches <= 5% of BL. The primary cell is
the selected cell with the highest BR rate (v1's ties); the verdicts are v1's. Runs without "rule" in their config use
v1. Fresh scenes (config "scenes": "fresh"): n scenes sampled (seed FRESH_SEED) from those eligible in all four
families under suite_split's rule (every competence prompt right) and not in the map run at all.

Rule v2.1 (amended 2026-10-22 20:35 +0200, Dan, while d4_where_fresh_27b ran and before any of its results was
opened): v2 applied to d4_where_27b (already opened) picks the word at layer 16, 8x (recall 90%, lookup 20%:
inconclusive), while every valid cell at layers 20-36 has lookup 0%; at layer 16 the push moves lookups too (an input
edit by another name, or the lens writing the lookup early: open). So v2.1 = v2 with the decisive cell chosen among
valid cells at layers >= 20 (V21_MIN_LAYER); the valid cells below 20 are reported separately (below_v21). v2.1 was
written knowing the old data, so v2 stays the main rule (revised 20:55): both verdicts are reported, and a
disagreement is stated as such. v2.1 is written by `analyze --name N --rule v2.1` into <run>/analysis-v2.1-<stamp>/
(the run's own summary keeps v2).

Stages:  run --name N --why W [--n K] [--scenes map|fresh] [--rule v1|v2]   analyze --name N [--rule v2.1]
         figures --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts import early_push as EP
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp04_brew_parts import AddRows, null_rows

EXP = "early_push_where"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {"n": 100, "families": ["BL", "BR", "RL", "RR"], "map": "map_A8_v1", "wording": "A",
                            "layers": [12, 16, 20, 24, 28, 32, 36, 40, 44], "scales": [1.0, 2.0, 4.0, 8.0],
                            "context_layers": [28, 32, 36, 40, 44], "scenes": "map", "rule": "v1"}  # fmt: skip
WHERE = ("b", "s", "w", "c")
DIRS = ("lens", "random", "offscene")
SEED = 0
FRESH_SEED = 1
V21_MIN_LAYER = 20
SEL_RATE, SEL_LO, RAND_MAX, OFF_PATH_MAX = 0.30, 0.20, 0.05, 0.10
WHERE_RATE, WHERE_LO, AROUND_MAX, AROUND_GAP = 0.30, 0.20, 0.10, 0.20
SLIDE6 = {"RL": 0.73, "RR": 0.84, "BL": 0.01, "BR": 0.02}  # early_push d4_push_wording_b_v1, b, layer 20, 8x
BATCH = P.BATCH


# ---- positions and the off-scene animal (pure; tests/test_early_push_where.py) ---------------------------------------


def stated_positions(c: dict) -> dict[str, list[int]]:
    """Token positions of the bridge's owner sentence (s), the bridge's word in it (w) and the whole context (c) in the
    unedited prompt (early_push.augment's offsets)."""
    owner = c["people"][c["pets"].index(c["bridge"])]
    sent = S.WORDINGS["A"]["own"].format(p=owner, a=c["bridge"])
    ctx, rendered, offsets = c["context"], c["prompts"]["clean"], c["offsets"]
    assert rendered.count(ctx) == 1, f"{c['id']}: the context not once in the prompt"
    assert ctx.count(sent) == 1, f"{c['id']}: {sent!r} not once in the context"
    c0 = rendered.index(ctx)
    a = c0 + ctx.index(sent)
    wa = a + sent.rindex(c["bridge"])
    out = {"s": EP.overlapping(offsets, a, a + len(sent)), "w": EP.overlapping(offsets, wa, wa + len(c["bridge"])),
           "c": EP.overlapping(offsets, c0, c0 + len(ctx))}  # fmt: skip
    assert out["w"], f"{c['id']}: no tokens for the bridge's word"
    assert set(out["w"]) <= set(out["s"]) <= set(out["c"]), f"{c['id']}: nested positions"
    assert max(out["c"]) < min(c["subsets"]["b"]), f"{c['id']}: the context after the question"
    return out


def offscene_animal(c: dict) -> str:
    """An animal not in the scene whose leg count differs from the bridge's and X's, the same for the whole scene."""
    legs = {a: v[0] for a, v in S.ANIMALS.items()}
    used = set(c["pets"]) | {c["bridge"], c["cf_bridge"]}
    cands = sorted(a for a in legs if a not in used and legs[a] not in (legs[c["bridge"]], legs[c["cf_bridge"]]))
    return random.Random(f"{SEED}:{c['scene']}").choice(cands)


def role_of(top: int, cand: dict, y_tok: int | None) -> str:
    """A (unchanged), b (X's answer), y (the off-scene animal's answer), oc (another in-context answer), other."""
    if top in (cand["A"], cand["b"]):
        return "A" if top == cand["A"] else "b"
    if y_tok is not None and top == y_tok:
        return "y"
    return "oc" if top in cand["oc"] else "other"


def fresh_scenes(eligible: dict[str, set[str]], used: set[str], n: int, seed: int = FRESH_SEED) -> list[str]:
    """n scenes eligible in every family and not used, sampled by seed (sorted first, so the draw is reproducible)."""
    pool = sorted(set.intersection(*eligible.values()) - used)
    return random.Random(seed).sample(pool, min(n, len(pool)))


def fresh_cases(tok, cfg: dict) -> tuple[list[dict], dict]:
    """The fresh-scene cases (suite_split's eligibility, none of the map run's scenes); a scene whose C or O does not
    line up in one family is dropped in all four, so the families stay on the same scenes."""
    rows = [json.loads(x) for x in (P.RESULTS / cfg["map"] / "cases.jsonl").read_text().splitlines()]
    used = {r["scene"] for r in rows if r["family"] in cfg["families"]}
    eligible: dict[str, dict[str, dict]] = {}
    for fam in cfg["families"]:
        ok: dict[str, list[bool]] = collections.defaultdict(list)
        for line in P.competence_file(fam, cfg["wording"]).read_text().splitlines():
            r = json.loads(line)
            if r["family"] == fam:
                ok[r["id"]].append(r["correct"])
        good = {i for i, v in ok.items() if all(v)}
        eligible[fam] = {it["scene"]: it for it in S.load(fam, cfg["wording"]) if it["id"] in good}
    picked = fresh_scenes({f: set(v) for f, v in eligible.items()}, used, cfg["n"])
    cases, dropped = [], []
    for s in picked:
        try:
            cases += [{**eligible[f][s], **P.prepare(eligible[f][s], tok)} for f in cfg["families"]]
        except AssertionError:  # the comprehension fails before +=, so none of the scene's families is kept
            dropped.append(s)
    pool = len(set.intersection(*(set(v) for v in eligible.values())) - used)
    return cases, {"pool": pool, "picked": len(picked), "unaligned_dropped": dropped, "scenes": picked}


# ---- the decision (pure) ----------------------------------------------------------------------------------------------


def cell_rate(cell: dict[str, str], hit: str = "b") -> tuple[float, float, float]:
    """Wilson (rate, lo, hi) of items whose role is `hit` ('changed': anything but A)."""
    k = sum((r != "A") if hit == "changed" else (r == hit) for r in cell.values())
    return wilson(k, len(cell))


def cell_valid(cells: dict[tuple, dict[str, str]], key: tuple) -> tuple[bool, dict, tuple]:
    """At (subset, layer, scale): the lens push changes <= OFF_PATH_MAX of RL and of RR, the random push switches
    <= RAND_MAX of BL. Returns (valid, {RL, RR: changed}, BL random)."""
    off = {f: cell_rate(cells[(f, *key, "lens")], "changed") for f in ("RL", "RR") if cells.get((f, *key, "lens"))}
    bl_rand = cell_rate(cells.get(("BL", *key, "random"), {}))
    valid = all(v[0] <= OFF_PATH_MAX for v in off.values()) and (math.isnan(bl_rand[0]) or bl_rand[0] <= RAND_MAX)
    return valid, off, bl_rand


def decide(
    cells: dict[tuple, dict[str, str]],
    scene_of: dict[str, str],
    layers: list[int],
    scales: list[float],
    rule: str = "v1",
    min_layer: int = V21_MIN_LAYER,
) -> dict:
    """cells: (family, subset, layer, scale, dir) -> {item: role}, items answered right unedited only. rule v1:
    select on BR, then check validity at the primary cell; v2: only valid cells are selected; v2.1: v2 at layers
    >= min_layer (V21_MIN_LAYER on the 27B; scaled by depth on other models), the valid cells below in 'below_v21'."""
    assert rule in ("v1", "v2", "v2.1"), rule
    sel, below = [], []
    for sub in ("w", "s"):
        for la in layers:
            for sc in scales:
                br, rnd = cells.get(("BR", sub, la, sc, "lens")), cells.get(("BR", sub, la, sc, "random"))
                if not br or not rnd:
                    continue
                p, lo, _ = cell_rate(br)
                if p >= SEL_RATE and lo >= SEL_LO and cell_rate(rnd)[0] <= RAND_MAX:
                    if rule != "v1" and not cell_valid(cells, (sub, la, sc))[0]:
                        continue
                    row = {"subset": sub, "layer": la, "scale": sc, "br": round(p, 4)}
                    if rule == "v2.1" and la < min_layer:
                        bl = cell_rate(cells.get(("BL", sub, la, sc, "lens"), {}))
                        below.append({**row, "bl": None if math.isnan(bl[0]) else round(bl[0], 4)})
                        continue
                    sel.append(row)
    out: dict[str, Any] = {"rule": rule, "selected": sel, **({"below_v21": below} if rule == "v2.1" else {})}
    if not sel:
        none = "no cell" if rule == "v1" else "no valid cell"
        out.update(primary=None, valid=None, verdict=f"{none}: the lens does not write a stated bridge at its sentence")
        return out
    best = min(sel, key=lambda d: (-d["br"], d["scale"], d["layer"], 0 if d["subset"] == "w" else 1))
    key = (best["subset"], best["layer"], best["scale"])
    get = {f: cells.get((f, *key, "lens"), {}) for f in ("BL", "BR", "RL", "RR")}
    valid, off, bl_rand = cell_valid(cells, key)
    bl, br = cell_rate(get["BL"]), cell_rate(get["BR"])
    by_scene = {f: {scene_of[i]: float(r == "b") for i, r in get[f].items()} for f in ("BL", "BR")}
    common = sorted(set(by_scene["BL"]) & set(by_scene["BR"]))
    gap = paired_bootstrap_diff([by_scene["BR"][s] for s in common], [by_scene["BL"][s] for s in common], seed=SEED)
    if bl[0] >= WHERE_RATE and bl[1] >= WHERE_LO:
        verdict = "H-where: the lens writes a stated bridge for a lookup where it sits"
    elif bl[0] <= AROUND_MAX and gap[1] >= AROUND_GAP:
        verdict = "H-around: the lens writes a stated bridge for recall but not for a lookup where it sits"
    else:
        verdict = "inconclusive"
    out.update(primary=best, valid=valid, verdict=verdict if valid else f"not valid ({verdict})",
               rates={"BL": bl, "BR": br, "BL_random": bl_rand, **{f"{f}_changed": v for f, v in off.items()}},
               br_minus_bl=gap, n_scenes_paired=len(common))  # fmt: skip
    return out


# ---- model ------------------------------------------------------------------------------------------------------------


def run_scene(model, lens, scene: list[dict], cfg: dict, k0: int, out: dict) -> None:
    layers = cfg["layers"]
    for c in scene:
        ids = torch.tensor([c["read"]["clean"], c["read"]["E-cue"]], device="cuda")
        logits, rec = EP.forward_rows(model, ids, [{}, {}], tuple(layers))
        c["ld_clean"], c["ld_cf"] = (float(lg[c["cand"]["b"]] - lg[c["cand"]["A"]]) for lg in logits)
        r = c["subsets"]["r"]
        c["_ref"] = {la: float((rec[la][1][r] - rec[la][0][r]).norm(dim=-1).pow(2).mean().sqrt()) for la in layers}
        c["_logits"] = logits
    ref = {la: math.sqrt(statistics.mean(c["_ref"][la] ** 2 for c in scene)) for la in layers}
    y = offscene_animal(scene[0])
    for i, c in enumerate(scene):
        run_item(model, lens, c, ref, y, cfg, k0 + i, out)


def run_item(model, lens, c: dict, ref: dict, y: str, cfg: dict, k: int, out: dict) -> None:
    tok = model.tokenizer
    pos = {"b": c["subsets"]["b"], **stated_positions(c)}
    pair = torch.tensor([model.concept_token(a) for a in (c["bridge"], c["cf_bridge"], y)], device="cuda")
    dirs = {}
    for la in cfg["layers"]:
        v = lens.vectors(la, pair)
        dirs[la] = {"lens": v[1] - v[0], "offscene": v[2] - v[0]}
    y_tok = S.answer_token(tok, str(S.ANIMALS[y][0]), "digit") if c["family"].endswith("R") else None
    head = {"family": c["family"], "name": c["id"], "scene": c["scene"]}

    def emit(tags: dict, logits: torch.Tensor) -> None:
        top = int(logits.argmax())
        ld = float(logits[c["cand"]["b"]] - logits[c["cand"]["A"]])
        out["outcomes"].append({**head, **tags, "role": role_of(top, c["cand"], y_tok), "ld": round(ld, 3)})

    emit({"kind": "none"}, c["_logits"][0])
    for e in EP.EDITS:
        if e not in c["read"]:
            continue
        if e == "E-cue":
            emit({"kind": "edit", "edit": e}, c["_logits"][1])
        else:
            lg, _ = EP.forward_rows(model, torch.tensor([c["read"][e]], device="cuda"), [{}])
            emit({"kind": "edit", "edit": e}, lg[0])
    gen = torch.Generator(device="cuda").manual_seed(SEED + 1_000_003 * k)
    rows: list[tuple[dict, dict]] = []
    for la in cfg["layers"]:
        for sc in cfg["scales"]:
            for sname in WHERE:
                if sname == "c" and la not in cfg["context_layers"]:
                    continue
                p = pos[sname]
                norms = torch.full((len(p),), sc * ref[la], device="cuda")
                lens_vec = EP.push_rows(dirs[la]["lens"], norms)
                tags = {"kind": "push", "layer": la, "scale": sc, "subset": sname}
                rows.append(({**tags, "dir": "lens"}, {la: AddRows(lens_vec, p)}))
                rows.append(({**tags, "dir": "random"}, {la: AddRows(null_rows(lens_vec, gen), p)}))
                rows.append(({**tags, "dir": "offscene"}, {la: AddRows(EP.push_rows(dirs[la]["offscene"], norms), p)}))
    ids = torch.tensor([c["read"]["clean"]], device="cuda")
    for start in range(0, len(rows), BATCH - 1):
        chunk = rows[start : start + BATCH - 1]
        logits, _ = EP.forward_rows(model, ids, [{}] + [e for _, e in chunk])
        out["diag"].append(float((logits[0] - c["_logits"][0]).abs().max()))
        for j, (tags, _) in enumerate(chunk, start=1):
            emit(tags, logits[j])
    out["cases"].append({**head, "bridge": c["bridge"], "cf_bridge": c["cf_bridge"], "offscene": y,
                         "answer": c["answer"], "cf_answer": c["cf_answer"], "subject": c["subject"],
                         "positions": pos, "prompt": c["prompts"]["clean"],
                         "ref": {str(la): round(ref[la], 3) for la in cfg["layers"]}})  # fmt: skip


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    inputs = [P.RESULTS / cfg["map"] / "cases.jsonl"] + [
        S.data_dir(cfg["wording"]) / f"{f}.json" for f in cfg["families"]
    ]
    if cfg["scenes"] == "fresh":
        inputs += sorted({P.competence_file(f, cfg["wording"]) for f in cfg["families"]})
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
                "seeds": {"random": f"{SEED} + 1000003 x item index", "offscene": f"Random('{SEED}:<scene>')",
                          "bootstrap": SEED, **({"fresh_scenes": FRESH_SEED} if cfg["scenes"] == "fresh" else {})},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    if cfg["scenes"] == "fresh":
        raw, selection = fresh_cases(model.tokenizer, cfg)
        (out_dir / "selection.json").write_text(json.dumps(selection, indent=2) + "\n")
        cases = [EP.augment(c, model.tokenizer, cfg["wording"]) for c in raw]
    else:
        cases = EP.build_cases(model.tokenizer, {**cfg, "countries": False})
    scenes: dict[str, list[dict]] = {}
    for c in cases:
        scenes.setdefault(c["scene"], []).append(c)
    out: dict[str, Any] = {"outcomes": [], "cases": [], "diag": []}
    done = {"outcomes": 0, "cases": 0}
    k = 0
    for scene in progress(list(scenes.values()), desc="scenes"):
        run_scene(model, lens, scene, cfg, k, out)
        k += len(scene)
        for f in done:  # appended scene by scene: a run stopped early keeps every finished scene
            with open(out_dir / f"{f}.jsonl", "a") as fh:
                fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in out[f][done[f] :])
            done[f] = len(out[f])
    timing = {"seconds": round(time.time() - t0), "n_cases": len(cases), "n_outcomes": len(out["outcomes"]),
              "max_unedited_row_vs_clean_logit": max(out["diag"], default=None)}  # fmt: skip
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    stage_analyze(name)


# ---- analysis ---------------------------------------------------------------------------------------------------------


def load_cells(name: str) -> tuple[dict, dict, dict, list[dict]]:
    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    rows = [json.loads(x) for x in (d / "outcomes.jsonl").read_text().splitlines()]
    ok = {r["name"] for r in rows if r["kind"] == "none" and r["role"] == "A"}
    cells: dict[tuple, dict[str, str]] = collections.defaultdict(dict)
    edits: dict[tuple, dict[str, str]] = collections.defaultdict(dict)
    scene_of = {}
    for r in rows:
        scene_of[r["name"]] = r["scene"]
        if r["name"] not in ok:
            continue
        if r["kind"] == "push":
            cells[(r["family"], r["subset"], r["layer"], r["scale"], r["dir"])][r["name"]] = r["role"]
        elif r["kind"] == "edit":
            edits[(r["family"], r["edit"])][r["name"]] = r["role"]
    counts = collections.Counter(r["family"] for r in rows if r["kind"] == "none")
    eligible = collections.Counter(r["family"] for r in rows if r["kind"] == "none" and r["role"] == "A")
    return (
        m,
        dict(cells),
        dict(edits),
        [{"family": f, "n": counts[f], "right_unedited": eligible[f]} for f in sorted(counts)],
    )


def pct(t: tuple[float, float, float]) -> str:
    return "-" if math.isnan(t[0]) else f"{100 * t[0]:.0f}% [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"


def stage_analyze(name: str, rule: str | None = None) -> None:
    """The run's own rule into the run folder; another rule (an amendment) into a new <run>/analysis-<rule>-<stamp>/."""
    m, cells, edits, counts = load_cells(name)
    cfg = m["config"]
    rows = [json.loads(x) for x in (RESULTS / name / "outcomes.jsonl").read_text().splitlines()]
    scene_of = {r["name"]: r["scene"] for r in rows}
    out_dir = RESULTS / name
    if rule:
        out_dir = out_dir / f"analysis-{rule}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
        out_dir.mkdir()
    min_layer = cfg.get("v21_min_layer", V21_MIN_LAYER)
    dec = decide(cells, scene_of, cfg["layers"], cfg["scales"], rule or cfg.get("rule", "v1"), min_layer)
    anchor = {f: cell_rate(cells.get((f, "b", 20, 8.0, "lens"), {})) for f in cfg["families"]}
    summary = {"run": name, "decision": dec, "counts": counts,
               "slide6_anchor": {f: {"now": anchor[f], "slide6": SLIDE6.get(f)} for f in anchor},
               "cells": [{"family": f, "subset": s, "layer": la, "scale": sc, "dir": d, "n": len(v),
                          "to_x": cell_rate(v), "changed": cell_rate(v, "changed"), "to_y": cell_rate(v, "y")}
                         for (f, s, la, sc, d), v in sorted(cells.items())],
               "edits": [{"family": f, "edit": e, "n": len(v), "to_x": cell_rate(v), "changed": cell_rate(v, "changed")}
                         for (f, e), v in sorted(edits.items())]}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    lines = [f"# {EXP} / {name} (rule {dec['rule']})", "", f"Items: {counts}", "", f"**Verdict:** {dec['verdict']}", ""]
    if dec.get("primary"):
        p = dec["primary"]
        lines += [
            f"Primary cell: subset {p['subset']}, layer {p['layer']}, {p['scale']:g}x (valid: {dec['valid']})",
            "",
        ]
        lines += [f"- {k}: {pct(v)}" for k, v in dec["rates"].items()]
        g = dec["br_minus_bl"]
        lines += [f"- BR - BL (scene-paired, {dec['n_scenes_paired']} scenes): {100 * g[0]:+.0f} [{100 * g[1]:+.0f}, {100 * g[2]:+.0f}] points", ""]  # fmt: skip
    lines += [f"Selected cells (BR rows only): {len(dec['selected'])}", ""]
    if "below_v21" in dec:
        lines += [f"Valid cells below layer {min_layer} (reported, not decisive): "
                  + ("; ".join(f"{d['subset']} L{d['layer']} {d['scale']:g}x: BR {100 * d['br']:.0f}%, BL "
                               + ("-" if d["bl"] is None else f"{100 * d['bl']:.0f}%") for d in dec["below_v21"]) or "none"), ""]  # fmt: skip
    lines += ["Slide 6 anchor (b, layer 20, 8x, lens): " + ", ".join(f"{f} {pct(v)} (slide 6: {100 * SLIDE6[f]:.0f}%)" for f, v in anchor.items()), ""]  # fmt: skip
    lines += ["| family | where | layer | scale | lens → X | random → X | off-scene: changed | off-scene → Y |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for f in cfg["families"]:
        for s in WHERE:
            for la in cfg["layers"]:
                for sc in cfg["scales"]:
                    lens_c = cells.get((f, s, la, sc, "lens"))
                    if not lens_c:
                        continue
                    rnd, off = cells.get((f, s, la, sc, "random"), {}), cells.get((f, s, la, sc, "offscene"), {})
                    lines.append(f"| {f} | {s} | {la} | {sc:g} | {pct(cell_rate(lens_c))} | {pct(cell_rate(rnd))} | "
                                 f"{pct(cell_rate(off, 'changed'))} | {pct(cell_rate(off, 'y'))} |")  # fmt: skip
    lines += ["", "| family | edit | n | → X | changed |", "|---|---|---|---|---|"]
    for (f, e), v in sorted(edits.items()):
        lines.append(f"| {f} | {e} | {len(v)} | {pct(cell_rate(v))} | {pct(cell_rate(v, 'changed'))} |")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))


def stage_figures(name: str) -> None:
    """Per push position, % of answers switched to X's answer by layer: the four families under the lens push at the
    primary cell's scale (8x without one), the random push's highest family as a dotted line."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    m, cells, _, _ = load_cells(name)
    cfg = m["config"]
    dec = json.loads((RESULTS / name / "summary.json").read_text())["decision"]
    sc = dec["primary"]["scale"] if dec.get("primary") else 8.0
    cols = {"BL": "#eb6834", "BR": "#2a78d6", "RL": "#f2a27f", "RR": "#86b6ef"}
    names = {"BL": "prompt → prompt (stated bridge, lookup)", "BR": "prompt → memory (stated bridge, recall)",
             "RL": "memory → prompt (recalled bridge, lookup)", "RR": "memory → memory (recalled bridge, recall)"}  # fmt: skip
    titles = {"b": "the question's subject phrase\n(where slide 6 pushed)", "s": "the sentence stating the bridge",
              "w": "the bridge's word in that sentence", "c": "the whole context (layers 28-44)"}  # fmt: skip
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, sub in zip(axes, WHERE, strict=True):
        for f in cfg["families"]:
            pts = [(la, cell_rate(cells[(f, sub, la, sc, "lens")])) for la in cfg["layers"] if (f, sub, la, sc, "lens") in cells]  # fmt: skip
            if pts:
                ax.plot([p[0] for p in pts], [100 * p[1][0] for p in pts], marker="o", ms=3.5, lw=2, color=cols[f],
                        label=names[f])  # fmt: skip
        rnd = [(la, max(cell_rate(cells[(f, sub, la, sc, "random")])[0] for f in cfg["families"]
                        if (f, sub, la, sc, "random") in cells)) for la in cfg["layers"]
               if any((f, sub, la, sc, "random") in cells for f in cfg["families"])]  # fmt: skip
        ax.plot([p[0] for p in rnd], [100 * p[1] for p in rnd], color="#52514e", ls=":", lw=1.5, label="random push (highest family)")  # fmt: skip
        ax.set_title(titles[sub], loc="left", fontsize=9.5)
        ax.set_xlabel(f"layer (of {m['model'].get('n_layers', pins.N_LAYERS)})")
        ax.set_ylim(0, 100)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("% switched to the other\nbridge's answer")
    h, labs = axes[0].get_legend_handles_labels()
    fig.legend(h, labs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.16), fontsize=9)
    fig.suptitle(f"Where can the lens write a bridge? A lens push of {sc:g}x by layer and position ({m['model']['repo'].split('/')[-1]})",
                 x=0.125, ha="left", fontweight="bold")  # fmt: skip
    fig.savefig(RESULTS / name / "where.png", dpi=150, bbox_inches="tight")
    print("wrote", RESULTS / name / "where.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--n", type=int, default=DEFAULTS["n"])
    ap.add_argument("--scenes", choices=["map", "fresh"], default=DEFAULTS["scenes"])
    ap.add_argument("--rule", choices=["v1", "v2", "v2.1"], default=None,
                    help="run: the rule in the config (default v1); analyze: an amendment into a new folder")  # fmt: skip
    ap.add_argument("--layers", type=int, nargs="+", default=None, help="run: the layer grid (default the 27B's)")
    ap.add_argument("--context-layers", type=int, nargs="+", default=None, help="run, with --layers: the c layers")
    ap.add_argument("--v21-min-layer", type=int, default=V21_MIN_LAYER, help="run, with --layers: v2.1's lowest layer")
    a = ap.parse_args()
    if a.stage == "run":
        assert a.why, "run needs --why"
        cfg = {**DEFAULTS, "n": a.n, "scenes": a.scenes, "rule": a.rule or DEFAULTS["rule"]}
        if a.layers:  # another depth (Qwen3.5-122B: the 27B's grid scaled by depth)
            assert a.context_layers, "--layers needs --context-layers"
            assert set(a.context_layers) <= set(a.layers), "--context-layers must be in --layers"
            cfg.update(layers=a.layers, context_layers=a.context_layers, v21_min_layer=a.v21_min_layer)
        stage_run(a.name, a.why, cfg)
    elif a.stage == "analyze":
        stage_analyze(a.name, a.rule)
    else:
        stage_figures(a.name)
