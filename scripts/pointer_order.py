"""pointer_order (D3b, batch 3): does the pointer direction encode "the Nth statement" (ORDER) or "this token position"
(TOKEN)?

Background (UNVERIFIED): d3b_slot_direction_main_27b found that a direction fitted to "which statement the question asks"
(target minus current statement, at the tokens after the question, layer 48) switches 37% [30, 45] of memory → prompt
answers to the target statement's digit, the lens push 0%. In pointer_v1 every statement has the same length and there
is no filler, so "the 4th statement" and "the statement at token cell 4" are the same thing.

Data: pointer_v2 main (scripts/pointer_v2.py; gate d3v2_competence_27b): 5 statements and ONE filler sentence of exactly
a statement's token length, so every context is 6 equal cells and the filler takes one of them. Statement k sits in
cell k if the filler comes later, in cell k + 1 otherwise. All contexts have the same length, so "token position from
the start" and "distance back from the question" name the same cell.

Design (memory → prompt; animals and elements; scenes split in two halves by a seeded shuffle, two folds: fit on half A
and steer half B, then fit on half B and steer half A, so every scene is steered once by a fit that never saw it):
  fit    on the fit half: every prompt of the scene (the org prompt, the three alt prompts, the "same" prompt) whose asked
         statement comes BEFORE its filler, so its label (the asked statement k) is at once "the k-th statement" and
         "cell k"; the hidden states at every token after the question, layers 40-52; per-token class means (5 classes),
         a shuffled-label fit (seed 1), nearest-mean decodability (5-fold)
  read   on the steer half (no steering): the org prompt's states, classified by the nearest fitted class mean. Where the
         asked statement k comes AFTER the filler (it sits in cell k + 1), an ORDER code is read as k and a TOKEN code as
         k + 1 (k <= 3; cell 5 has no fitted class)
  steer  on the steer half, for every target statement j != the asked one, at the tokens after the question, layers 44
         and 48 one at a time and both at once, at 1x and 2x the per-token size of the alt-prompt patch there:
           slot       mean_j - mean_asked (target minus current, as d3b_slot_direction_main_27b)
           slot_mean  mean_j - the grand mean (no current subtracted: neutral between the readings)
           random     a random direction per token at the slot push's size; shuffled: the shuffled-label difference
         Predictions, the steered scene's filler in cell f:
           j < f   AGREE: both readings point at statement j (positive control: the direction works in these scenes)
           j = f   FILLER: ORDER -> statement j's digit; TOKEN -> cell j is the filler (no digit: answer org or noise)
           j > f   SEPARATE: ORDER -> statement j's digit (it sits in cell j + 1); TOKEN -> cell j holds statement j - 1,
                   so its digit (all digits of a scene differ)
         memory → memory items of the steer half get the slot and random pushes (control: no lookup, nothing to point at)
Decision rule (fixed before the 27B run). Primary cut: memory → prompt, steer-half scenes whose asked statement comes
before the filler (the subtracted current is the same under both readings), SEPARATE targets, slot push, layer 48, 2x
(the strongest clean cell of d3b_slot_direction_main_27b: 45%). order = share of answers = statement j's digit, token =
share = statement j - 1's digit; differences by a scene-cluster bootstrap (2000, seed 0). Verdict:
  ORDER    iff order - token has its 95% lower bound > 0, order >= 2 x token, and order's Wilson lower bound >= 0.10
  TOKEN    iff the reverse
  BOTH     iff both Wilson lower bounds >= 0.10 and neither of the above
  otherwise inconclusive
Valid only if (i) AGREE targets of the same scenes land on statement j with a Wilson lower bound >= 0.15 (the direction
works here at all), (ii) the random push and the shuffled-label direction land on either predicted digit of the SEPARATE
targets with a Wilson upper bound <= 0.10, and (iii) on memory → memory the slot push changes the answer with a Wilson
upper bound <= 0.10; each with n >= 35 (target instances; several per scene, so these intervals are a little narrow:
the primary difference uses the cluster bootstrap). Reported, not decisive: FILLER targets, scenes whose asked statement
comes after the filler, the neutral push, layer 44, 1x, both layers, and the read test.

Stages:  run --name N --why W [...] (manifest first)   analyze --name N   figures --name N   examples --name N [--k 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from bridge_jspace.stats import wilson
from scripts import pointer_fit as PF
from scripts import pointer_swap as PS
from scripts import pointer_v2 as PV2
from scripts import suite_v1 as S

EXP = "pointer_order"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {
    "domains": ["animals", "elements"], "collect_layers": [40, 42, 44, 46, 48, 50, 52], "steer_layers": [44, 48],
    "scales": [1.0, 2.0], "primary_layer": 48, "primary_scale": 2.0, "competence": "d3v2_competence_27b",
    "scene_limit": None,
}  # fmt: skip
N_SLOTS = 5
TYPES = ("off", "pln", "ref")
SPLIT_SEED, SHUFFLE_SEED, NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 1, 0, 0, 2000, 0
WIN_MIN, AGREE_MIN, CONTROL_MAX = 0.10, 0.15, 0.10
CONDS_RL = ("slot", "slot_mean", "random", "shuffled")
CONDS_RR = ("slot", "random")
BATCH = PS.BATCH


# ---- pure helpers (tests/test_pointer_order.py) ---------------------------------------------------------------------


def target_case(a: int, f: int, j: int) -> tuple[str, int, int | None]:
    """(case, statement the ORDER reading points at, statement the TOKEN reading points at or None for the filler) for
    target j in a scene whose asked statement is a and whose filler sits in cell f; the fitted class j means cell j."""
    tok = PV2.order(j, f)
    if j < f:
        return "agree", j, tok
    if j == f:
        return "filler", j, None
    return ("separate_on_current" if tok == a else "separate"), j, tok


def read_case(a: int, f: int) -> tuple[str, int | None]:
    """For the read test: ('pre', a) if the asked statement a precedes the filler (order and cell agree), ('post', a + 1)
    if it follows it (the TOKEN reading's fitted class is its cell a + 1), ('post_unreadable', None) if that cell is 5."""
    if f > a:
        return "pre", a
    cell = PV2.grid(a, f)
    return ("post", cell) if cell < N_SLOTS else ("post_unreadable", None)


def scene_split(scenes: list[str], seed: int = SPLIT_SEED) -> tuple[list[str], list[str]]:
    """(fit half, steer half) of the scene ids, seeded and order-free."""
    order = sorted(scenes)
    random.Random(seed).shuffle(order)
    half = len(order) // 2
    return sorted(order[:half]), sorted(order[half:])


def fit_prompts(types: dict[str, dict]) -> list[tuple[str, str, int, int]]:
    """(item type, source key, filler cell, asked statement) of a scene's prompts whose asked statement precedes the
    filler: the org prompt (once), each type's alt prompt, the 'same' prompt."""
    pln = types["pln"]
    out = [("pln", "base", pln["filler_cell"], pln["slots"]["query"])]
    for t, it in types.items():
        d = it["sources"]["dissoc"]
        out.append((t, "dissoc", d["filler_cell"], d["query_slot"]))
    sm = pln["sources"]["same"]
    out.append(("pln", "same", sm.get("filler_cell", pln["filler_cell"]), sm.get("query_slot", pln["slots"]["query"])))
    return [p for p in out if p[2] > p[3]]


def cluster_boot(x, y, clusters, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> list[float]:
    """mean(x) - mean(y) over paired instances, resampling clusters (scenes) with replacement: [point, lo, hi]."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.size == 0:
        return [math.nan] * 3
    ids = sorted(set(clusters))
    members = {c: [i for i, k in enumerate(clusters) if k == c] for c in ids}
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        idx = [i for c in rng.choice(len(ids), size=len(ids)) for i in members[ids[c]]]
        vals.append(x[idx].mean() - y[idx].mean())
    return [float(x.mean() - y.mean()), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def share(rows: list[dict], role: str) -> list[float]:
    k = sum(r["role"] == role for r in rows)
    return [round(v, 4) for v in wilson(k, len(rows))] + [len(rows)]


# ---- items ----------------------------------------------------------------------------------------------------------


def eligible(comp_run: str | None) -> set[str] | None:
    if not comp_run:
        return None
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    for line in (PV2.RESULTS / comp_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("label", "").startswith("main/"):
            ok[r["id"]].append(r["correct"])
    return {i for i, v in ok.items() if all(v)}


def load_scenes(cfg: dict) -> tuple[dict[str, dict[str, dict]], dict[str, dict]]:
    """Eligible memory → prompt scenes {scene: {type: item}} and memory → memory org items {scene: item}."""
    good = eligible(cfg["competence"])
    rl: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    rr: dict[str, dict] = {}
    for d in cfg["domains"]:
        for t in TYPES:
            for it in PV2.PV.load_file(PV2.DATA / "main" / f"{d}_RL_e5-{t}.json"):
                rl[it["scene"]][t] = it
        for it in PV2.PV.load_file(PV2.DATA / "main" / f"{d}_RR_e5-pln.json"):
            if good is None or it["id"] in good:
                rr[it["scene"]] = it
    keep = {
        s: v
        for s, v in rl.items()
        if len(v) == len(TYPES) and (good is None or all(i["id"] in good for i in v.values()))
    }
    if cfg["scene_limit"]:
        names = sorted(keep)[: cfg["scene_limit"]]
        keep = {s: keep[s] for s in names}
    return keep, rr


def input_files(cfg: dict) -> list[Path]:
    files = [PV2.DATA / "main" / f"{d}_RL_e5-{t}.json" for d in cfg["domains"] for t in TYPES]
    files += [PV2.DATA / "main" / f"{d}_RR_e5-pln.json" for d in cfg["domains"]]
    if cfg["competence"]:
        files.append(PV2.RESULTS / cfg["competence"] / "items.jsonl")
    return files


# ---- the run ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows

    pins.check_run_name(name)
    assert set(cfg["steer_layers"]) <= set(cfg["collect_layers"]), "every steer layer must be a fitted layer"
    assert cfg["primary_layer"] in cfg["steer_layers"], "the primary layer must be a steer layer"
    assert cfg["primary_scale"] in cfg["scales"], "the primary scale must be one of the scales"
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    scenes, rr = load_scenes(cfg)
    half_a, half_b = scene_split(list(scenes))
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in input_files(cfg)},
                "split": {"half_a": half_a, "half_b": half_b, "folds": "fit on A, steer B; then fit on B, steer A"},
                "seeds": {"split": SPLIT_SEED, "shuffle": SHUFFLE_SEED, "null": NULL_SEED, "bootstrap": BOOT_SEED,
                          "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    layers = tuple(cfg["collect_layers"])
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    out_f = open(out_dir / "outcomes.jsonl", "w")  # noqa: SIM115 - appended scene by scene, closed below
    reads: list[dict] = []
    cases: list[dict] = []
    fit_info: list[dict] = []
    n_rows = 0
    for fold, (fit_s, steer_s) in enumerate(((half_a, half_b), (half_b, half_a))):
        fits, info = fit_half(model, scenes, fit_s, layers, progress, forward_rows)
        fit_info.append({"fold": fold, **info})
        n_rows += steer_half(model, cfg, scenes, rr, steer_s, fits, fold, digit_tok, out_f, reads, cases, progress,
                             forward_rows)  # fmt: skip
    out_f.close()
    PF.write_rows(out_dir / "cases.jsonl", cases)
    PF.write_rows(out_dir / "reads.jsonl", reads)
    (out_dir / "fit.json").write_text(json.dumps({"folds": fit_info}, indent=2) + "\n")
    sm = summarise(load_rows(name, "outcomes"), reads, cfg)
    sm |= {"seconds": round(time.time() - t0), "edited_reads": n_rows}
    (out_dir / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(sm))
    print((out_dir / "summary.md").read_text())


def fit_half(
    model, scenes: dict, fit_s: list[str], layers: tuple[int, ...], progress, forward_rows
) -> tuple[dict, dict]:
    """Collect the fit half's clean prompts (asked statement before the filler) and fit per-layer class means."""
    tok = model.tokenizer
    jobs: list[tuple[list[int], list[int], int]] = []
    for s in fit_s:
        preps = {t: PS.prepare(it, tok) for t, it in scenes[s].items()}
        for t, key, _f, a in fit_prompts(scenes[s]):
            p = preps[t]
            jobs.append((p["read_ids"][key], p["groups"]["final"], a))
    by_len: dict[int, list[tuple[list[int], list[int], int]]] = collections.defaultdict(list)
    for j_ in jobs:
        by_len[len(j_[0])].append(j_)
    feats: dict[int, list[torch.Tensor]] = {la: [] for la in layers}
    labels: list[int] = []
    for group in progress([g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)], "collect"):
        _, rec = forward_rows(model, torch.tensor([g[0] for g in group], device="cuda"), [{}] * len(group), layers)
        for ri, (_, fin, a) in enumerate(group):
            for la in layers:
                feats[la].append(rec[la][ri, fin].half().cpu())
            labels.append(a)
    y = torch.tensor(labels, device="cuda")
    y_shuf = y[torch.randperm(len(y), generator=torch.Generator().manual_seed(SHUFFLE_SEED)).to(y.device)]
    fits, fit_rows = {}, []
    for la in layers:
        x = torch.stack(feats[la]).cuda().float()
        mu, m = PF.class_means(x, y)
        mu_s, _ = PF.class_means(x, y_shuf)
        fits[la] = {"mu": mu, "m": m, "mu_shuf": mu_s}
        fit_rows.append({"layer": la, "n": int(x.shape[0]), "per_slot": [int((y == c).sum()) for c in range(N_SLOTS)],
                         "decode_cv": round(PF.nearest_mean_cv(x, y), 4),
                         "decode_cv_shuffled": round(PF.nearest_mean_cv(x, y_shuf), 4)})  # fmt: skip
        del x
    return fits, {"prompts": len(labels), "scenes": len(fit_s), "layers": fit_rows}


def steer_half(
    model, cfg, scenes, rr, steer_s, fits, fold, digit_tok, out_f, reads, cases, progress, forward_rows
) -> int:
    """The read test and the pushes on the steer half's org prompts (memory → prompt) and memory → memory items."""
    tok = model.tokenizer
    layers = tuple(cfg["collect_layers"])
    steer = tuple(cfg["steer_layers"])
    n_rows = 0
    items = [("RL", s, scenes[s]["pln"]) for s in steer_s] + [("RR", s, rr[s]) for s in steer_s if s in rr]
    for ci, (fam, s, it) in enumerate(progress(items, f"steer (fold {fold})")):
        p = PS.prepare(it, tok)
        fin = p["groups"]["final"]
        logits0, rec = forward_rows(model, torch.tensor([p["read_ids"]["base"], p["read_ids"]["dissoc"]], device="cuda"),
                                    [{}, {}], layers)  # fmt: skip
        a, f = it["slots"]["query"], it["filler_cell"]
        if fam == "RL":
            rc, tok_cls = read_case(a, f)
            for la in layers:
                h = rec[la][0, fin]
                dist = ((h[None] - fits[la]["mu"]) ** 2).sum((1, 2))
                pred = int(dist.argmin())
                reads.append({"scene": s, "domain": it["domain"], "fold": fold, "layer": la, "asked": a, "filler": f,
                              "case": rc, "pred": pred, "order_class": a, "token_class": tok_cls})  # fmt: skip
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_003 * ci + 7 * fold)
        conds = CONDS_RL if fam == "RL" else CONDS_RR
        settings: list[tuple[Any, tuple[int, ...]]] = [(la, (la,)) for la in steer] + [("both", steer)]
        jobs2: list[tuple[dict, dict]] = [({"cond": "unedited", "target": None, "layer": None, "scale": None}, {})]
        for j in range(N_SLOTS):
            if j == a:
                continue
            vec: dict[tuple[int, float, str], torch.Tensor] = {}
            for la in steer:
                ft = fits[la]
                size = (rec[la][1, fin] - rec[la][0, fin]).norm(dim=-1)
                for sc in cfg["scales"]:
                    sv = PF.matched(ft["mu"][j] - ft["mu"][a], sc * size)
                    vec[(la, sc, "slot")] = sv
                    vec[(la, sc, "random")] = PS.null_rows(sv, gen)
                    if fam == "RL":
                        vec[(la, sc, "slot_mean")] = PF.matched(ft["mu"][j] - ft["m"], sc * size)
                        vec[(la, sc, "shuffled")] = PF.matched(ft["mu_shuf"][j] - ft["mu_shuf"][a], sc * size)
            for key, group in settings:
                for sc in cfg["scales"]:
                    for cn in conds:
                        tags = {"cond": cn, "target": j, "layer": key, "scale": sc}
                        jobs2.append((tags, {la: PS.AddRows(vec[(la, sc, cn)], fin) for la in group}))
        digits = [str(d) for d in it["digits"]]
        read = torch.tensor([p["read_ids"]["base"]], device="cuda")
        base_top = -1
        for start in range(0, len(jobs2), BATCH):
            chunk = jobs2[start : start + BATCH]
            logits, _ = forward_rows(model, read, [e for _, e in chunk])
            for ri, (tags, _) in enumerate(chunk):
                top = int(logits[ri].argmax())
                if tags["cond"] == "unedited":  # always the first row: the reference for "answer changed"
                    base_top = top
                dg = digit_tok.get(top)
                o = {"family": fam, "domain": it["domain"], "scene": s, "name": it["id"], "fold": fold, "asked": a,
                     "filler": f, **tags, "top": tok.decode([top]).strip()}  # fmt: skip
                if fam == "RL" and tags["target"] is not None:
                    case, o_slot, t_slot = target_case(a, f, tags["target"])
                    o |= {"case": case, "pre_filler": a < f, "order_digit": digits[o_slot],
                          "token_digit": digits[t_slot] if t_slot is not None else None,
                          "role": ("order" if dg == digits[o_slot] else
                                   "token" if t_slot is not None and dg == digits[t_slot] else
                                   "org" if dg == it["answer"] else "context" if dg in digits else
                                   "other_digit" if dg is not None else "other")}  # fmt: skip
                else:
                    o["role"] = (
                        "kept" if top == base_top else "changed"
                    )  # vs the unedited read, not the expected answer
                out_f.write(json.dumps(o) + "\n")
                n_rows += 1
        cases.append({"scene": s, "family": fam, "id": it["id"], "domain": it["domain"], "fold": fold, "asked": a,
                      "filler": f, "digits": digits, "answer": it["answer"], "text": p["text"], "context": it["context"],
                      "final_chars": [list(p["offsets"][i]) for i in fin],
                      "unedited_top": tok.decode([int(logits0[0].argmax())]).strip()})  # fmt: skip
    return n_rows


def load_rows(name: str, which: str) -> list[dict]:
    return [json.loads(x) for x in (RESULTS / name / f"{which}.jsonl").read_text().splitlines()]


# ---- analysis ---------------------------------------------------------------------------------------------------------


def sel(rows: list[dict], **where) -> list[dict]:
    return [o for o in rows if all(o.get(k) == v for k, v in where.items())]


def summarise(rows: list[dict], reads: list[dict], cfg: dict) -> dict:
    la, sc = cfg["primary_layer"], cfg["primary_scale"]
    rl = sel(rows, family="RL")

    def cut(cond: str, case: str, pre: bool | None = True, layer: Any = la, scale: float = sc) -> list[dict]:
        out = sel(rl, cond=cond, case=case, layer=layer, scale=scale)
        return out if pre is None else [o for o in out if o["pre_filler"] == pre]

    prim = cut("slot", "separate")
    order_v = [float(o["role"] == "order") for o in prim]
    token_v = [float(o["role"] == "token") for o in prim]
    diff = cluster_boot(order_v, token_v, [o["scene"] for o in prim])
    o_sh, t_sh = share(prim, "order"), share(prim, "token")
    agree = share(cut("slot", "agree"), "order")
    rnd, shf = cut("random", "separate"), cut("shuffled", "separate")
    ctrl = {
        k: {"order": share(v, "order"), "token": share(v, "token")} for k, v in (("random", rnd), ("shuffled", shf))
    }
    rr = [o for o in sel(rows, family="RR", cond="slot", layer=la, scale=sc)]
    rr_changed = share(rr, "changed")
    valid = (agree[1] >= AGREE_MIN and all(c[r][2] <= CONTROL_MAX and c[r][3] >= 35 for c in ctrl.values() for r in c)
             and rr_changed[2] <= CONTROL_MAX and rr_changed[3] >= 35)  # fmt: skip
    if diff[1] > 0 and o_sh[0] >= 2 * t_sh[0] and o_sh[1] >= WIN_MIN:
        verdict = "ORDER: the pointer direction encodes the Nth statement"
    elif diff[2] < 0 and t_sh[0] >= 2 * o_sh[0] and t_sh[1] >= WIN_MIN:
        verdict = "TOKEN: the pointer direction encodes a token position"
    elif o_sh[1] >= WIN_MIN and t_sh[1] >= WIN_MIN:
        verdict = "BOTH: answers follow the order and the token position"
    else:
        verdict = "inconclusive"
    if not valid:
        verdict += " (controls failed or n too small: not interpretable)"
    grid: dict[str, Any] = {}
    for cond in CONDS_RL:
        for case in ("agree", "filler", "separate", "separate_on_current"):
            for pre in (True, False):
                for key in [*cfg["steer_layers"], "both"]:
                    for s_ in cfg["scales"]:
                        c_ = cut(cond, case, pre, key, s_)
                        if c_:
                            grid[f"{cond}|{case}|{'pre' if pre else 'post'}|{key}|{s_}"] = dict(collections.Counter(o["role"] for o in c_)) | {"n": len(c_)}  # fmt: skip
    read_tab: dict[str, Any] = {}
    for layer in sorted({r["layer"] for r in reads}):
        post = [r for r in reads if r["layer"] == layer and r["case"] == "post"]
        pre = [r for r in reads if r["layer"] == layer and r["case"] == "pre"]
        read_tab[str(layer)] = {
            "post_order": [round(v, 4) for v in wilson(sum(r["pred"] == r["order_class"] for r in post), len(post))] + [len(post)],
            "post_token": [round(v, 4) for v in wilson(sum(r["pred"] == r["token_class"] for r in post), len(post))] + [len(post)],
            "pre_correct": [round(v, 4) for v in wilson(sum(r["pred"] == r["order_class"] for r in pre), len(pre))] + [len(pre)],
        }  # fmt: skip
    return {"primary": {"layer": la, "scale": sc, "order": o_sh, "token": t_sh, "order_minus_token": diff,
                        "agree": agree, "controls": ctrl, "rr_changed": rr_changed,
                        "filler_order": share(cut("slot", "filler"), "order"), "filler_org": share(cut("slot", "filler"), "org"),
                        "neutral_order": share(cut("slot_mean", "separate"), "order"),
                        "neutral_token": share(cut("slot_mean", "separate"), "token"),
                        "post_order": share(cut("slot", "separate", False), "order"),
                        "post_token": share(cut("slot", "separate", False), "token")},
            "valid": valid, "verdict": verdict, "read": read_tab, "grid": grid}  # fmt: skip


def summary_md(sm: dict) -> str:
    p = sm["primary"]

    def r(x):
        return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}] (n={x[3]})"

    d = p["order_minus_token"]
    lines = [f"# {EXP}", "", f"Verdict: **{sm['verdict']}**", "",
             f"Primary (memory → prompt, asked statement before the filler, targets after it, layer {p['layer']}, "
             f"{p['scale']:g}x): order {r(p['order'])}, token {r(p['token'])}; order - token {100 * d[0]:+.0f} "
             f"[{100 * d[1]:+.0f}, {100 * d[2]:+.0f}] points (scene bootstrap)", "",
             f"Positive control (targets before the filler): {r(p['agree'])}",
             f"Random push: {json.dumps(p['controls']['random'])}", f"Shuffled labels: {json.dumps(p['controls']['shuffled'])}",
             f"memory → memory, answer changed: {r(p['rr_changed'])}",
             f"Filler-cell targets: order {r(p['filler_order'])}, answer org {r(p['filler_org'])}",
             f"Neutral push (target minus the mean): order {r(p['neutral_order'])}, token {r(p['neutral_token'])}",
             f"Asked statement after the filler: order {r(p['post_order'])}, token {r(p['post_token'])}", "",
             "Read test (asked statement after the filler; nearest fitted mean): " + json.dumps(sm["read"])]  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_analyze(name: str) -> Path:
    m = json.loads((RESULTS / name / "manifest.json").read_text())
    sm = summarise(load_rows(name, "outcomes"), load_rows(name, "reads"), m["config"])
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(sm))
    print(out)
    return out


# ---- figures and examples ---------------------------------------------------------------------------------------------

ORDER_C, TOKEN_C = "#2a78d6", "#eb6834"


def example_text(cases: list[dict]) -> str:
    """A real steered scene with a SEPARATE target: what each reading predicts."""
    for c in cases:
        a, f = c["asked"], c["filler"]
        if c["family"] != "RL" or not a < f < N_SLOTS - 1:
            continue
        j = f + 1
        _, o, t = target_case(a, f, j)
        assert t is not None  # j > f: cell j holds statement j - 1
        q = c["text"][c["text"].rindex("Which") :].split("?")[0] + "?"
        return (f"\"{c['context'][:70]}... {q}\" -> answer org {c['answer']} (statement {a + 1}; the filler sentence "
                f"takes position {f + 1}). Push toward statement {j + 1}: order reading -> {c['digits'][o]} (statement "
                f"{j + 1}, now at position {j + 2}); token reading -> {c['digits'][t]} (position {j + 1} now holds statement "
                f"{t + 1}).")  # fmt: skip
    return ""


def stage_figures(name: str) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as PL

    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    cfg = m["config"]
    for old in d.glob("analysis-*-figures"):  # one figures folder per run
        for f_ in old.iterdir():
            f_.unlink()
        old.rmdir()
    out = d / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    rows = load_rows(name, "outcomes")
    reads = load_rows(name, "reads")
    cases = [json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines()]
    fitj = json.loads((d / "fit.json").read_text())
    sm = summarise(rows, reads, cfg)
    model_name = m["model"]["repo"].split("/")[-1]
    ex = example_text(cases)
    figs: list[str] = []
    keys = [*cfg["steer_layers"], "both"]
    xs = np.arange(len(keys))
    rl = sel(rows, family="RL")

    def rate(c: list[dict], role: str) -> list[float]:
        return list(wilson(sum(o["role"] == role for o in c), len(c))) if c else [math.nan] * 3

    # 1. order vs token on the separating targets
    fig, axes = plt.subplots(1, len(cfg["scales"]) + 1, figsize=(5.2 * (len(cfg["scales"]) + 1) + 1.5, 4.8), squeeze=False,
                             gridspec_kw={"width_ratios": [1] * len(cfg["scales"]) + [1.5]})  # fmt: skip
    for i, sc in enumerate(cfg["scales"]):
        ax = axes[0][i]
        PL.style_axes(ax)
        PL.percent_axis(ax)
        for cond, ls, mfc in (("slot", "-", None), ("random", "--", PL.SURFACE), ("shuffled", ":", PL.SURFACE)):
            for role, colour, off in (("order", ORDER_C, -0.06), ("token", TOKEN_C, 0.06)):
                v = np.array([rate([o for o in sel(rl, cond=cond, case="separate", layer=k, scale=sc) if o["pre_filler"]], role)
                              for k in keys], float)  # fmt: skip
                ax.errorbar(xs + off, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None), color=colour if cond == "slot" else PL.MUTED,
                            ls=ls, lw=2 if cond == "slot" else 1.2, marker="o", ms=5, mfc=mfc or colour, elinewidth=1, capsize=0)  # fmt: skip
        ax.set_xticks(xs, [str(k) if k != "both" else "both" for k in keys])
        ax.set_ylim(-0.04, 1.04)
        ax.set_title(f"{sc:g}x the alt-prompt patch's size", fontsize=9.5, color=PL.INK, loc="left")
        ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
        if i == 0:
            ax.set_ylabel(
                "% of original answers that become\nthe digit each reading predicts", fontsize=9, color=PL.INK
            )
    ax = axes[0][-1]
    PL.style_axes(ax)
    PL.percent_axis(ax, "x")
    p = sm["primary"]
    bars = [("targets before the filler (both readings agree)", p["agree"], ORDER_C),
            ("target at the filler's position: order digit", p["filler_order"], ORDER_C),
            ("target at the filler's position: answer org kept", p["filler_org"], PL.MUTED),
            ("push without the current statement: order", p["neutral_order"], ORDER_C),
            ("push without the current statement: token", p["neutral_token"], TOKEN_C),
            ("asked statement after the filler: order", p["post_order"], ORDER_C),
            ("asked statement after the filler: token", p["post_token"], TOKEN_C),
            ("memory → memory: answer changed (control)", p["rr_changed"], PL.MUTED)]  # fmt: skip
    ys = np.arange(len(bars))[::-1]
    for y_, (_, r_, colour) in zip(ys, bars, strict=True):
        if not math.isnan(r_[0]):
            ax.barh(y_, r_[0], height=0.62, color=colour, zorder=2)
            ax.errorbar(
                r_[0],
                y_,
                xerr=np.clip([[r_[0] - r_[1]], [r_[2] - r_[0]]], 0, None),
                color=PL.INK,
                elinewidth=0.9,
                capsize=0,
                zorder=3,
            )
            ax.text(
                min(r_[2], 1) + 0.02, y_, f"{100 * r_[0]:.0f}% (n={r_[3]})", va="center", fontsize=7.5, color=PL.INK
            )
    ax.set_yticks(ys, [b[0] for b in bars], fontsize=8, color=PL.INK)
    ax.set_xlim(0, 1)
    ax.set_title(f"layer {p['layer']}, {p['scale']:g}x: other cuts", fontsize=9.5, color=PL.INK, loc="left")
    handles = [Line2D([], [], color=ORDER_C, lw=2, marker="o", label="order reading: the target statement's digit"),
               Line2D([], [], color=TOKEN_C, lw=2, marker="o", label="token reading: the digit now at the target's old position"),
               Line2D([], [], color=PL.MUTED, ls="--", marker="o", mfc=PL.SURFACE, label="control: random push (same size)"),
               Line2D([], [], color=PL.MUTED, ls=":", marker="o", mfc=PL.SURFACE, label="control: shuffled-label direction")]  # fmt: skip
    explain = [("What we did", "Fitted the pointer direction on scenes where 'the Nth statement' and 'the Nth position' "
                               "coincide, then pushed scenes where a filler sentence shifts the later statements by one "
                               "position, toward a statement after the filler."),
               ("Example", ex),
               ("How to read", f"Left panels: share of answers that become the digit each reading predicts. Verdict: "
                               f"'{sm['verdict']}'."),
               ("Control", "Gray: a random push and a direction fitted with shuffled labels, same size; memory → memory "
                           "items, where nothing is looked up.")]  # fmt: skip
    PF.save_fig(fig, out, "fig1_order_or_position", "Does the pointer direction mean 'the Nth statement' or 'this token position'?",
                explain, f"{model_name}; held-out scenes, asked statement before the filler, targets after it; error bars: "
                "Wilson 95% over target instances (several per scene).", handles, ncols=2, figs=figs)  # fmt: skip

    # 2. the read test
    fig, ax = plt.subplots(figsize=(8, 4.4))
    PL.style_axes(ax)
    PL.percent_axis(ax)
    lay = sorted(int(k) for k in sm["read"])
    for key, colour, label in (("post_order", ORDER_C, "reads its order (the Nth statement)"),
                               ("post_token", TOKEN_C, "reads its position (one later)"),
                               ("pre_correct", PL.MUTED, "control: asked statement before the filler (both agree)")):  # fmt: skip
        v = np.array([sm["read"][str(la)][key][:3] for la in lay], float)
        ax.errorbar(lay, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None), color=colour, lw=2,
                    ls="--" if key == "pre_correct" else "-", marker="o", ms=5, elinewidth=1, capsize=0, label=label)  # fmt: skip
    ax.axhline(1 / N_SLOTS, color=PL.MUTED, ls=":", lw=1)
    ax.set_xticks(lay, [str(la) for la in lay])
    ax.set_ylim(0, 1.04)
    ax.set_xlabel("layer", fontsize=9, color=PL.MUTED)
    ax.set_ylabel("share of held-out scenes", fontsize=9, color=PL.INK)
    ax.legend(frameon=False, fontsize=8)
    explain = [("What we did", "No push: read which statement the last tokens point at, by the nearest fitted statement "
                               "mean, on held-out scenes whose asked statement sits after the filler (one position later "
                               "than its number)."),
               ("Example", ex),
               ("How to read", "Blue: the read-out picks the statement's number; orange: it picks the position one later. "
                               "Chance 20% (dotted)."),
               ("Control", "Gray dashed: scenes where the asked statement precedes the filler, so both readings agree.")]  # fmt: skip
    PF.save_fig(fig, out, "fig2_read_order_or_position", "Without pushing: do the last tokens point at the Nth statement or at a position?",
                explain, f"{model_name}; two folds (fit on one half of the scenes, read the other): "
                f"{' and '.join(str(f_['prompts']) for f_ in fitj['folds'])} fit prompts; error bars: Wilson 95%.", figs=figs)  # fmt: skip
    (out / "summary.json").write_text(json.dumps({"run": name, "verdict": sm["verdict"], "valid": sm["valid"],
                                                  "primary": sm["primary"], "read": sm["read"], "fit": fitj, "figures": figs}, indent=2) + "\n")  # fmt: skip
    print(out)
    return out


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    m = json.loads((d / "manifest.json").read_text())
    la, sc = m["config"]["primary_layer"], m["config"]["primary_scale"]
    rows = load_rows(name, "outcomes")
    cases = {c["id"]: c for c in (json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines())}
    prim = [o for o in sel(rows, family="RL", cond="slot", case="separate", layer=la, scale=sc) if o["pre_filler"]]
    groups = {"order": "the answer is the target statement's digit (order reading)",
              "token": "the answer is the digit now at the target's old position (token reading)",
              "neither": "neither predicted digit"}  # fmt: skip
    members: dict[str, list[dict]] = {g: [] for g in groups}
    for o in prim:
        members[o["role"] if o["role"] in ("order", "token") else "neither"].append(o)
    rng = np.random.default_rng(seed)
    examples = []
    for g, os_ in members.items():
        for o in [os_[i] for i in sorted(rng.choice(len(os_), size=min(k, len(os_)), replace=False))] if os_ else []:
            c = cases[o["name"]]
            spans = PF.statement_spans(c["text"], c["context"])
            j = o["target"]
            _, os_slot, ts_slot = target_case(c["asked"], c["filler"], j)
            cells = sorted(spans)  # the 6 cells in order: statements and the filler
            base = [{"start": cells[PV2.grid(c["asked"], c["filler"])][0], "end": cells[PV2.grid(c["asked"], c["filler"])][1], "role": "asked statement"},
                    {"start": cells[c["filler"]][0], "end": cells[c["filler"]][1], "role": "filler"},
                    {"start": cells[PV2.grid(os_slot, c["filler"])][0], "end": cells[PV2.grid(os_slot, c["filler"])][1], "role": "order target"},
                    {"start": c["final_chars"][0][0], "end": c["final_chars"][-1][1], "role": "pushed tokens"}]  # fmt: skip
            if ts_slot is not None:
                cell = PV2.grid(ts_slot, c["filler"])
                base.append({"start": cells[cell][0], "end": cells[cell][1], "role": "token target"})
            for cn in ("slot", "slot_mean", "random", "shuffled"):
                r_ = next((x for x in sel(rows, name=o["name"], cond=cn, target=j, layer=la, scale=sc)), None)
                if r_ is None:
                    continue
                examples.append({"group": g, "family": "RL", "item_id": o["name"], "prompt": c["text"] + " ", "spans": base,
                                 "condition": f"{cn} push toward statement {j + 1} at layer {la}, {sc:g}x the alt-prompt patch's size",
                                 "answers": {"clean": c["answer"], "edited": r_["top"],
                                             "expected": {"H-order": o["order_digit"], "H-token": o["token_digit"]}},
                                 "numbers": {"role": r_["role"]},
                                 "why": f"{groups[g]} (asked statement {c['asked'] + 1}, filler in cell {c['filler'] + 1})"})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g, "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--domains", nargs="+", default=DEFAULTS["domains"])
    for key in ("collect_layers", "steer_layers"):
        ap.add_argument("--" + key.replace("_", "-"), nargs="+", type=int, default=DEFAULTS[key])
    ap.add_argument("--scales", nargs="+", type=float, default=DEFAULTS["scales"])
    ap.add_argument("--primary-layer", type=int, default=DEFAULTS["primary_layer"])
    ap.add_argument("--primary-scale", type=float, default=DEFAULTS["primary_scale"])
    ap.add_argument("--competence", default=DEFAULTS["competence"])
    ap.add_argument("--no-eligibility", action="store_true", help="a smoke on another model: no competence filter")
    ap.add_argument("--scene-limit", type=int, default=None, help="first K eligible scenes (a smoke: few)")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        config = {"domains": args.domains, "collect_layers": args.collect_layers, "steer_layers": args.steer_layers,
                  "scales": args.scales, "primary_layer": args.primary_layer, "primary_scale": args.primary_scale,
                  "competence": None if args.no_eligibility else args.competence, "scene_limit": args.scene_limit}  # fmt: skip
        stage_run(args.name, args.why, config)
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
