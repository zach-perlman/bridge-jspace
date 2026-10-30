"""x49_gain (batch 49, test 49.1; jobs/c3/batch49.yaml, design and rules fixed in advance, with amendment 2's 49.1 item;
Q49.1 in predictions/2026-10-28_dan.md): the gain map. Is the difference between the readers a difference of weights on
the same two parts, rather than two routes?

Scenes: the main test (x0_necessity, alt cf: two people swap their picks; d1_topics_v3, chat), locker-first (x45m's
group: the bridge's and S's bridge's locker sentences both before the asked pick), taken from each model's stored X0 run
at the layer fixed in advance (x45b_binding.MAIN_RUN; selected and rebuilt on the target's tokenizer by
x47_cumulative.select, which checks the ids and the bridge position against the run's). X0's gate (0.80 per reader on O
unedited, >= 150 eligible) is the source run's: asserted from its gate.json; a failed gate means "not tested".

At the bridge word and L: Δ = h_S - h_O (one unedited forward of each on the lookup's prompts); P_J Δ = X0's 25-atom
signed OMP part over the J++ lens's letter-token atoms at L (x0_necessity.fit); the rest = Δ - P_J Δ. Each arm adds a
vector at the bridge word at L on O (X0's AddRows) and is read by both readers with X0's chat read (switch = the top
token over the vocabulary is S's answer's first token):
  J(α,β)     α P_J Δ + β (Δ - P_J Δ), α, β in {0, 0.5, 1, 1.5, 2} (25 arms; J(1,1) = Δ, X0's whole arm; J(0,0) = O)
  R(α,β)     α R Δ + β (Δ - R Δ) at the corners (0,1), (1,0), (2,0), (0,2): R Δ = X0's random part of P_J Δ's share
             of ||Δ||^2 (the first k columns of the random basis, seed 888 + L; statement_positions.random_subspace_part)
  J(0,2)-U   amendment 2, as written: 2 (Δ - P_J Δ - U U^T Δ); U = the pointer directions fit on fresh scenes
             (x0_massmean pointer_means, x47_atoms.pointer_basis; never refit)
  J(0,2)-RU  its twin: 2 (Δ - P_J Δ - R_U Δ), R_U Δ the random part of U U^T Δ's share (same basis)
  J100(α,β), R100(α,β)   the 9B only (dumbest way 2): the four corners with P_J at K = 100 and its random twin
Plain-text loss (dumbest way 1): the model's next-token loss on O's own text at the bridge word (the logits at the bridge
word under the arm, against O's next token), for every arm, from a forward of O's lookup prompt up to the bridge word.

Rules (fixed in advance; point estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs over the bridge items,
10,000, seed 0, beside):
  (a)  "weights, not routes": the recall's switch at J(2,0) >= 0.5 and at J(0,2)-U >= 0.5, random corners <= 0.15;
       the lookup's switch at J(2,0) <= 0.10 and at J(0,1) >= 0.6
  (b)  "routes": the recall's switch at J(0,2) <= 0.2 while J(2,0) >= 0.5
  (a') "the rest moves the recall only through the address": J(0,2) >= 0.5 but J(0,2)-U <= 0.2
  (c)  "neither": none of the three; report the two heatmaps
"Random corners <= 0.15", as computed: the recall's R(1,0) and R(2,0), the corners where the random part stands where the
J++ part is written (R(0,1) and R(0,2) keep most of the change, so the whole change's switch is expected there); all four
are reported beside, with the literal reading's outcome (Dan may override before the verdict). Dumbest way 1: loss at
J(2,0), J(0,2), J(2,2) and J(0,2)-U against J(1,1); a corner above 2x J(1,1)'s mean is flagged, descriptive.

SEALED: the job writes per-item files only; verdict refuses until predictions/2026-10-28_dan.md holds Dan's Q49.1
answer at HEAD.

uv run python scripts/x49_gain.py plan                                                   # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x49_gain.py run --name qwen35_9b_x49_1        # GPU (sealed)
uv run python scripts/x49_gain.py verdict                                                 # CPU, after Dan's Q49.1
"""

from __future__ import annotations

import argparse
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
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x47_cumulative as C

EXP = "x49_gain"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch49.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q49.1"
RENDERING = "chat"
GROUP = "locker-first"
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x49_1", "qwen3.6-27b": "x49_1_27b", "muse-glimmer-30b": "muse30_x49_1"}
# batch 52 C coverage (amendment 2: the full grid on Lightning): read by verdict --coverage alone (RUNS / MODELS and the
# design's own verdict unchanged)
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_gain", "qwen3.5-122b-a10b": "qwen35_122b_gain"}  # 122B: Dan 30 Oct ~02:10
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x49_gain/x49_1-20261028T154510Z"  # 49.1's rule first scored (9B, 27B, Muse)
# target -> the main test's X0 run (chat, at X.PREDICTED); the 122B's r2 run at L33 for Dan's 18:20 coverage
# (jobs/c3/batch53.yaml coverage_122b_1820), kept out of B.MAIN_RUN as x51_answer.E1_SOURCE_EXTRA does
SOURCES = {**B.MAIN_RUN, "qwen3.5-122b-a10b": "qwen35_122b_x0_necessity_r2"}
K = X.K_MAIN  # 25
K_WIDE = 100  # dumbest way 2
WIDE_TARGETS = ("qwen3.5-9b",)
GAINS = (0.0, 0.5, 1.0, 1.5, 2.0)
CORNERS = ((0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (0.0, 2.0))
RAND_RULE_CORNERS = ((1.0, 0.0), (2.0, 0.0))  # "random corners <= 0.15": Dan's reading (amendment 3, ~15:40)
MATCHED_CORNERS, MATCHED_TOL = ((0.0, 1.0), (0.0, 2.0)), 0.10  # matched-share controls (amendment 3), reported
N_PROMPTS = 5  # the plan's rendered prompts
EPS = 1e-9  # a value exactly at a bar counts as at the bar
REC_J, REC_NOU, RAND_MAX = 0.5, 0.5, 0.15  # (a), the recall
LK_J_MAX, LK_REST_MIN = 0.10, 0.6  # (a), the lookup
ROUTES_REST_MAX, ROUTES_J_MIN = 0.2, 0.5  # (b)
ADDR_REST_MIN, ADDR_NOU_MAX = 0.5, 0.2  # (a')
LOSS_FLAG = 2.0  # dumbest way 1: a corner's mean loss above this multiple of J(1,1)'s
LABELS = {"a": "(a) weights, not routes", "b": "(b) routes",
          "a_prime": "(a') the rest moves the recall only through the address", "c": "(c) neither"}  # fmt: skip
RULE = ('(a) "weights, not routes": the recall\'s switch at (2,0) >= 0.5 and at (0,2, no U) >= 0.5, random corners <= '
        "0.15; the lookup's switch at (2,0) <= 0.10 and at (0,1) >= 0.6. (b) \"routes\": the recall's switch at (0,2) "
        "<= 0.2 while (2,0) >= 0.5. (a') \"the rest moves the recall only through the address\": (0,2) >= 0.5 but (0,2, "
        'no U) <= 0.2. (c) "neither": report the two heatmaps')  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


def gname(kind: str, a: float, b: float) -> str:
    """An arm's name: J(α,β) the J++ part's gain α and the rest's β; R(α,β) a random part in place of the J++ part;
    J100 / R100 the same at K = 100."""
    return f"{kind}({a:g},{b:g})"


NOU, NOU_RAND = "J(0,2)-U", "J(0,2)-RU"
WHOLE, NONE = gname("J", 1, 1), gname("J", 0, 0)
LOSS_ARMS = (gname("J", 2, 0), gname("J", 0, 2), gname("J", 2, 2), NOU)  # against WHOLE
ARM_TEXT = {
    "J(α,β)": "α P_J Δ + β (Δ - P_J Δ), P_J Δ the 25-atom signed OMP J++ part of Δ (J(1,1) = Δ, J(0,0) = O unedited)",
    "R(α,β)": "α R Δ + β (Δ - R Δ), R Δ a random subspace's part of Δ at P_J Δ's share of ||Δ||^2 (seed 888 + L)",
    NOU: "2 (Δ - P_J Δ - U U^T Δ), U the pointer directions (amendment 2, as written)",
    NOU_RAND: "2 (Δ - P_J Δ - R_U Δ), R_U Δ a random part at U U^T Δ's share of ||Δ||^2 (same random basis)",
    "J100 / R100": f"the four corners with P_J at K = {K_WIDE} and its random twin ({', '.join(WIDE_TARGETS)} only)",
}


def arm_names(wide: bool) -> list[str]:
    """Every arm in read order: the 5x5 grid (α outer, β inner), the random corners, the no-U arm and its twin, and on
    a wide target the K = 100 corners and their twins."""
    out = [gname("J", a, b) for a in GAINS for b in GAINS] + [gname("R", a, b) for a, b in CORNERS] + [NOU, NOU_RAND]
    if wide:
        out += [gname(kind, a, b) for kind in ("J100", "R100") for a, b in CORNERS]
    return out


# ---- the parts and the arms (CPU-testable) -------------------------------------------------------------------------


def share(part, x):
    """Per row: ||part||^2 / ||x||^2 (float32)."""
    return part.float().norm(dim=-1) ** 2 / (x.float().norm(dim=-1) ** 2).clamp_min(1e-30)


def lens_parts(jdic, delta, k: int, basis) -> tuple[Any, Any]:
    """Per row of Δ [n, d]: the k-atom signed OMP part over jdic (X0's J++ part) and X0's random part of its share."""
    from scripts import statement_positions as SP

    pj = X.fit(jdic, delta.float(), k, "signed")
    return pj, SP.random_subspace_part(delta, share(pj, delta), basis)


def pointer_parts(delta, u, basis) -> tuple[Any, Any]:
    """Per row of Δ: U U^T Δ (U [d, r] orthonormal) and the random part of its share."""
    from scripts import statement_positions as SP

    up = (delta.float() @ u) @ u.T
    return up, SP.random_subspace_part(delta, share(up, delta), basis)


def arm_deltas(delta, pj, rj, up, ru, wide: tuple[Any, Any] | None = None) -> dict[str, Any]:
    """Each arm's added vector per item [n, d], in arm_names order (wide = (P_J Δ, R Δ) at K = 100, or None)."""
    out = {gname("J", a, b): a * pj + b * (delta - pj) for a in GAINS for b in GAINS}
    out |= {gname("R", a, b): a * rj + b * (delta - rj) for a, b in CORNERS}
    out[NOU] = 2.0 * (delta - pj - up)
    out[NOU_RAND] = 2.0 * (delta - pj - ru)
    if wide is not None:
        for kind, part in (("J100", wide[0]), ("R100", wide[1])):
            out |= {gname(kind, a, b): a * part + b * (delta - part) for a, b in CORNERS}
    assert list(out) == arm_names(wide is not None)
    return out


def norm_records(delta, pj, rj, up, ru, u, wide: tuple[Any, Any] | None = None) -> list[dict]:
    """Per item: ||Δ||, the shares of ||Δ||^2 of each part and of its random twin, and of U U^T P_J Δ: the part of U
    that the no-U arm as written takes out twice (inside P_J Δ and again inside U U^T Δ); "U removed from the rest",
    (1 - U U^T)(Δ - P_J Δ), differs from the written arm by exactly 2 U U^T P_J Δ."""
    both = (pj.float() @ u) @ u.T
    sh = {"share_J": share(pj, delta), "share_J_rand": share(rj, delta), "share_U": share(up, delta),
          "share_U_rand": share(ru, delta), "share_U_in_J": share(both, delta)}  # fmt: skip
    if wide is not None:
        sh |= {"share_J100": share(wide[0], delta), "share_J100_rand": share(wide[1], delta)}
    norms = delta.float().norm(dim=-1)
    return [{"norm_delta": round(float(norms[i]), 4), **{k: round(float(v[i]), 6) for k, v in sh.items()}}
            for i in range(delta.shape[0])]  # fmt: skip


def pointer_basis(target: str) -> tuple[np.ndarray, dict]:
    """U (x47_atoms.pointer_basis: x0_massmean's layout-free mass-mean slot directions on the probe run's fresh scenes;
    never refit), [d, r] orthonormal, and its record."""
    from scripts import x6_routes as R
    from scripts import x47_atoms as A

    u = np.asarray(A.pointer_basis(target), dtype=np.float64)
    assert np.allclose(u.T @ u, np.eye(u.shape[1]), atol=1e-6), "U is not orthonormal"
    return u, {"states_run": R.STATES[target], "rank": int(u.shape[1]),
               "how": "x47_atoms.pointer_basis (x0_massmean.subspaces' Alf on the probe run's states), not refit"}  # fmt: skip


# ---- items (tokenizer only) ----------------------------------------------------------------------------------------


def source_gate(run: str) -> dict:
    """The source X0 run's gate for the chat rendering, as its gate.json stores it."""
    return json.loads((X.RESULTS / run / "gate.json").read_text())["gate"][RENDERING]


def gate_passes(gate: dict) -> bool:
    """X0's gate fixed in advance: 0.80 per reader on O unedited and >= 150 eligible (pass and enough)."""
    return bool(gate.get("pass")) and bool(gate.get("enough"))


def select_items(tok, target: str) -> tuple[list[dict], dict]:
    """The main test's locker-first items of the target's X0 run at L, in its scene order (x47_cumulative.select:
    rebuilt on the tokenizer and checked against the run's ids and bridge positions), and the counts."""
    items, counts = C.select(tok, "main", SOURCES[target], X.PREDICTED[target])
    mine = [it for it in items if it["group"] == GROUP]
    return mine, {**counts, "group": GROUP, "items_in_group": len(mine),
                  "entities_in_group": len({it["entity"] for it in mine})}  # fmt: skip


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    """k random indices of n (seed 0), as X0 picks its examples."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def as_read(decode, it: dict, reader: str, variant: str = "org") -> str:
    """The reader's prompt exactly as the model reads it (the digit's space token appended), the bridge word in ⟦...⟧
    (where every arm adds its vector)."""
    from scripts import x6_routes as R

    return R.marked(decode, it["readers"][reader]["ids"][variant] + it["space"], it["pos"])


def write_plan(blob: dict, prompts: list[tuple[str, str]]) -> Path:
    """The plan's counts (plan.json) and its rendered prompts (prompts.md) in a new results/x49_gain/plan-<UTC>/."""
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan on {blob['target']} (tokenizer only): {len(prompts)} rendered prompts, ⟦…⟧ the bridge word "
             "(where each arm adds its vector at L)", ""]  # fmt: skip
    for scene, text in prompts:
        lines += [f"## {scene}", "", "```", text, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def stage_plan(k_prompts: int = N_PROMPTS) -> dict:
    """Tokenizer only: the source run's gate, the items and drops, the arms and reads, U's rank, and k rendered
    prompts (seed 0): both readers' O as read and the lookup's S, the bridge word marked; the loss's target token."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    gate = source_gate(SOURCES[target])
    items, counts = select_items(tok, target)
    names = arm_names(target in WIDE_TARGETS)
    try:
        u_rank: int | str = pointer_basis(target)[1]["rank"]
    except (OSError, KeyError) as e:  # the probe run's states are not on this machine
        u_rank = f"not available here: {e}"
    chosen = [items[i] for i in example_indices(len(items), k_prompts)]
    blob = {
        "target": target, "layer": X.PREDICTED[target], "prefix": pins.RUN_PREFIX, "run": RUNS.get(target),
        "source": SOURCES[target], "source_gate": gate, "gate_passes": gate_passes(gate), "counts": counts,
        "arms": names, "n_arms": len(names), "reads": len(items) * len(X.READERS) * len(names),
        "loss_rows": len(items) * len(names), "U_rank": u_rank,
        "prompts": [{"scene": it["scene"], "bridge": f"{it['entity']} -> {it['cf_bridge']}",
                     "loss_target": decode([it["readers"][X.LOOKUP]["ids"]["org"][it["pos"] + 1]]),
                     **{f"{READER_NAME[w]}_O_as_read": as_read(decode, it, w) for w in X.READERS},
                     "lookup_S_as_read": as_read(decode, it, X.LOOKUP, "alt")} for it in chosen],
    }  # fmt: skip
    print(json.dumps({k: v for k, v in blob.items() if k != "prompts"}, indent=1, ensure_ascii=False))
    write_plan(
        blob, [(p["scene"], f"{k}: {v}") for p in blob["prompts"] for k, v in p.items() if k.endswith("as_read")]
    )
    return blob


# ---- GPU -----------------------------------------------------------------------------------------------------------


def greedy_texts(model, ids: list[int], edits: list[dict]) -> list[str]:
    """X0's example texts (GEN_TOKENS greedy tokens of O) under each edit set, in batches of BJ_SUITE_BATCH rows."""
    import torch

    from scripts import suite_split as P

    out: list[str] = []
    for s in range(0, len(edits), P.BATCH):
        out += model.generate_batch(torch.tensor([ids], device=model.device), X.GEN_TOKENS, edits[s : s + P.BATCH])
    return out


def run_items(model, lens, items: list[dict], layer: int, digits, u, wide: bool) -> tuple[list, list, list, list]:
    """Every arm on each item's O, both readers (outcome rows), per item the parts' shares (norms), the plain-text
    loss at the bridge word under every arm (losses), and the example items' greedy texts. Δ: one unedited forward of
    O and of S per item on the lookup's prompts (both readers' prompts agree through the bridge word)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    names = arm_names(wide)
    with torch.no_grad():
        rows_d = []
        for it in progress(items, f"49.1: Δ at the bridge word, L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=dev), record=(layer,))[1][layer][it["pos"]].float()
                 for v in ("org", "alt")}  # fmt: skip
            rows_d.append(h["alt"] - h["org"])
        delta = torch.stack(rows_d)
        basis = SP.random_basis(delta.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        jdic = lens.vectors(layer, model.letter_token_ids())
        pj, rj = lens_parts(jdic, delta, K, basis)
        wide_parts = lens_parts(jdic, delta, K_WIDE, basis) if wide else None
        del jdic
        uu = torch.as_tensor(u, dtype=torch.float32, device=dev)
        assert uu.shape[0] == delta.shape[1], (
            f"U is [{uu.shape[0]}, {uu.shape[1]}], the states are d = {delta.shape[1]}"
        )
        up, ru = pointer_parts(delta, uu, basis)
        arms = arm_deltas(delta, pj, rj, up, ru, wide_parts)
        assert torch.allclose(arms[WHOLE], delta, atol=1e-4 * float(delta.abs().max())), "J(1,1) is not Δ"
        assert not arms[NONE].any(), "J(0,0) is not O unedited"
        norms = [{"scene": it["scene"], "entity": it["entity"], **r}
                 for it, r in zip(items, norm_records(delta, pj, rj, up, ru, uu, wide_parts), strict=True)]  # fmt: skip
        examples = set(example_indices(len(items)))
        rows, losses, greedy = [], [], []
        for i, it in enumerate(progress(items, f"49.1: {len(names)} arms x 2 readers + the loss (item)")):
            pos = it["pos"]
            edits = [{layer: AddRows(arms[a][i : i + 1], [pos])} for a in names]
            base = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"]}
            for w, rd in it["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], None)
                rows += [{**base, "reader": w, "arm": a, **X.read_row(lg, rd, digits)}
                         for a, lg in zip(names, logits, strict=True)]  # fmt: skip
                if i in examples:
                    greedy += [{"scene": it["scene"], "reader": w, "arm": a, "greedy": t}
                               for a, t in zip(names, greedy_texts(model, rd["ids"]["org"], edits), strict=True)]  # fmt: skip
            # dumbest way 1: O's own next token at the bridge word, the prompt cut after the bridge word
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            nxt = ids[pos + 1]
            logits, _ = X.read_logits(model, ids[: pos + 1], edits, RENDERING, [], None)
            lp = torch.log_softmax(logits.float(), dim=-1)
            losses += [{**base, "arm": a, "next": nxt, "loss": round(float(-row[nxt]), 5), "top_is_next": int(int(row.argmax()) == nxt)}
                       for a, row in zip(names, lp, strict=True)]  # fmt: skip
    return rows, norms, losses, greedy


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state
    from scripts import suite_split as SUITE

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.1 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in SOURCES, f"49.1 runs on {sorted(SOURCES)}, not {target}"
    layer, source, wide = X.PREDICTED[target], SOURCES[target], target in WIDE_TARGETS
    src = X.RESULTS / source
    u, u_info = pointer_basis(target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    names = arm_names(wide)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "49.1",
         "spec": "jobs/c3/batch49.yaml (49.1, amendment 2's 49.1 item)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl")))},
         "source": source, "layer": layer, "rendering": RENDERING, "group": GROUP, "k": K, "wide": wide,
         "k_wide": K_WIDE if wide else None, "gains": list(GAINS), "corners": [list(c) for c in CORNERS],
         "arms": names, "arm_text": ARM_TEXT, "pointer": u_info,
         "items_rule": "the source X0 run's scenes at L (chat outcomes: the items its unedited run made eligible), "
                       "rebuilt by x47_cumulative.select (ids and bridge position checked against the run's; items "
                       "its alignment checks refuse dropped and counted), x45m.group_of locker-first only",
         "parts": {"P_J": f"x0_necessity.fit(J++ letter-token atoms at L, Δ, {K}, signed)",
                   "R": f"statement_positions.random_subspace_part(Δ, P_J Δ's share of ||Δ||^2, random basis seed "
                        f"{X.SUBSPACE_SEED} + L)", "U": "U U^T Δ", "R_U": "random_subspace_part at U U^T Δ's share, same basis"},
         "edit": "AddRows: the arm's vector added at the bridge word's block output at L, on O",
         "read": "X0's chat read: O's prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token",
         "loss": "dumbest way 1: -log p(O's token after the bridge word) at the bridge word, from O's lookup prompt cut "
                 "after the bridge word, under each arm",
         "gate": f"the source run's (X0: {X.GATE} per reader on O unedited, >= {X.N_MIN} eligible); asserted",
         "rule": RULE, "rand_rule_corners": [list(c) for c in RAND_RULE_CORNERS], "loss_flag": LOSS_FLAG,
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "order": {"items": "the source run's scene order (locker-first only)",
                   "reads": f"per item and reader: O's prompt under the {len(names)} arms in arm order, one batch of at "
                            f"most {SUITE.BATCH} rows (BJ_SUITE_BATCH); then the loss: O's lookup prompt cut after the "
                            "bridge word under the same arms, one batch", "batch": SUITE.BATCH},
         "sealed": f"no verdict in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    gate = source_gate(source)
    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    items, counts = select_items(model.tokenizer, target)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    tested = gate_passes(gate) and bool(items)
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
    rows, norms, losses, greedy = run_items(model, lens, items, layer, digits, u, wide)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "losses.jsonl", losses)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU, sealed) -----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q49.1 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
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


def per_item(rows: list[dict], key: str, names: list[str], reader: str | None = None) -> tuple[list[str], dict]:
    """Rows -> (the bridge entity per item in row order, {arm: [value per item]}); every item must have every arm."""
    by: dict[tuple[str, str], float] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if reader is None or r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = r[key]
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in names if (s, a) not in by]
    assert not missing, f"{reader or 'loss'}: {len(missing)} item-arm values missing, e.g. {missing[:3]}"
    return [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in names}


def reader_numbers(rows: list[dict], reader: str, names: list[str], n_boot: int = X.N_BOOT,
                   seed: int = X.BOOT_SEED) -> dict:  # fmt: skip
    """One reader's switch rate per arm, with 95% CIs from X0's cluster bootstrap over the bridge items (paired)."""
    entities, sw = per_item(rows, "switched", names, reader)
    boot = X.resampled_rates(sw, entities, n_boot, seed)
    return {"n": len(entities), "entities": len(set(entities)), "hits": {a: int(sum(v)) for a, v in sw.items()},
            "rate": {a: [float(np.mean(v)), *X.interval(boot[a])] for a, v in sw.items()}}  # fmt: skip


def rule(recall: dict[str, float], lookup: dict[str, float]) -> dict:
    """The rules fixed in advance on point estimates (EPS at the bars): every condition, the clauses, the label; and
    (a) under the literal reading of "random corners" (all four), beside."""
    rc, lk = recall, lookup
    j20, j02, j01 = gname("J", 2, 0), gname("J", 0, 2), gname("J", 0, 1)
    cond = {"recall J(2,0) >= 0.5": rc[j20] >= REC_J - EPS, "recall J(0,2)-U >= 0.5": rc[NOU] >= REC_NOU - EPS,
            "recall random corners <= 0.15": all(rc[gname("R", a, b)] <= RAND_MAX + EPS for a, b in RAND_RULE_CORNERS),
            "lookup J(2,0) <= 0.10": lk[j20] <= LK_J_MAX + EPS, "lookup J(0,1) >= 0.6": lk[j01] >= LK_REST_MIN - EPS,
            "recall J(0,2) <= 0.2": rc[j02] <= ROUTES_REST_MAX + EPS, "recall J(0,2) >= 0.5": rc[j02] >= ADDR_REST_MIN - EPS,
            "recall J(0,2)-U <= 0.2": rc[NOU] <= ADDR_NOU_MAX + EPS}  # fmt: skip
    a_core = all(cond[k] for k in ("recall J(2,0) >= 0.5", "recall J(0,2)-U >= 0.5", "lookup J(2,0) <= 0.10",
                                   "lookup J(0,1) >= 0.6"))  # fmt: skip
    clauses = {"a": a_core and cond["recall random corners <= 0.15"],
               "b": cond["recall J(0,2) <= 0.2"] and cond["recall J(2,0) >= 0.5"],
               "a_prime": cond["recall J(0,2) >= 0.5"] and cond["recall J(0,2)-U <= 0.2"]}  # fmt: skip
    holds = [k for k in ("a", "b", "a_prime") if clauses[k]]
    literal = a_core and all(rc[gname("R", a, b)] <= RAND_MAX + EPS for a, b in CORNERS)
    # Dan (amendment 3, ~15:40): R(0,1) and R(0,2) are matched-share controls, not nulls: within 0.10 of their J cells
    matched = {f"{w} R({a:g},{b:g}) within {MATCHED_TOL} of J": abs(x[gname("R", a, b)] - x[gname("J", a, b)]) <= MATCHED_TOL + EPS
               for w, x in (("recall", rc), ("lookup", lk)) for a, b in MATCHED_CORNERS}  # fmt: skip
    return {"conditions": cond, "clauses": clauses, "holds": holds,
            "label": " and ".join(LABELS[k] for k in holds) or LABELS["c"], "a_literal_all_four_corners": literal,
            "matched_share_controls": matched}  # fmt: skip


def loss_numbers(losses: list[dict], names: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """Dumbest way 1: the mean plain-text loss per arm (cluster-bootstrap CIs), each loss arm's mean over J(1,1)'s
    (paired CI), flagged above LOSS_FLAG (descriptive); the share of items whose top token is O's own next token."""
    entities, vals = per_item(losses, "loss", names)
    _, top = per_item(losses, "top_is_next", names)
    boot = X.resampled_rates(vals, entities, n_boot, seed)
    mean = {a: [float(np.mean(v)), *X.interval(boot[a])] for a, v in vals.items()}
    base = mean[WHOLE][0]
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = {
            a: [mean[a][0] / base if base > 0 else math.nan, *X.interval(boot[a] / boot[WHOLE])] for a in LOSS_ARMS
        }
    return {"n": len(entities), "mean": mean, "ratio_to_whole": ratio,
            "flag": {a: bool(ratio[a][0] > LOSS_FLAG) for a in LOSS_ARMS},
            "top_is_next": {a: float(np.mean(v)) for a, v in top.items()}}  # fmt: skip


def side_checks(rows: list[dict], cases: list[dict]) -> dict:
    """Per reader: J(0,0) (O unedited) reads O's answer; J(1,1) against the source run's stored whole arm."""
    stored = {c["scene"]: c["stored"]["whole"] for c in cases}
    out = {}
    for w in X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        whole = [(int(r["switched"]), stored[r["scene"]].get(w)) for r in mine if r["arm"] == WHOLE]
        none = [r for r in mine if r["arm"] == NONE]
        out[READER_NAME[w]] = {"n": len(none), "none_reads_O": sum(r["role"] == "A" for r in none),
                               "whole_vs_stored": {"n": len(whole), "agree": sum(x == y for x, y in whole),
                                                   "rerun": sum(x for x, _ in whole), "stored": sum(y or 0 for _, y in whole)}}  # fmt: skip
    return out


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), not tested (the gate, or no items), or its numbers, rule and checks."""
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending", "label": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    if not gate.get("tested") or not rows:
        return {"target": target, "run": run, "status": "not tested", "label": "not tested", "gate": gate.get("gate"),
                "why": "the gate fixed in advance failed, no locker-first items, or the run did not finish"}  # fmt: skip
    names = arm_names(bool(m["wide"]))
    readers = {READER_NAME[w]: reader_numbers(rows, w, names, n_boot) for w in X.READERS}
    pts = {w: {a: v[0] for a, v in readers[w]["rate"].items()} for w in readers}
    r = rule(pts["recall"], pts["lookup"])
    norms = X.read_jsonl(src / "norms.jsonl")
    keys = [k for k in norms[0] if k not in ("scene", "entity")]
    return {"target": target, "run": run, "status": "tested", "layer": m["layer"], "wide": bool(m["wide"]),
            "n": readers["recall"]["n"], "arms": names, "label": r["label"], **r, "readers": readers,
            "loss": loss_numbers(X.read_jsonl(src / "losses.jsonl"), names, n_boot),
            "checks": side_checks(rows, X.read_jsonl(src / "cases.jsonl")), "gate": gate.get("gate"),
            "pointer": m["pointer"], "shares_median": {k: float(np.median([n[k] for n in norms])) for k in keys}}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None or v[0] is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def grid_lines(rate: dict[str, list[float]]) -> list[str]:
    """A 5x5 markdown table of one reader's switch rates: rows β (the rest's gain, 2 at the top), columns α."""
    lines = ["| β \\ α | " + " | ".join(f"{a:g}" for a in GAINS) + " |", "|---|" + "---|" * len(GAINS)]
    for b in reversed(GAINS):
        lines.append(f"| {b:g} | " + " | ".join(f"{rate[gname('J', a, b)][0]:.2f}" for a in GAINS) + " |")
    return lines


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    tested = [m for m in models if m["status"] == "tested"]
    lines = ["# 49.1: the gain map", "",
             f"Batch 49, test 49.1 (jobs/c3/batch49.yaml, amendment 2; {QUESTION}, Dan: {answer}). Main-test scenes, "
             "locker-first, chat; at the bridge word at L, α × the change's J++ part + β × the rest added to O; switch = "
             f"the top token is S's answer (X0's chat read). Cluster bootstrap over the bridge items ({n_boot}, seed "
             f"{X.BOOT_SEED}). UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             "Random corners in (a), as computed: the recall's R(1,0) and R(2,0) (the random part where the J++ part is "
             "written); the literal reading (all four corners, incl. R(0,1) and R(0,2), which keep most of the change) is "
             "shown beside.", "",
             "| model | run | n | recall J(2,0) | J(0,2) | J(0,2)-U | R(1,0) | R(2,0) | lookup J(2,0) | lookup J(0,1) | "
             "label | (a) literal |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(
                f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | | | | | | **{m['label']}** | |"
            )
            continue
        rc, lk = m["readers"]["recall"]["rate"], m["readers"]["lookup"]["rate"]
        lines.append(f"| {m['target']} | {m['run']} | {m['n']} | " + " | ".join(
            fmt(rc[a]) for a in (gname("J", 2, 0), gname("J", 0, 2), NOU, gname("R", 1, 0), gname("R", 2, 0)))
            + f" | {fmt(lk[gname('J', 2, 0)])} | {fmt(lk[gname('J', 0, 1)])} | **{m['label']}** | "
            f"{m['a_literal_all_four_corners']} |")  # fmt: skip
    for m in tested:
        lines += ["", f"## {m['target']} ({m['run']}, L{m['layer']}, n = {m['n']}, "
                  f"{m['readers']['recall']['entities']} bridge items)", "",
                  "Conditions: " + "; ".join(f"{k}: {v}" for k, v in m["conditions"].items()) + ".", ""]  # fmt: skip
        for w in ("recall", "lookup"):
            lines += [f"**{w}**, switch rate by gain (α the J++ part's, β the rest's; J(1,1) = the whole change):", "",
                      *grid_lines(m["readers"][w]["rate"]), ""]  # fmt: skip
        extra = [gname("R", a, b) for a, b in CORNERS] + [NOU, NOU_RAND, *[gname("J", a, b) for a, b in CORNERS]]
        if m["wide"]:
            extra += [gname(k, a, b) for k in ("J100", "R100") for a, b in CORNERS]
        lines += ["| arm | recall | lookup |", "|---|---|---|"]
        lines += [f"| {a} | {fmt(m['readers']['recall']['rate'][a])} | {fmt(m['readers']['lookup']['rate'][a])} |"
                  for a in extra]  # fmt: skip
        lo = m["loss"]
        lines += ["", f"Dumbest way 1 (descriptive): plain-text loss at the bridge word (O's next token), mean over the "
                  f"items; a corner above {LOSS_FLAG:g}x J(1,1)'s is flagged.", "",
                  "| arm | mean loss | ÷ J(1,1) | flagged | top token = O's next |", "|---|---|---|---|---|"]  # fmt: skip
        for a in (NONE, WHOLE, *LOSS_ARMS):
            ratio = lo["ratio_to_whole"].get(a)
            lines.append(f"| {a} | {fmt(lo['mean'][a])} | {fmt(ratio) if ratio else ''} | "
                         f"{lo['flag'].get(a, '')} | {lo['top_is_next'][a]:.2f} |")  # fmt: skip
        for w, s in m["checks"].items():
            wv = s["whole_vs_stored"]
            lines.append(f"- {w}: J(0,0) reads O's answer on {s['none_reads_O']} of {s['n']}; J(1,1) vs the source "
                         f"run's whole arm: {wv['agree']} of {wv['n']} agree (rerun {wv['rerun']}, stored {wv['stored']})")  # fmt: skip
        lines.append("- shares of ||Δ||^2 (median): " + ", ".join(f"{k} {v:.4g}" for k, v in m["shares_median"].items())
                     + f"; U rank {m['pointer']['rank']} ({m['pointer']['states_run']})")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def example_lines(m: dict, decode, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view of one run: k random items (seed 0), each reader's O prompt as read with the bridge word in
    ⟦...⟧, and every arm's answer (the top token read, switched or not, the greedy text)."""
    src = RESULTS / m["run"]
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {m['target']}: {m['run']}, {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} (O) → {it['cf_bridge']} (S), token "
                  f"{it['pos']}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "",
                      "O, as read:", "", "```", as_read(decode, it, w), "```", "",
                      "| arm | answer (top token) | switched | greedy |", "|---|---|---|---|"]  # fmt: skip
            for a in m["arms"]:
                r = reads[(it["scene"], w, a)]
                g = greedy.get((it["scene"], w, a))
                lines.append(f"| {a} | {decode([r['top']])!r} | {r['switched']} | {'' if g is None else repr(g)} |")
            lines.append("")
    return lines


def stage_verdict(
    runs: dict[str, str] | None = None, n_boot: int = X.N_BOOT, decode_for=None, coverage: bool = False
) -> Path:
    """49.1's verdict (sealed until Q49.1) over MODELS, or with coverage (batch 52 C) the same rule on the given coverage
    runs (target -> run, default COVERAGE_RUNS) alone: no seal guard, "no prediction" in place of Dan's answer, written to
    x52_gain-<UTC>/."""
    from scripts import x47_atoms as A

    answer = f"{NO_PREDICTION}; rule first scored in {SCORED}" if coverage else unsealed()
    runs = runs or (COVERAGE_RUNS if coverage else RUNS)
    if coverage:
        assert set(runs) <= set(COVERAGE_RUNS), f"49.1 coverage runs on {sorted(COVERAGE_RUNS)}, not {sorted(runs)}"
    models = [model_result(t, runs[t], n_boot) for t in (runs if coverage else MODELS)]
    out = RESULTS / f"{'x52_gain' if coverage else 'x49_1'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 C coverage, ") for ln in lines]
    blob = {"dan": answer, "rule": RULE, "labels": LABELS, "gains": list(GAINS), "corners": [list(c) for c in CORNERS],
            "rand_rule_corners": [list(c) for c in RAND_RULE_CORNERS], "models": models,
            "per_model": {m["target"]: m["label"] for m in models}}  # fmt: skip
    (out / "x49_1.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "x49_1.md").write_text("\n".join(lines) + "\n")
    ex = ["# 49.1 verify pack: O's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the "
          "bridge word, where each arm adds its vector at L. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] == "tested":
            ex += example_lines(m, (decode_for or A.default_decode)(m["target"]))
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x49_gain/<name>/)")
    ap.add_argument("--why", default="batch 49, test 49.1 (jobs/c3/batch49.yaml; Q49.1): the gain map; sealed")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--runs", nargs=3, default=None, metavar=("9B", "27B", "MUSE"),
                    help=f"verdict: runs in place of the specs' {[RUNS[t] for t in MODELS]}")  # fmt: skip
    ap.add_argument("--coverage", action="store_true",
                    help=f"verdict: batch 52 coverage runs {COVERAGE_RUNS} ('{NO_PREDICTION}')")  # fmt: skip
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        assert not (a.coverage and a.runs), "verdict --coverage reads COVERAGE_RUNS (no --runs)"
        stage_verdict(dict(zip(MODELS, a.runs, strict=True)) if a.runs else None, n_boot=a.n_boot, coverage=a.coverage)


if __name__ == "__main__":
    main()
