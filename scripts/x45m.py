"""x45m (batch 45, test 45m; jobs/c3/batch45.yaml, design, rule and readings fixed in advance; Q45.10 in
predictions/2026-10-26_dan.md): the split in a clean one-pick design (no duplicate).

The one-pick design (x0_necessity --alt single) changes the asked pick to an item another person already picks, so the
changed prompt holds a duplicate. 45m (x0_necessity --alt fresh, x0_necessity.fresh_pair) adds one locker item that
nobody picks to both prompts and changes the asked pick from the bridge to it: one token changes, no duplicate. The run
is X0's own (set d1_topics_v3, chat, the layer fixed in advance, arms whole / no J++ / no random part with J++ k = 25
signed, both readers, X0's read, gate and eligibility).

Groups (as_computed): locker-before = both the bridge's and the new item's locker sentences come before the asked pick
(x0_strata's 'org / alt locker vs asked pick'); locker-after = both after; mixed scenes go only into "all scenes". Per
model and group: the lookup's and the recall's extra loss (X0's excess = Jdep - Rdep = (S_no_rand - S_no_part) /
S_whole), the gap (recall's minus lookup's), cluster-bootstrap CIs over the bridge items (10,000 resamples, seed 0; the
gap on the same draws as both readers), and X0's validity bar per cell (S_whole >= 0.30 and >= 30 switches; reported,
not in the rule).
Rule: "the split holds in the clean design" if on at least 2 of 3 models, in locker-before scenes, the gap is at least
0.3 and the lookup's extra loss at most 0.10 (point estimates, EPS tolerance). A model whose read gate fails is "not
tested" and does not count as holding.

uv run python scripts/x45m.py plan        # CPU, the target's tokenizer: scenes made / dropped, groups, 3 examples
uv run python scripts/x45m.py score --runs qwen35_9b_x45m_fresh x45m_fresh_27b muse30b_x45m_fresh
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x0_strata as ST

SET = "d1_topics_v3"
GROUPS = ("locker-before", "locker-after", "all")
GAP_MIN, LOOKUP_MAX, MODELS_MIN = 0.3, 0.10, 2
EPS = 1e-9  # a value exactly at a bar counts as at the bar (float sums such as 0.1 + 0.2)
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


def group_of(case: dict) -> str:
    """locker-before / locker-after / mixed: where the bridge's and the new item's locker sentences sit relative to
    the asked pick sentence (x0_strata.features on the org context, which holds both)."""
    f = ST.features(case)
    org, alt = f["org locker vs asked pick"], f["alt locker vs asked pick"]
    assert "none" not in (org, alt), f"{case['scene']}: a locker sentence is missing"
    return "locker-before" if org == alt == "before" else "locker-after" if org == alt == "after" else "mixed"


# ---- the plan check (tokenizer only) ------------------------------------------------------------------------------


def tokenizer():
    """The target's tokenizer as a run loads it; on a machine without the weights, its cached files with the target's
    chat-template edits (Muse), which statement_positions.load_tokenizer's fallback leaves out."""
    from bridge_jspace.tokens import load_tokenizer
    from scripts import statement_positions as SP

    try:
        return load_tokenizer()
    except Exception:
        tok = SP.load_tokenizer()
        for before, after in pins.TARGETS[pins.TARGET].get("chat_template_edits", []):
            assert tok.chat_template.count(before) == 1, f"chat template edit does not apply once: {before[:60]!r}"
            tok.chat_template = tok.chat_template.replace(before, after)
        return tok


def plan(n_examples: int = 3) -> dict:
    """The fresh cases (chat) on the target's tokenizer: scenes made / dropped by reason, the groups, the slots, and a
    few examples (seed 0) with the inserted sentence and the changed pick marked."""
    X.ALT, X.RENDERINGS = "fresh", ("chat",)
    cases, counts = X.build_cases(tokenizer(), SET)
    groups = collections.Counter(group_of(c) for c in cases)
    first = cases[: X.N_ITEMS]  # the run keeps the first N_ITEMS eligible ones; the first N_ITEMS made, for scale
    out = {"target": pins.TARGET, "set": SET, **counts, "groups": dict(groups),
           "groups_first_200": dict(collections.Counter(group_of(c) for c in first)),
           "slots": dict(collections.Counter(f"{c['fresh']['slot']} of {c['fresh']['slots']}" for c in cases)),
           "domains": dict(collections.Counter(c["domain"] for c in cases)),
           "candidates_min": min(c["fresh"]["candidates"] for c in cases), "examples": []}  # fmt: skip
    for c in random.Random(0).sample(cases, min(n_examples, len(cases))):
        sent = c["fresh"]["sentence"]
        out["examples"].append({"scene": c["scene"], "domain": c["domain"], "group": group_of(c),
                                "org": c["context"].replace(sent, f"[+ {sent}]"),
                                "alt": c["cf_context"].replace(sent, f"[+ {sent}]"),
                                "bridge": c["bridge"], "new": c["cf_bridge"],
                                "asked_pick_place": ST.features(c)["asked pick place"],
                                "answers": {READER_NAME[w]: [rd["answer"], rd["cf_answer"]] for w, rd in c["readers"].items()},
                                "question": {READER_NAME[w]: rd["question"] for w, rd in c["readers"].items()}})  # fmt: skip
    print(json.dumps(out, indent=2))
    return out


# ---- the verdict (CPU) --------------------------------------------------------------------------------------------


def group_cells(rows: list[dict], scenes: list[str], entity: dict[str, str], n_boot: int) -> dict | None:
    """Per reader X0's cell on these scenes (J++ k = 25 signed), and the gap (recall's extra loss minus the lookup's)
    on the same cluster-bootstrap draws; None without scenes."""
    if not scenes:
        return None
    got = {(r["reader"], r["arm"], r["scene"]): int(r["switched"]) for r in rows}
    ents = [entity[s] for s in scenes]
    out: dict = {"n": len(scenes)}
    resampled = {}
    for w in X.READERS:
        sw = {a: [got[(w, a, s)] for s in scenes] for a in X.ARMS}
        out[READER_NAME[w]] = X.cell(sw, ents, n_boot)
        r = X.resampled_rates(sw, ents, n_boot)  # the draws depend only on the entities and the seed: paired
        resampled[w] = X.dependence(r["whole"], r["no_part"]) - X.dependence(r["whole"], r["no_rand"])
    gap = out["recall"]["excess"][0] - out["lookup"]["excess"][0]
    out["gap"] = [gap, *X.interval(resampled[X.RECALL] - resampled[X.LOOKUP])]
    return out


def holds(before: dict | None) -> tuple[bool, str]:
    """The rule on one tested model's locker-before cells (point estimates)."""
    if before is None:
        return False, "no locker-before scenes"
    gap, lookup = before["gap"][0], before["lookup"]["excess"][0]
    if math.isnan(gap) or math.isnan(lookup):
        return False, "no switches with the whole change in locker-before scenes (extra loss undefined)"
    ok_gap, ok_lookup = gap >= GAP_MIN - EPS, lookup <= LOOKUP_MAX + EPS
    why = (f"gap {gap:.3f} {'>=' if ok_gap else '<'} {GAP_MIN}; lookup's extra loss {lookup:.3f} "
           f"{'<=' if ok_lookup else '>'} {LOOKUP_MAX:.2f}")  # fmt: skip
    return ok_gap and ok_lookup, why


def model_result(run: str, n_boot: int) -> dict:
    """One model's run: pending (not run / no outcomes), not tested (gate), or its groups and the rule's check."""
    src = X.RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "gate.json").exists():
        return {"run": run, "status": "pending", "why": "the run has no manifest or gate.json yet"}
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt") == "fresh", f"{run}: alt {m.get('alt')!r}, not the fresh alt of 45m"
    target, layer = m["model"]["target"], m["predicted"]
    assert layer == X.PREDICTED[target], f"{run}: layer {layer} is not the one fixed in advance for {target}"
    gate = json.loads((src / "gate.json").read_text())
    g = gate["gate"]["chat"]
    base = {"run": run, "target": target, "layer": layer, "gate": g, "counts": gate["counts"]}
    if not g["pass"]:
        return {**base, "status": "not tested", "why": f"read gate failed ({g['org_accuracy']} < {m['gate']})"}
    if not g["enough"]:
        return {**base, "status": "not tested", "why": f"{g['eligible']} eligible scenes, fewer than {X.N_MIN}"}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == layer
            and (r["arm"] == "whole" or ((r["dict"], r["k"], r["omp"]) == X.MAIN and r["arm"] in X.ARMS))]  # fmt: skip
    if not rows:
        return {**base, "status": "pending", "why": "the gate passed but outcomes.jsonl has no rows yet"}
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    scenes = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    entity = {r["scene"]: r["entity"] for r in rows}
    group = {s: group_of(cases[s]) for s in scenes}
    cells = {"locker-before": group_cells(rows, [s for s in scenes if group[s] == "locker-before"], entity, n_boot),
             "locker-after": group_cells(rows, [s for s in scenes if group[s] == "locker-after"], entity, n_boot),
             "all": group_cells(rows, scenes, entity, n_boot)}  # fmt: skip
    ok, why = holds(cells["locker-before"])
    return {**base, "status": "tested", "holds": ok, "why": why,
            "n": {**dict(collections.Counter(group.values())), "all": len(scenes)}, "cells": cells}  # fmt: skip


def verdict(models: list[dict]) -> dict:
    """The rule over the models: pending while a run is missing; else holds iff at least MODELS_MIN tested models hold."""
    tested = [m for m in models if m["status"] == "tested"]
    n_hold = sum(m["holds"] for m in tested)
    if any(m["status"] == "pending" for m in models):
        label = "pending"
    else:
        label = "holds" if n_hold >= MODELS_MIN else "does not hold"
    answer = {"holds": "(a) yes", "does not hold": "(b) no"}.get(label, "pending")
    return {"label": label, "q45_10": answer, "models_holding": n_hold, "models_tested": len(tested),
            "models": len(models), "not_tested": [m["run"] for m in models if m["status"] == "not tested"]}  # fmt: skip


def fmt(v: list[float]) -> str:
    return "-" if math.isnan(v[0]) else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def bar(c: dict) -> str:
    return f"{'yes' if c['valid'] else 'NO'} ({c['S_whole'][0]:.2f}, {c['switched_whole']})"


def score(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    models = [model_result(r, n_boot) for r in runs]
    v = verdict(models)
    out = X.RESULTS / f"x45m-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = ["# 45m: the split in a clean one-pick design (no duplicate)", "",
             "Batch 45, test 45m (jobs/c3/batch45.yaml; Q45.10). The asked pick changes from the bridge to an added "
             "locker item that nobody picks (x0_necessity --alt fresh). J++ k = 25 signed at the layer fixed in advance, "
             f"chat. Extra loss = Jdep - Rdep; gap = recall's minus lookup's; cluster bootstrap over bridge items "
             f"({n_boot}, seed {X.BOOT_SEED}). Valid = X0's bar (S_whole >= {X.VALID_S}, >= {X.VALID_N} switches): "
             "(S_whole, switches), reported, not in the rule. UNVERIFIED.", "",
             f"**Verdict: {v['label']}** (Q45.10 {v['q45_10']}): {v['models_holding']} of {v['models']} models hold "
             f"(at least {MODELS_MIN} needed); tested {v['models_tested']}"
             + (f"; not tested: {', '.join(v['not_tested'])}" if v["not_tested"] else "") + ".", "",
             "| model | run | status | locker-before: gap >= 0.3 and lookup <= 0.10 |", "|---|---|---|---|"]  # fmt: skip
    for m in models:
        check = ("holds" if m["holds"] else "does not hold") + f" ({m['why']})" if m["status"] == "tested" else m["why"]
        lines.append(f"| {m.get('target', '-')} | {m['run']} | {m['status']} | {check} |")
    lines += ["", "| model | group | n | lookup extra loss | recall extra loss | gap | lookup valid | recall valid |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for g in GROUPS:
            c = m["cells"][g]
            if c is None:
                lines.append(f"| {m['target']} | {g} | 0 | - | - | - | - | - |")
                continue
            lines.append(f"| {m['target']} | {g} | {c['n']} | {fmt(c['lookup']['excess'])} | "
                         f"{fmt(c['recall']['excess'])} | {fmt(c['gap'])} | {bar(c['lookup'])} | {bar(c['recall'])} |")  # fmt: skip
        lines.append(f"| {m['target']} | mixed (in all only) | {m['n'].get('mixed', 0)} | | | | | |")
    lines += ["", "Gates (unedited org accuracy under the decisive read, both readers; eligible scenes): " + "; ".join(
        f"{m.get('target', m['run'])}: {m['gate']['org_accuracy']} pass={m['gate']['pass']}, eligible "
        f"{m['gate']['eligible']}" for m in models if "gate" in m)]  # fmt: skip
    (out / "x45m.json").write_text(json.dumps({"runs": runs, "verdict": v, "models": models}, indent=1) + "\n")
    (out / "x45m.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "score"])
    ap.add_argument("--runs", nargs="+", help="score: the 45m runs under results/x0_necessity/ (9B, 27B, Muse)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        plan()
    else:
        assert a.runs, "score needs --runs"
        score(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
