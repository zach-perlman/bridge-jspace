"""x51_dose (batch 51, test 51.1; jobs/c3/batch51.yaml, design and rules fixed in advance; Q51.1 in
predictions/2026-10-28_dan.md): dose curves with a matched random part at every dose. Does the lookup stay blind to the
change's J++ part at every dose, and does the recall read it above its share?

Items, layer and parts are 49.1's (scripts/x49_gain.py, reused by import): the main test's locker-first scenes of each
model's X0 run at L (12 / 32 / 26), chat; at the bridge word at L, Δ = h_S - h_O, P_J Δ = X0's 25-atom signed OMP part
over the J++ lens's letter-token atoms, the rest = Δ - P_J Δ, the address U = x47_atoms.pointer_basis (never refit), R Δ
= X0's random part at P_J Δ's share of ||Δ||^2 (seed 888 + L), R_U Δ the random part at U U^T Δ's share. Each arm adds a
vector at the bridge word at L on O (X0's AddRows) and is read by both readers with X0's chat read:
  J(α,0)       α P_J Δ                          α in ALPHAS (the J++ part alone)
  R(α,0)       α R Δ                            its twin: a random part of the same share at the same gain
  J(0,β)       β (Δ - P_J Δ)                    β in BETAS (the rest alone, with the address)
  R(0,β)       β (Δ - R Δ)                      its twin: the random complement, the rest's share, same gain
  J(0,β)-U     β (Δ - P_J Δ - U U^T Δ)          the rest without the address (49.1's J(0,2)-U at gain β)
  J(0,β)-RU    β (Δ - P_J Δ - R_U Δ)            its twin: a random part of U's share removed in place of U
  J(1,1)       Δ (the whole change: the loss bar's reference and 49.1's J(1,1) to reproduce); J(0,0) O unedited
Plain-text loss at the bridge word under every arm (49.1's: -log p(O's next token), O's lookup prompt cut after the
bridge word). The loss bar: an arm is under it when its mean loss <= LOSS_BAR x J(1,1)'s mean loss.

Rules (fixed in advance; point estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs over the bridge items,
10,000, seed 0, beside):
  (i)   "the lookup is blind to the J++ part": the lookup's J(α,0) - R(α,0) <= 0.10 at every α whose J(α,0) loss is under
        the bar (no α under the bar: undecided) -- per model, and on all three
  (ii)  "the recall reads the J++ part above its share": at the first α where the recall's J(α,0) >= 0.3, J(α,0) -
        R(α,0) >= 0.2 (no α reaches 0.3: no) -- per model
  (iii) "together only" (Muse): 49.1's stored (1,1) >= 0.8 while the best single-part dose under the loss bar (J(α,0)
        and J(0,β)) stays <= 0.3; decisive on the recall, the lookup and the other models beside
Fit (descriptive, per model and reader): logit(switch) = a0 + a α + b β (+ c α β) on every J(α,β) cell with the address
(this run's, and 49.1's 5x5 grid cells on the same items that this run does not repeat), by Newton-IRLS with a small
ridge (RIDGE) on a, b, c; b/a from the additive fit; c is needed when its cluster-bootstrap 95% CI excludes 0 (the same
10,000 draws, seed 0); the naive likelihood-ratio statistic (reads as independent) beside.

SEALED: the run stage writes per-item files only; verdict and view refuse until predictions/2026-10-28_dan.md holds
Dan's Q51.1 answer at HEAD.

uv run python scripts/x51_dose.py plan                                                   # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_dose.py run --name qwen35_9b_x51_1        # GPU (sealed)
uv run python scripts/x51_dose.py verdict                                                 # CPU, after Dan's Q51.1
uv run python scripts/x51_dose.py view                                                    # CPU, after Dan's Q51.1
"""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x48_heads as H
from scripts import x49_gain as G

EXP = "x51_dose"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.1"
MODELS = G.MODELS
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_1", "qwen3.6-27b": "x51_1_27b", "muse-glimmer-30b": "muse30_x51_1"}
X49_RUNS = G.RUNS  # 49.1's runs of record: the (1,1) value of rule (iii), the J(1,1) check, the fit's grid cells
# batch 52 C coverage (amendment 3, extra b): Lightning, where 49.1 never ran (no J(1,1) beside; rule (iii) is Muse's);
# verdict --coverage reads it alone, 51.1's RUNS and own verdict unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_dose",
                 "qwen3.5-122b-a10b": "qwen35_122b_x51_1"}  # Dan 18:20 (batch53.yaml coverage_122b_1820) # fmt: skip
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_dose/x51_1-20261028T170335Z"  # 51.1's rules first scored
ALPHAS = (0.5, 1.0, 1.5, 2.0, 3.0)
BETAS = (0.25, 0.5, 0.75, 1.0, 1.5)
LOSS_BAR = 2.0  # x the whole change's mean plain-text loss
BLIND_MAX = 0.10  # (i)
READS_AT, ABOVE_MIN = 0.3, 0.2  # (ii)
TOGETHER_MIN, SINGLE_MAX = 0.8, 0.3  # (iii)
TOGETHER_MODEL, TOGETHER_READER = "muse-glimmer-30b", "recall"
RIDGE = 1.0  # L2 penalty on a, b, c (not a0): keeps the fit finite when a reader never switches along an axis
EPS = G.EPS
N_PROMPTS = 5  # rendered prompts per model in the plan and the view
N_ROWS = 10  # random rows per arm in the view
gname, NONE, WHOLE, READER_NAME = G.gname, G.NONE, G.WHOLE, G.READER_NAME
RULE = {
    "i": '"the lookup is blind to the J++ part": switch minus random <= 0.10 at every α whose plain-text loss stays '
         "under 2x the whole change's -- on all three",
    "ii": '"the recall reads the J++ part above its share": at the first α where the J++ part alone switches >= 0.3, '
          "J minus random >= 0.2 -- per model",
    "iii": '"together only" (Muse): (1,1) from 49.1 >= 0.8 while the best single-part dose under the loss bar stays '
           "<= 0.3",
}  # fmt: skip


def nou(b: float) -> str:
    return f"J(0,{b:g})-U"


def nou_rand(b: float) -> str:
    return f"J(0,{b:g})-RU"


def arm_names() -> list[str]:
    """Every arm in read order: O unedited, the whole change, the J++ part's doses with their twins, the rest's doses
    with their twins, the rest without the address with its twins."""
    return ([NONE, WHOLE] + [x for a in ALPHAS for x in (gname("J", a, 0), gname("R", a, 0))]
            + [x for b in BETAS for x in (gname("J", 0, b), gname("R", 0, b))]
            + [x for b in BETAS for x in (nou(b), nou_rand(b))])  # fmt: skip


ARM_TEXT = {
    "J(α,0)": "α P_J Δ, the change's 25-atom signed OMP J++ part alone at gain α",
    "R(α,0)": "α R Δ, R Δ a random subspace's part of Δ at P_J Δ's share of ||Δ||^2 (seed 888 + L)",
    "J(0,β)": "β (Δ - P_J Δ), the rest alone at gain β (with the address)",
    "R(0,β)": "β (Δ - R Δ), the random complement at the rest's share",
    "J(0,β)-U": "β (Δ - P_J Δ - U U^T Δ), the rest without the address (49.1's J(0,2)-U at gain β)",
    "J(0,β)-RU": "β (Δ - P_J Δ - R_U Δ), R_U Δ a random part at U U^T Δ's share (same random basis)",
    WHOLE: "Δ, the whole change (X0's whole arm; 49.1's J(1,1))",
    NONE: "O unedited",
}


# ---- the arms (CPU-testable) ---------------------------------------------------------------------------------------


def arm_deltas(delta, pj, rj, up, ru) -> dict[str, Any]:
    """Each arm's added vector per item [n, d], in arm_names order; the J and R arms as 49.1 writes them (α part +
    β (Δ - part)), so J(1,1) and the doses 49.1 shares are the same floats."""
    out = {}
    for name in arm_names():
        if name.endswith("-RU"):
            out[name] = float(name[4:-4]) * (delta - pj - ru)
        elif name.endswith("-U"):
            out[name] = float(name[4:-3]) * (delta - pj - up)
        else:
            a, b = (float(x) for x in name[2:-1].split(","))
            part = pj if name[0] == "J" else rj
            out[name] = a * part + b * (delta - part)
    return out


def dose_cells(names: list[str]) -> list[tuple[float, float, str]]:
    """The (α, β, arm) of every J(α,β) arm with the address among names (the fit's cells)."""
    out = []
    for n in names:
        if n.startswith("J(") and n.endswith(")"):
            a, b = (float(x) for x in n[2:-1].split(","))
            out.append((a, b, n))
    return out


# ---- items (tokenizer only) ----------------------------------------------------------------------------------------


def stage_plan(k_prompts: int = N_PROMPTS) -> Path:
    """Tokenizer only: 49.1's items (the source run's gate, the drops), whether they are 49.1's run's items in its
    order, the arms and reads, U's rank, and k rendered prompts (seed 0) with the loss's target token."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    gate = G.source_gate(G.SOURCES[target])
    items, counts = G.select_items(tok, target)
    names = arm_names()
    try:
        u_rank: int | str = G.pointer_basis(target)[1]["rank"]
    except (OSError, KeyError) as e:  # the probe run's states are not on this machine
        u_rank = f"not available here: {e}"
    x49 = G.RESULTS / X49_RUNS[target] / "cases.jsonl"
    same = [c["scene"] for c in X.read_jsonl(x49)] == [it["scene"] for it in items] if x49.exists() else None
    chosen = [items[i] for i in G.example_indices(len(items), k_prompts)]
    blob = {
        "target": target, "layer": X.PREDICTED[target], "prefix": pins.RUN_PREFIX, "run": RUNS.get(target),
        "source": G.SOURCES[target], "source_gate": gate, "gate_passes": G.gate_passes(gate), "counts": counts,
        "x49_run": X49_RUNS[target], "same_items_as_x49": same, "alphas": list(ALPHAS), "betas": list(BETAS),
        "arms": names, "n_arms": len(names), "reads": len(items) * len(X.READERS) * len(names),
        "loss_rows": len(items) * len(names), "U_rank": u_rank,
        "prompts": [{"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}",
                     "loss_target": decode([it["readers"][X.LOOKUP]["ids"]["org"][it["pos"] + 1]]),
                     **{f"{READER_NAME[w]}_O_as_read": G.as_read(decode, it, w) for w in X.READERS},
                     "lookup_S_as_read": G.as_read(decode, it, X.LOOKUP, "alt")} for it in chosen],
    }  # fmt: skip
    print(json.dumps({k: v for k, v in blob.items() if k != "prompts"}, indent=1, ensure_ascii=False))
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan on {target} (tokenizer only): {len(chosen)} rendered prompts, ⟦…⟧ the bridge word (where "
             "each arm adds its vector at L)", ""]  # fmt: skip
    for p in blob["prompts"]:
        lines += [f"## {p['scene']} ({p['bridge']}; loss target {p['loss_target']!r})", ""]
        for k, v in p.items():
            if k.endswith("as_read"):
                lines += [f"{k}:", "", "```", v, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- GPU -----------------------------------------------------------------------------------------------------------


def run_items(model, lens, items: list[dict], layer: int, digits, u) -> tuple[list, list, list, list]:
    """49.1's loop (x49_gain.run_items) on this test's arms: every arm on each item's O, both readers (outcome rows),
    per item the parts' shares (norms), the plain-text loss at the bridge word under every arm, and the example items'
    greedy texts."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    names = arm_names()
    with torch.no_grad():
        rows_d = []
        for it in progress(items, f"51.1: Δ at the bridge word, L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            # .clone(): the recorded state is a view of the whole [seq, d] tensor (memory lesson 2)
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][it["pos"]].float().clone()
                 for v in ("org", "alt")}  # fmt: skip
            rows_d.append(h["alt"] - h["org"])
        delta = torch.stack(rows_d)
        basis = SP.random_basis(delta.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        jdic = lens.vectors(layer, model.letter_token_ids())
        pj, rj = G.lens_parts(jdic, delta, G.K, basis)
        del jdic
        uu = torch.as_tensor(u, dtype=torch.float32, device=dev)
        assert uu.shape[0] == delta.shape[1], (
            f"U is [{uu.shape[0]}, {uu.shape[1]}], the states are d = {delta.shape[1]}"
        )
        up, ru = G.pointer_parts(delta, uu, basis)
        del basis
        arms = arm_deltas(delta, pj, rj, up, ru)
        assert torch.allclose(arms[WHOLE], delta, atol=1e-4 * float(delta.abs().max())), "J(1,1) is not Δ"
        assert not arms[NONE].any(), "J(0,0) is not O unedited"
        norms = [{"scene": it["scene"], "entity": it["entity"], **r}
                 for it, r in zip(items, G.norm_records(delta, pj, rj, up, ru, uu), strict=True)]  # fmt: skip
        examples = set(G.example_indices(len(items)))
        rows, losses, greedy = [], [], []
        for i, it in enumerate(progress(items, f"51.1: {len(names)} arms x 2 readers + the loss (item)")):
            pos = it["pos"]
            edits = [{layer: AddRows(arms[a][i : i + 1], [pos])} for a in names]
            base = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"]}
            for w, rd in it["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, G.RENDERING, it["space"], None)
                rows += [{**base, "reader": w, "arm": a, **X.read_row(lg, rd, digits)}
                         for a, lg in zip(names, logits, strict=True)]  # fmt: skip
                if i in examples:
                    greedy += [{"scene": it["scene"], "reader": w, "arm": a, "greedy": t}
                               for a, t in zip(names, G.greedy_texts(model, rd["ids"]["org"], edits), strict=True)]  # fmt: skip
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            nxt = ids[pos + 1]
            logits, _ = X.read_logits(model, ids[: pos + 1], edits, G.RENDERING, [], None)
            lp = torch.log_softmax(logits.float(), dim=-1)
            losses += [{**base, "arm": a, "next": nxt, "loss": round(float(-row[nxt]), 5),
                        "top_is_next": int(int(row.argmax()) == nxt)} for a, row in zip(names, lp, strict=True)]  # fmt: skip
    return rows, norms, losses, greedy


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state
    from scripts import suite_split as SUITE

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.1 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in G.SOURCES, f"51.1 runs on {sorted(G.SOURCES)}, not {target}"
    layer, source = X.PREDICTED[target], G.SOURCES[target]
    src = X.RESULTS / source
    x49 = G.RESULTS / X49_RUNS[target] if target in X49_RUNS else src / "no-49.1-run"  # Lightning: none (missing files)
    u, u_info = G.pointer_basis(target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    names = arm_names()
    inputs = [SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl"))]
    inputs += [
        x49 / f for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "losses.jsonl") if (x49 / f).exists()
    ]
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "51.1",
         "spec": "jobs/c3/batch51.yaml (51.1)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs},
         "source": source, "x49_run": X49_RUNS.get(target), "layer": layer, "rendering": G.RENDERING, "group": G.GROUP,
         "k": G.K, "alphas": list(ALPHAS), "betas": list(BETAS), "arms": names, "arm_text": ARM_TEXT,
         "pointer": u_info,
         "items_rule": "49.1's: the source X0 run's scenes at L (chat outcomes: the items its unedited run made "
                       "eligible), rebuilt by x47_cumulative.select (ids and bridge position checked against the run's), "
                       "x45m.group_of locker-first only",
         "parts": {"P_J": f"x0_necessity.fit(J++ letter-token atoms at L, Δ, {G.K}, signed)",
                   "R": f"statement_positions.random_subspace_part(Δ, P_J Δ's share of ||Δ||^2, random basis seed "
                        f"{X.SUBSPACE_SEED} + L)", "U": "U U^T Δ", "R_U": "random_subspace_part at U U^T Δ's share, same basis"},
         "edit": "AddRows: the arm's vector added at the bridge word's block output at L, on O",
         "read": "X0's chat read: O's prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token",
         "loss": "-log p(O's token after the bridge word) at the bridge word, from O's lookup prompt cut after the "
                 f"bridge word, under each arm; the bar: mean loss <= {LOSS_BAR:g} x J(1,1)'s",
         "gate": f"the source run's (X0: {X.GATE} per reader on O unedited, >= {X.N_MIN} eligible); asserted",
         "rule": RULE, "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                                 "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "order": {"items": "the source run's scene order (locker-first only)",
                   "reads": f"per item and reader: O's prompt under the {len(names)} arms in arm order, batches of at "
                            f"most {SUITE.BATCH} rows (BJ_SUITE_BATCH); then the loss: O's lookup prompt cut after the "
                            "bridge word under the same arms", "batch": SUITE.BATCH},
         "sealed": f"no verdict in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {
            "question": NO_PREDICTION,
            "batch": 52,
            "rules_first_scored": SCORED,
            "sealed": "none (batch 52 coverage)",
        }
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    gate = G.source_gate(source)
    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    items, counts = G.select_items(model.tokenizer, target)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    tested = G.gate_passes(gate) and bool(items)
    (out / "gate.json").write_text(json.dumps({"source": source, "gate": gate, "tested": tested,
                                              "order": [it["scene"] for it in items],
                                              "hub_kernels": loaded_hub_kernels()}, indent=2) + "\n")  # fmt: skip
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    if not tested:
        print(
            "the gate fixed in advance did not pass (or no locker-first items): not tested; see gate.json", flush=True
        )
        return out
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
    rows, norms, losses, greedy = run_items(model, lens, items, layer, digits, u)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "losses.jsonl", losses)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- the seal ------------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.1 at `rev` (x48_heads.parse_answer: 'Dan:' / 'Dan (27B):' lines and bullet
    continuations), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return H.parse_answer(text, QUESTION)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


# ---- the rules (CPU, on point estimates) ---------------------------------------------------------------------------


def rule_blind(lk: dict[str, float], under: dict[str, bool]) -> dict:
    """(i) on the lookup: J(α,0) - R(α,0) <= BLIND_MAX at every α whose J(α,0) is under the loss bar."""
    diff = {a: lk[gname("J", a, 0)] - lk[gname("R", a, 0)] for a in ALPHAS}
    tested = [a for a in ALPHAS if under[gname("J", a, 0)]]
    if not tested:
        return {"label": "undecided", "why": "no α under the loss bar", "alphas_under_bar": [], "diff": diff}
    bad = [a for a in tested if diff[a] > BLIND_MAX + EPS]
    return {"label": "no" if bad else "yes", "alphas_under_bar": tested, "alphas_failing": bad, "diff": diff}


def rule_above(x: dict[str, float], under: dict[str, bool]) -> dict:
    """(ii) on one reader: at the first α (ascending) where J(α,0) >= READS_AT, J(α,0) - R(α,0) >= ABOVE_MIN; no such α:
    no. Whether that α is under the loss bar is reported beside (the rule does not condition on it)."""
    diff = {a: x[gname("J", a, 0)] - x[gname("R", a, 0)] for a in ALPHAS}
    first = next((a for a in ALPHAS if x[gname("J", a, 0)] >= READS_AT - EPS), None)
    if first is None:
        return {"label": "no", "why": f"the J++ part alone never switches >= {READS_AT}", "first_alpha": None,
                "diff": diff}  # fmt: skip
    return {"label": "yes" if diff[first] >= ABOVE_MIN - EPS else "no", "first_alpha": first,
            "first_under_bar": under[gname("J", first, 0)], "diff": diff}  # fmt: skip


def rule_together(x: dict[str, float], under: dict[str, bool], whole49: float | None) -> dict:
    """(iii) on one reader: 49.1's (1,1) >= TOGETHER_MIN while the best single-part dose (J(α,0), J(0,β)) under the loss
    bar stays <= SINGLE_MAX. No 49.1 value or no single dose under the bar: undecided."""
    singles = {a: x[a] for a in [gname("J", al, 0) for al in ALPHAS] + [gname("J", 0, b) for b in BETAS] if under[a]}
    if whole49 is None or not singles:
        return {"label": "undecided", "why": "no 49.1 (1,1)" if whole49 is None else "no single dose under the bar",
                "whole49": whole49, "best_single": None}  # fmt: skip
    best = max(singles, key=lambda a: singles[a])
    holds = whole49 >= TOGETHER_MIN - EPS and singles[best] <= SINGLE_MAX + EPS
    return {"label": "yes" if holds else "no", "whole49": whole49, "best_single": [best, singles[best]],
            "whole49_ok": whole49 >= TOGETHER_MIN - EPS, "singles_ok": singles[best] <= SINGLE_MAX + EPS}  # fmt: skip


# ---- the fit (CPU) -------------------------------------------------------------------------------------------------


def irls(
    design: np.ndarray,
    succ: np.ndarray,
    trials: np.ndarray,
    weights: np.ndarray,
    ridge: float = RIDGE,
    iters: int = 100,
    tol: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray]:
    """Binomial logistic regression by Newton-IRLS, batched over weight vectors: design [n, p] (column 0 the intercept,
    unpenalized), succ / trials [n], weights [B, n] (a row's multiplicity in each resample). Returns the coefficients
    [B, p] and each fit's data log-likelihood [B] (without the penalty)."""
    from scipy.special import expit

    n_b, p = weights.shape[0], design.shape[1]
    pen = np.full(p, ridge)
    pen[0] = 0.0
    beta = np.zeros((n_b, p))
    for _ in range(iters):
        eta = beta @ design.T  # [B, n]
        mu = expit(eta)
        grad = (weights * (succ - trials * mu)) @ design - beta * pen
        w = weights * trials * mu * (1.0 - mu)
        hess = (w[:, None, :] * design.T[None]) @ design + np.diag(pen)[None] + 1e-10 * np.eye(p)[None]
        step = np.linalg.solve(hess, grad[..., None])[..., 0]
        beta = beta + step
        if np.abs(step).max() < tol:
            break
    eta = beta @ design.T
    ll = (weights * (succ * eta - trials * np.logaddexp(0.0, eta))).sum(1)
    return beta, ll


def fit_table(per_item: dict[tuple[float, float], list[int]], entities: list[str]) -> tuple[np.ndarray, ...]:
    """Per (bridge item, cell): α, β, successes, trials, and the bridge item's index (the fit's rows)."""
    keys = sorted(set(entities))
    idx = {e: i for i, e in enumerate(keys)}
    rows = []
    for (a, b), ys in per_item.items():
        agg: dict[int, list[int]] = {}
        for e, y in zip(entities, ys, strict=True):
            s = agg.setdefault(idx[e], [0, 0])
            s[0] += int(y)
            s[1] += 1
        rows += [(a, b, s, t, e) for e, (s, t) in agg.items()]
    arr = np.array(rows, dtype=float)
    return arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3], arr[:, 4].astype(int)


def logistic_fit(
    per_item: dict[tuple[float, float], list[int]],
    entities: list[str],
    n_boot: int = X.N_BOOT,
    seed: int = X.BOOT_SEED,
    chunk: int = 1000,
) -> dict:
    """logit(switch) = a0 + a α + b β (additive) and + c α β (interaction) on the cells' per-item outcomes, with
    cluster-bootstrap CIs (X0's draws: whole bridge items with replacement, seed 0); b/a from the additive fit; c needed
    when its 95% CI excludes 0; the naive LR statistic and p (reads as independent) beside."""
    from scipy.stats import chi2

    al, be, s, t, ent = fit_table(per_item, entities)
    n_ent = int(ent.max()) + 1
    designs = {"additive": np.stack([np.ones_like(al), al, be], 1),
               "interaction": np.stack([np.ones_like(al), al, be, al * be], 1)}  # fmt: skip
    pick = np.random.default_rng(seed).integers(0, n_ent, size=(n_boot, n_ent))
    out: dict[str, Any] = {"cells": len(per_item), "items": len(entities), "bridge_items": n_ent, "ridge": RIDGE}
    for kind, dz in designs.items():
        coef, ll = irls(dz, s, t, np.ones((1, len(s))))
        boots = []
        for c0 in range(0, n_boot, chunk):
            mult = np.stack([np.bincount(p, minlength=n_ent) for p in pick[c0 : c0 + chunk]])  # [B, n_ent]
            boots.append(irls(dz, s, t, mult[:, ent].astype(float))[0])
        bt = np.concatenate(boots) if boots else np.zeros((0, dz.shape[1]))
        names = ["a0", "a", "b", "c"][: dz.shape[1]]
        out[kind] = {k: [float(coef[0, j]), *(X.interval(bt[:, j]) if len(bt) else (math.nan, math.nan))]
                     for j, k in enumerate(names)}  # fmt: skip
        out[kind]["loglik"] = float(ll[0])
        if kind == "additive":
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = bt[:, 2] / bt[:, 1]
            a, b = coef[0, 1], coef[0, 2]
            out["b_over_a"] = [float(b / a) if a != 0 else math.nan,
                               *(X.interval(ratio[np.isfinite(ratio)]) if np.isfinite(ratio).any() else (math.nan, math.nan))]  # fmt: skip
    c = out["interaction"]["c"]
    out["c_needed"] = bool(c[1] > 0 or c[2] < 0)
    lr = max(0.0, 2.0 * (out["interaction"]["loglik"] - out["additive"]["loglik"]))
    out["lr_naive"] = {"stat": lr, "p": float(chi2.sf(lr, 1))}
    return out


# ---- verdict (CPU, sealed) -----------------------------------------------------------------------------------------


def scene_values(rows: list[dict], key: str, names: list[str], reader: str | None = None) -> tuple[list, list, dict]:
    """(scenes, entities, {arm: [value per item]}) in row order; x49_gain.per_item with the scenes kept."""
    entities, vals = G.per_item(rows, key, names, reader)
    scenes = list(dict.fromkeys(r["scene"] for r in rows if reader is None or r["reader"] == reader))
    return scenes, entities, vals


def reader_numbers(rows: list[dict], reader: str, names: list[str], n_boot: int = X.N_BOOT,
                   seed: int = X.BOOT_SEED) -> dict:  # fmt: skip
    """One reader's switch rate per arm and each twin pair's difference (J - its random twin), with paired 95% CIs from
    X0's cluster bootstrap over the bridge items."""
    _, entities, sw = scene_values(rows, "switched", names, reader)
    boot = X.resampled_rates(sw, entities, n_boot, seed)
    pairs = [(gname("J", a, 0), gname("R", a, 0)) for a in ALPHAS] + [
        (gname("J", 0, b), gname("R", 0, b)) for b in BETAS
    ]
    pairs += [(nou(b), nou_rand(b)) for b in BETAS]
    return {"n": len(entities), "entities": len(set(entities)), "hits": {a: int(sum(v)) for a, v in sw.items()},
            "rate": {a: [float(np.mean(v)), *X.interval(boot[a])] for a, v in sw.items()},
            "diff": {f"{j} - {r}": [float(np.mean(sw[j]) - np.mean(sw[r])), *X.interval(boot[j] - boot[r])]
                     for j, r in pairs}}  # fmt: skip


def loss_numbers(losses: list[dict], names: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """The mean plain-text loss per arm (cluster-bootstrap CI), its ratio to J(1,1)'s (paired CI), under the bar when
    the ratio's point estimate <= LOSS_BAR, and the share of items whose top token is O's own next token."""
    _, entities, vals = scene_values(losses, "loss", names)
    _, _, top = scene_values(losses, "top_is_next", names)
    boot = X.resampled_rates(vals, entities, n_boot, seed)
    mean = {a: [float(np.mean(v)), *X.interval(boot[a])] for a, v in vals.items()}
    base = mean[WHOLE][0]
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = {a: [mean[a][0] / base if base > 0 else math.nan, *X.interval(boot[a] / boot[WHOLE])] for a in names}
    return {"n": len(entities), "mean": mean, "ratio_to_whole": ratio, "bar": LOSS_BAR * base,
            "under_bar": {a: bool(mean[a][0] <= LOSS_BAR * base + EPS) for a in names},
            "top_is_next": {a: float(np.mean(v)) for a, v in top.items()}}  # fmt: skip


def x49_numbers(x49_run: str, scenes: list[str], rows: list[dict]) -> dict | None:
    """49.1's run of record on this model: its J(1,1) rate per reader (rule iii), per reader the item-level agreement
    of the cells both runs read (the reproduction check), and its outcome rows (the fit's grid cells); None if absent
    or on other items."""
    if not x49_run:  # no 49.1 run on this model (batch 52's Lightning)
        return None
    src = G.RESULTS / x49_run
    if not (src / "outcomes.jsonl").exists():
        return None
    old = X.read_jsonl(src / "outcomes.jsonl")
    old_scenes = list(dict.fromkeys(r["scene"] for r in old))
    if old_scenes != scenes:
        return {"run": x49_run, "same_items": False}
    shared = sorted({r["arm"] for r in old} & {r["arm"] for r in rows})
    mine = {(r["scene"], r["reader"], r["arm"]): r["switched"] for r in rows}
    out: dict[str, Any] = {"run": x49_run, "same_items": True, "rows": old, "shared_arms": shared}
    for w in X.READERS:
        o = [r for r in old if r["reader"] == w]
        whole = [r["switched"] for r in o if r["arm"] == WHOLE]
        agree = [int(mine[(r["scene"], w, r["arm"])] == r["switched"]) for r in o if r["arm"] in shared]
        out[READER_NAME[w]] = {"whole": float(np.mean(whole)), "whole_n": len(whole),
                               "shared_cells_agree": [int(sum(agree)), len(agree)],
                               "whole_agree": [sum(int(mine[(r["scene"], w, WHOLE)] == r["switched"]) for r in o
                                                   if r["arm"] == WHOLE), len(whole)]}  # fmt: skip
    return out


def fit_cells(rows: list[dict], reader: str, names: list[str], x49: dict | None) -> tuple[dict, list[str], str]:
    """The fit's per-item outcomes by (α, β): this run's J cells, plus 49.1's grid cells it does not repeat (same
    items) when 49.1's run is here."""
    _, entities, sw = scene_values(rows, "switched", names, reader)
    cells = {(a, b): sw[n] for a, b, n in dose_cells(names)}
    source = "this run's J cells"
    if x49 and x49.get("same_items"):
        extra = [(a, b, n) for a, b, n in dose_cells(G.arm_names(False)) if (a, b) not in cells]
        if extra:
            _, ent49, sw49 = scene_values(x49["rows"], "switched", [n for *_, n in extra], reader)
            assert ent49 == entities, "49.1's bridge items differ from this run's"
            cells |= {(a, b): sw49[n] for a, b, n in extra}
            source = f"this run's J cells + {len(extra)} of 49.1's grid cells ({x49['run']})"
    return cells, entities, source


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), not tested (the gate, or no items), or its numbers, rules, fit and
    checks."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    rows = X.read_jsonl(src / "outcomes.jsonl") if (src / "outcomes.jsonl").exists() else []
    if not gate.get("tested") or not rows:
        return {"target": target, "run": run, "status": "not tested", "gate": gate.get("gate"),
                "why": "the gate fixed in advance failed, no locker-first items, or the run did not finish"}  # fmt: skip
    names = arm_names()
    readers = {READER_NAME[w]: reader_numbers(rows, w, names, n_boot) for w in X.READERS}
    pts = {w: {a: v[0] for a, v in readers[w]["rate"].items()} for w in readers}
    loss = loss_numbers(X.read_jsonl(src / "losses.jsonl"), names, n_boot)
    scenes = list(dict.fromkeys(r["scene"] for r in rows))
    x49 = x49_numbers(m.get("x49_run", X49_RUNS.get(target)), scenes, rows)
    whole49 = {w: (x49 or {}).get(w, {}).get("whole") for w in readers}
    rules = {"i": rule_blind(pts["lookup"], loss["under_bar"]),
             "ii": {w: rule_above(pts[w], loss["under_bar"]) for w in readers},
             "iii": {w: rule_together(pts[w], loss["under_bar"], whole49[w]) for w in readers}}  # fmt: skip
    fits = {}
    for w in X.READERS:
        cells, entities, source = fit_cells(rows, w, names, x49)
        fits[READER_NAME[w]] = {**logistic_fit(cells, entities, n_boot), "source": source}
    norms = X.read_jsonl(src / "norms.jsonl")
    keys = [k for k in norms[0] if k not in ("scene", "entity")]
    return {"target": target, "run": run, "status": "tested", "layer": m["layer"], "n": readers["recall"]["n"],
            "arms": names, "readers": readers, "loss": loss, "rules": rules, "fit": fits,
            "x49": {k: v for k, v in (x49 or {}).items() if k != "rows"} or None,
            "checks": G.side_checks(rows, X.read_jsonl(src / "cases.jsonl")), "gate": gate.get("gate"),
            "pointer": m["pointer"], "shares_median": {k: float(np.median([n[k] for n in norms])) for k in keys}}  # fmt: skip


def summary(models: list[dict]) -> dict:
    """Q51.1's three parts: (i) per model and on all three; (ii) per model (the recall); (iii) Muse's recall."""
    tested = {m["target"]: m for m in models if m["status"] == "tested"}
    targets = [m["target"] for m in models]  # MODELS in 51.1's verdict; the coverage models in batch 52's
    i = {t: (tested[t]["rules"]["i"]["label"] if t in tested else m_status(models, t)) for t in targets}
    ii = {t: (tested[t]["rules"]["ii"]["recall"]["label"] if t in tested else m_status(models, t)) for t in targets}
    mu = tested.get(TOGETHER_MODEL)
    iii = (mu["rules"]["iii"][TOGETHER_READER]["label"] if mu else m_status(models, TOGETHER_MODEL)
           if TOGETHER_MODEL in targets else "not this run's model (rule (iii) is Muse's)")  # fmt: skip
    all3 = "yes" if all(v == "yes" for v in i.values()) else "no" if any(v == "no" for v in i.values()) else "undecided"
    return {"i": i, "i_all_three": all3, "ii": ii, "iii_muse": iii}


def m_status(models: list[dict], target: str) -> str:
    return next(m["status"] for m in models if m["target"] == target)


def fmt(v) -> str:
    return "-" if v is None or v[0] is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(models: list[dict], path: Path) -> None:
    """Per model: the J++ part's dose (α) and the rest's dose (β); per reader a solid curve (J), its random twin dashed,
    the rest without the address dash-dotted; doses whose J arm's loss is above the bar shaded."""
    from scripts import story_style as S

    plt = S.setup()
    tested = [m for m in models if m["status"] == "tested"]
    nrow = max(1, len(tested))
    fig, axes = plt.subplots(nrow, 2, figsize=(S.WIDTH, 2.9 * nrow + 0.9), squeeze=False, sharey=True)
    for r, m in enumerate(tested):
        for c, (doses, jn, rn, un, label) in enumerate((
            (ALPHAS, lambda a: gname("J", a, 0), lambda a: gname("R", a, 0), None, "α (the J++ part alone)"),
            (BETAS, lambda b: gname("J", 0, b), lambda b: gname("R", 0, b), nou, "β (the rest alone)"),
        )):  # fmt: skip
            ax = axes[r, c]
            half = (doses[1] - doses[0]) / 2
            for d in doses:
                if not m["loss"]["under_bar"][jn(d)]:
                    ax.axvspan(d - half, d + half, color=S.COL["band"], zorder=0, lw=0)
            for w in ("lookup", "recall"):
                rate = m["readers"][w]["rate"]
                y = np.array([rate[jn(d)] for d in doses])
                yerr = np.clip([y[:, 0] - y[:, 1], y[:, 2] - y[:, 0]], 0, None)
                ax.errorbar(doses, y[:, 0], yerr=yerr, color=S.COL[w], marker="o",
                            ms=4, lw=1.8, capsize=2, label=f"{w}: J++ part" if c == 0 else f"{w}: the rest")  # fmt: skip
                ax.plot(doses, [rate[rn(d)][0] for d in doses], color=S.COL[w], ls="--", lw=1.2, alpha=0.7,
                        label=f"{w}: random, same share")  # fmt: skip
                if un is not None:
                    ax.plot(doses, [rate[un(d)][0] for d in doses], color=S.COL[w], ls="-.", lw=1.2,
                            label=f"{w}: the rest without U")  # fmt: skip
            ax.axhline(READS_AT, color=S.COL["muted"], lw=0.6, ls=":")
            ax.set_ylim(-0.03, 1.03)
            ax.set_xticks(doses)
            ax.set_xlabel(label)
            name = next((n for t, _, n in S.MODELS if t == m["target"]), m["target"])
            ax.set_title(f"{name} (L{m['layer']}, n = {m['n']})", fontsize=S.FONT)
            if c == 0:
                ax.set_ylabel("switch rate")
            if r == 0:
                ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle("Dose curves: each part alone, against a random part of its share", x=0.01, ha="left", fontsize=13,
                 weight="bold")  # fmt: skip
    fig.text(0.01, 0.005, f"shaded: the J arm's plain-text loss above {LOSS_BAR:g}x the whole change's; dotted line: "
             f"{READS_AT}; whiskers: 95% cluster-bootstrap CIs. UNVERIFIED.", fontsize=9, color=S.COL["muted"])  # fmt: skip
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    s = summary(models)
    lines = ["# 51.1: dose curves with a matched random part at every dose", "",
             f"Batch 51, test 51.1 (jobs/c3/batch51.yaml; {QUESTION}, Dan: {answer}). 49.1's items (main test, "
             "locker-first, chat) and parts; at the bridge word at L, one part of the change at a gain, against a random "
             "part of the same share at the same gain; switch = the top token is S's answer (X0's chat read). Cluster "
             f"bootstrap over the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             "Rules (fixed in advance):", "", *[f"- ({k}) {v}." for k, v in RULE.items()], "",
             f"As computed: the loss bar = the J arm's mean plain-text loss <= {LOSS_BAR:g}x J(1,1)'s mean (this run); "
             "(i) on the lookup, R(α,0) the random twin, no α under the bar = undecided; (ii) on the recall (the lookup "
             "beside), the first α ascending, not conditioned on the loss bar (reported); (iii) on Muse's recall (the "
             "lookup and the other models beside), (1,1) = 49.1's stored J(1,1) rate, single parts = J(α,0) and J(0,β) "
             "under the bar. Point estimates decide (EPS 1e-9).", "",
             f"**Q51.1 (i)** lookup blind: {', '.join(f'{t} {v}' for t, v in s['i'].items())}; on all three: "
             f"**{s['i_all_three']}**. **(ii)** recall above its share: "
             f"{', '.join(f'{t} {v}' for t, v in s['ii'].items())}. **(iii)** Muse together only: **{s['iii_muse']}**.", "",
             "| model | run | n | (i) lookup blind | (ii) recall above share (first α) | (iii) recall / lookup | "
             "fit b/a recall | lookup | c needed recall / lookup |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | | | | |")
            continue
        ru, f = m["rules"], m["fit"]
        lines.append(f"| {m['target']} | {m['run']} | {m['n']} | **{ru['i']['label']}** | **{ru['ii']['recall']['label']}** "
                     f"({ru['ii']['recall']['first_alpha']}) | {ru['iii']['recall']['label']} / {ru['iii']['lookup']['label']} | "
                     f"{fmt(f['recall']['b_over_a'])} | {fmt(f['lookup']['b_over_a'])} | "
                     f"{f['recall']['c_needed']} / {f['lookup']['c_needed']} |")  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        rc, lk, lo = m["readers"]["recall"], m["readers"]["lookup"], m["loss"]
        lines += ["", f"## {m['target']} ({m['run']}, L{m['layer']}, n = {m['n']}, {rc['entities']} bridge items)", "",
                  f"Loss bar: {lo['bar']:.3f} (= {LOSS_BAR:g} x J(1,1)'s mean {lo['mean'][WHOLE][0]:.3f}).", "",
                  "| arm | lookup | recall | mean loss | ÷ J(1,1) | under bar | top = O's next |",
                  "|---|---|---|---|---|---|---|"]  # fmt: skip
        for a in m["arms"]:
            lines.append(f"| {a} | {fmt(lk['rate'][a])} | {fmt(rc['rate'][a])} | {fmt(lo['mean'][a])} | "
                         f"{fmt(lo['ratio_to_whole'][a])} | {lo['under_bar'][a]} | {lo['top_is_next'][a]:.2f} |")  # fmt: skip
        lines += ["", "J minus its random twin (paired CIs):", "", "| pair | lookup | recall |", "|---|---|---|"]
        lines += [f"| {k} | {fmt(lk['diff'][k])} | {fmt(rc['diff'][k])} |" for k in lk["diff"]]
        ru = m["rules"]
        lines += ["", f"- (i) {json.dumps(ru['i'])}", f"- (ii) recall {json.dumps(ru['ii']['recall'])}; lookup "
                  f"{json.dumps(ru['ii']['lookup'])}",
                  f"- (iii) recall {json.dumps(ru['iii']['recall'])}; lookup {json.dumps(ru['iii']['lookup'])}"]  # fmt: skip
        for w in ("recall", "lookup"):
            f = m["fit"][w]
            lines += ["", f"Fit, {w} ({f['source']}; {f['cells']} cells, {f['items']} items, {f['bridge_items']} bridge "
                      f"items, ridge {f['ridge']:g}): additive "
                      + ", ".join(f"{k} {fmt(f['additive'][k])}" for k in ("a0", "a", "b"))
                      + f", b/a {fmt(f['b_over_a'])}; interaction "
                      + ", ".join(f"{k} {fmt(f['interaction'][k])}" for k in ("a0", "a", "b", "c"))
                      + f"; c needed (95% CI excludes 0): {f['c_needed']}; naive LR {f['lr_naive']['stat']:.2f}, "
                      f"p {f['lr_naive']['p']:.3g} (reads as independent, anti-conservative)."]  # fmt: skip
        for w, ck in m["checks"].items():
            wv = ck["whole_vs_stored"]
            lines.append(f"- {w}: J(0,0) reads O's answer on {ck['none_reads_O']} of {ck['n']}; J(1,1) vs the source "
                         f"run's whole arm: {wv['agree']} of {wv['n']} agree (rerun {wv['rerun']}, stored {wv['stored']})")  # fmt: skip
        x49 = m["x49"]
        if x49 and x49.get("same_items"):
            for w in ("lookup", "recall"):
                x = x49[w]
                lines.append(f"- {w} vs 49.1 ({x49['run']}): J(1,1) {x['whole']:.2f} there; J(1,1) agrees on "
                             f"{x['whole_agree'][0]} of {x['whole_agree'][1]} items; the {len(x49['shared_arms'])} shared "
                             f"cells agree on {x['shared_cells_agree'][0]} of {x['shared_cells_agree'][1]} reads")  # fmt: skip
        else:
            lines.append(
                f"- 49.1's run: {'absent' if not x49 else 'other items'}; (iii) undecided, the fit on this run alone"
            )
        lines.append("- shares of ||Δ||^2 (median): " + ", ".join(f"{k} {v:.4g}" for k, v in m["shares_median"].items())
                     + f"; U rank {m['pointer']['rank']} ({m['pointer']['states_run']})")  # fmt: skip
    lines += ["", "![dose curves](dose_curves.png)", "",
              "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]  # fmt: skip
    return lines


def stage_verdict(runs: dict[str, str] | None = None, n_boot: int = X.N_BOOT, coverage: bool = False) -> Path:
    """51.1's verdict (sealed until Q51.1), or with coverage (batch 52) the same rules on COVERAGE_RUNS alone, no seal
    guard, "no prediction" in place of Dan's answer, written to x52_dose-<UTC>/."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else unsealed()
    runs = runs or (COVERAGE_RUNS if coverage else RUNS)
    models = [model_result(t, runs[t], n_boot) for t in (runs if coverage else MODELS)]
    out = RESULTS / f"{'x52_dose' if coverage else 'x51_1'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ") for ln in lines]
    blob = {"dan": answer, "rule": RULE, "alphas": list(ALPHAS), "betas": list(BETAS), "loss_bar": LOSS_BAR,
            "summary": summary(models), "models": models}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    figure(models, out / "dose_curves.png")
    print("\n".join(lines))
    print(out)
    return out


# ---- view (CPU, sealed): the verify pack ---------------------------------------------------------------------------


def view_lines(target: str, run: str, decode, k_prompts: int = N_PROMPTS, k_rows: int = N_ROWS,
               seed: int = X.EXAMPLES_SEED) -> list[str]:  # fmt: skip
    """k_prompts random items (seed 0) with both readers' O as read and the lookup's S; then per arm k_rows random rows
    (seed 0) of its reads: the item, the reader, O's and S's answers, the top token, switched, the loss and the greedy
    text where the run kept one."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    by_scene = {it["scene"]: it for it in items}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    loss = {(r["scene"], r["arm"]): r["loss"] for r in X.read_jsonl(src / "losses.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [
        f"## {target}: {run} ({len(items)} items)",
        "",
        f"### {min(k_prompts, len(items))} rendered prompts (seed {seed})",
        "",
    ]
    for i in G.example_indices(len(items), k_prompts, seed):
        it = items[i]
        lines += [
            f"#### {it['scene']} ({it['domain']}): bridge {it['entity']} (O) → {it['cf_bridge']} (S), token {it['pos']}",
            "",
        ]
        for w in X.READERS:
            lines += [f"{READER_NAME[w]}, O as read:", "", "```", G.as_read(decode, it, w), "```", ""]
        lines += ["lookup, S as read:", "", "```", G.as_read(decode, it, X.LOOKUP, "alt"), "```", ""]
    for a in arm_names():
        mine = [r for r in rows if r["arm"] == a]
        pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
        lines += [f"### {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                  "| scene | reader | O's answer | S's answer | top token | switched | loss | greedy |",
                  "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for j in pick:
            r = mine[j]
            rd = by_scene[r["scene"]]["readers"][r["reader"]]
            g = greedy.get((r["scene"], r["reader"], a))
            lines.append(f"| {r['scene']} | {READER_NAME[r['reader']]} | {rd['answer']} | {rd['cf_answer']} | "
                         f"{decode([r['top']])!r} | {r['switched']} | {loss[(r['scene'], a)]:.3f} | "
                         f"{'' if g is None else repr(g)} |")  # fmt: skip
        lines.append("")
    return lines


def stage_view(runs: dict[str, str] | None = None, decode_for=None) -> Path:
    from scripts import x47_atoms as A

    unsealed()
    runs = runs or RUNS
    out = RESULTS / f"x51_1-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.1 view (verify pack): prompts exactly as the model reads them (the read appends the digit's space "
             "token); ⟦...⟧ the bridge word, where each arm adds its vector at L. UNVERIFIED.", ""]  # fmt: skip
    for t in MODELS:
        gate = RESULTS / runs[t] / "gate.json"
        if not gate.exists() or not json.loads(gate.read_text()).get("tested"):
            lines += [f"## {t}: {runs[t]} not here or not tested", ""]
            continue
        lines += view_lines(t, runs[t], (decode_for or A.default_decode)(t))
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_dose/<name>/)")
    ap.add_argument("--why", default="batch 51, test 51.1 (jobs/c3/batch51.yaml; Q51.1): dose curves; sealed")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--runs", nargs=3, default=None, metavar=("9B", "27B", "MUSE"),
                    help=f"verdict / view: runs in place of the specs' {[RUNS[t] for t in MODELS]}")  # fmt: skip
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    runs: dict[str, str] | None = {str(t): str(r) for t, r in zip(MODELS, a.runs, strict=True)} if a.runs else None
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "view":
        stage_view(runs)
    else:
        stage_verdict(runs, n_boot=a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
