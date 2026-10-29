"""x51_depth (batch 51, test 51.5; jobs/c3/batch51.yaml, design and rule fixed in advance; Q51.5 in
predictions/2026-10-28_dan.md): the anatomy by depth on Zach's passages. 47.8's per-layer sweep (scripts/x47_anatomy.py)
on batch 50 Z1's items (scripts/x50_zach.py), both imported, neither changed.

Items: Z1's chosen passages on the model (results/x50_zach/<Z1 run>/: gate.json's order joined to cases.jsonl), so the
items, the alignment (the pointer sentence's name changed, the patch token at the name's last token, at one index in O and
S), the fact-first / fact-after strata, the gate (0.80 per reader on O; both readers say and read O's and S's answers
right) and the K (lookup: every fact stated) / M (recall: the bridge's fact from memory) readers are Z1's own. Before any
GPU work the run rebuilds each chosen passage with x50_zach.z1_cases on the model's tokenizer and asserts the stored ids,
patch token and answer tokens are the rebuilt ones.

Per layer l of the sweep (9B every 2nd L2-L30, 47.8's 9B grid; 27B every 2nd L4-L60, 47.8's 27B span at step 2), per
reader, Delta_l = h_S - h_O at the patch token (one forward of O and of S per passage and reader, every sweep layer),
added at l alone on O. Arms: whole; no_jpp (the change minus its J++ part: signed OMP, k = 25, the layer's own
letter-token J++ atoms, X0's fit, as Z1); no_jpp_ratoms (minus a random part of the J++ part's share drawn from random
lens atoms of the layer, seed 777 + l: 47.8's control for the J++ part); no_jpp_rand (minus a random part of the same
share in X0's random subspace, seed 888 + l: Z1's control). The read: Z1's (his chat framing, the top token against the
first token of S's answer: switch; routes switch / original / lure / other). The fact-first passages run first and their
rows are written before the fact-after passages start (a partial run keeps them). No slot probe (no slots).

Optional (--split, off by default; batch51.yaml: "only if Z3 shows position answers", Z3 sealed when this was written):
the identity / position split per layer on Z3's items (x50_zach.z3_cases: level-0 passages, every fact before the
pointer, B named, B's and C's fact sentences swapped, B's with a new value), Z3's competence and gate on this model, the
whole change at every sweep layer, the lookup's answer classified as x6_routes does (identity / position / value /
original / other). Descriptive; not in the rule.

SEALED: the run writes per-item outcomes and no verdict; verdict and view refuse until predictions/2026-10-28_dan.md holds
Dan's committed Q51.5 answer at HEAD.

Rule (fixed in advance, batch51.yaml 51.5): "the same read window as ours" if the last layer where each reader's switch
>= 0.3 lies within 4 layers of ours. Ours: REFERENCE below, computed by reference() from the stored 47.8 runs (9B
qwen35_9b_x47_anatomy, 27B x49_4_anatomy_27b) by the same switch_rates / window_end code as his, before any 51.5 run.
Report against Zach's swap window (L4-20, gone by L25) beside.

uv run python scripts/x51_depth.py plan --plan-dir results/x51_depth/plan-<UTC>        # CPU, per BJ_TARGET
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_depth.py run --name qwen35_9b_x51_5     # GPU, sealed
uv run python scripts/x51_depth.py verdict | view                                       # CPU, after Q51.5
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
from scripts import x47_anatomy as A
from scripts import x50_zach as Z

EXP = "x51_depth"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.5"
TEST = "51.5"
TARGETS = ("qwen3.5-9b", "qwen3.6-27b")
LAYERS = {"qwen3.5-9b": tuple(range(2, 31, 2)), "qwen3.6-27b": tuple(range(4, 61, 2))}
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_5", "qwen3.6-27b": "x51_5_27b"}
OURS = {"qwen3.5-9b": "qwen35_9b_x47_anatomy", "qwen3.6-27b": "x49_4_anatomy_27b"}  # the stored 47.8 sweeps
# Ours, written before any 51.5 run (28 Oct): reference() on OURS, the last layer where the whole change switches >= 0.3
# of the reader (lookup: identity + position + value; recall: the changed item). 9B grid L2-L30 every 2nd; 27B 49.4's
# grid L8, 16, 24, 30, 32, 34, 40, 48, 56.
REFERENCE = {"qwen3.5-9b": {"lookup": 16, "recall": 14}, "qwen3.6-27b": {"lookup": 40, "recall": 32}}
# Batch 52, Dan's morning queue (29 Oct) item 2: 51.5 on Lightning, the design from the 9B / 27B spec: 47.8's Lightning
# grid (every 4th L2-L50, x47_anatomy.LAYERS), Z1's Lightning run as the items, ours = reference() on Lightning's 47.8
# sweep nem35l_x52_anatomy, computed before any Lightning 51.5 run (29 Oct ~09:45: lookup L22, recall L22); read by
# verdict --design-from alone (TARGETS / RUNS and 51.5's own verdict unchanged)
DESIGN_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_depth51"}
LAYERS["nemotron-3.5-lightning"] = A.LAYERS["nemotron-3.5-lightning"]
OURS["nemotron-3.5-lightning"] = "nem35l_x52_anatomy"
REFERENCE["nemotron-3.5-lightning"] = {"lookup": 22, "recall": 22}
DESIGN_NOTE = ("design from the 9B / 27B spec (jobs/c3/x51_5_9b.yaml / x51_5_27b.yaml), 51.5's rule verbatim; Zach's "
               "Lightning band L27-33 (x50_zach.BESIDE_BAND) beside the script's fixed swap window; no prediction (Dan's "
               "morning queue, 29 Oct)")  # fmt: skip
STRATA = ("fact-first", "fact-after")
ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_jpp_ratoms")
READERS = Z.READERS  # K (lookup), M (recall)
NAME = {Z.LOOKUP: "lookup", Z.RECALL: "recall"}
HIS_MOVED = ("switch",)  # the other entity's answer
OURS_MOVED = {"lookup": A.MOVED, "recall": ("changed",)}  # 47.8's switch (x47_anatomy.layer_cells)
OURS_READER = {"lookup": X.LOOKUP, "recall": X.RECALL}
SWITCH_BAR, WINDOW_TOL = 0.30, 4
ZACH_WINDOW, ZACH_GONE = (4, 20), 25
ATOMS_SEED = A.ATOMS_SEED  # 777 + layer
SPLIT_ROUTES = Z.ROUTES
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0
EPS = 1e-9
RULE = ('"The same read window as ours" if the last layer where each reader\'s switch >= 0.3 lies within 4 layers of ours '
        "(9B: both readers to ~L16, the recall to L24; 27B: from 49.4). Report against Zach's swap window (L4-20, gone "
        "by L25).")  # fmt: skip
AS_COMPUTED = (
    "Items: Z1's chosen passages on the model (its gate.json order joined to its cases.jsonl; Z1's gate, alignment, "
    "strata, readers K = lookup and M = recall), re-aligned on the tokenizer before the run. Sweep: 9B L2-L30 every 2nd "
    "(47.8's 9B grid), 27B L4-L60 every 2nd (47.8's 27B span at step 2). Delta_l = h_S - h_O at the pointer name's last "
    "token per reader, added at layer l alone on O. Arms: whole; no_jpp (minus the signed-OMP J++ part, k = 25, the "
    "layer's own letter-token atoms); no_jpp_ratoms (minus a random part of the same share from random lens atoms, seed "
    "777 + l, 47.8's control); no_jpp_rand (minus a random part of the same share in X0's random subspace, seed 888 + l, "
    "Z1's control). Switch = Z1's read (top token = the first token of S's answer). Per layer and reader: the whole "
    "change's switch share; extra loss without J++ = X0's excess against no_jpp_ratoms (Z1's no_jpp_rand beside); "
    "cluster bootstrap over the original bridge entity (10,000, seed 0). Window end = the last sampled layer whose "
    "switch share (point estimate) >= 0.30 (EPS 1e-9); None if no layer reaches it. Ours = the same function on the "
    "stored 47.8 runs (9B qwen35_9b_x47_anatomy, 27B x49_4_anatomy_27b; C2 test half; lookup switch = identity + "
    "position + value, recall = the changed item): 9B lookup L16, recall L14; 27B lookup L40, recall L32 (27B grid "
    "every 8th with L30-34). Per model: the same read window iff, for both readers, his window end exists and |his - "
    "ours| <= 4; decided on all of Z1's items (both strata pooled), each stratum's window end beside (a run that stopped "
    "after fact-first: the rule on fact-first alone, labelled partial). Z1's gate failed -> not tested (numbers "
    "descriptive). Zach's swap window beside, descriptive: each reader's first and last layer >= 0.3 against L4-L20, "
    "and whether the switch is < 0.3 at every sampled layer >= L25. The identity / position split (--split) runs only "
    "when the job's command carries the flag (off in the spec)."
)


# ---- items (CPU) --------------------------------------------------------------------------------------------------


def z1_run(target: str) -> Path:
    return Z.RESULTS / {**Z.RUNS["z1"], **Z.COVERAGE_RUNS["z1"]}[target]  # batch 52: Lightning's Z1 (nem35l_x52_z1)


def rel(p: Path) -> str:
    """The path relative to the repo where it lies inside it (as manifests record inputs), else as given."""
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


def run_order(cases: list[dict]) -> list[dict]:
    """The fact-first passages first, then the fact-after ones, each in Z1's order."""
    return [c for s in STRATA for c in cases if c["stratum"] == s]


def z1_items(target: str) -> tuple[list[dict], dict]:
    """Z1's chosen passages on the target (its gate.json order joined to its cases.jsonl) in run order, and its gate."""
    src = z1_run(target)
    for f in ("gate.json", "cases.jsonl"):
        assert (src / f).exists(), f"no Z1 run at {src} ({f}): 51.5 needs Z1's items"
    gate = json.loads((src / "gate.json").read_text())
    by = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    chosen = [by[(s, sc)] for s, sc in gate["order"]]
    info = {"run": src.name, "pass": gate["pass"], "org_read_accuracy": gate["org_read_accuracy"],
            "cases": gate["cases"], "eligible": gate["eligible"], "chosen": len(chosen),
            "sets": dict(collections.Counter(c["set"] for c in chosen)),
            "strata": {s: sum(c["stratum"] == s for c in chosen) for s in STRATA}}  # fmt: skip
    return run_order(chosen), info


def check_alignment(tok, items: list[dict]) -> dict:
    """Each item rebuilt with x50_zach.z1_cases on this tokenizer: the same other entity, the same O and S ids, patch
    token and answer tokens per reader."""
    keys = ("ids", "pos", "tok_A", "tok_b", "tok_lure")
    differ = []
    for s in sorted({c["set"] for c in items}):
        mine = {c["scene"]: c for c in items if c["set"] == s}
        ps = [p for p in Z.load_pairs(s, "z1")[0] if p[Z.LOOKUP]["scene"] in mine]
        rebuilt = {c["scene"]: c for c in Z.z1_cases(tok, ps)[0]}
        for scene, c in mine.items():
            r = rebuilt.get(scene)
            same = (
                r is not None
                and r["cf_bridge"] == c["cf_bridge"]
                and all(r["readers"][w][k] == c["readers"][w][k] for w in READERS for k in keys)
            )
            if not same:
                differ.append([s, scene])
    return {"items": len(items), "same": len(items) - len(differ), "differ": differ}


# ---- the switch by layer and the window (CPU; ours and his by the same code) ---------------------------------------


def switch_rates(rows: list[dict], reader: str, moved: tuple[str, ...], arm: str = "whole") -> dict[int, float]:
    """Per layer, the share of the reader's rows under `arm` whose route is in `moved` (point estimates)."""
    by: dict[int, list[int]] = collections.defaultdict(list)
    for r in rows:
        if r["reader"] == reader and r["arm"] == arm and r["layer"] is not None:
            by[int(r["layer"])].append(int(r["route"] in moved))
    return {la: float(np.mean(v)) for la, v in sorted(by.items())}


def window_end(rates: dict[int, float], bar: float = SWITCH_BAR) -> int | None:
    """The last layer whose switch share >= bar; None if none does."""
    hit = [la for la, v in rates.items() if v >= bar - EPS]
    return max(hit) if hit else None


def window_start(rates: dict[int, float], bar: float = SWITCH_BAR) -> int | None:
    hit = [la for la, v in rates.items() if v >= bar - EPS]
    return min(hit) if hit else None


def same_window(ours: dict[str, int | None], his: dict[str, int | None], tol: int = WINDOW_TOL) -> dict:
    """Per reader: within iff both ends exist and |his - ours| <= tol; the rule holds iff both readers are within."""
    per = {}
    for w in ("lookup", "recall"):
        o, h = ours.get(w), his.get(w)
        d = None if o is None or h is None else h - o
        per[w] = {"ours": o, "his": h, "diff": d, "within": d is not None and abs(d) <= tol}
    holds = all(v["within"] for v in per.values())
    return {"holds": holds, "label": "the same read window as ours" if holds else "not the same read window as ours",
            "per_reader": per}  # fmt: skip


def zach_beside(rates: dict[int, float]) -> dict:
    """Descriptive, against Zach's swap window (L4-L20, gone by L25): the first and last layer >= 0.3, and whether every
    sampled layer >= L25 is < 0.3."""
    late = {la: v for la, v in rates.items() if la >= ZACH_GONE}
    return {"first": window_start(rates), "last": window_end(rates), "his_window": list(ZACH_WINDOW),
            "gone_by_25": bool(late) and all(v < SWITCH_BAR - EPS for v in late.values())}  # fmt: skip


def ours_rows(target: str) -> list[dict]:
    """The stored 47.8 sweep's C2 rows (the test half), readers named lookup / recall."""
    src = A.RESULTS / OURS[target] / "outcomes.jsonl"
    inv = {v: k for k, v in OURS_READER.items()}
    return [{**r, "reader": inv[r["reader"]]} for r in X.read_jsonl(src) if r["condition"] == "C2"]


def ours_verdict(target: str) -> dict | None:
    """The newest opened 47.8 verdict (results/x47_anatomy/x47_8-<UTC>/x47_8.json) with the target tested, or None."""
    for d in sorted(A.RESULTS.glob("x47_8-*"), reverse=True):
        f = d / "x47_8.json"
        if f.exists():
            for m in json.loads(f.read_text())["models"]:
                if m["target"] == target and m["status"] == "tested":
                    return {"folder": rel(d), **m}
    return None


def reference(target: str) -> dict:
    """Ours: the stored 47.8 run's window ends per reader (switch_rates / window_end, as his), checked against the
    opened verdict's switch shares where one holds the target."""
    rows = ours_rows(target)
    rates = {w: switch_rates(rows, w, OURS_MOVED[w]) for w in ("lookup", "recall")}
    v = ours_verdict(target)
    check = None
    if v is not None:
        check = all(abs(v["cells"][str(la)][w]["switch"]["whole"][0] - r) <= EPS
                    for w in rates for la, r in rates[w].items() if str(la) in v["cells"])  # fmt: skip
    return {"run": OURS[target], "verdict": v["folder"] if v else None, "matches_verdict": check,
            "rates": {w: {str(la): round(x, 4) for la, x in r.items()} for w, r in rates.items()},
            **{w: window_end(r) for w, r in rates.items()},
            "zach": {w: zach_beside(r) for w, r in rates.items()}}  # fmt: skip


# ---- plan (CPU) ---------------------------------------------------------------------------------------------------


def stage_plan(plan_dir: str | None = None) -> Path:
    """On BJ_TARGET's tokenizer: Z1's chosen items after every filter (from its run), their re-alignment, the sweep, the
    arms and rows; the reference (ours) for both models; 2 marked prompts per stratum. Writes plan-<target>.{json,md}
    and reference.json into plan_dir (default results/x51_depth/plan-<UTC>/)."""
    from bridge_jspace.utils import git_state
    from scripts import x45m

    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    t = pins.TARGET
    assert t in LAYERS, f"51.5 runs on {TARGETS}, not {t}"
    tok = x45m.tokenizer()
    items, info = z1_items(t)
    align = check_alignment(tok, items)
    gate = json.loads((z1_run(t) / "gate.json").read_text())
    per_reader = 1 + len(LAYERS[t]) * len(ARMS)
    blob = {"target": t, "code": git_state(), "z1": info, "z1_counts": gate.get("counts"), "alignment": align,
            "layers": list(LAYERS[t]), "arms": list(ARMS), "rows_per_item_per_reader": per_reader,
            "rows": len(items) * len(READERS) * per_reader, "read_calls_rows": per_reader, "run": RUNS[t],
            "reference": REFERENCE[t], "order": [[c["set"], c["scene"], c["stratum"]] for c in items]}  # fmt: skip
    ref = {m: reference(m) for m in TARGETS}
    for m in TARGETS:
        assert {w: ref[m][w] for w in ("lookup", "recall")} == REFERENCE[m], f"{m}: REFERENCE differs from {ref[m]}"
    (out / "reference.json").write_text(json.dumps(ref, indent=1) + "\n")
    lines = [f"# x51_depth plan on {t}'s tokenizer (51.5; UNVERIFIED)", "",
             f"Z1 run {info['run']}: gate pass {info['pass']} (O read {info['org_read_accuracy']} over {info['cases']} "
             f"passages), eligible {info['eligible']}, chosen {info['chosen']} (sets {info['sets']}; strata "
             f"{info['strata']}). Re-aligned on this tokenizer: {align['same']} of {align['items']} the same.", "",
             f"Sweep {list(LAYERS[t])} ({len(LAYERS[t])} layers); arms {list(ARMS)}; rows per item and reader "
             f"{per_reader} (none once + layers x arms); {blob['rows']} rows.", "",
             "Ours (reference, last layer >= 0.3): " + "; ".join(
                 f"{m} {ref[m]['run']}: lookup L{ref[m]['lookup']}, recall L{ref[m]['recall']} (matches the opened "
                 f"verdict {ref[m]['verdict']}: {ref[m]['matches_verdict']})" for m in TARGETS), ""]  # fmt: skip
    for s in STRATA:
        for c in [c for c in items if c["stratum"] == s][:2]:
            lines += [f"### {c['scene']} ({c['set']}, {s}): {c['bridge']} -> {c['cf_bridge']} ({c['answer']} -> "
                      f"{c['cf_answer']})", ""]  # fmt: skip
            for w, rd in c["readers"].items():
                lines += [f"**{w}** O:", "", "```", Z.mark(tok.decode, rd["ids"]["org"], rd["pos"]), "```", ""]
    (out / f"plan-{t}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / f"plan-{t}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:8]))
    print(out)
    return out


# ---- GPU ----------------------------------------------------------------------------------------------------------


def changes(model, cases: list[dict], layers: tuple[int, ...]) -> dict[str, Any]:
    """Per reader, Delta = h_S - h_O at the patch token at every sweep layer [n, layers, d] (CPU, fp32)."""
    import torch

    from bridge_jspace.utils import progress

    out: dict[str, list] = {w: [] for w in READERS}
    for c in progress(cases, f"the change at the patch token, {len(layers)} layers (passage)"):
        for w, rd in c["readers"].items():
            h = {
                v: model.run(torch.tensor([rd["ids"][v]], device=model.device), record=layers)[1]
                for v in ("org", "alt")
            }
            out[w].append(
                torch.stack([(h["alt"][la][rd["pos"]] - h["org"][la][rd["pos"]]).float().cpu() for la in layers])
            )
            del h
    return {w: torch.stack(v) for w, v in out.items()}


def layer_arms(model, lens, letters, deltas: dict[str, Any], layers: tuple[int, ...], cases: list[dict]):
    """Per layer, from the layer's own J++ atoms: every arm's rows per reader (CPU) and the norms / shares per item."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    dev = model.device
    arms: dict[str, dict[int, dict[str, Any]]] = {w: {} for w in deltas}
    norms = []
    for li, la in enumerate(progress(layers, "per-layer parts (layer)")):
        jdic = lens.vectors(la, letters).to(dev)
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
        abasis = A.random_atoms_basis(jdic, ATOMS_SEED + la)
        for w, d in deltas.items():
            x = d[:, li].to(dev)
            more, sh = R.removal_arms(x, {"jpp": X.fit(jdic, x, X.K_MAIN, "signed").to(dev)}, basis)
            ratoms = SP.random_subspace_part(x, sh["jpp"], abasis)
            arms[w][la] = {
                "whole": x.cpu(),
                **{k: v.cpu() for k, v in more.items()},
                "no_jpp_ratoms": (x - ratoms).cpu(),
            }
            assert tuple(arms[w][la]) == ARMS, tuple(arms[w][la])
            sh_r = A.shares_of(x, {"rand": x - more["no_jpp_rand"], "ratoms": ratoms})
            norms += [{"scene": c["scene"], "set": c["set"], "stratum": c["stratum"], "layer": la, "reader": w,
                       "norm": round(float(x[i].norm()), 4), "share_jpp": round(float(sh["jpp"][i]), 5),
                       "share_rand": round(float(sh_r["rand"][i]), 5), "share_ratoms": round(float(sh_r["ratoms"][i]), 5)}
                      for i, c in enumerate(cases)]  # fmt: skip
            del x, more, ratoms
        del jdic, basis, abasis
    return arms, norms


def read_labels(layers: tuple[int, ...]) -> list[tuple[int | None, str]]:
    """One item's rows per reader: none once, then every arm at every layer."""
    return [(None, "none")] + [(la, a) for la in layers for a in ARMS]


def reads(model, cases: list[dict], arms, layers: tuple[int, ...], ws, desc: str) -> list[dict]:
    """Every arm at every layer read on O per reader (Z1's read and routes)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    labels = read_labels(layers)
    rows = []
    for i, c in enumerate(progress(cases, desc)):
        for w, rd in c["readers"].items():
            cands = torch.tensor(
                sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}), device=dev
            )
            edits = [
                {} if la is None else {la: AddRows(arms[w][la][a][i : i + 1].to(dev), [rd["pos"]])} for la, a in labels
            ]
            logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", [], ws)
            for (la, a), lg in zip(labels, logits, strict=True):
                row = X.read_row(lg, rd, cands)
                rows.append({"scene": c["scene"], "set": c["set"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                             "relation": c["relation"], "stratum": c["stratum"], "layer": la, "reader": w, "arm": a,
                             "route": Z.route(row["top"], rd), **row})  # fmt: skip
    return rows


def split_sweep(model, tok, ws, layers: tuple[int, ...], out: Path) -> dict:
    """--split: Z3's items on this model (x50_zach's build, competence and gate, sets in order until N_ITEMS are
    eligible), the whole change at every sweep layer, the lookup's route (x6_routes.classify)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    cases, comp, counts, ok = [], [], {}, []
    for s in Z.sets_of("z3"):
        got, counts[s] = Z.build(tok, model, "z3", s, out)
        cases += got
        comp += Z.competence(model, got, ws)
        _, ok = Z.gate_of(cases, comp)
        if len(ok) >= Z.N_ITEMS:
            break
    gate, ok = Z.gate_of(cases, comp)
    chosen = ok[: Z.N_ITEMS]
    gate.update({"chosen": len(chosen), "counts": counts, "order": [[c["set"], c["scene"]] for c in chosen]})
    X.write_jsonl(out / "split_competence.jsonl", comp)
    X.write_jsonl(out / "split_cases.jsonl", chosen)
    (out / "split_gate.json").write_text(json.dumps(gate, indent=1) + "\n")
    rows = []
    for c in progress(chosen, "split: the whole change by layer (passage)"):
        rd = c["readers"][Z.LOOKUP]
        h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=layers)[1] for v in ("org", "alt")}
        deltas = {la: (h["alt"][la][rd["pos"]] - h["org"][la][rd["pos"]]).float()[None] for la in layers}
        del h
        labels = [(None, "none")] + [(la, "whole") for la in layers]
        edits = [{} if la is None else {la: AddRows(deltas[la], [rd["pos"]])} for la, _ in labels]
        cands = torch.tensor(sorted(set(rd["route_tokens"].values())), device=dev)
        logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", [], ws)
        for (la, a), lg in zip(labels, logits, strict=True):
            row = X.read_row(lg, rd, cands)
            rows.append({"scene": c["scene"], "set": c["set"], "entity": c["bridge"], "layer": la, "reader": Z.LOOKUP,
                         "condition": "C2", "arm": a, "route": R.classify(row["top"], rd), **row})  # fmt: skip
    X.write_jsonl(out / "split_outcomes.jsonl", rows)
    return {k: v for k, v in gate.items() if k != "order"}


def stage_run(name: str, why: str, split: bool = False) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state
    from scripts import x6_routes as R

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.5 reads Z1's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in LAYERS, f"51.5 runs on {TARGETS}, not {target}"
    layers = LAYERS[target]
    pins.check_lens_layers(layers)
    items, z1 = z1_items(target)
    src = z1_run(target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, src / "gate.json", src / "cases.jsonl", A.RESULTS / OURS[target] / "outcomes.jsonl"]
    m = {"exp": EXP, "run": name, "why": why, "test": TEST, "spec": "jobs/c3/batch51.yaml (51.5)",
         "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
         "inputs": {rel(p): X.sha256_of(p) for p in inputs if p.exists()}, "z1": z1,
         "layers": list(layers), "n_layers": pins.N_LAYERS, "arms": list(ARMS), "strata_order": list(STRATA),
         "k": X.K_MAIN, "omp": "signed", "patch": "the last token of the pointer sentence's name (Z1)",
         "read": "Z1's: the top token after the prompt (his chat framing, no prefill) against S's answer's first token",
         "rule": RULE, "as_computed": AS_COMPUTED, "reference": {"ours": OURS[target], **REFERENCE[target]},
         "split": split, "seeds": {"random_atoms": f"{ATOMS_SEED} + layer", "random_subspace": f"{X.SUBSPACE_SEED} + layer",
                                   "bootstrap": X.BOOT_SEED, "view": VIEW_SEED},
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    if target in DESIGN_RUNS:  # batch 52: no Q-line
        m |= {"question": DESIGN_NOTE, "batch": 52, "sealed": "none: verdict --design-from"}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    align = check_alignment(tok, items)
    (out / "gate.json").write_text(json.dumps({"z1": z1, "alignment": align,
                                               "order": [[c["set"], c["scene"], c["stratum"]] for c in items]}, indent=1) + "\n")  # fmt: skip
    assert align["same"] == align["items"], f"Z1's items do not re-align on this tokenizer: {align['differ'][:5]}"
    X.write_jsonl(out / "cases.jsonl", items)
    ws = X.whitespace_mask(model)
    lens = JLens(model, "jpp")
    letters = model.letter_token_ids()
    rows: list[dict] = []
    norms: list[dict] = []
    done = []
    with torch.no_grad():
        for s in STRATA:
            mine = [c for c in items if c["stratum"] == s]
            if not mine:
                continue
            deltas = changes(model, mine, layers)
            arms, nm = layer_arms(model, lens, letters, deltas, layers, mine)
            del deltas
            rows += reads(model, mine, arms, layers, ws, f"{s}: reads over {len(layers)} layers (passage)")
            norms += nm
            del arms
            done.append(s)
            X.write_jsonl(out / "outcomes.jsonl", rows)  # the stratum's rows written before the next one starts
            X.write_jsonl(out / "norms.jsonl", norms)
            print(f"wrote {len(rows)} rows ({', '.join(done)} done)", flush=True)
        split_gate = split_sweep(model, tok, ws, layers, out) if split else None
    m.update({"items": len(items), "strata_done": done, "complete": True, "split_gate": split_gate})
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out} (sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU, sealed) ----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer (the 'Dan:' line of the question's block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def nan3() -> list[float]:
    return [math.nan, math.nan, math.nan]


def layer_cell(rows: list[dict], layer: int, n_boot: int) -> dict:
    """At one layer per reader: the whole change's switch share (and per stratum), the extra loss without J++ against
    47.8's random atoms (and against Z1's random subspace beside), cluster bootstrap over the bridge entity."""
    out: dict[str, Any] = {"layer": layer}
    for w in READERS:
        by = {(r["set"], r["scene"], r["arm"]): r for r in rows if r["reader"] == w and r["layer"] == layer}
        keys = list(dict.fromkeys((r["set"], r["scene"]) for r in rows if r["reader"] == w and r["layer"] == layer))
        keys = [k for k in keys if all((*k, a) in by for a in ARMS)]
        if not keys:
            continue
        ents = [by[(*k, "whole")]["entity"] for k in keys]
        sw = {a: [int(by[(*k, a)]["route"] in HIS_MOVED) for k in keys] for a in ARMS}
        cell: dict[str, Any] = {
            "n": len(keys),
            "entities": len(set(ents)),
            "switch": Z.share_ci(sw["whole"], ents, n_boot),
        }
        cell["interpretable"] = bool(cell["switch"][0] >= SWITCH_BAR - EPS)
        for tag, rand in (("loss", "no_jpp_ratoms"), ("loss_subspace", "no_jpp_rand")):
            c = X.cell({"whole": sw["whole"], "no_part": sw["no_jpp"], "no_rand": sw[rand]}, ents, n_boot)
            cell[tag] = {k: c[k] for k in ("excess", "Jdep", "Rdep", "S_whole", "valid")}
        cell["strata"] = {}
        for s in STRATA:
            idx = [i for i, k in enumerate(keys) if by[(*k, "whole")]["stratum"] == s]
            cell["strata"][s] = {"n": len(idx), "switch": Z.share_ci([sw["whole"][i] for i in idx], [ents[i] for i in idx], n_boot)
                                 if idx else nan3()}  # fmt: skip
        cell["routes"] = {a: dict(collections.Counter(by[(*k, a)]["route"] for k in keys)) for a in ARMS}
        out[NAME[w]] = cell
    return out


def split_result(src: Path, n_boot: int) -> dict | None:
    """--split's identity / position / value / original / other shares under the whole change per layer (descriptive)."""
    f = src / "split_outcomes.jsonl"
    if not f.exists():
        return None
    rows = X.read_jsonl(f)
    keys = list(dict.fromkeys((r["set"], r["scene"]) for r in rows if r["arm"] == "whole"))
    ent = {(r["set"], r["scene"]): r["entity"] for r in rows}
    out = {}
    for la in sorted({r["layer"] for r in rows if r["layer"] is not None}):
        mine = [r for r in rows if r["layer"] == la and r["arm"] == "whole"]
        out[str(la)] = Z.route_shares(mine, keys, [ent[k] for k in keys], n_boot)
    return {"n": len(keys), "shares": out, "gate": json.loads((src / "split_gate.json").read_text())}


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    target = {r: t for d in (RUNS, DESIGN_RUNS) for t, r in d.items()}.get(run)
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        return {"run": run, "target": target, "status": "pending", "why": "no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    target = m["model"]["target"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    strata = [s for s in STRATA if any(r["stratum"] == s for r in rows)]
    partial = strata != list(STRATA) and not m.get("complete")
    layers = [la for la in m["layers"] if any(r["layer"] == la for r in rows)]
    cells = {la: layer_cell(rows, la, n_boot) for la in layers}
    his = {NAME[w]: switch_rates(rows, w, HIS_MOVED) for w in READERS}
    by_stratum = {s: {NAME[w]: switch_rates([r for r in rows if r["stratum"] == s], w, HIS_MOVED) for w in READERS}
                  for s in strata}  # fmt: skip
    ref = reference(target)
    ours = {w: ref[w] for w in ("lookup", "recall")}
    decisive = his if not partial else by_stratum.get("fact-first", {})
    rule = same_window(ours, {w: window_end(r) for w, r in decisive.items()})
    z1 = m["z1"]
    status = "tested" if z1["pass"] else "not tested (Z1's gate; numbers descriptive only)"
    return {"run": run, "target": target, "status": status, "partial": partial, "strata": strata,
            "layers": layers, "n_layers": m["n_layers"], "n": len({(r["set"], r["scene"]) for r in rows}),
            "z1": z1, "reference": ref, "reference_matches_spec": ours == REFERENCE[target], "rule": rule,
            "decided_on": "fact-first only (partial run)" if partial else "all of Z1's items (both strata)",
            "ends": {"pooled": {w: window_end(r) for w, r in his.items()},
                     **{s: {w: window_end(r) for w, r in v.items()} for s, v in by_stratum.items()}},
            "zach": {"his_passages": {w: zach_beside(r) for w, r in his.items()}, "our_scenes": ref["zach"]},
            "cells": {str(la): c for la, c in cells.items()}, "split": split_result(src, n_boot)}  # fmt: skip


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, (list, tuple)):
        if v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
            return "-"
        return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")
    return f"{v:.2f}" if isinstance(v, float) else str(v)


def end(la: int | None) -> str:
    return "none" if la is None else f"L{la}"


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.5: the anatomy by depth on Zach's passages (UNVERIFIED)", "",
             f"Batch 51, test 51.5 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). Z1's items (his v2 passages, the "
             f"pointer's name changed), the whole change at the name's last token at one layer at a time; readers K "
             f"(lookup) and M (recall). Cluster bootstrap over the bridge entity ({n_boot}, seed {X.BOOT_SEED}).", "",
             f"Rule (fixed in advance): {RULE}", "", f"As computed: {AS_COMPUTED}", "",
             "| model | run | status | n | decided on | lookup end: his / ours (diff) | recall end: his / ours (diff) | label |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if "rule" not in mm:
            lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} ({mm.get('why', '')}) | | | | | |")
            continue
        pr = mm["rule"]["per_reader"]
        lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} | {mm['n']} | {mm['decided_on']} | "
                     + " | ".join(f"{end(pr[w]['his'])} / {end(pr[w]['ours'])} ({pr[w]['diff']})" for w in ("lookup", "recall"))
                     + f" | {mm['rule']['label'] if mm['status'] == 'tested' else '(' + mm['rule']['label'] + ')'} |")  # fmt: skip
    for mm in models:
        if "rule" not in mm:
            continue
        ref, e = mm["reference"], mm["ends"]
        lines += ["", f"## {mm['target']} ({mm['run']})", "",
                  f"Z1's items: {mm['z1']['chosen']} (strata {mm['z1']['strata']}; Z1's gate pass {mm['z1']['pass']}, "
                  f"O read {mm['z1']['org_read_accuracy']}). Ours: {ref['run']} (lookup {end(ref['lookup'])}, recall "
                  f"{end(ref['recall'])}; matches the opened verdict {ref['verdict']}: {ref['matches_verdict']}; the "
                  f"spec's reference {mm['reference_matches_spec']}).", "",
                  "Window ends (last layer >= 0.30): " + "; ".join(f"{k}: lookup {end(v['lookup'])}, recall {end(v['recall'])}"
                                                                  for k, v in e.items()) + ".", "",
                  "Beside, Zach's swap window (L4-L20, gone by L25): " + "; ".join(
                      f"{side} {w} L{z['first']}-L{z['last']} gone by L25 {z['gone_by_25']}" if z["first"] is not None
                      else f"{side} {w} none" for side, zz in mm["zach"].items() for w, z in zz.items()) + ".", "",
                  "| layer | n | lookup switch | recall switch | fact-first lookup / recall | fact-after lookup / recall "
                  "| lookup extra loss no J++ (subspace) | recall extra loss no J++ (subspace) |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for la, c in mm["cells"].items():
            lk, rc = c.get("lookup"), c.get("recall")
            if not lk or not rc:
                continue
            st = {s: f"{fmt(lk['strata'][s]['switch'])} / {fmt(rc['strata'][s]['switch'])}" for s in STRATA}
            lines.append(f"| {la} | {lk['n']} | {fmt(lk['switch'])} | {fmt(rc['switch'])} | {st['fact-first']} | "
                         f"{st['fact-after']} | {fmt(lk['loss']['excess'])} ({fmt(lk['loss_subspace']['excess'])}) | "
                         f"{fmt(rc['loss']['excess'])} ({fmt(rc['loss_subspace']['excess'])}) |")  # fmt: skip
        if mm.get("split"):
            sp = mm["split"]
            lines += ["", f"Identity / position split (--split; Z3's items, n {sp['n']}; descriptive):", "",
                      "| layer | " + " | ".join(SPLIT_ROUTES) + " |", "|---|" + "---|" * len(SPLIT_ROUTES)]  # fmt: skip
            lines += [
                f"| {la} | " + " | ".join(fmt(s[rt]) for rt in SPLIT_ROUTES) + " |" for la, s in sp["shares"].items()
            ]
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, design_from: bool = False) -> Path:
    """51.5's verdict (sealed until Q51.5), or with design_from (batch 52, Dan's morning queue item 2) Lightning's run
    made with the 9B / 27B spec's design, alone: no seal, x52_depth51-<UTC>/."""
    answer = DESIGN_NOTE if design_from else unsealed()
    models = [model_result(r, n_boot) for r in runs]
    out = RESULTS / f"{'x52_depth51' if design_from else 'x51_5'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if design_from:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52, ") for ln in lines]
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "x51_5.json").write_text(
        json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str) + "\n"
    )
    tested = [mm for mm in models if "rule" in mm]
    if tested:
        figure(tested, out / "x51_5_depth.png")
    print("\n".join(lines[:12]))
    print(out)
    return out


# ---- figure (fig06b's layout: ours beside his) ----------------------------------------------------------------------


def ours_panel(v: dict | None) -> dict | None:
    """Our scenes' fig06b quantities from an opened 47.8 verdict model blob: per layer the lookup's identity / position
    shares, the recall's switch, the extra losses without J++."""
    if v is None:
        return None
    layers = list(v["layers"])
    c = [v["cells"][str(la)] for la in layers]
    return {"layers": layers, "n": c[0]["lookup"]["n"],
            "bars": {rt: [x["lookup"]["share"]["whole"][rt] for x in c] for rt in ("identity", "position")},
            "lookup": [x["lookup"]["switch"]["whole"] for x in c], "recall": [x["recall"]["switch"]["whole"] for x in c],
            "loss": {w: [x[w]["loss"]["J"]["excess"] if "J" in x[w]["loss"] else nan3() for x in c] for w in ("lookup", "recall")},
            "strata": None}  # fmt: skip


def his_panel(mm: dict) -> dict:
    layers = [int(la) for la in mm["cells"]]
    c = [mm["cells"][str(la)] for la in layers]
    return {"layers": layers, "n": mm["n"], "bars": {"identity": [x["lookup"]["switch"] for x in c]},
            "lookup": [x["lookup"]["switch"] for x in c], "recall": [x["recall"]["switch"] for x in c],
            "loss": {w: [x[w]["loss"]["excess"] for x in c] for w in ("lookup", "recall")},
            "strata": {s: [x["lookup"]["strata"][s]["switch"][0] for x in c] for s in STRATA}}  # fmt: skip


def _ni_spans(layers: list[int], flags: list[bool]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    gaps = np.diff(layers) if len(layers) > 1 else np.array([2])
    for i, (la, f) in enumerate(zip(layers, flags, strict=True)):
        if not f:
            continue
        lo = la - (gaps[i - 1] if i > 0 else gaps[0]) / 2
        hi = la + (gaps[i] if i < len(gaps) else gaps[-1]) / 2
        if out and abs(out[-1][1] - lo) < 1e-9:
            out[-1] = (out[-1][0], hi)
        else:
            out.append((lo, hi))
    return out


def figure(models: list[dict], path: Path) -> Path:
    """Per model two rows (fig06b's panel: lookup bars, recall line, not-interpretable shading; under it the extra loss
    without J++ per reader), columns our scenes (47.8) | his passages (51.5); the window ends marked, Zach's L4-L20."""
    from scripts import story_style as S

    plt = S.setup()
    h = 4.6 * len(models) + 2.4
    fig, axes = plt.subplots(2 * len(models), 2, figsize=(S.WIDTH, h), sharey="row",
                             squeeze=False, gridspec_kw={"height_ratios": [2, 1] * len(models)})  # fmt: skip
    fig.subplots_adjust(left=0.1, right=0.98, top=1 - 1.2 / h, bottom=1.25 / h, hspace=0.45, wspace=0.08)
    S.title(fig, "The read window by depth: his passages beside our scenes",
            "Bars: lookup switches under the whole change at one layer; line: recall switches; 95% whiskers, bands.\n"
            "Lower: extra loss without J++. Dashed: each reader's last layer >= 0.3. UNVERIFIED.", limit=100)  # fmt: skip
    for i, mm in enumerate(models):
        panels = (("our scenes (47.8)", ours_panel(ours_verdict(mm["target"]))), ("his passages (51.5)", his_panel(mm)))
        for j, (title, p) in enumerate(panels):
            ax, lx = axes[2 * i, j], axes[2 * i + 1, j]
            ax.set_title(f"{mm['target']}: {title}", fontsize=S.FONT, loc="left")
            if p is None:
                S.empty(ax, "no opened 47.8 verdict")
                continue
            x = np.array(p["layers"], dtype=float)
            w = 0.8 * (float(np.min(np.diff(x))) if len(x) > 1 else 2.0)
            for a in (ax, lx):
                for lo, hi in _ni_spans(p["layers"], [v[0] < S.NI_SWITCH - EPS for v in p["lookup"]]):
                    a.axvspan(lo, hi, **S.NI_SHADE)
                if j == 1:
                    a.axvspan(*ZACH_WINDOW, color=S.COL["shade"], alpha=0.5, lw=0, zorder=0)
            bottom = np.zeros(len(x))
            for rt, vals in p["bars"].items():
                v = np.array(vals, dtype=float)
                ax.bar(x, v[:, 0], bottom=bottom, width=w, color=S.COL[rt], zorder=2)
                ax.vlines(x, bottom + v[:, 1], bottom + v[:, 2], color="#1e1e1e", lw=0.8, zorder=3)
                bottom += v[:, 0]
            ax.bar(x, 1 - bottom, bottom=bottom, width=w, zorder=2, **S.EMPTY)
            rc = np.array(p["recall"], dtype=float)
            ax.fill_between(x, rc[:, 1], rc[:, 2], color=S.COL["recall"], alpha=0.18, lw=0, zorder=4)
            ax.plot(x, rc[:, 0], color=S.COL["recall"], marker="D", ms=4, lw=1.6, zorder=5)
            if p["strata"]:
                ax.plot(x, p["strata"]["fact-first"], color=S.COL["lookup"], ls=":", lw=1.4, zorder=5)
                ax.plot(x, p["strata"]["fact-after"], color=S.COL["lookup"], ls="--", lw=1.0, zorder=5)
            for rates, col in ((p["lookup"], S.COL["lookup"]), (p["recall"], S.COL["recall"])):
                e = window_end({int(la): v[0] for la, v in zip(p["layers"], rates, strict=True)})
                if e is not None:
                    ax.axvline(e, color=col, ls="--", lw=1.2, zorder=6)
            ax.axhline(SWITCH_BAR, color=S.COL["muted"], lw=0.6, ls=":", zorder=1)
            ax.set_ylim(0, 1)
            S.panel_tag(ax, str(p["n"]), "fixed", inside=True)
            lx.axhspan(S.XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
            for wname in ("lookup", "recall"):
                v = np.array(p["loss"][wname], dtype=float)
                lx.fill_between(x, v[:, 1], v[:, 2], color=S.COL[wname], alpha=0.15, lw=0)
                lx.plot(x, v[:, 0], color=S.COL[wname], marker="o", ms=3, lw=1.4)
            lx.axhline(0, color="#1e1e1e", lw=0.5)
            lx.set_ylim(*S.XLIM)
            lx.set_xlabel("layer", loc="right")
            for a in (ax, lx):
                a.set_xlim(0, mm["n_layers"])
        axes[2 * i, 0].set_ylabel("share")
        axes[2 * i + 1, 0].set_ylabel("extra loss\nno J++")
    hs = [plt.Rectangle((0, 0), 1, 1, color=S.COL["identity"]), plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]),
          plt.Rectangle((0, 0), 1, 1, **S.EMPTY), plt.Line2D([], [], color=S.COL["recall"], marker="D", lw=1.6),
          plt.Line2D([], [], color=S.COL["lookup"], ls=":"), plt.Line2D([], [], color=S.COL["lookup"], ls="--", lw=1.0),
          plt.Rectangle((0, 0), 1, 1, color=S.COL["shade"], alpha=0.5)]  # fmt: skip
    fig.legend(hs, ["identity (his: the other entity's answer)", "position", "the original answer", "recall switches",
                    "his lookup, fact-first", "his lookup, fact-after", "Zach's swap window L4-L20"],
               loc="lower center", ncol=3, fontsize=S.FONT - 2, frameon=False, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    return path


# ---- view (CPU, sealed) -------------------------------------------------------------------------------------------


def view_lines(
    run: str, decode=None, n_prompts: int = N_PROMPTS, n_rows: int = N_ROWS, seed: int = VIEW_SEED
) -> list[str]:
    """The verify pack: n_prompts random items (seed) with each reader's O and S prompt as the model reads it (the patch
    token in ⟦…⟧), and n_rows random rows per arm (seed) with their top token and route."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    cases = X.read_jsonl(src / "cases.jsonl")
    rows = X.read_jsonl(src / "outcomes.jsonl")
    lines = [f"## {run} ({m['model']['target']}): {min(n_prompts, len(cases))} random items of {len(cases)} "
             f"(random.Random({seed}))", ""]  # fmt: skip
    for i in sorted(random.Random(seed).sample(range(len(cases)), min(n_prompts, len(cases)))):
        c = cases[i]
        lines += [f"### {c['scene']} ({c['set']}, {c['stratum']}): {c['bridge']} -> {c['cf_bridge']} ({c['answer']} -> "
                  f"{c['cf_answer']})", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            lines += [f"**{w}** ({rd['id']}), O:", "", "```", Z.mark(decode, rd["ids"]["org"], rd["pos"]), "```", "",
                      "S (the source):", "", "```", Z.mark(decode, rd["ids"]["alt"], rd["pos"]), "```", ""]  # fmt: skip
    for a in ("none", *ARMS):
        mine = [r for r in rows if r["arm"] == a]
        pick = sorted(random.Random(seed).sample(range(len(mine)), min(n_rows, len(mine))))
        lines += [f"### arm {a}: {len(pick)} random rows of {len(mine)} (random.Random({seed}))", "",
                  "| scene | stratum | reader | layer | top token | route | switched |", "|---|---|---|---|---|---|---|"]  # fmt: skip
        lines += [f"| {mine[k]['scene']} | {mine[k]['stratum']} | {mine[k]['reader']} | {mine[k]['layer']} | "
                  f"{decode([mine[k]['top']])!r} | {mine[k]['route']} | {mine[k]['switched']} |" for k in pick]  # fmt: skip
        lines.append("")
    return lines


def stage_view(runs: list[str], decode=None) -> Path:
    unsealed()
    out = RESULTS / f"x51_5-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.5 verify-pack view: prompts as the model reads them (⟦…⟧ the patch token) and random rows per arm. "
             "UNVERIFIED.", ""]  # fmt: skip
    for r in runs:
        if (RESULTS / r / "outcomes.jsonl").exists():
            lines += view_lines(r, decode)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_depth/<name>/)")
    ap.add_argument(
        "--why",
        default="batch 51, test 51.5 (jobs/c3/batch51.yaml; Q51.5, sealed): the anatomy by depth on Zach's passages",
    )
    ap.add_argument(
        "--split", action="store_true", help="run: also the identity / position split on Z3's items (off by default)"
    )
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the 51.5 runs")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--plan-dir", help="plan: the folder to write into (one per model, the same folder)")
    ap.add_argument("--design-from", action="store_true",
                    help="verdict: batch 52, the runs made with the 9B / 27B spec's design (DESIGN_RUNS: Lightning)")  # fmt: skip
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.plan_dir)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.split)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, a.design_from)
    else:
        stage_view(a.runs)


if __name__ == "__main__":
    main()
