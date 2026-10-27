"""x45s (test 45s; Dan 27 Oct ~15:00; jobs/c3/x45s_*.yaml; Q46.2 and Q46.3 in predictions/2026-10-27_dan.md, batch 46):
our main test (two people swap) and 45m's clean one-pick design on NVIDIA Nemotron 3.5 Lightning, with Zach's pinned J++,
at L30 (the middle of Zach's pre-registered band L27-33; one layer, no sweep). Arms whole / without the J++ part (signed
OMP, k = 25) / without a random part of the same share, both readers. The two runs are x0_necessity's own (sealed: no
verdict in the job); this script holds what comes before them (the smoke) and after them (the sealed verdict).

Stages:
  fetch            the pinned Lightning snapshot into the HF cache (the lens is a local file Zach copies in)
  smoke-manifest   CPU: results/x45s/<name>/manifest.json, written before anything else runs
  smoke            GPU, after kernel_nll.py has written <run>/knll_kernels.pt and <run>/knll_torch.pt:
                   - kernels: the mamba-ssm commit the load used equals BJ_MAMBA_SSM_REVISION (a 40-hex commit);
                     kernels vs the torch path on 32 WikiText rows within Zach's bar (|mean NLL diff| <= 0.01, top-1
                     agreement >= 0.95; docs/prereg_replication_1022.md, amendment 44)
                   - lens: the pinned J++ loads (its sha256 asserted by JLens) and has a map at L; the J++ readout of
                     the bridge word at L ranks the bridge among its domain's one-token items (top 10: reported)
                   - scenes: per design (two people swap / clean), the scenes whose bridge is one token at one position
                     and whose answers are one token each, per reader; at least X.N_MIN (150) needed
                   - mechanics on the first N_SMOKE scenes per design (scene order): a zero patch at L reproduces the
                     unedited logits exactly (same batch); the whole change written at the bridge word makes L's output
                     there the changed prompt's (within 1e-2 of its max |value|); per reader the unedited read, S's own
                     read and the whole change's switch (reported); the unedited read alone vs in the batch (reported)
                   exits 1 when a stop check fails (kernels, lens, scenes, no-op, write)
  smoke-gates      CPU: the read gate (>= 0.80 both readers; [0.75, 0.80) labelled descriptive) and >= 150 eligible
                   scenes of the two 8-scene x0_necessity smoke runs; exits 1 unless both pass
  verdict          CPU, SEALED: refuses until predictions/2026-10-27_dan.md holds Dan's Q46.2 and Q46.3 answers at
                   HEAD. 45s-a: X0's rule at L (jobs/c3/X0.md, as the main test's spec); 45s-b: 45m's rule's per-model
                   check (scripts/x45m.py). Beside them: the gap, its logit-difference and probability versions
                   (x0_logit_diff, x0_prob_and_shares), split by sentence order; a verify-pack view (10 random scenes,
                   seed 0, the prompt with the patch position marked, each arm's answer).

uv run python scripts/x45s.py smoke-manifest --name nem35l_x45s_smoke     # then kernel_nll.py x2, then smoke
uv run python scripts/x45s.py verdict --main nem35l_x45s_main --clean nem35l_x45s_clean --smoke nem35l_x45s_smoke
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import check_switches, loaded_hub_kernels, switches
from scripts import x0_necessity as X

EXP = "x45s"
RESULTS = pins.RESULTS_DIR / EXP
TARGET = "nemotron-3.5-lightning"
LAYER = X.PREDICTED[TARGET]
SET = "d1_topics_v3"
DESIGNS = {"main": "cf", "clean": "fresh"}  # 45s-a: two people swap; 45s-b: 45m's clean one-pick design
PREDICTIONS = "predictions/2026-10-27_dan.md"
QUESTIONS = {"main": "Q46.2", "clean": "Q46.3"}  # batch 46 (Dan ~15:20; reserved as Q45.14 / Q45.15 before)
KERNEL_REPO = "kernels-community/mamba-ssm"
REVISION_ENV = "BJ_MAMBA_SSM_REVISION"
NLL_DIFF_MAX, TOP1_MIN = 0.01, 0.95  # Zach's kernel bar (amendment 44)
WRITE_TOL = 1e-2  # the written state vs the changed prompt's, relative to its max |value| (multigpu_check's tolerance)
N_SMOKE, TOP_K = 8, 10
GATE, GATE_LOW = 0.80, 0.75
COMMIT = re.compile(r"^[0-9a-f]{40}$")
N_VIEW, VIEW_SEED = 10, 0


# ---- checks (CPU) -------------------------------------------------------------------------------------------------


def kernel_compare(with_kernels: dict, torch_path: dict) -> dict:
    """kernel_nll.py's two files: mean NLL with the hub kernels and with the torch path, their difference, the
    per-position top-1 agreement, and Zach's bar."""
    import torch

    assert with_kernels["kernels"], "the first file must be the kernels run"
    assert not torch_path["kernels"], "the second file must be the torch-path run (BJ_NO_KERNELS=1)"
    a, b = torch.cat(with_kernels["nll"]), torch.cat(torch_path["nll"])
    ta, tb = torch.cat(with_kernels["top"]), torch.cat(torch_path["top"])
    assert a.shape == b.shape, "the two files hold different rows"
    assert ta.shape == tb.shape, "the two files hold different rows"
    diff, agree = float(a.mean() - b.mean()), float((ta == tb).float().mean())
    return {"nll_kernels": round(float(a.mean()), 4), "nll_torch": round(float(b.mean()), 4), "diff": round(diff, 5),
            "top1_agreement": round(agree, 4), "positions": int(a.numel()),
            "pass": abs(diff) <= NLL_DIFF_MAX and agree >= TOP1_MIN}  # fmt: skip


def kernel_revision_check(loaded: dict[str, list[str]], expected: str | None) -> dict:
    """The mamba-ssm commit the load used against the expected one (BJ_MAMBA_SSM_REVISION, a 40-hex commit)."""
    got = loaded.get(KERNEL_REPO, [])
    if not expected or not COMMIT.match(expected):
        return {"pass": False, "loaded": got, "expected": expected,
                "why": f"{REVISION_ENV}={expected!r} is not a 40-hex commit: set it to Zach's revision"}  # fmt: skip
    ok = got == [expected]
    why = (
        "the loaded commit is the expected one"
        if ok
        else f"loaded {got or 'no mamba-ssm hub kernel'}, expected {expected}"
    )
    return {"pass": ok, "loaded": got, "expected": expected, "why": why}


def rank_among(scores, target: int, candidates: list[int]) -> int:
    """1 + the number of other candidates scoring at least the target's (a tie ranks the target lower)."""
    t = float(scores[target])
    return 1 + sum(float(scores[c]) >= t for c in candidates if c != target)


def gate_status(gate_json: dict, rendering: str = "chat") -> dict:
    """An x0_necessity run's read gate: pass (>= GATE both readers) with >= X.N_MIN eligible scenes; a gate in
    [GATE_LOW, GATE) is labelled descriptive only (never scored)."""
    g = gate_json["gate"][rendering]
    acc = g.get("org_accuracy") or {}
    low = min(acc.values()) if acc else 0.0
    label = "pass" if low >= GATE else "descriptive only (0.75 to 0.80)" if low >= GATE_LOW else "fail"
    return {"accuracy": acc, "label": label, "eligible": g.get("eligible"), "enough": bool(g.get("enough")),
            "ok": label == "pass" and bool(g.get("enough"))}  # fmt: skip


def dan_answers(rev: str = "HEAD") -> dict[str, str]:
    """Dan's committed answers (the 'Dan:' line of each question's own block, headed **Q46.2** / **Q46.3**, in the
    predictions file at `rev`), '' where none (also when the file is not committed there)."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=False).stdout  # fmt: skip
    return answers_in(text)


def answers_in(text: str) -> dict[str, str]:
    """Per design, the 'Dan:' line of its question's block in a predictions file's text ('' where none): the block
    starts at the line that begins with its bold id (a mention elsewhere does not count) and ends at the next one."""
    out = {}
    for design, q in QUESTIONS.items():
        start = re.search(rf"^\*\*{re.escape(q)}\*\*", text, re.M)
        block = text[start.end() :].split("\n**Q", 1)[0] if start else ""
        m = re.search(r"^Dan:(.*)$", block, re.M)
        out[design] = m.group(1).strip() if m else ""
    return out


# ---- fetch and manifest (CPU) -------------------------------------------------------------------------------------


def stage_fetch() -> None:
    from huggingface_hub import snapshot_download

    from scripts.prefetch import with_retries

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    path = with_retries(lambda: snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION), pins.MODEL_REPO)
    print("cached", pins.MODEL_REPO, pins.MODEL_REVISION[:8], path, flush=True)


def stage_smoke_manifest(name: str, why: str) -> Path:
    from bridge_jspace import chat

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "45s renders chat prompts: run with BJ_FORMAT unset"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": pins.git_state(), "lens": X.lens_record(),
         "set": SET, "layer": LAYER, "designs": DESIGNS, "n_smoke": N_SMOKE, "smoke_scenes": "the first N_SMOKE "
         "scenes made per design, in scene order (X0's build_cases)", "order": X.order_record(),
         "kernel": {"repo": KERNEL_REPO, "expected_revision": os.environ.get(REVISION_ENV),
                    "bar": {"nll_diff_max": NLL_DIFF_MAX, "top1_min": TOP1_MIN}, "files": ["knll_kernels.pt", "knll_torch.pt"]},
         "stop_checks": ["kernel revision", "kernel vs torch NLL", "lens sha256 and map at the layer",
                         f"scenes >= {X.N_MIN} per reader per design", "no-op patch exact", "write at the bridge word"],
         "reported": ["lens readout rank of the bridge among its domain's one-token items", "unedited, S and whole-change "
                      "reads", "the unedited read alone vs in the batch"],
         "spec": "jobs/c3/x45s_smoke_lightning.yaml"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    return out


# ---- the smoke (GPU) ----------------------------------------------------------------------------------------------


def candidate_ids(tok, domain: str) -> list[int]:
    """The domain's items that are one token after a space, as their token ids (the bridge's candidates)."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    return sorted({S.ids(tok, " " + t)[0] for t in T.DOMAINS[domain].values if len(S.ids(tok, " " + t)) == 1})


def scene_counts(tok, design: str) -> tuple[list[dict], dict]:
    """The design's chat cases on this tokenizer (X0's build_cases) and the counts: scenes made, dropped by reason,
    and per reader the cases whose org and alt answers are one token each."""
    from scripts import suite_v1 as S

    X.ALT, X.RENDERINGS = DESIGNS[design], ("chat",)
    cases, counts = X.build_cases(tok, SET)
    one = {w: sum(all(len(S.ids(tok, a)) == 1 for a in (c["readers"][w]["answer"], c["readers"][w]["cf_answer"]))
                  for c in cases) for w in X.READERS}  # fmt: skip
    return cases, {**counts, "one_token_answers": one, "enough": min(one.values(), default=0) >= X.N_MIN}


def mechanics(model, lens, cases: list[dict], layer: int, candidates) -> list[dict]:
    """Per smoke scene and reader: the no-op patch, the write at the bridge word, the reads, the batch check and the
    lens readout (see the module docstring). `candidates(domain)` gives the domain's one-token item ids."""
    import torch

    from scripts.exp04_brew_parts import AddRows

    ws = X.whitespace_mask(model)
    rows = []
    with torch.no_grad():
        for c in cases:
            ids = c["readers"][X.LOOKUP]["ids"]  # both readers' prompts agree through the bridge (scene_case)
            pos = c["pos"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer] for v in ids}
            delta = (h["alt"][pos] - h["org"][pos])[None]
            written = model.run(torch.tensor([ids["org"]], device=model.device), edits={layer: AddRows(delta, [pos])},
                                record=(layer,))[1][layer][pos]  # fmt: skip
            write_rel = float((written - h["alt"][pos]).abs().max() / h["alt"][pos].abs().max().clamp_min(1e-30))
            cand = candidates(c["domain"])
            lens_rank = {}
            for v in ("org", "alt"):
                target = ids[v][pos]
                scores = lens.readout(h[v][pos], layer)
                lens_rank[v] = rank_among(scores, target, sorted({*cand, target}))
            for w, rd in c["readers"].items():
                edits = [{}, {layer: AddRows(torch.zeros_like(delta), [pos])}, {layer: AddRows(delta, [pos])}]
                lg, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                alone, _ = X.read_logits(model, rd["ids"]["org"], [{}], "chat", c["space"], ws)
                alt, _ = X.read_logits(model, rd["ids"]["alt"], [{}], "chat", c["space"], ws)
                rows.append({"scene": c["scene"], "reader": w, "pos": pos, "write_rel": write_rel,
                             "noop_exact": bool(torch.equal(lg[0], lg[1])), "noop_max": float((lg[0] - lg[1]).abs().max()),
                             "unedited_right": int(lg[0].argmax()) == rd["tok_A"], "s_right": int(alt[0].argmax()) == rd["tok_b"],
                             "whole_switched": int(lg[2].argmax()) == rd["tok_b"],
                             "alone_vs_batch_max": float((alone[0] - lg[0]).abs().max()),
                             "alone_vs_batch_same_top": int(alone[0].argmax()) == int(lg[0].argmax()),
                             "lens_rank_org": lens_rank["org"], "lens_rank_alt": lens_rank["alt"],
                             "candidates": len(set(cand))})  # fmt: skip
    return rows


def summarize(rows: list[dict]) -> dict:
    """The smoke's mechanics checks over its rows (stop: no-op, write; reported: the rest)."""
    n = len(rows)
    return {"rows": n, "noop_exact": sum(r["noop_exact"] for r in rows), "noop_max": max((r["noop_max"] for r in rows), default=None),
            "write_max_rel": max((r["write_rel"] for r in rows), default=None),
            "unedited_right": sum(r["unedited_right"] for r in rows), "s_right": sum(r["s_right"] for r in rows),
            "whole_switched": sum(r["whole_switched"] for r in rows),
            "whole_switched_where_s_right": sum(r["whole_switched"] for r in rows if r["s_right"]),
            "alone_vs_batch_max": max((r["alone_vs_batch_max"] for r in rows), default=None),
            "alone_vs_batch_same_top": sum(r["alone_vs_batch_same_top"] for r in rows),
            "lens_top10_org": sum(r["lens_rank_org"] <= TOP_K for r in rows if r["reader"] == X.LOOKUP),
            "lens_top10_alt": sum(r["lens_rank_alt"] <= TOP_K for r in rows if r["reader"] == X.LOOKUP),
            "scenes": n // len(X.READERS),
            "pass": n > 0 and all(r["noop_exact"] for r in rows) and all(r["write_rel"] <= WRITE_TOL for r in rows)}  # fmt: skip


def stage_smoke(name: str) -> int:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out = RESULTS / name
    m = json.loads((out / "manifest.json").read_text())
    check_switches(m)
    report: dict[str, Any] = {"run": name, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    files = [out / f for f in m["kernel"]["files"]]
    report["kernel_nll"] = kernel_compare(*(torch.load(f, weights_only=True) for f in files))
    model = load_model()
    model.run(model.encode("The capital of France is"))  # a forward first: some hub kernels load at their first call
    report["hub_kernels"] = loaded_hub_kernels()
    report["kernel_revision"] = kernel_revision_check(report["hub_kernels"], os.environ.get(REVISION_ENV))
    lens = JLens(model, "jpp")  # asserts the local file's sha256 against the pin
    report["lens"] = {**X.lens_record(), "has_layer": LAYER in lens.source_layers, "layers": lens.source_layers}
    tok = model.tokenizer
    cand: dict[str, list[int]] = {}
    report["designs"] = {}
    all_rows = []
    for design in DESIGNS:
        cases, counts = scene_counts(tok, design)
        rows = [{"design": design, **r} for r in mechanics(model, lens, cases[:N_SMOKE], LAYER,
                                                           lambda d: cand.setdefault(d, candidate_ids(tok, d)))]  # fmt: skip
        all_rows += rows
        report["designs"][design] = {"counts": counts, "mechanics": summarize(rows)}
    X.write_jsonl(out / "rows.jsonl", all_rows)
    stops = {"kernel revision": report["kernel_revision"]["pass"], "kernel vs torch NLL": report["kernel_nll"]["pass"],
             "lens map at the layer": report["lens"]["has_layer"],
             **{f"{d}: scenes": v["counts"]["enough"] for d, v in report["designs"].items()},
             **{f"{d}: no-op and write": v["mechanics"]["pass"] for d, v in report["designs"].items()}}  # fmt: skip
    report["stop_checks"] = stops
    report["pass"] = all(stops.values())
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [f"# 45s smoke: {name} ({'PASS' if report['pass'] else 'STOP'})", "",
             *(f"- {k}: {'ok' if v else 'STOP'}" for k, v in stops.items()), "",
             f"Kernel: loaded {report['kernel_revision']['loaded']}, expected {report['kernel_revision']['expected']}; "
             f"NLL kernels {report['kernel_nll']['nll_kernels']} vs torch {report['kernel_nll']['nll_torch']} (diff "
             f"{report['kernel_nll']['diff']}), top-1 agreement {report['kernel_nll']['top1_agreement']}.", ""]  # fmt: skip
    for d, v in report["designs"].items():
        s, c = v["mechanics"], v["counts"]
        lines += [f"## {d} ({DESIGNS[d]})", "",
                  f"Scenes made {c['cases']} of {c['scenes']}; dropped {c['dropped']}; one-token answers per reader "
                  f"{c['one_token_answers']} (need {X.N_MIN}).",
                  f"First {s['scenes']} scenes x 2 readers: no-op exact {s['noop_exact']}/{s['rows']} (max |dlogit| "
                  f"{s['noop_max']}); write max rel {s['write_max_rel']:.2e} (tol {WRITE_TOL}); unedited right "
                  f"{s['unedited_right']}, S right {s['s_right']}, whole change switches {s['whole_switched']} "
                  f"({s['whole_switched_where_s_right']} where S reads its answer); alone vs batch: max |dlogit| "
                  f"{s['alone_vs_batch_max']}, same top {s['alone_vs_batch_same_top']}/{s['rows']}; lens top {TOP_K} "
                  f"among the domain's items: org bridge {s['lens_top10_org']}/{s['scenes']}, alt "
                  f"{s['lens_top10_alt']}/{s['scenes']}.", ""]  # fmt: skip
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return 0 if report["pass"] else 1


def stage_smoke_gates(runs: list[str]) -> int:
    ok = True
    for run in runs:
        st = gate_status(json.loads((X.RESULTS / run / "gate.json").read_text()))
        n_rows = len(X.read_jsonl(X.RESULTS / run / "outcomes.jsonl"))
        print(f"{run}: gate {st['label']} {st['accuracy']}, eligible {st['eligible']} (enough: {st['enough']}); "
              f"{n_rows} outcome rows", flush=True)  # fmt: skip
        ok &= st["ok"] and n_rows > 0
    print("PASS" if ok else "STOP: a design is not testable at gate 0.80 (0.75 is descriptive only)", flush=True)
    return 0 if ok else 1


# ---- the sealed verdict (CPU) -------------------------------------------------------------------------------------


def jpp_rows(run: str) -> list[dict]:
    """The run's chat rows at LAYER: none, whole, and J++ k = 25 signed's no_part / no_rand."""
    return [r for r in X.read_jsonl(X.RESULTS / run / "outcomes.jsonl") if r["rendering"] == "chat"
            and r["layer"] == LAYER and (r["arm"] in ("none", "whole") or (r["dict"], r["k"], r["omp"]) == X.MAIN)]  # fmt: skip


def versions(run: str, rows: list[dict], scenes: list[str], n_boot: int) -> dict:
    """Over these scenes: the gap on switches (x45m.group_cells), on the logit difference (x0_logit_diff.gap_of) and on
    p_alt (x0_prob_and_shares.prob_cells)."""
    from scripts import x0_logit_diff as LD
    from scripts import x0_prob_and_shares as PS
    from scripts import x45m as M

    if not scenes:
        return {"n": 0}
    keep = set(scenes)
    mine = [r for r in rows if r["scene"] in keep]
    entity = {r["scene"]: r["entity"] for r in mine}
    switch = M.group_cells([r for r in mine if r["arm"] != "none"], sorted(keep), entity, n_boot)
    ld_items = {w: {s: it for s, it in by.items() if s in keep} for w, by in LD.items(run, LAYER).items()}
    ld = LD.gap_of(ld_items, n_boot)
    prob = PS.prob_cells(mine, LAYER, n_boot)
    return {"n": len(keep), "switch": switch, "ld": {"lookup": ld["lookup"]["extra"], "recall": ld["recall"]["extra"],
            "gap": ld["gap"]}, "prob": {k: prob[k] for k in ("prob_lookup", "prob_recall", "prob_gap")}}  # fmt: skip


def run_header(run: str, alt: str) -> tuple[dict, dict]:
    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == TARGET, f"{run}: target {m['model']['target']}, not {TARGET}"
    assert m["predicted"] == LAYER, f"{run}: layer {m['predicted']}, not the fixed L{LAYER}"
    assert m.get("alt") == alt, f"{run}: alt {m.get('alt')!r}, not {alt!r}"
    return m, json.loads((src / "gate.json").read_text())


def main_result(run: str, n_boot: int) -> dict:
    """45s-a: X0's rule at LAYER on the two-people-swap run, with the gap and its versions, all scenes and split by
    the original bridge's locker sentence before / after the asked pick (x0_strata)."""
    from scripts import x0_strata as ST

    _, gate = run_header(run, "cf")
    st = gate_status(gate)
    base = {"run": run, "gate": st, "hub_kernels": gate.get("hub_kernels")}
    if not st["ok"]:
        return {**base, "status": "not tested", "verdict": "can't test (gate or n)"}
    rows = jpp_rows(run)
    cells = X.cells_of([r for r in rows if r["arm"] != "none"], n_boot)
    v = X.verdict_of(cells, LAYER, ("chat",))["chat"]
    if "lookup_label" not in v:
        return {**base, "status": "pending", "verdict": v["verdict"]}
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    scenes = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    order = {s: ST.features(cases[s])["org locker vs asked pick"] for s in scenes}
    return {**base, "status": "tested", "verdict": v["verdict"], "labels": [v["lookup_label"], v["recall_label"]],
            "cells": {X.LOOKUP: cells[("chat", LAYER, X.LOOKUP, *X.MAIN)], X.RECALL: cells[("chat", LAYER, X.RECALL, *X.MAIN)]},
            "groups": {g: versions(run, rows, [s for s in scenes if g == "all" or order[s] == g.split("-")[1]], n_boot)
                       for g in ("all", "locker-before", "locker-after")}}  # fmt: skip


def clean_result(run: str, n_boot: int) -> dict:
    """45s-b: 45m's per-model check (x45m.model_result) on the clean run, with the versions per group."""
    from scripts import x45m as M

    run_header(run, "fresh")
    res = M.model_result(run, n_boot)
    if res["status"] != "tested":
        return res
    rows = jpp_rows(run)
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    scenes = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    group = {s: M.group_of(cases[s]) for s in scenes}
    gate = json.loads((X.RESULTS / run / "gate.json").read_text())
    return {**res, "hub_kernels": gate.get("hub_kernels"),
            "groups": {g: versions(run, rows, [s for s in scenes if g == "all" or group[s] == g], n_boot)
                       for g in M.GROUPS}}  # fmt: skip


def view(run: str, tok, n: int = N_VIEW, seed: int = VIEW_SEED) -> list[str]:
    """The verify-pack view: n random scenes of the run (seed, over its scenes sorted), the org prompt as the model
    reads it with the bridge position marked, S's changed tokens, and each arm's top token per reader."""
    from scripts import suite_v1 as S

    rows = jpp_rows(run)
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    top = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    scenes = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    lines = [f"# 45s view: {run}", "", f"{min(n, len(scenes))} random scenes (random.Random({seed}) over the "
             f"{len(scenes)} scenes read, sorted); ⟦ ⟧ marks the patched position (the asked bridge word) at L{LAYER}.", ""]  # fmt: skip
    for s in sorted(random.Random(seed).sample(scenes, min(n, len(scenes)))):
        c = cases[s]
        lines += [f"## {s} ({c['domain']}): {c['bridge']} → {c['cf_bridge']}", ""]
        for w, rd in c["readers"].items():
            org, alt = rd["ids"]["org"], rd["ids"]["alt"]
            text = "".join(f"⟦{tok.decode([t])}⟧" if i == c["pos"] else tok.decode([t]) for i, t in enumerate(org))
            changed = S.changed(org, alt) or []
            arms = "; ".join(f"{a}: {tok.decode([top[(s, w, a)]['top']])!r} ({top[(s, w, a)]['role']})"
                             for a in ("none", "whole", "no_part", "no_rand") if (s, w, a) in top)  # fmt: skip
            lines += [f"**{'lookup' if w == X.LOOKUP else 'recall'}** ({rd['id']}): O's answer {rd['answer']}, S's "
                      f"{rd['cf_answer']}; S differs at positions {changed} "
                      f"({', '.join(f'{tok.decode([org[i]])!r}→{tok.decode([alt[i]])!r}' for i in changed)})", "",
                      "```", text, "```", "", f"Arms (top token, role b = S's answer, A = O's): {arms}", ""]  # fmt: skip
    return lines


def fmt(v: list | None) -> str:
    return "-" if v is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def stage_verdict(main: str, clean: str, smoke: str, n_boot: int) -> Path:
    from scripts import statement_positions as SP

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    answers = dan_answers()
    missing = [QUESTIONS[d] for d, a in answers.items() if not a]
    assert not missing, f"sealed: {PREDICTIONS} has no committed answer to {', '.join(missing)} at HEAD"
    smoke_report = json.loads((RESULTS / smoke / "report.json").read_text())
    verified = smoke_report["kernel_revision"]["loaded"]
    res = {"main": main_result(main, n_boot), "clean": clean_result(clean, n_boot)}
    for r in res.values():  # each run's own loaded mamba-ssm against the one the smoke checked
        r["kernel_as_smoke"] = (r.get("hub_kernels") or {}).get(KERNEL_REPO) == verified
    out = RESULTS / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    a, b = res["main"], res["clean"]
    lines = [f"# 45s: Lightning at L{LAYER} (UNVERIFIED)", "",
             f"Dan: {QUESTIONS['main']} {answers['main']}; {QUESTIONS['clean']} {answers['clean']}. Smoke {smoke} "
             f"(mamba-ssm {verified}); runs {main}, {clean}. Cluster bootstrap over bridge items ({n_boot}, seed "
             f"{X.BOOT_SEED}).", "",
             f"## 45s-a, the main test (two people swap): {a['verdict'].upper()}", ""]  # fmt: skip
    if a["status"] == "tested":
        lk, rc = a["cells"][X.LOOKUP], a["cells"][X.RECALL]
        lines += [f"X0's rule (jobs/c3/X0.md): lookup excess {fmt(lk['excess'])} (bar <= 0.10 confirms, >= 0.20 kills), "
                  f"recall Jdep {fmt(rc['Jdep'])} (bar >= 0.30 confirms, < 0.20 kills); labels lookup {a['labels'][0]}, "
                  f"recall {a['labels'][1]}; valid cells lookup {lk['valid']} ({lk['S_whole'][0]:.2f}, "
                  f"{lk['switched_whole']}), recall {rc['valid']} ({rc['S_whole'][0]:.2f}, {rc['switched_whole']}).", ""]  # fmt: skip
    lines += [f"Gate {a['gate']['label']} {a['gate']['accuracy']}, eligible {a['gate']['eligible']}; kernel as the "
              f"smoke's: {a['kernel_as_smoke']}.", "",
              f"## 45s-b, the clean one-pick design: {('HOLDS' if b.get('holds') else 'DOES NOT HOLD') if b['status'] == 'tested' else b['status'].upper()}",
              "", f"45m's per-model check (locker-before: gap >= 0.3 and lookup's extra loss <= 0.10): {b.get('why')}.", ""]  # fmt: skip
    lines += ["## Beside the rules (descriptive)", "",
              "| design | scenes | n | lookup extra loss | recall extra loss | gap | gap, logit diff | gap, probability |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for d, r in res.items():
        for g, c in r.get("groups", {}).items():
            if not c or not c.get("n"):
                lines.append(f"| {d} | {g} | 0 | - | - | - | - | - |")
                continue
            sw = c["switch"]
            lines.append(f"| {d} | {g} | {c['n']} | {fmt(sw['lookup']['excess'])} | {fmt(sw['recall']['excess'])} | "
                         f"{fmt(sw['gap'])} | {fmt(c['ld']['gap'])} | {fmt(c['prob']['prob_gap'])} |")  # fmt: skip
    (out / "x45s.json").write_text(json.dumps({"answers": answers, "smoke": smoke, "results": res}, indent=1,
                                              default=str) + "\n")  # fmt: skip
    (out / "x45s.md").write_text("\n".join(lines) + "\n")
    tok = SP.load_tokenizer()
    for d, run in (("main", main), ("clean", clean)):
        (out / f"view_{d}.md").write_text("\n".join(view(run, tok)) + "\n")
    print("\n".join(lines), flush=True)
    print(out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["fetch", "smoke-manifest", "smoke", "smoke-gates", "verdict"])
    ap.add_argument("--name", help="smoke-manifest / smoke: the smoke run (results/x45s/<name>/)")
    ap.add_argument("--why", default="")
    ap.add_argument("--runs", nargs="+", help="smoke-gates: the two 8-scene x0_necessity smoke runs")
    ap.add_argument("--main", help="verdict: the 45s-a run (x0_necessity, --alt cf)")
    ap.add_argument("--clean", help="verdict: the 45s-b run (x0_necessity, --alt fresh)")
    ap.add_argument("--smoke", help="verdict: the smoke run whose report names the checked kernel")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "fetch":
        stage_fetch()
    elif a.stage == "smoke-manifest":
        stage_smoke_manifest(a.name, a.why)
    elif a.stage == "smoke":
        sys.exit(stage_smoke(a.name))
    elif a.stage == "smoke-gates":
        sys.exit(stage_smoke_gates(a.runs))
    else:
        stage_verdict(a.main, a.clean, a.smoke, a.n_boot)


if __name__ == "__main__":
    main()
